from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
# Data model and defaults for the research card.
s=s.replace('''  notes: { id: number; type: string; title: string; description: string; readTime: string }[];
};''','''  notes: { id: number; type: string; title: string; description: string; readTime: string }[];
  nowKicker: string;
  nowTitle: string;
  nowItems: string[];
  nowFooter: string;
};''')
s=s.replace('''  notes: [
    { id: 1, type: 'FIELD NOTE / 01', title: '為什麼我還在拍\\n城市的背面？', description: '那些沒有被拍進旅遊指南的邊角，往往更接近一座城市真正的呼吸。', readTime: '06 MIN READ' },
    { id: 2, type: 'PROCESS / 02', title: '從一張紙開始的\\n互動原型', description: '在螢幕之前，先讓手和眼睛一起想。', readTime: '04 MIN READ' },
  ],''','''  notes: [
    { id: 1, type: 'FIELD NOTE / 01', title: '為什麼我還在拍\\n城市的背面？', description: '那些沒有被拍進旅遊指南的邊角，往往更接近一座城市真正的呼吸。', readTime: '06 MIN READ' },
    { id: 2, type: 'PROCESS / 02', title: '從一張紙開始的\\n互動原型', description: '在螢幕之前，先讓手和眼睛一起想。', readTime: '04 MIN READ' },
  ],
  nowKicker: 'NOW / 2026.09',
  nowTitle: '目前正在研究',
  nowItems: ['城市聲景與移動中的記憶', '小型展覽的可重複系統', '一個還在長大的作品集後台'],
  nowFooter: '更新於今天，保持開放。',''',1)
# Normalize both local and remote loaders.
for marker in ['''      notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,
''','''    notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,
''']:
    if marker in s:
        s=s.replace(marker, marker + '''      nowKicker: typeof parsed.nowKicker === "string" ? parsed.nowKicker : DEFAULT_CONTENT.nowKicker,
      nowTitle: typeof parsed.nowTitle === "string" ? parsed.nowTitle : DEFAULT_CONTENT.nowTitle,
      nowItems: Array.isArray(parsed.nowItems) ? parsed.nowItems.filter((item): item is string => typeof item === "string") : DEFAULT_CONTENT.nowItems,
      nowFooter: typeof parsed.nowFooter === "string" ? parsed.nowFooter : DEFAULT_CONTENT.nowFooter,
''',1)
# Public section navigation state.
s=s.replace('''  const [filter, setFilter] = useState<Category>("全部");
''','''  const [filter, setFilter] = useState<Category>("全部");
  const [activeSection, setActiveSection] = useState<"profile" | "timeline" | "work" | "certificates" | "journal" | "contact">("profile");
''',1)
s=s.replace('''  const [dragging, setDragging] = useState(false);
''','''  const [dragging, setDragging] = useState(false);
  const [dragKey, setDragKey] = useState<string | null>(null);
''',1)
# Replace scroll function.
s=s.replace('''  const scrollTo = (id: string) => {
    setPage("home");
    setMobileNav(false);
    window.setTimeout(() => document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }), 40);
  };''','''  const scrollTo = (id: string) => {
    setPage("home");
    setMobileNav(false);
    const next = id === "about" ? "profile" : id as "timeline" | "work" | "certificates" | "journal" | "contact";
    setActiveSection(next);
    window.setTimeout(() => document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }), 40);
  };''',1)
# Root class gets active public section.
s=s.replace('''<div className={`site-shell ${theme === "light" ? "is-light" : ""}`}>''','''<div className={`site-shell section-${activeSection} ${theme === "light" ? "is-light" : ""}`}>''',1)
# Research card becomes data-driven.
old='''<article className="now-card"><div className="now-header"><span className="pulse-dot" /> NOW / 2026.09</div><h3>目前正在研究</h3><ul><li><span>01</span>城市聲景與移動中的記憶</li><li><span>02</span>小型展覽的可重複系統</li><li><span>03</span>一個還在長大的作品集後台</li></ul><span className="now-footer">更新於今天，保持開放。</span></article>'''
new='''<article className="now-card"><div className="now-header"><span className="pulse-dot" /> {content.nowKicker}</div><h3>{content.nowTitle}</h3><ul>{content.nowItems.map((item, index) => <li key={`${item}-${index}`}><span>{String(index + 1).padStart(2, "0")}</span>{item}</li>)}</ul><span className="now-footer">{content.nowFooter}</span></article>'''
if old not in s: raise SystemExit('now card not found')
s=s.replace(old,new,1)
# Add drag callbacks before sync.
anchor='''  const syncFirebase = async () => {'''
callbacks='''  const moveByDrag = (kind: "projects" | "experiences" | "notes", sourceId: number, targetId: number) => {
    if (sourceId === targetId) return;
    setAdminDraft((previous) => {
      const list = previous[kind] as { id: number }[];
      const from = list.findIndex((item) => item.id === sourceId);
      const to = list.findIndex((item) => item.id === targetId);
      if (from < 0 || to < 0) return previous;
      const next = [...list];
      const [item] = next.splice(from, 1);
      next.splice(to, 0, item);
      return { ...previous, [kind]: next } as SiteContent;
    });
    setDragKey(null);
  };
  const beginDrag = (key: string) => setDragKey(key);
  const dropDrag = (kind: "projects" | "experiences" | "notes", targetId: number) => {
    if (!dragKey) return;
    const [sourceKind, sourceId] = dragKey.split(":");
    if (sourceKind === kind) moveByDrag(kind, Number(sourceId), targetId);
    else setDragKey(null);
  };

'''
if anchor not in s: raise SystemExit('sync anchor missing')
s=s.replace(anchor,callbacks+anchor,1)
# AdminPanel props and call are on the same long line; add functions to signature and call.
s=s.replace('''moveExperience, addExperience, deleteExperience, moveNote, addNote, deleteNote, reorder, adminUser''','''moveExperience, addExperience, deleteExperience, moveNote, addNote, deleteNote, reorder, beginDrag, dropDrag, adminUser''',1)
s=s.replace('''deleteNote: (id: number) => void; reorder: <T,>(items: T[], index: number, direction: -1 | 1) => T[]; saveAdmin''','''deleteNote: (id: number) => void; reorder: <T,>(items: T[], index: number, direction: -1 | 1) => T[]; beginDrag: (key: string) => void; dropDrag: (kind: "projects" | "experiences" | "notes", targetId: number) => void; saveAdmin''',1)
# Existing AdminPanel invocation props near bottom.
s=s.replace('''moveNote={moveNote} addNote={addNote} deleteNote={deleteNote} reorder={reorder}''','''moveNote={moveNote} addNote={addNote} deleteNote={deleteNote} reorder={reorder} beginDrag={beginDrag} dropDrag={dropDrag}''',1)
# Add native drag handlers to project, experience, note editor wrappers.
s=s.replace('''<div className="project-editor" key={project.id}>''','''<div className="project-editor" key={project.id} draggable onDragStart={() => beginDrag(`projects:${project.id}`)} onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("projects", project.id)}>''',1)
s=s.replace('''<div className="repeat-editor" key={experience.id}>''','''<div className="repeat-editor" key={experience.id} draggable onDragStart={() => beginDrag(`experiences:${experience.id}`)} onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("experiences", experience.id)}>''',1)
s=s.replace('''<div className="repeat-editor note-editor" key={note.id}>''','''<div className="repeat-editor note-editor" key={note.id} draggable onDragStart={() => beginDrag(`notes:${note.id}`)} onDragOver={(event) => event.preventDefault()} onDrop={() => dropDrag("notes", note.id)}>''',1)
# Add editable research-card fields after work description in the home-copy panel.
needle='''<textarea value={draft.workDescription} rows={3} placeholder="作品集說明" onChange={(event) => setDraft((previous) => ({ ...previous, workDescription: event.target.value }))} /></section>'''
replacement='''<textarea value={draft.workDescription} rows={3} placeholder="作品集說明" onChange={(event) => setDraft((previous) => ({ ...previous, workDescription: event.target.value }))} /><div className="admin-subhead">目前正在研究卡片</div><input value={draft.nowKicker} placeholder="卡片眉標" onChange={(event) => setDraft((previous) => ({ ...previous, nowKicker: event.target.value }))} /><input value={draft.nowTitle} placeholder="卡片標題" onChange={(event) => setDraft((previous) => ({ ...previous, nowTitle: event.target.value }))} /><textarea value={draft.nowItems.join("\\n")} rows={4} placeholder="每行一項研究內容" onChange={(event) => setDraft((previous) => ({ ...previous, nowItems: event.target.value.split("\\n") }))} /><input value={draft.nowFooter} placeholder="卡片底部文字" onChange={(event) => setDraft((previous) => ({ ...previous, nowFooter: event.target.value }))} /></section>'''
if needle not in s: raise SystemExit('home copy end missing')
s=s.replace(needle,replacement,1)
p.write_text(s)

css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
c += '''\n/* Public site: keep the profile visible and open other sections on demand. */\n.site-shell.section-profile #timeline, .site-shell.section-profile #work, .site-shell.section-profile #certificates, .site-shell.section-profile #journal, .site-shell.section-profile #contact { display:none; }\n.site-shell.section-timeline #work, .site-shell.section-timeline #certificates, .site-shell.section-timeline #journal, .site-shell.section-timeline #contact { display:none; }\n.site-shell.section-work #timeline, .site-shell.section-work #certificates, .site-shell.section-work #journal, .site-shell.section-work #contact { display:none; }\n.site-shell.section-certificates #timeline, .site-shell.section-certificates #work, .site-shell.section-certificates #journal, .site-shell.section-certificates #contact { display:none; }\n.site-shell.section-journal #timeline, .site-shell.section-journal #work, .site-shell.section-journal #certificates, .site-shell.section-journal #contact { display:none; }\n.site-shell.section-contact #timeline, .site-shell.section-contact #work, .site-shell.section-contact #certificates, .site-shell.section-contact #journal { display:none; }\n.site-shell::before, .site-shell::after { content:""; position:fixed; pointer-events:none; z-index:0; border-radius:999px; filter:blur(2px); opacity:.24; }\n.site-shell::before { width:42vw; height:42vw; top:18vh; right:-16vw; background:radial-gradient(circle, rgba(53,117,255,.24), transparent 68%); animation: drift-a 13s ease-in-out infinite alternate; }\n.site-shell::after { width:30vw; height:30vw; bottom:4vh; left:-12vw; background:radial-gradient(circle, rgba(214,255,93,.18), transparent 68%); animation: drift-b 16s ease-in-out infinite alternate; }\n.site-shell > * { position:relative; z-index:1; }\n@keyframes drift-a { from { transform:translate3d(0,0,0) scale(1); } to { transform:translate3d(-4vw,3vh,0) scale(1.08); } }\n@keyframes drift-b { from { transform:translate3d(0,0,0) scale(1); } to { transform:translate3d(5vw,-2vh,0) scale(1.12); } }\n.project-editor[draggable], .repeat-editor[draggable] { cursor:grab; transition:transform .18s ease, border-color .18s ease, background .18s ease; }\n.project-editor[draggable]:active, .repeat-editor[draggable]:active { cursor:grabbing; transform:scale(.99); border-color:var(--accent); background:rgba(214,255,93,.045); }\n@media (prefers-reduced-motion: reduce) { .site-shell::before, .site-shell::after { animation:none; } }\n'''
css.write_text(c)
