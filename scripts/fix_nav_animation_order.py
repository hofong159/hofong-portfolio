from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
# Add display helper and array normalizer before DEFAULT_CONTENT.
anchor='const DEFAULT_CONTENT: SiteContent = {'
insert='''const withoutSectionNumber = (value: string) => value.replace(/^\\s*\\d+\\s*\\/\\s*/, "");
const uniqueById = <T extends { id: number }>(items: T[]) => {
  const seen = new Set<number>();
  return items.filter((item) => {
    if (seen.has(item.id)) return false;
    seen.add(item.id);
    return true;
  });
};

'''
if insert not in s:
    s=s.replace(anchor,insert+anchor,1)
# Normalize loaded repeated items.
s=s.replace('''certificates: Array.isArray(parsed.certificates) ? parsed.certificates : DEFAULT_CONTENT.certificates,''','''certificates: uniqueById(Array.isArray(parsed.certificates) ? parsed.certificates : DEFAULT_CONTENT.certificates),''')
s=s.replace('''stats: Array.isArray(parsed.stats) ? parsed.stats : DEFAULT_CONTENT.stats,''','''stats: uniqueById(Array.isArray(parsed.stats) ? parsed.stats : DEFAULT_CONTENT.stats),''')
s=s.replace('''skills: Array.isArray(parsed.skills) ? parsed.skills : DEFAULT_CONTENT.skills,''','''skills: uniqueById(Array.isArray(parsed.skills) ? parsed.skills : DEFAULT_CONTENT.skills),''')
s=s.replace('''notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,''','''notes: uniqueById(Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes),''')
s=s.replace('''experiences: (Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences).map''','''experiences: uniqueById((Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences).map''')
# close the experiences map call in both loaders.
s=s.replace('''map((item) => ({ ...item, link: item.link || "" })),
      notes:''','''map((item) => ({ ...item, link: item.link || "" }))),
      notes:''')
s=s.replace('''experiences: (Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences).map((item) => ({ ...item, link: item.link || "" })),
    notes:''','''experiences: uniqueById((Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences).map((item) => ({ ...item, link: item.link || "" }))),
    notes:''')
# Projects mapping gets unique wrapper.
s=s.replace('''projects: (Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({''','''projects: uniqueById((Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({''')
s=s.replace('''pdfFile: project.pdfFile || project.pdf || "",
      })),
      experiences:''','''pdfFile: project.pdfFile || project.pdf || "",
      }))),
      experiences:''')
s=s.replace('''projects: (Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({ ...project, imageFiles: Array.isArray(project.imageFiles) ? project.imageFiles : project.images, pdfFile: project.pdfFile || project.pdf || "" })),
    experiences:''','''projects: uniqueById((Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({ ...project, imageFiles: Array.isArray(project.imageFiles) ? project.imageFiles : project.images, pdfFile: project.pdfFile || project.pdf || "" }))),
    experiences:''')
# clean section labels in public page.
for old,new in [
 ('{content.profileKicker}','{withoutSectionNumber(content.profileKicker)}'),
 ('{content.timelineKicker}','{withoutSectionNumber(content.timelineKicker)}'),
 ('{content.workKicker}','{withoutSectionNumber(content.workKicker)}'),
 ('03 / CREDENTIALS','CREDENTIALS'),('04 / NOTES & NOW','NOTES & NOW'),('05 / SAY HELLO','SAY HELLO'),('06 / GUESTBOOK','GUESTBOOK')]:
    s=s.replace(old,new)
# Add contact summary to profile, shown on homepage.
needle='''<div className="stats-row">{content.stats.map((stat) => <div key={stat.id}><strong>{stat.value}</strong><span>{stat.label}</span></div>)}</div>'''
replacement=needle+'''<div className="home-contact"><span className="home-contact-label">CONTACT</span><button onClick={copyEmail}><Mail size={15} /> {content.email}</button><a href={content.instagram} target="_blank" rel="noreferrer"><Instagram size={15} /> Instagram</a></div>'''
if needle not in s: raise SystemExit('stats anchor missing')
s=s.replace(needle,replacement,1)
# Make drag operations deterministic and preserve unique IDs.
s=s.replace('''const list = previous[kind] as { id: number }[];''','''const list = uniqueById(previous[kind] as { id: number }[]);''')
s=s.replace('''return { ...previous, [kind]: next } as SiteContent;''','''return { ...previous, [kind]: uniqueById(next) } as SiteContent;''')
# Add explicit drag handle and stop drag from text fields by using handle style marker.
s=s.replace('''<div className="project-editor" key={project.id} draggable onDragStart={() => beginDrag(`projects:${project.id}`)}''','''<div className="project-editor" key={project.id} draggable onDragStart={() => beginDrag(`projects:${project.id}`)}''')
# Prevent duplicated add operations by ensuring IDs are unique.
s=s.replace('''setAdminDraft((previous) => ({ ...previous, projects: [project, ...previous.projects] }));''','''setAdminDraft((previous) => ({ ...previous, projects: uniqueById([project, ...previous.projects]) }));''')
s=s.replace('''setAdminDraft((previous) => ({ ...previous, experiences: [...previous.experiences, { id: Date.now(),''','''setAdminDraft((previous) => ({ ...previous, experiences: uniqueById([...previous.experiences, { id: Date.now(),''')
s=s.replace('''link: "" }] }));''','''link: "" }]) }));''',1)
s=s.replace('''setAdminDraft((previous) => ({ ...previous, notes: [...previous.notes, { id: Date.now(), type:''','''setAdminDraft((previous) => ({ ...previous, notes: uniqueById([...previous.notes, { id: Date.now(), type:''')
s=s.replace('''readTime: "03 MIN READ" }] }));''','''readTime: "03 MIN READ" }]) }));''',1)
p.write_text(s)

css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
# Fix site nav fixed positioning being overwritten by broad child rule.
c=c.replace('.site-shell > * { position:relative; z-index:1; }','.site-shell > *:not(.site-nav) { position:relative; z-index:1; }')
# Replace prior display:none section rules with animated visibility rules.
start=c.find('/* Public site: keep the profile visible')
if start>=0: c=c[:start]
c += '''/* Public site navigation and section transitions */
.site-nav { top: 0 !important; left: 0; right: 0; position: fixed !important; }
.site-shell { padding-top: 0; }
.site-shell section[id] { opacity: 0; visibility: hidden; pointer-events: none; transform: translateY(22px); max-height: 0; overflow: hidden; padding-top: 0; padding-bottom: 0; transition: opacity .42s var(--ease-out), transform .42s var(--ease-out), visibility .42s, max-height .52s var(--ease-out), padding .42s var(--ease-out); }
.site-shell.section-profile #about,
.site-shell.section-timeline #about, .site-shell.section-timeline #timeline,
.site-shell.section-work #about, .site-shell.section-work #work,
.site-shell.section-certificates #about, .site-shell.section-certificates #certificates,
.site-shell.section-journal #about, .site-shell.section-journal #journal,
.site-shell.section-contact #about, .site-shell.section-contact #contact { opacity: 1; visibility: visible; pointer-events: auto; transform: translateY(0); max-height: 3000px; padding-top: clamp(90px, 12vw, 165px); padding-bottom: clamp(90px, 12vw, 165px); }
.site-shell.section-profile #about { padding-top: 138px; }
.site-shell.section-profile #about { transition-delay: .03s; }
.site-shell.section-timeline #timeline, .site-shell.section-work #work, .site-shell.section-certificates #certificates, .site-shell.section-journal #journal, .site-shell.section-contact #contact { transition-delay: .06s; }
.home-contact { display:flex; flex-wrap:wrap; gap:12px 22px; align-items:center; margin-top:28px; padding-top:18px; border-top:1px solid var(--line); }
.home-contact-label { color:var(--accent); font:9px 'DM Mono',monospace; letter-spacing:.14em; }
.home-contact button, .home-contact a { display:inline-flex; align-items:center; gap:7px; color:var(--muted); background:none; border:0; text-decoration:none; font:11px 'DM Mono',monospace; cursor:pointer; }
.home-contact button:hover, .home-contact a:hover { color:var(--accent); }
.card-number, .project-index { display:none !important; }
.admin-sidebar { position: sticky; top: 76px; height: calc(100vh - 76px); align-self: start; overflow-y: auto; }
.admin-main { min-width: 0; }
.project-editor[draggable], .repeat-editor[draggable] { user-select:none; }
@media (max-width: 850px) { .site-nav { top:0 !important; } .admin-sidebar { position: static; height:auto; overflow:visible; } .site-shell section[id] { transition-duration:.36s; } }
@media (prefers-reduced-motion: reduce) { .site-shell section[id] { transition:none; } }
'''
css.write_text(c)
