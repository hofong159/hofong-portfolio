from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
s=s.replace('''experiences: { id: number; year: string; title: string; detail: string }[];''','''experiences: { id: number; year: string; title: string; detail: string; link?: string }[];''')
s=s.replace('''{ id: 1, year: '2026', title: 'Independent Practice', detail:''','''{ id: 1, year: '2026', title: 'Independent Practice', link: '', detail:''')
s=s.replace('''{ id: 2, year: '2024', title: 'Urban Research Lab', detail:''','''{ id: 2, year: '2024', title: 'Urban Research Lab', link: '', detail:''')
s=s.replace('''{ id: 3, year: '2022', title: 'M.Arch / Taipei', detail:''','''{ id: 3, year: '2022', title: 'M.Arch / Taipei', link: '', detail:''')
s=s.replace('''experiences: Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences,''','''experiences: (Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences).map((item) => ({ ...item, link: item.link || "" })),''')
old='''<div className="timeline"><div className="timeline-line" />{content.experiences.map((experience) => <div className="timeline-item" key={experience.id}><span className="timeline-date">{experience.year}</span><div><h3>{experience.title}</h3><p>{experience.detail}</p></div></div>)}</div>'''
new='''<div className="timeline"><div className="timeline-line" />{content.experiences.map((experience) => <div className="timeline-item" key={experience.id}><span className="timeline-date">{experience.year}</span><div><h3>{experience.link ? <a className="experience-link" href={experience.link} target="_blank" rel="noreferrer">{experience.title} <ExternalLink size={13} /></a> : experience.title}</h3><p>{experience.detail}</p></div></div>)}</div>'''
if old not in s: raise SystemExit('timeline anchor missing')
s=s.replace(old,new,1)
old2='''<input value={experience.title} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, title: event.target.value } : item) }))} /><textarea value={experience.detail} rows={2}'''
new2='''<input value={experience.title} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, title: event.target.value } : item) }))} /><input value={experience.link || ""} placeholder="連結（可留白，例如 https://...）" onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, link: event.target.value } : item) }))} /><textarea value={experience.detail} rows={2}'''
if old2 not in s: raise SystemExit('admin experience anchor missing')
s=s.replace(old2,new2,1)
p.write_text(s)
css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
if '.experience-link' not in c:
    c += '''\n.experience-link { color:inherit; display:inline-flex; align-items:center; gap:6px; text-decoration:none; border-bottom:1px solid transparent; transition:color .18s ease,border-color .18s ease; }.experience-link:hover { color:var(--accent); border-color:var(--accent); }\n'''
css.write_text(c)
