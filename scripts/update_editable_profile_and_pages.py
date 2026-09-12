from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
# first-level asset convention
s=s.replace('const GITHUB_ASSET_BASE = "https://raw.githubusercontent.com/hofong159/portfolio-assets/main/";', 'const GITHUB_ASSET_BASE = "https://raw.githubusercontent.com/hofong159/portfolio-assets/main/";')
# types
s=s.replace('''type Certificate = {
  id: number;''','''type Stat = { id: number; value: string; label: string };
type SkillGroup = { id: number; label: string; tools: string };
type Certificate = {
  id: number;''')
s=s.replace('''  certificates: Certificate[];
  heroBackground:''','''  certificates: Certificate[];
  stats: Stat[];
  skills: SkillGroup[];
  heroBackground:''')
# default content
needle='''  certificates: [
    { id: 1, title: '建築師資格證書', issuer: '台灣建築師公會', year: '2025', credential: 'TW-ARCH-2025-001', description: '建築專業資格與執業相關證明。', imageFile: '', pdfFile: '', link: '' },
    { id: 2, title: '互動媒體設計證書', issuer: 'Digital Futures Lab', year: '2024', credential: 'DFL-IM-2024-018', description: '互動設計與數位敘事實務認證。', imageFile: '', pdfFile: '', link: '' },
  ],
'''
replacement=needle+'''  stats: [
    { id: 1, value: '08', label: '跨域專案' },
    { id: 2, value: '04', label: '合作城市' },
    { id: 3, value: '12', label: '展覽與發表' },
    { id: 4, value: '∞', label: '持續研究中' },
  ],
  skills: [
    { id: 1, label: '設計／空間', tools: 'Rhino · Grasshopper · AutoCAD · Blender · Adobe CC' },
    { id: 2, label: '程式／系統', tools: 'React · TypeScript · WebGL · Firebase · Prototyping' },
    { id: 3, label: '方法／研究', tools: '田野調查 · 編輯 · 展覽 · 視覺敘事' },
  ],
'''
if needle not in s: raise SystemExit('default certificates anchor missing')
s=s.replace(needle,replacement,1)
# loader
s=s.replace('''      certificates: Array.isArray(parsed.certificates) ? parsed.certificates : DEFAULT_CONTENT.certificates,
      projects:''','''      certificates: Array.isArray(parsed.certificates) ? parsed.certificates : DEFAULT_CONTENT.certificates,
      stats: Array.isArray(parsed.stats) ? parsed.stats : DEFAULT_CONTENT.stats,
      skills: Array.isArray(parsed.skills) ? parsed.skills : DEFAULT_CONTENT.skills,
      projects:''')
# render stats and skills
old='''<div className="stats-row"><div><strong>08</strong><span>跨域專案</span></div><div><strong>04</strong><span>合作城市</span></div><div><strong>12</strong><span>展覽與發表</span></div><div><strong>∞</strong><span>持續研究中</span></div></div>'''
new='''<div className="stats-row">{content.stats.map((stat) => <div key={stat.id}><strong>{stat.value}</strong><span>{stat.label}</span></div>)}</div>'''
if old not in s: raise SystemExit('stats render anchor missing')
s=s.replace(old,new,1)
old='''<div className="skills-grid"><div><span className="skill-label">DESIGN / SPACE</span><p>Rhino · Grasshopper · AutoCAD · Blender · Adobe CC</p></div><div><span className="skill-label">CODE / SYSTEMS</span><p>React · TypeScript · WebGL · Firebase · Prototyping</p></div><div><span className="skill-label">METHOD / RESEARCH</span><p>Fieldwork · Editorial · Exhibition · Visual Storytelling</p></div></div>'''
new='''<div className="skills-grid">{content.skills.map((skill) => <div key={skill.id}><span className="skill-label">{skill.label}</span><p>{skill.tools}</p></div>)}</div>'''
if old not in s: raise SystemExit('skills render anchor missing')
s=s.replace(old,new,1)
# Admin menu make usable, with section ids
old='''<div className="admin-menu"><a className="active"><Pencil size={15} /> 個人資料</a><a><Layers3 size={15} /> 作品集 <span>{draft.projects.length}</span></a><a><ImagePlus size={15} /> 媒體素材</a><a><Cloud size={15} /> Firebase 同步</a></div>'''
new='''<div className="admin-menu"><button className="active" onClick={() => document.getElementById("admin-profile")?.scrollIntoView({ behavior: "smooth" })}><Pencil size={15} /> 個人資料</button><button onClick={() => document.getElementById("admin-projects")?.scrollIntoView({ behavior: "smooth" })}><Layers3 size={15} /> 作品集 <span>{draft.projects.length}</span></button><button onClick={() => document.getElementById("admin-media")?.scrollIntoView({ behavior: "smooth" })}><ImagePlus size={15} /> 媒體素材</button><button onClick={() => document.getElementById("admin-sync")?.scrollIntoView({ behavior: "smooth" })}><Cloud size={15} /> Firebase 同步</button></div>'''
if old not in s: raise SystemExit('admin menu anchor missing')
s=s.replace(old,new,1)
# Add ids to existing sections by unique snippets
s=s.replace('''<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">01</span><h3>首頁主視覺</h3>''','''<section className="editor-card" id="admin-profile"><div className="editor-card-head"><div><span className="card-number">01</span><h3>首頁主視覺</h3>''',1)
s=s.replace('''<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">02</span><h3>作品集管理</h3>''','''<section className="editor-card" id="admin-projects"><div className="editor-card-head"><div><span className="card-number">02</span><h3>作品集管理</h3>''',1)
# first-level filename placeholders and wording
s=s.replace('placeholder="portrait-2026.webp"','placeholder="portrait-2026.webp（放在素材 repo 第一層）"')
s=s.replace('照片檔名（每行一個）','照片檔名（每行一個，直接放素材 repo 第一層）')
s=s.replace('PDF 檔名或網址（可留白）','PDF 檔名或網址（可留白，直接放素材 repo 第一層）')
s=s.replace('placeholder="case-study.pdf"','placeholder="case-study.pdf"')
s=s.replace('placeholder="照片檔名或路徑"','placeholder="照片檔名（例如 project.jpg）"')
s=s.replace('placeholder="PDF 檔名或路徑"','placeholder="PDF 檔名（例如 case-study.pdf）"')
# Add editable stats/skills before category editor
marker='''<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">03</span><h3>分類標籤</h3></div>'''
insert='''<section className="editor-card" id="admin-profile-details"><div className="editor-card-head"><div><span className="card-number">03</span><h3>首頁統計與技能</h3></div><span>PUBLIC / PROFILE</span></div><div className="admin-subhead">統計數字</div>{draft.stats.map((stat) => <div className="repeat-editor" key={stat.id}><input value={stat.value} placeholder="數字" onChange={(event) => setDraft((previous) => ({ ...previous, stats: previous.stats.map((item) => item.id === stat.id ? { ...item, value: event.target.value } : item) }))} /><input value={stat.label} placeholder="標籤" onChange={(event) => setDraft((previous) => ({ ...previous, stats: previous.stats.map((item) => item.id === stat.id ? { ...item, label: event.target.value } : item) }))} /></div>)}<div className="admin-subhead notes-head">技能分類與內容</div>{draft.skills.map((skill) => <div className="repeat-editor" key={skill.id}><input value={skill.label} placeholder="中文分類名稱" onChange={(event) => setDraft((previous) => ({ ...previous, skills: previous.skills.map((item) => item.id === skill.id ? { ...item, label: event.target.value } : item) }))} /><input value={skill.tools} placeholder="軟體或技能，用 · 分隔" onChange={(event) => setDraft((previous) => ({ ...previous, skills: previous.skills.map((item) => item.id === skill.id ? { ...item, tools: event.target.value } : item) }))} /></div>)}</section><section className="editor-card"><div className="editor-card-head"><div><span className="card-number">04</span><h3>分類標籤</h3></div>'''
if marker not in s: raise SystemExit('category marker missing')
s=s.replace(marker,insert,1)
# IDs for media and sync based on content snippets
s=s.replace('''<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">04</span><h3>背景與社群</h3>''','''<section className="editor-card" id="admin-media"><div className="editor-card-head"><div><span className="card-number">07</span><h3>背景與社群</h3>''',1)
s=s.replace('''<section className="editor-card mini-editor"><div className="editor-card-head"><div><span className="card-number">05</span><h3>聯絡資訊</h3>''','''<section className="editor-card mini-editor" id="admin-sync"><div className="editor-card-head"><div><span className="card-number">08</span><h3>聯絡資訊</h3>''',1)
# Ensure user sees first-level rule in sidebar
s=s.replace('''<p>編輯文字、圖片、作品與網站狀態。儲存後會保留在此瀏覽器。</p>''','''<p>編輯文字、圖片、作品與網站狀態。素材請直接放在 GitHub 素材 repository 第一層，儲存後保留在此瀏覽器。</p>''')
p.write_text(s)

# Make direct first-level assets clear in guide
for guide in [Path('/home/ubuntu/hofong-portfolio/ASSET_GUIDE.md'), Path('/home/ubuntu/portfolio-assets-repo/ASSET_GUIDE.md')]:
    if guide.exists():
        text=guide.read_text()
        text=text.replace('images/\n', '').replace('pdf/\n', '')
        text += '\n## 最新規則：直接放在 repository 第一層\n\n照片與 PDF 不需要建立子資料夾，直接拖曳到 `portfolio-assets` repository 的第一層即可。後台只填完整檔名，例如 `portrait.webp` 或 `case-study.pdf`。\n'
        guide.write_text(text)
