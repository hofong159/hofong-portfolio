from pathlib import Path
import re
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
# Restore a robust floating public nav without changing mobile menu behavior.
css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
c += '''\n/* Public navigation stays visible while scrolling. */\n.site-nav { position: fixed !important; top: 0; left: 0; right: 0; z-index: 50; }\n/* Compact project editors reduce long admin pages while keeping every field editable. */\n.project-editor-list { gap: 8px; }\n.project-editor-collapsible { border: 1px solid var(--line); background: var(--surface); }\n.project-editor-summary { display:grid; grid-template-columns:28px 72px 1fr auto; gap:12px; align-items:center; padding:10px 13px; cursor:pointer; list-style:none; }\n.project-editor-summary::-webkit-details-marker { display:none; }\n.project-editor-summary:after { content:'+'; color:var(--accent); font:18px 'DM Mono',monospace; }\n.project-editor-collapsible[open] .project-editor-summary:after { content:'−'; }\n.project-editor-summary img { width:72px; height:54px; object-fit:cover; background:#141918; }\n.project-editor-summary strong { display:block; font-size:13px; font-weight:500; }\n.project-editor-summary small { display:block; color:var(--muted); font:9px 'DM Mono',monospace; margin-top:4px; }\n.project-editor-collapsible .project-editor { border:0; border-top:1px solid var(--line); }\n@media (max-width:650px) { .project-editor-summary { grid-template-columns:28px 54px 1fr auto; gap:9px; } .project-editor-summary img { width:54px; height:45px; } }\n'''
css.write_text(c)
# Replace project editor wrapper with details/summary, retaining existing inner editor fields.
old='''<div className="project-editor" key={project.id} onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("projects", project.id)}><span className="drag-handle" draggable onDragStart={() => beginDrag(`projects:${project.id}`)} title="拖曳以排序" aria-label="拖曳排序">⠿</span><img src={project.images[0]} alt="" /><div className="project-editor-copy">'''
new='''<details className="project-editor-collapsible" key={project.id}><summary className="project-editor-summary"><span className="drag-handle" draggable onDragStart={(event) => { event.stopPropagation(); beginDrag(`projects:${project.id}`); }} onClick={(event) => event.preventDefault()} title="拖曳以排序" aria-label="拖曳排序">⠿</span><img src={project.images[0]} alt="" /><span><strong>{project.title || "未命名作品"}</strong><small>{project.category} · {project.year}</small></span></summary><div className="project-editor" onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("projects", project.id)}><div></div><div className="project-editor-copy">'''
if old not in s:
    raise SystemExit('project editor opening not found')
s=s.replace(old,new,1)
# The original editor ends with </div> after delete button; add details close after that specific project block.
needle='''</div></div>)}<div className="new-project-form">'''
if needle not in s:
    raise SystemExit('project editor closing not found')
s=s.replace(needle,'''</div></div></details>)}<div className="new-project-form">''',1)
p.write_text(s)
