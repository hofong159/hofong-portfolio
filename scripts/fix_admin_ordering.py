from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
anchor='function loadContent(): SiteContent {'
helper='''const uniqueItems = <T extends { id: number }>(items: T[]) => {
  const seen = new Set<number>();
  return items.filter((item) => {
    if (seen.has(item.id)) return false;
    seen.add(item.id);
    return true;
  });
};

'''
if helper not in s: s=s.replace(anchor,helper+anchor,1)
for old,new in [
('certificates: Array.isArray(parsed.certificates) ? parsed.certificates : DEFAULT_CONTENT.certificates,','certificates: uniqueItems(Array.isArray(parsed.certificates) ? parsed.certificates : DEFAULT_CONTENT.certificates),'),
('stats: Array.isArray(parsed.stats) ? parsed.stats : DEFAULT_CONTENT.stats,','stats: uniqueItems(Array.isArray(parsed.stats) ? parsed.stats : DEFAULT_CONTENT.stats),'),
('skills: Array.isArray(parsed.skills) ? parsed.skills : DEFAULT_CONTENT.skills,','skills: uniqueItems(Array.isArray(parsed.skills) ? parsed.skills : DEFAULT_CONTENT.skills),'),
('notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,','notes: uniqueItems(Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes),'),
('projects: (Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({','projects: uniqueItems((Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({'),
('pdfFile: project.pdfFile || project.pdf || "",\n      })),','pdfFile: project.pdfFile || project.pdf || "",\n      }))),'),
('experiences: (Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences).map((item) => ({ ...item, link: item.link || "" })),','experiences: uniqueItems((Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences).map((item) => ({ ...item, link: item.link || "" }))),'),
('projects: (Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({ ...project, imageFiles: Array.isArray(project.imageFiles) ? project.imageFiles : project.images, pdfFile: project.pdfFile || project.pdf || "" })),','projects: uniqueItems((Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({ ...project, imageFiles: Array.isArray(project.imageFiles) ? project.imageFiles : project.images, pdfFile: project.pdfFile || project.pdf || "" }))),'),
]:
    s=s.replace(old,new)
# protect reorder against missing IDs
s=s.replace('''const next = index + direction;
    if (next < 0 || next >= items.length) return items;''','''if (index < 0 || index >= items.length) return items;
    const next = index + direction;
    if (next < 0 || next >= items.length) return items;''')
# Prevent adding duplicate IDs from accidental repeated clicks.
s=s.replace('''projects: [project, ...previous.projects]''','''projects: uniqueItems([project, ...previous.projects])''')
s=s.replace('''experiences: [...previous.experiences, { id: Date.now(), year:''','''experiences: uniqueItems([...previous.experiences, { id: Date.now(), year:''')
s=s.replace('''link: "" }] }));''','''link: "" }]) }));''')
s=s.replace('''notes: [...previous.notes, { id: Date.now(), type:''','''notes: uniqueItems([...previous.notes, { id: Date.now(), type:''')
s=s.replace('''readTime: "03 MIN READ" }] }));''','''readTime: "03 MIN READ" }]) }));''')
# Use dedicated drag handles instead of making text inputs draggable.
s=s.replace('''<div className="project-editor" key={project.id} draggable onDragStart={() => beginDrag(`projects:${project.id}`)} onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("projects", project.id)}><img''','''<div className="project-editor" key={project.id} onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("projects", project.id)}><span className="drag-handle" draggable onDragStart={() => beginDrag(`projects:${project.id}`)} title="拖曳以排序" aria-label="拖曳排序">⠿</span><img''')
s=s.replace('''<div className="repeat-editor" key={experience.id} draggable onDragStart={() => beginDrag(`experiences:${experience.id}`)} onDragOver''','''<div className="repeat-editor" key={experience.id} onDragOver''')
s=s.replace('''dropDrag("experiences", experience.id)}><input value={experience.year}''','''dropDrag("experiences", experience.id)}><span className="drag-handle" draggable onDragStart={() => beginDrag(`experiences:${experience.id}`)} title="拖曳以排序" aria-label="拖曳排序">⠿</span><input value={experience.year}''')
s=s.replace('''<div className="repeat-editor note-editor" key={note.id} draggable onDragStart={() => beginDrag(`notes:${note.id}`)} onDragOver''','''<div className="repeat-editor note-editor" key={note.id} onDragOver''')
s=s.replace('''dropDrag("notes", note.id)}><input value={note.type}''','''dropDrag("notes", note.id)}><span className="drag-handle" draggable onDragStart={() => beginDrag(`notes:${note.id}`)} title="拖曳以排序" aria-label="拖曳排序">⠿</span><input value={note.type}''')
# CSS grid needs room for handles, inserted through class stylesheet.
p.write_text(s)
css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
c += '''\n/* Stable admin ordering: only the handle starts a drag, form fields remain editable. */\n.drag-handle { display:grid; place-items:center; width:28px; min-height:28px; color:var(--accent); border:1px solid var(--line); cursor:grab; user-select:none; font-size:18px; line-height:1; }\n.drag-handle:active { cursor:grabbing; background:rgba(214,255,93,.12); }\n.project-editor { grid-template-columns:28px 92px 1fr 34px; }\n.repeat-editor { grid-template-columns:28px .22fr .7fr 1.2fr 58px; }\n.repeat-editor.note-editor { grid-template-columns:28px .45fr .35fr .7fr 1.2fr 58px; }\n@media (max-width:650px) { .project-editor { grid-template-columns:28px 60px 1fr 28px; } .repeat-editor, .repeat-editor.note-editor { grid-template-columns:28px 1fr; } .repeat-editor .editor-order { grid-column:2; } }\n'''
css.write_text(c)
