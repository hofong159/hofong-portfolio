from pathlib import Path
import re
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
s=s.replace('''<div className="hero-meta"><span>01 / 04</span><span className="meta-line" /><span>{content.availability}</span></div>''','''<div className="hero-meta"><span>{content.availability}</span></div>''')
s=s.replace('''<div className="portrait-caption"><span>PORTRAIT / 2026</span><span className="caption-signal">● LIVE</span></div>
                <div className="vertical-label">MAKE / SPACE / MATTER</div>''','')
s=s.replace('''            <div className="scroll-cue"><span>SCROLL TO EXPLORE</span><ArrowDownRight size={15} /></div>''','')
s=s.replace('''                    <span className="project-index">0{index + 1}</span>
''','')
s=s.replace('''<div className="social-links"><a href="https://github.com/" target="_blank" rel="noreferrer"><Github size={17} /> GitHub</a><a href="https://www.linkedin.com/" target="_blank" rel="noreferrer"><Linkedin size={17} /> LinkedIn</a><a href={content.instagram} target="_blank" rel="noreferrer"><Instagram size={17} /> Instagram</a></div>''','''<div className="social-links"><a href={content.instagram} target="_blank" rel="noreferrer"><Instagram size={17} /> Instagram</a></div>''')
start='<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">04</span><h3>分類標籤</h3>'
end='<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">04</span><h3>證照與證書</h3>'
a=s.find(start)
b=s.find(end,a)
if a<0 or b<0: raise SystemExit(f'category anchors missing: {a}, {b}')
replacement='''<section className="editor-card"><div className="editor-card-head"><div><span className="card-number">04</span><h3>作品分類</h3></div><span>EDITABLE / FILTERS</span></div><p className="helper-copy">可直接修改名稱、刪除分類或新增分類；前台篩選與作品下拉選單會同步更新。</p><div className="category-editor-list">{draft.categories.map((category, index) => <div className="category-editor-row" key={`${category}-${index}`}><input value={category} onChange={(event) => setDraft((previous) => ({ ...previous, categories: previous.categories.map((item, itemIndex) => itemIndex === index ? event.target.value : item) }))} /><button className="delete-button" onClick={() => setDraft((previous) => ({ ...previous, categories: previous.categories.filter((_, itemIndex) => itemIndex !== index) }))}>刪除</button></div>)}</div><button className="button button-outline" onClick={() => { const name = window.prompt("請輸入新的作品分類名稱"); if (name?.trim()) setDraft((previous) => ({ ...previous, categories: [...previous.categories, name.trim()] })); }}><span>＋</span> 新增分類</button></section>'''
s=s[:a]+replacement+s[b:]
p.write_text(s)
css=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
c=css.read_text()
if '.category-editor-list' not in c:
    c += '''\n.category-editor-list { display:grid; gap:8px; margin:12px 0 16px; }.category-editor-row { display:grid; grid-template-columns:1fr auto; gap:8px; align-items:center; }.category-editor-row input { margin:0; }.category-editor-row .delete-button { font-size:10px; }\n'''
# Override the existing portrait frame geometry with a square frame.
c += '''\n.portrait-frame { inset: 7% auto auto 12%; width: 78%; aspect-ratio: 1; }\n'''
css.write_text(c)
html=Path('/home/ubuntu/hofong-portfolio/client/index.html')
h=html.read_text()
if 'rel="icon"' not in h:
    h=h.replace('''    <meta name="theme-color" content="#0b0d0e" />''','''    <meta name="theme-color" content="#0b0d0e" />
    <link rel="icon" type="image/jpeg" href="https://raw.githubusercontent.com/hofong159/hofong-portfolio/main/logo.jpg" />''')
html.write_text(h)
