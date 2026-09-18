from pathlib import Path
import subprocess
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=subprocess.check_output(['git','show','e9ab9db:client/src/pages/Home.tsx'], text=True)
old='''<div className="project-editor" key={project.id} onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("projects", project.id)}><span className="drag-handle" draggable onDragStart={() => beginDrag(`projects:${project.id}`)} title="拖曳以排序" aria-label="拖曳排序">⠿</span><img src={project.images[0]} alt="" /><div className="project-editor-copy">'''
if old not in s:
    raise SystemExit('stable opening missing')
new='''<details className="project-editor-collapsible" key={project.id}><summary className="project-editor-summary"><span className="drag-handle" draggable onDragStart={(event) => { event.stopPropagation(); beginDrag(`projects:${project.id}`); }} onClick={(event) => event.preventDefault()} title="拖曳以排序" aria-label="拖曳排序">⠿</span><img src={project.images[0]} alt="" /><span><strong>{project.title || "未命名作品"}</strong><small>{project.category} · {project.year}</small></span></summary><div className="project-editor" onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("projects", project.id)}><div className="project-editor-spacer"></div><div className="project-editor-copy">'''
s=s.replace(old,new,1)
a=s.index('<div className="project-editor-list">')
b=s.index('<div className="new-project-form">',a)
chunk=s[a:b]
# Stable block ends with editor div, map close, list close.
end='</div></div>)}</div>'
if not chunk.endswith(end):
    raise SystemExit('stable closing missing: '+chunk[-80:])
chunk=chunk[:-len(end)] + '</div></div></details>)}</div>'
s=s[:a]+chunk+s[b:]
p.write_text(s)
