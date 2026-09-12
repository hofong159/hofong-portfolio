from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
old='''<span>技能標籤（逗號分隔）</span><input value={project.tags.join(", ")} onChange={(event) => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, tags: event.target.value.split(",").map((tag) => tag.trim()).filter(Boolean) } : item) }))} /></div><div className="tag-list">{project.tags.map((tag) => <span key={tag}>{tag}</span>)}</div>'''
new='''<span>作品標籤（可逐項修改、新增、刪除）</span><div className="tag-editor-list">{project.tags.map((tag, tagIndex) => <div className="tag-editor-row" key={`${project.id}-${tagIndex}`}><input value={tag} placeholder="例如：建築設計" onChange={(event) => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, tags: item.tags.map((current, currentIndex) => currentIndex === tagIndex ? event.target.value : current) } : item) }))} /><button className="delete-button" onClick={() => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, tags: item.tags.filter((_, currentIndex) => currentIndex !== tagIndex) } : item) }))}>刪除</button></div>)}</div><button className="button button-outline tag-add-button" onClick={() => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, tags: [...item.tags, "新標籤"] } : item) }))}><Plus size={14} /> 新增作品標籤</button></div><div className="tag-list">{project.tags.filter(Boolean).map((tag, tagIndex) => <span key={`${project.id}-preview-${tagIndex}`}>{tag}</span>)}</div>'''
if old not in s:
    raise SystemExit('project tag editor anchor missing')
p.write_text(s.replace(old,new,1))
css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
if '.tag-editor-list' not in c:
    c += '''\n.tag-editor-list { display:grid; gap:7px; margin:8px 0; }.tag-editor-row { display:grid; grid-template-columns:1fr auto; gap:7px; align-items:center; }.tag-editor-row input { margin:0; }.tag-add-button { min-height:30px; padding:0 10px; font-size:10px; }\n'''
css.write_text(c)
