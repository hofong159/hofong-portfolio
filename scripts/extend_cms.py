from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()

s=s.replace('''  images: string[];\n  link?: string;\n  pdf?: string;''','''  images: string[];
  imageFiles?: string[];
  link?: string;
  pdf?: string;
  pdfFile?: string;''')

# Add helper after IMAGE_BASE
s=s.replace('const IMAGE_BASE = "https://images.unsplash.com/";', '''const IMAGE_BASE = "https://images.unsplash.com/";
const GITHUB_ASSET_BASE = "https://raw.githubusercontent.com/hofong/portfolio-assets/main/";
const assetUrl = (value: string) => value.startsWith("http") ? value : `${GITHUB_ASSET_BASE}${value.replace(/^\\/+/, "")}`;''')

# Add imageFiles/pdfFile to defaults based on current images using minimal insertion after each images arrays is hard; normalize loadContent instead.
old='''      projects: Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects,
      experiences: Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences,
      notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,'''
new='''      projects: (Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({
        ...project,
        imageFiles: Array.isArray(project.imageFiles) ? project.imageFiles : project.images,
        pdfFile: project.pdfFile || project.pdf || "",
      })),
      experiences: Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences,
      notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,'''
s=s.replace(old,new)

# Replace addImageByName behavior to use assetUrl helper and keep portrait.
s=s.replace('''    const imageUrl = `https://raw.githubusercontent.com/hofong/portfolio-assets/main/${cleanName}`;''','''    const imageUrl = assetUrl(cleanName);''')

# Add reorder helper before addProject
needle='''  const addProject = () => {'''
insert='''  const reorder = <T,>(items: T[], index: number, direction: -1 | 1) => {
    const next = index + direction;
    if (next < 0 || next >= items.length) return items;
    const copy = [...items];
    [copy[index], copy[next]] = [copy[next], copy[index]];
    return copy;
  };

  const moveProject = (id: number, direction: -1 | 1) => setAdminDraft((previous) => {
    const index = previous.projects.findIndex((project) => project.id === id);
    return { ...previous, projects: reorder(previous.projects, index, direction) };
  });
  const moveExperience = (id: number, direction: -1 | 1) => setAdminDraft((previous) => {
    const index = previous.experiences.findIndex((item) => item.id === id);
    return { ...previous, experiences: reorder(previous.experiences, index, direction) };
  });
  const moveNote = (id: number, direction: -1 | 1) => setAdminDraft((previous) => {
    const index = previous.notes.findIndex((item) => item.id === id);
    return { ...previous, notes: reorder(previous.notes, index, direction) };
  });

  const addProject = () => {'''
s=s.replace(needle,insert)

# New project has imageFiles and pdfFile
s=s.replace('''      images: [`${IMAGE_BASE}photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1600&q=85`],''','''      images: [`${IMAGE_BASE}photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1600&q=85`],
      imageFiles: [`${IMAGE_BASE}photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1600&q=85`],
      pdfFile: "",''')

# Project media uses pdfFile too
s=s.replace('''{project.pdf ? setSelectedProject(project) : setLightbox({ images: project.images, index: imageIndex })}''','''{(project.pdf || project.pdfFile) ? setSelectedProject(project) : setLightbox({ images: project.images, index: imageIndex })}''')
s=s.replace('''{project.pdf ? "OPEN CASE STUDY" : "VIEW IMAGES"}''','''{(project.pdf || project.pdfFile) ? "OPEN CASE STUDY" : "VIEW IMAGES"}''')
s=s.replace('''{selectedProject.pdf ? <iframe className="pdf-preview" src={`${selectedProject.pdf}#toolbar=0&navpanes=0`}''','''{(selectedProject.pdf || selectedProject.pdfFile) ? <iframe className="pdf-preview" src={`${assetUrl(selectedProject.pdfFile || selectedProject.pdf || "")}#toolbar=0&navpanes=0`}''')

# Extend AdminPanel props with reorder functions
s=s.replace('''saveAdmin, syncFirebase, dragging, setDragging, handleDrop, goHome, adminUser,''','''saveAdmin, syncFirebase, dragging, setDragging, handleDrop, goHome, moveProject, moveExperience, moveNote, adminUser,''')
s=s.replace('''deleteProject: (id: number) => void; saveAdmin:''','''deleteProject: (id: number) => void; moveProject: (id: number, direction: -1 | 1) => void; moveExperience: (id: number, direction: -1 | 1) => void; moveNote: (id: number, direction: -1 | 1) => void; saveAdmin:''')
# invocation add props
s=s.replace('''deleteProject={deleteProject} saveAdmin={saveAdmin} syncFirebase''','''deleteProject={deleteProject} moveProject={moveProject} moveExperience={moveExperience} moveNote={moveNote} saveAdmin={saveAdmin} syncFirebase''')

# Add asset file controls and project reordering buttons by replacing project editor opening and image/title section.
s=s.replace('''<div className="project-editor" key={project.id}><img src={project.images[0]} alt="" /><div className="project-editor-copy">''','''<div className="project-editor" key={project.id}><img src={project.images[0]} alt="" /><div className="project-editor-copy">''')
# Insert fields before tags inside project editor
s=s.replace('''<textarea value={project.description} onChange={(event) => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, description: event.target.value } : item) }))} rows={2} /><div className="tag-list">''','''<textarea value={project.description} onChange={(event) => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, description: event.target.value } : item) }))} rows={2} /><div className="asset-editor"><span>照片檔名（每行一個）</span><textarea value={(project.imageFiles || project.images).join("\\n")} rows={3} onChange={(event) => { const files = event.target.value.split("\\n").map((item) => item.trim()).filter(Boolean); setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, imageFiles: files, images: files.map(assetUrl) } : item) })); }} /><span>PDF 檔名或網址（可留白）</span><input value={project.pdfFile || project.pdf || ""} placeholder="case-study.pdf" onChange={(event) => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, pdfFile: event.target.value, pdf: event.target.value ? assetUrl(event.target.value) : "" } : item) }))} /></div><div className="tag-list">''')
# Add order buttons beside delete
s=s.replace('''<button className="delete-button" onClick={() => deleteProject(project.id)} aria-label={`刪除 ${project.title}`}><Trash2 size={17} /></button>''','''<div className="editor-order"><button onClick={() => moveProject(project.id, -1)} aria-label="作品上移">↑</button><button onClick={() => moveProject(project.id, 1)} aria-label="作品下移">↓</button><button className="delete-button" onClick={() => deleteProject(project.id)} aria-label={`刪除 ${project.title}`}><Trash2 size={17} /></button></div>''')
# Experiences map add order buttons
s=s.replace('''<textarea value={experience.detail} rows={2} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, detail: event.target.value } : item) }))} /></div>)}''','''<textarea value={experience.detail} rows={2} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, detail: event.target.value } : item) }))} /><div className="editor-order"><button onClick={() => moveExperience(experience.id, -1)}>↑</button><button onClick={() => moveExperience(experience.id, 1)}>↓</button></div></div>)}''')
# Notes map add order buttons
s=s.replace('''<textarea value={note.description} rows={2} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, description: event.target.value } : item) }))} /></div>)}</section>''','''<textarea value={note.description} rows={2} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, description: event.target.value } : item) }))} /><div className="editor-order"><button onClick={() => moveNote(note.id, -1)}>↑</button><button onClick={() => moveNote(note.id, 1)}>↓</button></div></div>)}</section>''')

p.write_text(s)

css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
c += '''\n.asset-editor { display:grid; gap:5px; margin:8px 0 5px; }.asset-editor span { color:var(--faint); font:9px 'DM Mono',monospace; }.asset-editor textarea, .asset-editor input { font-size:10px; padding:7px 8px; }.editor-order { display:flex; flex-direction:column; gap:4px; }.editor-order button { width:25px; height:25px; border:1px solid var(--line); color:var(--muted); background:transparent; cursor:pointer; }.editor-order button:hover { color:var(--accent); border-color:var(--accent); }.project-editor { grid-template-columns:92px 1fr 34px; }.repeat-editor { grid-template-columns:.22fr .7fr 1.2fr 58px; }.repeat-editor.note-editor { grid-template-columns:.45fr .35fr .7fr 1.2fr 58px; }\n@media (max-width:650px) { .repeat-editor, .repeat-editor.note-editor { grid-template-columns:1fr; }.editor-order { flex-direction:row; }.project-editor { grid-template-columns:60px 1fr 28px; } }\n'''
css.write_text(c)
