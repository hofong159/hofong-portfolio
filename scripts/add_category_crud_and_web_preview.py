from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
# Add a safe helper for choosing a project image and preview URL.
anchor='''const assetUrl = (value: string) => {
  if (value.startsWith("http")) return value;
  const clean = value.trim().replace(/^\\/+/, "");
  const encoded = clean.split("/").map((part) => encodeURIComponent(part)).join("/");
  const base = /^(images|pdf)\\//i.test(clean) ? LEGACY_ASSET_BASE : GITHUB_ASSET_BASE;
  return `${base}${encoded}`;
};'''
replacement=anchor+'''\nconst isPreviewableUrl = (value?: string) => Boolean(value && /^https?:\\/\\//i.test(value));'''
if anchor not in s: raise SystemExit('asset anchor missing')
s=s.replace(anchor,replacement,1)
# Empty image list should stay empty; only use the first image when present.
s=s.replace('''<div className="project-media" onClick={() => project.pdf ? setSelectedProject(project) : setLightbox({ images: project.images, index: imageIndex })}>
                    <img src={project.images[imageIndex]} alt={`${project.title} 作品照片 ${imageIndex + 1}`} />
                    <div className="media-overlay"><span>{(project.pdf || project.pdfFile) ? "OPEN CASE STUDY" : "VIEW IMAGES"}</span><ArrowUpRight size={17} /></div>''','''<div className={`project-media ${project.images.length === 0 ? "has-web-preview" : ""}`} onClick={() => project.pdf ? setSelectedProject(project) : project.images.length ? setLightbox({ images: project.images, index: imageIndex }) : setSelectedProject(project)}>
                    {project.images.length ? <img src={project.images[imageIndex]} alt={`${project.title} 作品照片 ${imageIndex + 1}`} /> : isPreviewableUrl(project.link) ? <iframe src={project.link} title={`${project.title} 網站預覽`} loading="lazy" sandbox="allow-scripts allow-same-origin" /> : <div className="empty-project-media">尚未設定照片或網站預覽</div>}
                    <div className="media-overlay"><span>{(project.pdf || project.pdfFile) ? "OPEN CASE STUDY" : project.images.length ? "VIEW IMAGES" : "PREVIEW WEBSITE"}</span><ArrowUpRight size={17} /></div>''')
# Avoid slider controls when there are no images.
s=s.replace('''{project.images.length > 1 && <><button className="slider-button left"''','''{project.images.length > 1 && <><button className="slider-button left"''',1)
# Modal: PDF first, then website preview for projects with no photos, then gallery.
s=s.replace('''{(selectedProject.pdf || selectedProject.pdfFile) ? <iframe className="pdf-preview" src={`${assetUrl(selectedProject.pdfFile || selectedProject.pdf || "")}#toolbar=0&navpanes=0`} title={`${selectedProject.title} PDF 預覽`} /> : <div className="modal-gallery">{selectedProject.images.map((image) => <img key={image} src={image} alt="作品詳細照片" />)}</div>}''','''{(selectedProject.pdf || selectedProject.pdfFile) ? <iframe className="pdf-preview" src={`${assetUrl(selectedProject.pdfFile || selectedProject.pdf || "")}#toolbar=0&navpanes=0`} title={`${selectedProject.title} PDF 預覽`} /> : selectedProject.images.length ? <div className="modal-gallery">{selectedProject.images.map((image) => <img key={image} src={image} alt="作品詳細照片" />)}</div> : isPreviewableUrl(selectedProject.link) ? <iframe className="website-preview" src={selectedProject.link} title={`${selectedProject.title} 網站預覽`} sandbox="allow-scripts allow-same-origin allow-forms allow-popups" /> : <div className="empty-project-media">請在後台填入網站連結或照片檔名。</div>}''')
# Make category delete also repair projects currently using that category.
old='''onClick={() => setDraft((previous) => ({ ...previous, categories: previous.categories.filter((_, itemIndex) => itemIndex !== index) }))}'''
new='''onClick={() => setDraft((previous) => { const nextCategories = previous.categories.filter((_, itemIndex) => itemIndex !== index); const fallback = nextCategories[0] || "未分類"; return { ...previous, categories: nextCategories, projects: previous.projects.map((project) => project.category === category ? { ...project, category: fallback } : project) }; })}'''
if old not in s: raise SystemExit('category delete anchor missing')
s=s.replace(old,new,1)
# New-project form must use the first available category instead of stale hard-coded value.
s=s.replace('''setNewProject({ title: "", category: "建築圖面", description: "" });''','''setNewProject({ title: "", category: (previousCategory || "") as Exclude<Category, "全部">, description: "" });''') if False else s
p.write_text(s)

css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
if '.website-preview' not in c:
    c += '''\n.project-media iframe { width:100%; height:100%; border:0; background:#fff; pointer-events:none; }.empty-project-media { width:100%; height:100%; display:grid; place-items:center; padding:20px; color:var(--muted); background:var(--surface-2); font-size:12px; text-align:center; }.website-preview { width:100%; min-height:62vh; border:1px solid var(--line); background:#fff; }.has-web-preview { cursor:pointer; }\n'''
css.write_text(c)
