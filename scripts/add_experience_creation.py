from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
# Add creator near the existing reorder helpers.
needle='''  const moveExperience = (id: number, direction: -1 | 1) => setAdminDraft((previous) => {\n    const index = previous.experiences.findIndex((item) => item.id === id);\n    return { ...previous, experiences: reorder(previous.experiences, index, direction) };\n  });'''
replacement=needle+'''\n  const addExperience = () => setAdminDraft((previous) => ({ ...previous, experiences: [...previous.experiences, { id: Date.now(), year: "2026", title: "新經歷", detail: "請補上這段經歷的說明。", link: "" }] }));'''
if needle not in s: raise SystemExit('moveExperience anchor missing')
s=s.replace(needle,replacement,1)
# Pass the handler into AdminPanel.
s=s.replace('''moveProject={moveProject} moveExperience={moveExperience} moveNote={moveNote}''','''moveProject={moveProject} moveExperience={moveExperience} addExperience={addExperience} moveNote={moveNote}''',1)
# Extend AdminPanel props type.
s=s.replace('''moveExperience: (id: number, direction: -1 | 1) => void; moveNote:''','''moveExperience: (id: number, direction: -1 | 1) => void; addExperience: () => void; moveNote:''',1)
# Add the button after the timeline editor list, before notes.
old='''</div>)}<div className="admin-subhead notes-head">筆記卡片</div>'''
new='''</div>)}<button className="button button-outline add-experience-button" onClick={addExperience}><Plus size={15} /> 新增經歷</button><div className="admin-subhead notes-head">筆記卡片</div>'''
if old not in s: raise SystemExit('experience list ending anchor missing')
s=s.replace(old,new,1)
p.write_text(s)
css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
if '.add-experience-button' not in c:
    c += '''\n.add-experience-button { margin-top:12px; }\n'''
css.write_text(c)
