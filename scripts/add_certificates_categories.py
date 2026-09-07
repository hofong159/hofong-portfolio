from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()

s=s.replace('type Category = "全部" | "建築圖面" | "互動體驗" | "研究實作";', 'type Category = string;')
s=s.replace('''  pdfFile?: string;
};
type SiteContent = {''','''  pdfFile?: string;
};
type Certificate = {
  id: number;
  title: string;
  issuer: string;
  year: string;
  credential: string;
  description: string;
  imageFile?: string;
  pdfFile?: string;
  link?: string;
};
type SiteContent = {''')
s=s.replace('''  projects: Project[];
  heroBackground: string;''','''  projects: Project[];
  categories: string[];
  certificates: Certificate[];
  heroBackground: string;''')

s=s.replace('''  notes: [
    { id: 1, type: 'FIELD NOTE / 01', title: '為什麼我還在拍\\n城市的背面？', description: '那些沒有被拍進旅遊指南的邊角，往往更接近一座城市真正的呼吸。', readTime: '06 MIN READ' },
    { id: 2, type: 'PROCESS / 02', title: '從一張紙開始的\\n互動原型', description: '在螢幕之前，先讓手和眼睛一起想。', readTime: '04 MIN READ' },
  ],
  projects: [''', '''  notes: [
    { id: 1, type: 'FIELD NOTE / 01', title: '為什麼我還在拍\\n城市的背面？', description: '那些沒有被拍進旅遊指南的邊角，往往更接近一座城市真正的呼吸。', readTime: '06 MIN READ' },
    { id: 2, type: 'PROCESS / 02', title: '從一張紙開始的\\n互動原型', description: '在螢幕之前，先讓手和眼睛一起想。', readTime: '04 MIN READ' },
  ],
  categories: ['建築圖面', '互動體驗', '研究實作'],
  certificates: [
    { id: 1, title: '建築師資格證書', issuer: '台灣建築師公會', year: '2025', credential: 'TW-ARCH-2025-001', description: '建築專業資格與執業相關證明。', imageFile: '', pdfFile: '', link: '' },
    { id: 2, title: '互動媒體設計證書', issuer: 'Digital Futures Lab', year: '2024', credential: 'DFL-IM-2024-018', description: '互動設計與數位敘事實務認證。', imageFile: '', pdfFile: '', link: '' },
  ],
  projects: [''')

s=s.replace('''      projects: (Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({''','''      categories: Array.isArray(parsed.categories) && parsed.categories.length ? parsed.categories.filter((item): item is string => typeof item === "string" && item.trim().length > 0) : DEFAULT_CONTENT.categories,
      certificates: Array.isArray(parsed.certificates) ? parsed.certificates : DEFAULT_CONTENT.certificates,
      projects: (Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({''')
s=s.replace('''    () => content.projects.filter((project) => filter === "全部" || project.category === filter),''','''    () => content.projects.filter((project) => filter === "全部" || project.category === filter),''')
# dynamic filter controls
old='''<div className="filter-row">{(["全部", "建築圖面", "互動體驗", "研究實作"] as Category[]).map((item) => <button key={item} className={filter === item ? "active" : ""} onClick={() => setFilter(item)}>{item}<span>0{item === "全部" ? content.projects.length : content.projects.filter((p) => p.category === item).length}</span></button>)}</div>'''
new='''<div className="filter-row">{["全部", ...content.categories].map((item) => <button key={item} className={filter === item ? "active" : ""} onClick={() => setFilter(item)}>{item}<span>0{item === "全部" ? content.projects.length : content.projects.filter((p) => p.category === item).length}</span></button>)}</div>'''
if old not in s: raise SystemExit('filter anchor missing')
s=s.replace(old,new)
# category select for new project
s=s.replace('''<select value={newProject.category} onChange={(event) => setNewProject((previous) => ({ ...previous, category: event.target.value as Exclude<Category, "全部"> }))}><option>建築圖面</option><option>互動體驗</option><option>研究實作</option></select>''','''<select value={newProject.category} onChange={(event) => setNewProject((previous) => ({ ...previous, category: event.target.value }))}>{draft.categories.map((category) => <option key={category}>{category}</option>)}</select>''')
# project editor category selector
s=s.replace('''<select value={project.category} onChange={(event) => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, category: event.target.value as Exclude<Category, "全部"> } : item) }))}><option>建築圖面</option><option>互動體驗</option><option>研究實作</option></select>''','''<select value={project.category} onChange={(event) => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, category: event.target.value } : item) }))}>{draft.categories.map((category) => <option key={category}>{category}</option>)}</select>''')
# public certificates section after work section closing anchor
marker='''          </section>

          <section className="journal-section" id="journal">'''
insert='''          </section>

          <section className="certificates-section" id="certificates">
            <div className="section-head"><div><div className="section-kicker">03 / CREDENTIALS</div><h2>證照與<br /><em>專業證明。</em></h2></div><p>把資格、證書與持續累積的專業能力，整理成清楚可查閱的公開紀錄。</p></div>
            <div className="certificate-grid">{content.certificates.map((certificate) => <article className="certificate-card" key={certificate.id}>{certificate.imageFile && <img src={assetUrl(certificate.imageFile)} alt={certificate.title} />}<div className="certificate-kicker">{certificate.year} · {certificate.issuer}</div><h3>{certificate.title}</h3><p>{certificate.description}</p><div className="certificate-meta"><span>{certificate.credential}</span>{certificate.pdfFile && <a href={`${assetUrl(certificate.pdfFile)}#toolbar=0`} target="_blank" rel="noreferrer"><FileText size={14} /> 查看證書 PDF</a>}{certificate.link && <a href={certificate.link} target="_blank" rel="noreferrer"><ExternalLink size={14} /> 官方連結</a>}</div></article>)}</div>
          </section>

          <section className="journal-section" id="journal">'''
if marker not in s: raise SystemExit('section marker missing')
s=s.replace(marker,insert)
# nav add certificate
s=s.replace('''<button onClick={() => scrollTo("work")}>作品</button>
          <button onClick={() => scrollTo("journal")}>筆記</button>''','''<button onClick={() => scrollTo("work")}>作品</button>
          <button onClick={() => scrollTo("certificates")}>證照</button>
          <button onClick={() => scrollTo("journal")}>筆記</button>''')
# Admin insert category editor and certificate editor before existing experiences section
marker2='''<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">03</span><h3>經歷與筆記</h3></div>'''
insert2='''<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">03</span><h3>分類標籤</h3></div><span>EDITABLE / FILTERS</span></div><p className="helper-copy">每行一個分類。作品下拉選單與前台篩選會同步更新。</p><textarea rows={4} value={draft.categories.join("\\n")} onChange={(event) => setDraft((previous) => ({ ...previous, categories: event.target.value.split("\\n").map((item) => item.trim()).filter(Boolean) }))} /></section><section className="editor-card"><div className="editor-card-head"><div><span className="card-number">04</span><h3>證照與證書</h3></div><span>{draft.certificates.length} CREDENTIALS</span></div><div className="certificate-editor-list">{draft.certificates.map((certificate, index) => <div className="certificate-editor" key={certificate.id}><div className="editor-order"><button onClick={() => setDraft((previous) => ({ ...previous, certificates: reorder(previous.certificates, index, -1) }))}>↑</button><button onClick={() => setDraft((previous) => ({ ...previous, certificates: reorder(previous.certificates, index, 1) }))}>↓</button></div><div className="certificate-editor-fields"><input value={certificate.title} placeholder="證照名稱" onChange={(event) => setDraft((previous) => ({ ...previous, certificates: previous.certificates.map((item) => item.id === certificate.id ? { ...item, title: event.target.value } : item) }))} /><div className="field-grid"><input value={certificate.issuer} placeholder="發證單位" onChange={(event) => setDraft((previous) => ({ ...previous, certificates: previous.certificates.map((item) => item.id === certificate.id ? { ...item, issuer: event.target.value } : item) }))} /><input value={certificate.year} placeholder="年份" onChange={(event) => setDraft((previous) => ({ ...previous, certificates: previous.certificates.map((item) => item.id === certificate.id ? { ...item, year: event.target.value } : item) }))} /></div><input value={certificate.credential} placeholder="證書編號" onChange={(event) => setDraft((previous) => ({ ...previous, certificates: previous.certificates.map((item) => item.id === certificate.id ? { ...item, credential: event.target.value } : item) }))} /><textarea rows={2} value={certificate.description} placeholder="說明" onChange={(event) => setDraft((previous) => ({ ...previous, certificates: previous.certificates.map((item) => item.id === certificate.id ? { ...item, description: event.target.value } : item) }))} /><div className="field-grid"><input value={certificate.imageFile || ""} placeholder="照片檔名或路徑" onChange={(event) => setDraft((previous) => ({ ...previous, certificates: previous.certificates.map((item) => item.id === certificate.id ? { ...item, imageFile: event.target.value } : item) }))} /><input value={certificate.pdfFile || ""} placeholder="PDF 檔名或路徑" onChange={(event) => setDraft((previous) => ({ ...previous, certificates: previous.certificates.map((item) => item.id === certificate.id ? { ...item, pdfFile: event.target.value } : item) }))} /></div><input value={certificate.link || ""} placeholder="官方連結（可留白）" onChange={(event) => setDraft((previous) => ({ ...previous, certificates: previous.certificates.map((item) => item.id === certificate.id ? { ...item, link: event.target.value } : item) }))} /></div></div>)}</div><button className="button button-outline" onClick={() => setDraft((previous) => ({ ...previous, certificates: [...previous.certificates, { id: Date.now(), title: "新證照", issuer: "發證單位", year: "2026", credential: "待補充", description: "請在這裡補上證照說明。", imageFile: "", pdfFile: "", link: "" }] }))}><Plus size={15} /> 新增證照</button></section><section className="editor-card"><div className="editor-card-head"><div><span className="card-number">05</span><h3>經歷與筆記</h3></div>'''
if marker2 not in s: raise SystemExit('admin marker missing')
s=s.replace(marker2,insert2)
# Rename later numbers optional not important
p.write_text(s)

css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
c += '''\n.certificates-section { padding: 7rem 5vw; background: var(--surface); }.certificate-grid { display:grid; grid-template-columns: repeat(2, 1fr); gap: 18px; }.certificate-card { border:1px solid var(--line); padding:26px; background:rgba(255,255,255,.025); }.certificate-card img { width:100%; max-height:180px; object-fit:cover; margin:-26px -26px 22px; width:calc(100% + 52px); }.certificate-kicker { color:var(--accent); font:10px 'DM Mono',monospace; letter-spacing:.08em; }.certificate-card h3 { margin:12px 0 8px; font-size:22px; }.certificate-card p { color:var(--muted); line-height:1.7; }.certificate-meta { display:flex; flex-wrap:wrap; gap:12px; margin-top:20px; color:var(--faint); font:10px 'DM Mono',monospace; }.certificate-meta a { color:var(--accent); display:inline-flex; gap:5px; align-items:center; }.certificate-editor-list { display:grid; gap:14px; margin-bottom:16px; }.certificate-editor { display:grid; grid-template-columns:34px 1fr; gap:10px; border-top:1px solid var(--line); padding-top:14px; }.certificate-editor-fields { display:grid; gap:8px; }.certificate-editor-fields input, .certificate-editor-fields textarea { margin:0; }.certificate-editor-fields .field-grid { margin:0; }.certificate-editor .editor-order { flex-direction:column; }\n@media (max-width:650px) { .certificate-grid { grid-template-columns:1fr; }.certificates-section { padding:5rem 22px; } }\n'''
css.write_text(c)
