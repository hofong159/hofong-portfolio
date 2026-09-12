from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
# Add action handlers.
needle='''  const addExperience = () => setAdminDraft((previous) => ({ ...previous, experiences: [...previous.experiences, { id: Date.now(), year: "2026", title: "新經歷", detail: "請補上這段經歷的說明。", link: "" }] }));'''
replacement=needle+'''\n  const deleteExperience = (id: number) => setAdminDraft((previous) => ({ ...previous, experiences: previous.experiences.filter((item) => item.id !== id) }));\n  const addNote = () => setAdminDraft((previous) => ({ ...previous, notes: [...previous.notes, { id: Date.now(), type: "NOTE / NEW", title: "新筆記", description: "請補上筆記內容。", readTime: "03 MIN READ" }] }));\n  const deleteNote = (id: number) => setAdminDraft((previous) => ({ ...previous, notes: previous.notes.filter((item) => item.id !== id) }));'''
if needle not in s: raise SystemExit('experience handler anchor missing')
s=s.replace(needle,replacement,1)
# Pass handlers.
s=s.replace('''moveExperience={moveExperience} addExperience={addExperience} moveNote={moveNote}''','''moveExperience={moveExperience} addExperience={addExperience} deleteExperience={deleteExperience} moveNote={moveNote} addNote={addNote} deleteNote={deleteNote}''',1)
# Add actions to prop type.
s=s.replace('''addExperience: () => void; moveNote:''','''addExperience: () => void; deleteExperience: (id: number) => void; moveNote:''',1)
s=s.replace('''moveNote: (id: number, direction: -1 | 1) => void; reorder:''','''moveNote: (id: number, direction: -1 | 1) => void; addNote: () => void; deleteNote: (id: number) => void; reorder:''',1)
# Certificate image becomes square clickable thumbnail.
s=s.replace('''{certificate.imageFile && <img src={assetUrl(certificate.imageFile)} alt={certificate.title} />}''','''{certificate.imageFile && <button className="certificate-image-button" onClick={() => setLightbox({ images: [assetUrl(certificate.imageFile || "")], index: 0 })} aria-label={`放大查看${certificate.title}`}><img src={assetUrl(certificate.imageFile)} alt={certificate.title} /></button>}''',1)
# Experience row: add delete button beside ordering.
s=s.replace('''<button onClick={() => moveExperience(experience.id, 1)}>↓</button></div></div>)}<button className="button button-outline add-experience-button"''','''<button onClick={() => moveExperience(experience.id, 1)}>↓</button><button className="delete-button" onClick={() => deleteExperience(experience.id)} aria-label={`刪除 ${experience.title}`}><Trash2 size={15} /></button></div></div>)}<button className="button button-outline add-experience-button"''',1)
# Note row: add delete button and add-note button.
s=s.replace('''<button onClick={() => moveNote(note.id, 1)}>↓</button></div></div>)}</section><section className="editor-card" id="admin-media">''','''<button onClick={() => moveNote(note.id, 1)}>↓</button><button className="delete-button" onClick={() => deleteNote(note.id)} aria-label={`刪除 ${note.title}`}><Trash2 size={15} /></button></div></div>)}<button className="button button-outline add-note-button" onClick={addNote}><Plus size={15} /> 新增筆記</button></section><section className="editor-card" id="admin-media">''',1)
p.write_text(s)
css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
if '.certificate-image-button' not in c:
    c += '''\n.certificate-image-button { display:block; width:calc(100% + 52px); margin:-26px -26px 22px; padding:0; border:0; background:var(--surface-2); cursor:zoom-in; }.certificate-card img { display:block; width:100%; aspect-ratio:1; max-height:none; object-fit:cover; margin:0; }.certificate-image-button:hover img { opacity:.82; }.add-note-button { margin-top:12px; }\n'''
css.write_text(c)
