from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
old='''<div className="project-editor" key={project.id} onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("projects", project.id)}><span className="drag-handle" draggable onDragStart={() => beginDrag(`projects:${project.id}`)} title="拖曳以排序" aria-label="拖曳排序">⠿</span><img src={project.images[0]} alt="" /><div className="project-editor-copy">'''
new='''<details className="project-editor-collapsible" key={project.id}><summary className="project-editor-summary"><span className="drag-handle" draggable onDragStart={(event) => { event.stopPropagation(); beginDrag(`projects:${project.id}`); }} onClick={(event) => event.preventDefault()} title="拖曳以排序" aria-label="拖曳排序">⠿</span><img src={project.images[0]} alt="" /><span><strong>{project.title || "未命名作品"}</strong><small>{project.category} · {project.year}</small></span></summary><div className="project-editor" onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("projects", project.id)}><div></div><div className="project-editor-copy">'''
if old not in s: raise SystemExit('opening missing')
s=s.replace(old,new,1)
a=s.index('<div className="project-editor-list">')
b=s.index('<div className="new-project-form">',a)
chunk=s[a:b]
if '</div>)}</div>' not in chunk: raise SystemExit('closing missing')
chunk=chunk.replace('</div>)}</div>','</div></div></details>)}</div>',1)
s=s[:a]+chunk+s[b:]
p.write_text(s)
