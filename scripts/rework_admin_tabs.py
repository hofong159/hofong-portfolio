from pathlib import Path
import re
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
# State and main data attribute.
s=s.replace('''function AdminPanel({ draft,''','''function AdminPanel({ draft,''',1)
needle='''  if (!adminUser) return <main className="admin-page login-page">'''
s=s.replace(needle,'''  const [activeTab, setActiveTab] = useState("home");
  const tabs = [{ id: "home", label: "首頁" }, { id: "experience", label: "經歷" }, { id: "work", label: "作品集" }, { id: "certificates", label: "證照" }, { id: "notes", label: "筆記" }, { id: "contact", label: "聯絡" }];

  if (!adminUser) return <main className="admin-page login-page">''',1)
s=s.replace('''<div className="admin-main"><div className="admin-heading">''','''<div className="admin-main" data-active-tab={activeTab}><div className="admin-heading">''',1)
# Replace sidebar static menu with tab controls.
old='''<div className="admin-menu"><button className="active" onClick={() => document.getElementById("admin-profile")?.scrollIntoView({ behavior: "smooth" })}><Pencil size={15} /> 個人資料</button><button onClick={() => document.getElementById("admin-projects")?.scrollIntoView({ behavior: "smooth" })}><Layers3 size={15} /> 作品集 <span>{draft.projects.length}</span></button><button onClick={() => document.getElementById("admin-media")?.scrollIntoView({ behavior: "smooth" })}><ImagePlus size={15} /> 媒體素材</button><button onClick={() => document.getElementById("admin-sync")?.scrollIntoView({ behavior: "smooth" })}><Cloud size={15} /> Firebase 同步</button></div>'''
new='''<div className="admin-menu">{tabs.map((tab) => <button key={tab.id} className={activeTab === tab.id ? "active" : ""} onClick={() => setActiveTab(tab.id)}><Pencil size={15} /> {tab.label}{tab.id === "work" && <span>{draft.projects.length}</span>}</button>)}</div>'''
if old not in s: raise SystemExit('admin menu anchor missing')
s=s.replace(old,new,1)
# Add panel metadata by unique section IDs.
for id_, panel in [("admin-home-copy","home"),("admin-profile","home"),("admin-projects","work"),("admin-profile-details","home"),("admin-media","contact"),("admin-sync","contact")]:
    s=s.replace(f'id="{id_}"', f'id="{id_}" data-admin-panels="{panel}"', 1)
# Sections without IDs identified by their headings.
for heading, panel in [("證照與證書","certificates"),("經歷與筆記","experience notes")]:
    pattern=r'<section className="editor-card">(?=(?:(?!</section>).)*<h3>'+re.escape(heading)+r'</h3>)'
    s,n=re.subn(pattern, f'<section className="editor-card" data-admin-panels="{panel}">', s, count=1, flags=re.S)
    if n != 1: raise SystemExit(f'section heading missing: {heading}')
# Remove non-editable promotional/helper copy from admin while retaining field labels.
s=re.sub(r'<div className="admin-status">.*?</div>', '', s, count=1)
s=re.sub(r'<p>編輯文字、圖片、作品與網站狀態。素材請直接放在 GitHub 素材 repository 第一層，儲存後保留在此瀏覽器。</p>', '', s, count=1)
s=re.sub(r'<div className="firebase-card">.*?</div></aside>', '</aside>', s, count=1, flags=re.S)
s=re.sub(r'<p className="helper-copy">.*?</p>', '', s, count=1)
s=re.sub(r'<div className="editor-note">.*?</div>', '', s, count=1)
p.write_text(s)

css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
c += '''\n/* Admin workspace tabs: one focused editor at a time, ordered like the public site. */\n.admin-main[data-active-tab] [data-admin-panels] { display:none; }\n.admin-main[data-active-tab="home"] [data-admin-panels~="home"], .admin-main[data-active-tab="experience"] [data-admin-panels~="experience"], .admin-main[data-active-tab="work"] [data-admin-panels~="work"], .admin-main[data-active-tab="certificates"] [data-admin-panels~="certificates"], .admin-main[data-active-tab="notes"] [data-admin-panels~="notes"], .admin-main[data-active-tab="contact"] [data-admin-panels~="contact"] { display:block; }\n.admin-menu { display:grid; gap:7px; }.admin-menu button { display:flex; align-items:center; gap:9px; width:100%; text-align:left; }.admin-menu button span { margin-left:auto; color:var(--accent); font:10px 'DM Mono',monospace; }.admin-menu button.active { color:var(--ink); border-color:var(--accent); background:rgba(214,255,93,.08); }\n'''
css.write_text(c)
