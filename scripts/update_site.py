from pathlib import Path

root = Path('/home/ubuntu/hofong-portfolio')
home = root / 'client/src/pages/Home.tsx'
text = home.read_text()

text = text.replace('import { syncSiteContent } from "@/lib/firebase";', 'import { auth, syncSiteContent } from "@/lib/firebase";\nimport { onAuthStateChanged, signInWithEmailAndPassword, signOut } from "firebase/auth";')
text = text.replace('  projects: Project[];\n};', '''  projects: Project[];
  heroBackground: string;
  instagram: string;
  experiences: { id: number; year: string; title: string; detail: string }[];
  notes: { id: number; type: string; title: string; description: string; readTime: string }[];
};''')
text = text.replace('  portrait: `${IMAGE_BASE}photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=1000&q=85`,\n  projects:', '''  portrait: `${IMAGE_BASE}photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=1000&q=85`,
  heroBackground: 'https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=2200&q=85',
  instagram: 'https://www.instagram.com/',
  experiences: [
    { id: 1, year: '2026', title: 'Independent Practice', detail: '以個人工作室形式承接建築視覺、互動展覽與數位敘事專案。' },
    { id: 2, year: '2024', title: 'Urban Research Lab', detail: '參與城市觀察計畫，將田野資料轉譯為可被公眾閱讀的開放檔案。' },
    { id: 3, year: '2022', title: 'M.Arch / Taipei', detail: '完成建築研究所學位，研究光、材料與短暫公共性之間的關係。' },
  ],
  notes: [
    { id: 1, type: 'FIELD NOTE / 01', title: '為什麼我還在拍\n城市的背面？', description: '那些沒有被拍進旅遊指南的邊角，往往更接近一座城市真正的呼吸。', readTime: '06 MIN READ' },
    { id: 2, type: 'PROCESS / 02', title: '從一張紙開始的\n互動原型', description: '在螢幕之前，先讓手和眼睛一起想。', readTime: '04 MIN READ' },
  ],
  projects:''')
text = text.replace('const [page, setPage] = useState<"home" | "admin">("home");', 'const [page, setPage] = useState<"home" | "admin">("home");\n  const [adminUser, setAdminUser] = useState<import("firebase/auth").User | null>(null);')
text = text.replace('  const [dragging, setDragging] = useState(false);', '''  const [dragging, setDragging] = useState(false);
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [loginError, setLoginError] = useState('');''')
text = text.replace('  useEffect(() => {\n    document.documentElement.dataset.theme = theme;\n  }, [theme]);', '''  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    return onAuthStateChanged(auth, setAdminUser);
  }, [theme]);''')
text = text.replace('  const filteredProjects = useMemo(', '''  const filteredProjects = useMemo(''')
text = text.replace('''<button onClick={() => scrollTo("about")}>關於</button>
          <button onClick={() => scrollTo("work")}>作品</button>
          <button onClick={() => scrollTo("journal")}>筆記</button>
          <button onClick={() => scrollTo("contact")}>聯絡</button>''', '''<button onClick={() => scrollTo("about")}>關於</button>
          <button onClick={() => scrollTo("timeline")}>經歷</button>
          <button onClick={() => scrollTo("work")}>作品</button>
          <button onClick={() => scrollTo("journal")}>筆記</button>
          <button onClick={() => scrollTo("contact")}>聯絡</button>''')
text = text.replace('''<div className="hero-backdrop" />''', '''<div className="hero-backdrop" style={{ backgroundImage: `linear-gradient(90deg, rgba(11,13,14,.97) 5%, rgba(11,13,14,.76) 45%, rgba(11,13,14,.34)), url('${content.heroBackground}')` }} />''')
# Move the timeline section before the work section by removing and reinserting the exact section block.
start = text.index('          <section className="timeline-section" id="timeline">')
end = text.index('          <section className="journal-section" id="journal">', start)
timeline = text[start:end]
text = text[:start] + text[end:]
work_marker = '          <section className="work-section" id="work">'
text = text.replace(work_marker, timeline + '\n' + work_marker, 1)
# Replace hard-coded timeline items with editable content.
old_timeline = '''{[
              ["2026", "Independent Practice", "以個人工作室形式承接建築視覺、互動展覽與數位敘事專案。"],
              ["2024", "Urban Research Lab", "參與城市觀察計畫，將田野資料轉譯為可被公眾閱讀的開放檔案。"],
              ["2022", "M.Arch / Taipei", "完成建築研究所學位，研究光、材料與短暫公共性之間的關係。"],
            ].map(([date, title, detail]) => <div className="timeline-item" key={date}><span className="timeline-date">{date}</span><div><h3>{title}</h3><p>{detail}</p></div></div>)}'''
new_timeline = '''content.experiences.map((experience) => <div className="timeline-item" key={experience.id}><span className="timeline-date">{experience.year}</span><div><h3>{experience.title}</h3><p>{experience.detail}</p></div></div>)'''
text = text.replace(old_timeline, new_timeline)
# Replace hard-coded journal cards with editable notes.
old_notes = '''<div className="journal-grid"><article className="note-card featured"><span className="note-type">FIELD NOTE / 01</span><h3>為什麼我還在拍<br />城市的背面？</h3><p>那些沒有被拍進旅遊指南的邊角，往往更接近一座城市真正的呼吸。</p><div className="note-footer"><span>06 MIN READ</span><ArrowUpRight size={16} /></div></article><article className="note-card"><span className="note-type">PROCESS / 02</span><h3>從一張紙開始的<br />互動原型</h3><p>在螢幕之前，先讓手和眼睛一起想。</p><div className="note-footer"><span>04 MIN READ</span><ArrowUpRight size={16} /></div></article><article className="now-card"><div className="now-header"><span className="pulse-dot" /> NOW / 2026.09</div><h3>目前正在研究</h3><ul><li><span>01</span>城市聲景與移動中的記憶</li><li><span>02</span>小型展覽的可重複系統</li><li><span>03</span>一個還在長大的作品集後台</li></ul><span className="now-footer">更新於今天，保持開放。</span></article></div>'''
new_notes = '''<div className="journal-grid">{content.notes.map((note, index) => <article className={`note-card ${index === 0 ? 'featured' : ''}`} key={note.id}><span className="note-type">{note.type}</span><h3>{note.title.split('\\n').map((line) => <span key={line}>{line}<br /></span>)}</h3><p>{note.description}</p><div className="note-footer"><span>{note.readTime}</span><ArrowUpRight size={16} /></div></article>)}<article className="now-card"><div className="now-header"><span className="pulse-dot" /> NOW / 2026.09</div><h3>目前正在研究</h3><ul><li><span>01</span>城市聲景與移動中的記憶</li><li><span>02</span>小型展覽的可重複系統</li><li><span>03</span>一個還在長大的作品集後台</li></ul><span className="now-footer">更新於今天，保持開放。</span></article></div>'''
text = text.replace(old_notes, new_notes)
text = text.replace('''<a href="https://www.instagram.com/" target="_blank" rel="noreferrer"><Instagram size={17} /> Instagram</a>''', '''<a href={content.instagram} target="_blank" rel="noreferrer"><Instagram size={17} /> Instagram</a>''')
# Replace AdminPanel invocation with auth-aware props.
old_call = '''<AdminPanel draft={adminDraft} setDraft={setAdminDraft} newImageName={newImageName} setNewImageName={setNewImageName} addImageByName={addImageByName} addProject={addProject} newProject={newProject} setNewProject={setNewProject} deleteProject={deleteProject} saveAdmin={saveAdmin} syncFirebase={syncFirebase} dragging={dragging} setDragging={setDragging} handleDrop={handleDrop} goHome={() => setPage("home")} />'''
new_call = '''<AdminPanel draft={adminDraft} setDraft={setAdminDraft} newImageName={newImageName} setNewImageName={setNewImageName} addImageByName={addImageByName} addProject={addProject} newProject={newProject} setNewProject={setNewProject} deleteProject={deleteProject} saveAdmin={saveAdmin} syncFirebase={syncFirebase} dragging={dragging} setDragging={setDragging} handleDrop={handleDrop} goHome={() => setPage("home")} adminUser={adminUser} loginEmail={loginEmail} setLoginEmail={setLoginEmail} loginPassword={loginPassword} setLoginPassword={setLoginPassword} loginError={loginError} setLoginError={setLoginError} onLogin={async (event) => { event.preventDefault(); setLoginError(''); try { await signInWithEmailAndPassword(auth, loginEmail, loginPassword); } catch { setLoginError('登入失敗，請確認 Firebase Email/Password 帳號與密碼。'); } }} onLogout={() => signOut(auth)} />'''
text = text.replace(old_call, new_call)
# Replace AdminPanel function signature and add login gate.
text = text.replace('''function AdminPanel({ draft, setDraft, newImageName, setNewImageName, addImageByName, addProject, newProject, setNewProject, deleteProject, saveAdmin, syncFirebase, dragging, setDragging, handleDrop, goHome }: { draft: SiteContent; setDraft: React.Dispatch<React.SetStateAction<SiteContent>>; newImageName: string; setNewImageName: (value: string) => void; addImageByName: (filename: string) => void; addProject: () => void; newProject: { title: string; category: Exclude<Category, "全部">; description: string }; setNewProject: React.Dispatch<React.SetStateAction<{ title: string; category: Exclude<Category, "全部">; description: string }>>; deleteProject: (id: number) => void; saveAdmin: () => void; syncFirebase: () => void; dragging: boolean; setDragging: (value: boolean) => void; handleDrop: (event: React.DragEvent<HTMLDivElement>) => void; goHome: () => void }) {\n  return <main className="admin-page">''', '''function AdminPanel({ draft, setDraft, newImageName, setNewImageName, addImageByName, addProject, newProject, setNewProject, deleteProject, saveAdmin, syncFirebase, dragging, setDragging, handleDrop, goHome, adminUser, loginEmail, setLoginEmail, loginPassword, setLoginPassword, loginError, setLoginError, onLogin, onLogout }: { draft: SiteContent; setDraft: React.Dispatch<React.SetStateAction<SiteContent>>; newImageName: string; setNewImageName: (value: string) => void; addImageByName: (filename: string) => void; addProject: () => void; newProject: { title: string; category: Exclude<Category, "全部">; description: string }; setNewProject: React.Dispatch<React.SetStateAction<{ title: string; category: Exclude<Category, "全部">; description: string }>>; deleteProject: (id: number) => void; saveAdmin: () => void; syncFirebase: () => void; dragging: boolean; setDragging: (value: boolean) => void; handleDrop: (event: React.DragEvent<HTMLDivElement>) => void; goHome: () => void; adminUser: import("firebase/auth").User | null; loginEmail: string; setLoginEmail: (value: string) => void; loginPassword: string; setLoginPassword: (value: string) => void; loginError: string; setLoginError: (value: string) => void; onLogin: (event: React.FormEvent) => void; onLogout: () => void }) {
  if (!adminUser) return <main className="admin-page login-page"><div className="login-card"><button className="brand" onClick={goHome}><span className="brand-mark">H</span><span><strong>廖和風</strong><small>Content Studio</small></span></button><div className="section-kicker">PRIVATE AREA / AUTH REQUIRED</div><h1>登入內容控制台</h1><p>使用已在 Firebase 啟用的 Email / Password 帳號登入，才能編輯網站內容與同步資料。</p><form onSubmit={onLogin}><label>Email<input type="email" required value={loginEmail} onChange={(event) => setLoginEmail(event.target.value)} placeholder="you@example.com" /></label><label>Password<input type="password" required value={loginPassword} onChange={(event) => setLoginPassword(event.target.value)} placeholder="••••••••" /></label>{loginError && <div className="login-error">{loginError}</div>}<button className="button button-primary" type="submit">登入控制台 <ArrowUpRight size={15} /></button></form><button className="back-home" onClick={goHome}>← 回到公開網站</button></div></main>;
  return <main className="admin-page">''')
text = text.replace('''<button className="button button-primary" onClick={saveAdmin}><Save size={15} /> 儲存變更</button>''', '''<div className="admin-user">{adminUser.email}<button className="logout-button" onClick={onLogout}>登出</button></div><button className="button button-primary" onClick={saveAdmin}><Save size={15} /> 儲存變更</button>''')
# Add editable social/background and experiences/notes panels before mini editor.
needle = '<section className="editor-card mini-editor">'
addition = '''<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">03</span><h3>經歷與筆記</h3></div><span>PUBLIC / CONTENT</span></div><div className="admin-subhead">經歷時間軸</div>{draft.experiences.map((experience) => <div className="repeat-editor" key={experience.id}><input value={experience.year} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, year: event.target.value } : item) }))} /><input value={experience.title} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, title: event.target.value } : item) }))} /><textarea value={experience.detail} rows={2} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, detail: event.target.value } : item) }))} /></div>)}<div className="admin-subhead notes-head">筆記卡片</div>{draft.notes.map((note) => <div className="repeat-editor note-editor" key={note.id}><input value={note.type} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, type: event.target.value } : item) }))} /><input value={note.readTime} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, readTime: event.target.value } : item) }))} /><input value={note.title} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, title: event.target.value } : item) }))} /><textarea value={note.description} rows={2} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, description: event.target.value } : item) }))} /></div>)}</section><section className="editor-card"><div className="editor-card-head"><div><span className="card-number">04</span><h3>背景與社群</h3></div><span>PUBLIC / LINKS</span></div><label>Hero 背景圖片網址<input value={draft.heroBackground} onChange={(event) => setDraft((previous) => ({ ...previous, heroBackground: event.target.value }))} /></label><div className="field-grid"><label>Email<input value={draft.email} onChange={(event) => setDraft((previous) => ({ ...previous, email: event.target.value }))} /></label><label>Instagram 連結<input value={draft.instagram} onChange={(event) => setDraft((previous) => ({ ...previous, instagram: event.target.value }))} /></label></div></section>'''
text = text.replace(needle, addition + needle)
# Rename duplicate card number for contact section.
text = text.replace('<span className="card-number">03</span><h3>聯絡資訊</h3>', '<span className="card-number">05</span><h3>聯絡資訊</h3>')
# keep safe no empty output
home.write_text(text)

firebase = root / 'client/src/lib/firebase.ts'
ftext = firebase.read_text()
ftext = ftext.replace('import { getApp, getApps, initializeApp } from "firebase/app";', 'import { getApp, getApps, initializeApp } from "firebase/app";\nimport { getAuth } from "firebase/auth";')
ftext = ftext.replace('export async function syncSiteContent', 'export const auth = getAuth(getApps().length ? getApp() : initializeApp(firebaseConfig));\n\nexport async function syncSiteContent')
firebase.write_text(ftext)

css = root / 'client/src/index.css'
ctext = css.read_text()
ctext += '''\n.admin-user { display: flex; align-items: center; gap: 12px; color: var(--muted); font: 10px 'DM Mono',monospace; }.logout-button { color: var(--accent); border: 0; background: none; cursor: pointer; font: inherit; }.admin-subhead { color: var(--accent); font: 10px 'DM Mono',monospace; letter-spacing: .1em; margin: 17px 0 9px; }.notes-head { margin-top: 31px; }.repeat-editor { display: grid; grid-template-columns: .22fr .7fr 1.2fr; gap: 9px; margin-bottom: 9px; }.repeat-editor.note-editor { grid-template-columns: .45fr .35fr .7fr 1.2fr; }.repeat-editor input, .repeat-editor textarea { margin: 0; }.login-page { display: grid; place-items: center; padding: 22px; }.login-card { width: min(440px, 100%); padding: clamp(27px, 6vw, 52px); background: var(--surface); border: 1px solid var(--line-strong); box-shadow: 0 20px 70px rgba(0,0,0,.25); }.login-card .brand { margin-bottom: 54px; }.login-card h1 { font-size: clamp(31px, 6vw, 48px); line-height: 1.1; letter-spacing: -.07em; margin: 17px 0 10px; }.login-card p { color: var(--muted); font-size: 12px; line-height: 1.8; margin-bottom: 27px; }.login-card form { display: grid; gap: 15px; }.login-card label { display: grid; gap: 6px; color: var(--muted); font: 10px 'DM Mono',monospace; }.login-card input { border: 1px solid var(--line); background: var(--surface-2); color: var(--ink); padding: 11px 12px; outline: 0; }.login-card input:focus { border-color: var(--accent); }.login-error { color: #ff8c7d; font-size: 11px; border-left: 2px solid #ff8c7d; padding-left: 9px; }.back-home { border: 0; background: none; color: var(--muted); padding: 0; margin-top: 24px; font-size: 11px; cursor: pointer; }.back-home:hover { color: var(--accent); }\n@media (max-width: 650px) { .repeat-editor, .repeat-editor.note-editor { grid-template-columns: 1fr; }.admin-user { display: none; } }\n'''
css.write_text(ctext)
