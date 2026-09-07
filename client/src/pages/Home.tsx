import { useEffect, useMemo, useState } from "react";
import {
  ArrowDownRight,
  ArrowUpRight,
  Check,
  ChevronLeft,
  ChevronRight,
  Cloud,
  Code2,
  Copy,
  Download,
  ExternalLink,
  FileText,
  Github,
  ImagePlus,
  Instagram,
  Layers3,
  Linkedin,
  Mail,
  Menu,
  Moon,
  MoveRight,
  Pencil,
  Plus,
  Quote,
  Save,
  Send,
  Settings2,
  Sparkles,
  Sun,
  Trash2,
  Upload,
  X,
} from "lucide-react";
import { auth, syncSiteContent } from "@/lib/firebase";
import { onAuthStateChanged, signInWithEmailAndPassword, signOut } from "firebase/auth";

type Category = "全部" | "建築圖面" | "互動體驗" | "研究實作";
type Project = {
  id: number;
  title: string;
  category: Exclude<Category, "全部">;
  description: string;
  role: string;
  year: string;
  tags: string[];
  images: string[];
  link?: string;
  pdf?: string;
};
type SiteContent = {
  heroEyebrow: string;
  heroTitle: string;
  heroDescription: string;
  email: string;
  availability: string;
  portrait: string;
  projects: Project[];
  heroBackground: string;
  instagram: string;
  experiences: { id: number; year: string; title: string; detail: string }[];
  notes: { id: number; type: string; title: string; description: string; readTime: string }[];
};
type Comment = { id: number; name: string; content: string; date: string };

const IMAGE_BASE = "https://images.unsplash.com/";
const DEFAULT_CONTENT: SiteContent = {
  heroEyebrow: "DIGITAL ARCHITECT / CREATIVE TECHNOLOGIST",
  heroTitle: "把空間思考，轉譯成可被使用的體驗。",
  heroDescription:
    "我是廖和風，專注於建築、互動設計與數位敘事之間的交界。從一張草圖到一個可操作的介面，我讓複雜的想法變得清晰、可感、可持續。",
  email: "hofong159@gmail.com",
  availability: "2026 春季可承接合作",
  portrait: `${IMAGE_BASE}photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=1000&q=85`,
  heroBackground: 'https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=2200&q=85',
  instagram: 'https://www.instagram.com/',
  experiences: [
    { id: 1, year: '2026', title: 'Independent Practice', detail: '以個人工作室形式承接建築視覺、互動展覽與數位敘事專案。' },
    { id: 2, year: '2024', title: 'Urban Research Lab', detail: '參與城市觀察計畫，將田野資料轉譯為可被公眾閱讀的開放檔案。' },
    { id: 3, year: '2022', title: 'M.Arch / Taipei', detail: '完成建築研究所學位，研究光、材料與短暫公共性之間的關係。' },
  ],
  notes: [
    { id: 1, type: 'FIELD NOTE / 01', title: '為什麼我還在拍\\n城市的背面？', description: '那些沒有被拍進旅遊指南的邊角，往往更接近一座城市真正的呼吸。', readTime: '06 MIN READ' },
    { id: 2, type: 'PROCESS / 02', title: '從一張紙開始的\\n互動原型', description: '在螢幕之前，先讓手和眼睛一起想。', readTime: '04 MIN READ' },
  ],
  projects: [
    {
      id: 1,
      title: "光隙計畫／Lightwell",
      category: "建築圖面",
      description: "以自然光為主要材料的城市微型公共空間，探索人與城市的短暫停留。",
      role: "概念、空間設計、視覺敘事",
      year: "2025",
      tags: ["Rhino", "Grasshopper", "Rendering"],
      images: [
        `${IMAGE_BASE}photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1600&q=85`,
        `${IMAGE_BASE}photo-1487958449943-2429e8be8625?auto=format&fit=crop&w=1600&q=85`,
        `${IMAGE_BASE}photo-1497366811353-6870744d04b2?auto=format&fit=crop&w=1600&q=85`,
      ],
    },
    {
      id: 2,
      title: "Common Ground",
      category: "互動體驗",
      description: "一個把社區口述歷史轉成可探索地圖的互動展覽，讓記憶在場域中重新流動。",
      role: "互動策劃、前端原型、展場整合",
      year: "2024",
      tags: ["React", "WebGL", "Exhibition"],
      images: [
        `${IMAGE_BASE}photo-1558655146-d09347e92766?auto=format&fit=crop&w=1600&q=85`,
        `${IMAGE_BASE}photo-1559028012-481c04fa702d?auto=format&fit=crop&w=1600&q=85`,
      ],
      link: "https://github.com/",
    },
    {
      id: 3,
      title: "未完成的城市檔案",
      category: "研究實作",
      description: "以攝影、聲音與開放資料組成的城市觀察檔案，記錄那些尚未被命名的日常。",
      role: "獨立研究、攝影、編輯",
      year: "2023—現在",
      tags: ["Fieldwork", "Archive", "Editorial"],
      images: [
        `${IMAGE_BASE}photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1600&q=85`,
        `${IMAGE_BASE}photo-1497366216548-37526070297c?auto=format&fit=crop&w=1600&q=85`,
      ],
      pdf: "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    },
  ],
};

const seedComments: Comment[] = [
  { id: 1, name: "Mina", content: "喜歡你把研究做得這麼有畫面。", date: "2026.03.12" },
  { id: 2, name: "Alex", content: "Lightwell 的光影敘事很迷人。", date: "2026.02.27" },
];

function loadContent(): SiteContent {
  try {
    const saved = localStorage.getItem("hofong-site-content");
    if (!saved) return DEFAULT_CONTENT;
    const parsed = JSON.parse(saved) as Partial<SiteContent>;
    return {
      ...DEFAULT_CONTENT,
      ...parsed,
      projects: Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects,
      experiences: Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences,
      notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,
    };
  } catch {
    return DEFAULT_CONTENT;
  }
}

function loadComments(): Comment[] {
  try {
    const saved = localStorage.getItem("hofong-comments");
    return saved ? JSON.parse(saved) : seedComments;
  } catch {
    return seedComments;
  }
}

export default function Home() {
  const [content, setContent] = useState<SiteContent>(loadContent);
  const [comments, setComments] = useState<Comment[]>(loadComments);
  const [page, setPage] = useState<"home" | "admin">("home");
  const [adminUser, setAdminUser] = useState<import("firebase/auth").User | null>(null);
  const [filter, setFilter] = useState<Category>("全部");
  const [theme, setTheme] = useState<"dark" | "light">("dark");
  const [activeImage, setActiveImage] = useState<Record<number, number>>({});
  const [selectedProject, setSelectedProject] = useState<Project | null>(null);
  const [lightbox, setLightbox] = useState<{ images: string[]; index: number } | null>(null);
  const [mobileNav, setMobileNav] = useState(false);
  const [notice, setNotice] = useState("");
  const [commentName, setCommentName] = useState("");
  const [commentText, setCommentText] = useState("");
  const [contactSent, setContactSent] = useState(false);
  const [adminDraft, setAdminDraft] = useState<SiteContent>(content);
  const [newImageName, setNewImageName] = useState("");
  const [newProject, setNewProject] = useState({ title: "", category: "建築圖面" as Exclude<Category, "全部">, description: "" });
  const [dragging, setDragging] = useState(false);
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [loginError, setLoginError] = useState('');

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    return onAuthStateChanged(auth, setAdminUser);
  }, [theme]);

  useEffect(() => {
    localStorage.setItem("hofong-site-content", JSON.stringify(content));
  }, [content]);

  useEffect(() => {
    localStorage.setItem("hofong-comments", JSON.stringify(comments));
  }, [comments]);

  useEffect(() => {
    if (!notice) return;
    const timeout = window.setTimeout(() => setNotice(""), 2600);
    return () => window.clearTimeout(timeout);
  }, [notice]);

  const filteredProjects = useMemo(
    () => content.projects.filter((project) => filter === "全部" || project.category === filter),
    [content.projects, filter],
  );

  const scrollTo = (id: string) => {
    setPage("home");
    setMobileNav(false);
    window.setTimeout(() => document.getElementById(id)?.scrollIntoView({ behavior: "smooth" }), 40);
  };

  const copyEmail = async () => {
    await navigator.clipboard?.writeText(content.email);
    setNotice("Email 已複製到剪貼簿");
  };

  const updateSlide = (projectId: number, direction: number) => {
    const project = content.projects.find((item) => item.id === projectId);
    if (!project) return;
    const current = activeImage[projectId] ?? 0;
    const next = (current + direction + project.images.length) % project.images.length;
    setActiveImage((previous) => ({ ...previous, [projectId]: next }));
  };

  const addComment = (event: React.FormEvent) => {
    event.preventDefault();
    const name = commentName.trim().slice(0, 24);
    const message = commentText.trim().slice(0, 50);
    if (!name || !message) return setNotice("請填寫姓名與留言內容");
    setComments((previous) => [{ id: Date.now(), name, content: message, date: new Date().toISOString().slice(0, 10).replaceAll("-", ".") }, ...previous]);
    setCommentName("");
    setCommentText("");
    setNotice("留言已加入，謝謝你的分享");
  };

  const saveAdmin = () => {
    setContent(adminDraft);
    setNotice("內容已儲存至本機預覽資料");
  };

  const addImageByName = (filename: string) => {
    const cleanName = filename.trim().replace(/^\/+/, "");
    if (!cleanName) return;
    const imageUrl = `https://raw.githubusercontent.com/hofong/portfolio-assets/main/${cleanName}`;
    setAdminDraft((previous) => ({
      ...previous,
      portrait: imageUrl,
    }));
    setNewImageName("");
    setNotice(`已加入 ${cleanName}（GitHub 檔名讀取模式）`);
  };

  const addProject = () => {
    if (!newProject.title.trim()) return setNotice("請先輸入作品名稱");
    const project: Project = {
      id: Date.now(),
      title: newProject.title.trim(),
      category: newProject.category,
      description: newProject.description.trim() || "在後台補上這個作品的簡短介紹。",
      role: "待補充",
      year: "2026",
      tags: ["New project"],
      images: [`${IMAGE_BASE}photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=1600&q=85`],
    };
    setAdminDraft((previous) => ({ ...previous, projects: [project, ...previous.projects] }));
    setNewProject({ title: "", category: "建築圖面", description: "" });
    setNotice("作品草稿已加入，儲存後會顯示在作品集");
  };

  const deleteProject = (id: number) => {
    setAdminDraft((previous) => ({ ...previous, projects: previous.projects.filter((project) => project.id !== id) }));
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setDragging(false);
    const file = event.dataTransfer.files?.[0];
    if (!file) return;
    addImageByName(file.name);
  };

  const syncFirebase = async () => {
    const ok = await syncSiteContent(content);
    setNotice(ok ? "Firebase 同步完成" : "Firebase 尚未連線，已保留本機版本");
  };

  return (
    <div className={`site-shell ${theme === "light" ? "is-light" : ""}`}>
      <div className="grain" />
      <header className="site-nav">
        <button className="brand" onClick={() => scrollTo("top")} aria-label="回到首頁">
          <span className="brand-mark">H</span>
          <span><strong>廖和風</strong><small>Digital Architect</small></span>
        </button>
        <nav className={`nav-links ${mobileNav ? "open" : ""}`}>
          <button onClick={() => scrollTo("about")}>關於</button>
          <button onClick={() => scrollTo("timeline")}>經歷</button>
          <button onClick={() => scrollTo("work")}>作品</button>
          <button onClick={() => scrollTo("journal")}>筆記</button>
          <button onClick={() => scrollTo("contact")}>聯絡</button>
          <button className="nav-admin" onClick={() => { setPage("admin"); setMobileNav(false); }}><Settings2 size={14} /> 後台</button>
        </nav>
        <div className="nav-actions">
          <button className="icon-button" onClick={() => setTheme(theme === "dark" ? "light" : "dark")} aria-label="切換深淺色模式">
            {theme === "dark" ? <Sun size={17} /> : <Moon size={17} />}
          </button>
          <button className="menu-button" onClick={() => setMobileNav(!mobileNav)} aria-label="開啟選單"><Menu size={20} /></button>
        </div>
      </header>

      {page === "home" ? (
        <main>
          <section className="hero-section" id="top">
            <div className="hero-backdrop" style={{ backgroundImage: `linear-gradient(90deg, rgba(11,13,14,.97) 5%, rgba(11,13,14,.76) 45%, rgba(11,13,14,.34)), url('${content.heroBackground}')` }} />
            <div className="hero-grid" />
            <div className="hero-content">
              <div className="hero-copy reveal-up">
                <p className="eyebrow"><span className="pulse-dot" /> {content.heroEyebrow}</p>
                <h1>{content.heroTitle}</h1>
                <p className="hero-description">{content.heroDescription}</p>
                <div className="hero-actions">
                  <button className="button button-primary" onClick={() => scrollTo("work")}>探索作品 <ArrowDownRight size={17} /></button>
                  <button className="button button-ghost" onClick={() => scrollTo("contact")}>聊聊你的想法 <MoveRight size={17} /></button>
                </div>
                <div className="hero-meta"><span>01 / 04</span><span className="meta-line" /><span>{content.availability}</span></div>
              </div>
              <div className="portrait-stage reveal-up delay-2">
                <div className="portrait-orbit orbit-one" /><div className="portrait-orbit orbit-two" />
                <div className="portrait-frame"><img src={content.portrait} alt="廖和風個人照" /></div>
                <div className="portrait-caption"><span>PORTRAIT / 2026</span><span className="caption-signal">● LIVE</span></div>
                <div className="vertical-label">MAKE / SPACE / MATTER</div>
              </div>
            </div>
            <div className="scroll-cue"><span>SCROLL TO EXPLORE</span><ArrowDownRight size={15} /></div>
          </section>

          <section className="intro-strip" id="about">
            <div className="section-kicker">01 / PROFILE</div>
            <div className="intro-layout">
              <h2>在物質與螢幕之間，<em>保留人的尺度。</em></h2>
              <div className="intro-text"><p>我相信好的設計不是把答案做得更複雜，而是讓人更容易感受到事情的本質。我的工作往返於空間設計、介面原型與田野研究，關注物件如何與記憶、行為和環境產生關係。</p><p>目前以台北為基地，和建築師、藝術家與開發團隊合作，將抽象的問題轉化為具體、可被使用的作品。</p><button className="text-link" onClick={() => scrollTo("timeline")}>查看完整經歷 <ArrowUpRight size={14} /></button></div>
            </div>
            <div className="stats-row"><div><strong>08</strong><span>跨域專案</span></div><div><strong>04</strong><span>合作城市</span></div><div><strong>12</strong><span>展覽與發表</span></div><div><strong>∞</strong><span>持續研究中</span></div></div>
          </section>

          <section className="timeline-section" id="timeline">
            <div className="section-kicker">03 / PATH & PRACTICE</div><div className="section-head compact"><h2>一路上，<em>保持好奇。</em></h2><p>學習、工作與展覽不是履歷上的標記，而是我持續更新方法的方式。</p></div>
            <div className="timeline"><div className="timeline-line" />{content.experiences.map((experience) => <div className="timeline-item" key={experience.id}><span className="timeline-date">{experience.year}</span><div><h3>{experience.title}</h3><p>{experience.detail}</p></div></div>)}</div>
            <div className="skills-grid"><div><span className="skill-label">DESIGN / SPACE</span><p>Rhino · Grasshopper · AutoCAD · Blender · Adobe CC</p></div><div><span className="skill-label">CODE / SYSTEMS</span><p>React · TypeScript · WebGL · Firebase · Prototyping</p></div><div><span className="skill-label">METHOD / RESEARCH</span><p>Fieldwork · Editorial · Exhibition · Visual Storytelling</p></div></div>
            <a className="cv-button" href="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf" target="_blank" rel="noreferrer"><FileText size={17} /> 下載履歷 PDF <Download size={15} /></a>
          </section>


          <section className="work-section" id="work">
            <div className="section-head"><div><div className="section-kicker">02 / SELECTED WORK</div><h2>被使用的想法，<br /><em>才算完成。</em></h2></div><p>選入三個關於空間、記憶與互動的實驗。每個作品都從一個問題出發，最後回到人的感受。</p></div>
            <div className="filter-row">{(["全部", "建築圖面", "互動體驗", "研究實作"] as Category[]).map((item) => <button key={item} className={filter === item ? "active" : ""} onClick={() => setFilter(item)}>{item}<span>0{item === "全部" ? content.projects.length : content.projects.filter((p) => p.category === item).length}</span></button>)}</div>
            <div className="project-list">
              {filteredProjects.map((project, index) => {
                const imageIndex = activeImage[project.id] ?? 0;
                return <article className="project-card reveal-up" key={project.id} style={{ animationDelay: `${index * 90}ms` }}>
                  <div className="project-media" onClick={() => project.pdf ? setSelectedProject(project) : setLightbox({ images: project.images, index: imageIndex })}>
                    <img src={project.images[imageIndex]} alt={`${project.title} 作品照片 ${imageIndex + 1}`} />
                    <div className="media-overlay"><span>{project.pdf ? "OPEN CASE STUDY" : "VIEW IMAGES"}</span><ArrowUpRight size={17} /></div>
                    {project.images.length > 1 && <><button className="slider-button left" onClick={(event) => { event.stopPropagation(); updateSlide(project.id, -1); }} aria-label="上一張"><ChevronLeft size={19} /></button><button className="slider-button right" onClick={(event) => { event.stopPropagation(); updateSlide(project.id, 1); }} aria-label="下一張"><ChevronRight size={19} /></button><div className="slider-dots">{project.images.map((_, imageIndexDot) => <span key={imageIndexDot} className={imageIndexDot === imageIndex ? "active" : ""} />)}</div></>}
                    <span className="project-index">0{index + 1}</span>
                  </div>
                  <div className="project-info"><div className="project-meta"><span>{project.category}</span><span>{project.year}</span></div><h3>{project.title}</h3><p>{project.description}</p><div className="tag-list">{project.tags.map((tag) => <span key={tag}>{tag}</span>)}</div><button className="case-link" onClick={() => setSelectedProject(project)}>查看案例 <ArrowUpRight size={15} /></button></div>
                </article>;
              })}
            </div>
          </section>

          <section className="journal-section" id="journal">
            <div className="section-head"><div><div className="section-kicker">04 / NOTES & NOW</div><h2>留下一些<br /><em>正在發生的事。</em></h2></div><p>設計之外，我也寫下觀察、測試與還沒有答案的問題。</p></div>
            <div className="journal-grid">{content.notes.map((note, index) => <article className={`note-card ${index === 0 ? 'featured' : ''}`} key={note.id}><span className="note-type">{note.type}</span><h3>{note.title.split('\n').map((line) => <span key={line}>{line}<br /></span>)}</h3><p>{note.description}</p><div className="note-footer"><span>{note.readTime}</span><ArrowUpRight size={16} /></div></article>)}<article className="now-card"><div className="now-header"><span className="pulse-dot" /> NOW / 2026.09</div><h3>目前正在研究</h3><ul><li><span>01</span>城市聲景與移動中的記憶</li><li><span>02</span>小型展覽的可重複系統</li><li><span>03</span>一個還在長大的作品集後台</li></ul><span className="now-footer">更新於今天，保持開放。</span></article></div>
          </section>

          <section className="contact-section" id="contact">
            <div className="contact-card"><div className="section-kicker">05 / SAY HELLO</div><div className="contact-layout"><div><h2>有一個想法？<br /><em>讓我們把它做出來。</em></h2><p>不論是作品合作、展覽邀請，或只是想交換一個好問題，都歡迎寫信給我。</p><button className="email-line" onClick={copyEmail}><Mail size={17} /> {content.email} <Copy size={14} /></button><div className="social-links"><a href="https://github.com/" target="_blank" rel="noreferrer"><Github size={17} /> GitHub</a><a href="https://www.linkedin.com/" target="_blank" rel="noreferrer"><Linkedin size={17} /> LinkedIn</a><a href={content.instagram} target="_blank" rel="noreferrer"><Instagram size={17} /> Instagram</a></div></div><form className="contact-form" onSubmit={(event) => { event.preventDefault(); setContactSent(true); }}><label>你的名字<input required placeholder="How should I call you?" /></label><label>Email<input required type="email" placeholder="you@example.com" /></label><label>想聊什麼？<textarea required rows={4} placeholder="Tell me a little about the project..." /></label><button className="button button-primary" type="submit">{contactSent ? <><Check size={16} /> 已送出</> : <><Send size={16} /> 送出訊息</>}</button></form></div></div>
          </section>

          <section className="guestbook-section"><div className="section-kicker">06 / GUESTBOOK</div><div className="guestbook-head"><h2>留下你的<br /><em>一句話。</em></h2><form className="guestbook-form" onSubmit={addComment}><input value={commentName} onChange={(event) => setCommentName(event.target.value)} maxLength={24} placeholder="姓名" aria-label="姓名" /><div className="comment-input-wrap"><input value={commentText} onChange={(event) => setCommentText(event.target.value.replace(/[<>]/g, ""))} maxLength={50} placeholder="最多 50 字，分享一個想法" aria-label="留言" /><span>{commentText.length}/50</span></div><button className="button button-outline" type="submit">送出 <ArrowUpRight size={15} /></button></form></div><div className="comment-grid">{comments.slice(0, 4).map((comment) => <article className="comment-card" key={comment.id}><Quote size={21} /><p>{comment.content}</p><div><strong>{comment.name}</strong><span>{comment.date}</span></div></article>)}</div></section>

          <footer className="site-footer"><div className="footer-brand"><span className="brand-mark">H</span><span>廖和風<br /><small>Digital Architect</small></span></div><p>© 2026 Hofong Liao. Built with curiosity.</p><div><button onClick={() => scrollTo("top")}>Back to top <ArrowUpRight size={14} /></button></div></footer>
        </main>
      ) : (
        <AdminPanel draft={adminDraft} setDraft={setAdminDraft} newImageName={newImageName} setNewImageName={setNewImageName} addImageByName={addImageByName} addProject={addProject} newProject={newProject} setNewProject={setNewProject} deleteProject={deleteProject} saveAdmin={saveAdmin} syncFirebase={syncFirebase} dragging={dragging} setDragging={setDragging} handleDrop={handleDrop} goHome={() => setPage("home")} adminUser={adminUser} loginEmail={loginEmail} setLoginEmail={setLoginEmail} loginPassword={loginPassword} setLoginPassword={setLoginPassword} loginError={loginError} setLoginError={setLoginError} onLogin={async (event) => { event.preventDefault(); setLoginError(''); try { await signInWithEmailAndPassword(auth, loginEmail, loginPassword); } catch { setLoginError('登入失敗，請確認 Firebase Email/Password 帳號與密碼。'); } }} onLogout={() => signOut(auth)} />
      )}

      {notice && <div className="toast"><Check size={15} /> {notice}</div>}
      {selectedProject && <div className="modal-backdrop" onClick={() => setSelectedProject(null)}><div className="case-modal" onClick={(event) => event.stopPropagation()}><button className="modal-close" onClick={() => setSelectedProject(null)}><X size={18} /></button><div className="modal-kicker">CASE STUDY / {selectedProject.category}</div><h2>{selectedProject.title}</h2><p className="modal-lede">{selectedProject.description}</p>{selectedProject.pdf ? <iframe className="pdf-preview" src={`${selectedProject.pdf}#toolbar=0&navpanes=0`} title={`${selectedProject.title} PDF 預覽`} /> : <div className="modal-gallery">{selectedProject.images.map((image) => <img key={image} src={image} alt="作品詳細照片" />)}</div>}<div className="modal-details"><div><span>ROLE</span><strong>{selectedProject.role}</strong></div><div><span>YEAR</span><strong>{selectedProject.year}</strong></div>{selectedProject.link && <a href={selectedProject.link} target="_blank" rel="noreferrer">開啟專案連結 <ExternalLink size={14} /></a>}</div></div></div>}
      {lightbox && <div className="lightbox" onClick={() => setLightbox(null)}><button className="modal-close" onClick={() => setLightbox(null)}><X size={18} /></button><button className="lightbox-arrow left" onClick={(event) => { event.stopPropagation(); setLightbox((previous) => previous ? { ...previous, index: (previous.index - 1 + previous.images.length) % previous.images.length } : previous); }}><ChevronLeft /></button><img src={lightbox.images[lightbox.index]} alt="作品放大檢視" onClick={(event) => event.stopPropagation()} /><button className="lightbox-arrow right" onClick={(event) => { event.stopPropagation(); setLightbox((previous) => previous ? { ...previous, index: (previous.index + 1) % previous.images.length } : previous); }}><ChevronRight /></button></div>}
    </div>
  );
}

function AdminPanel({ draft, setDraft, newImageName, setNewImageName, addImageByName, addProject, newProject, setNewProject, deleteProject, saveAdmin, syncFirebase, dragging, setDragging, handleDrop, goHome, adminUser, loginEmail, setLoginEmail, loginPassword, setLoginPassword, loginError, setLoginError, onLogin, onLogout }: { draft: SiteContent; setDraft: React.Dispatch<React.SetStateAction<SiteContent>>; newImageName: string; setNewImageName: (value: string) => void; addImageByName: (filename: string) => void; addProject: () => void; newProject: { title: string; category: Exclude<Category, "全部">; description: string }; setNewProject: React.Dispatch<React.SetStateAction<{ title: string; category: Exclude<Category, "全部">; description: string }>>; deleteProject: (id: number) => void; saveAdmin: () => void; syncFirebase: () => void; dragging: boolean; setDragging: (value: boolean) => void; handleDrop: (event: React.DragEvent<HTMLDivElement>) => void; goHome: () => void; adminUser: import("firebase/auth").User | null; loginEmail: string; setLoginEmail: (value: string) => void; loginPassword: string; setLoginPassword: (value: string) => void; loginError: string; setLoginError: (value: string) => void; onLogin: (event: React.FormEvent) => void; onLogout: () => void }) {
  if (!adminUser) return <main className="admin-page login-page"><div className="login-card"><button className="brand" onClick={goHome}><span className="brand-mark">H</span><span><strong>廖和風</strong><small>Content Studio</small></span></button><div className="section-kicker">PRIVATE AREA / AUTH REQUIRED</div><h1>登入內容控制台</h1><p>使用已在 Firebase 啟用的 Email / Password 帳號登入，才能編輯網站內容與同步資料。</p><form onSubmit={onLogin}><label>Email<input type="email" required value={loginEmail} onChange={(event) => setLoginEmail(event.target.value)} placeholder="you@example.com" /></label><label>Password<input type="password" required value={loginPassword} onChange={(event) => setLoginPassword(event.target.value)} placeholder="••••••••" /></label>{loginError && <div className="login-error">{loginError}</div>}<button className="button button-primary" type="submit">登入控制台 <ArrowUpRight size={15} /></button></form><button className="back-home" onClick={goHome}>← 回到公開網站</button></div></main>;
  return <main className="admin-page"><div className="admin-topbar"><button className="brand" onClick={goHome}><span className="brand-mark">H</span><span><strong>廖和風</strong><small>Content Studio</small></span></button><div className="admin-actions"><button className="button button-outline" onClick={goHome}>回到網站 <ExternalLink size={15} /></button><div className="admin-user">{adminUser.email}<button className="logout-button" onClick={onLogout}>登出</button></div><button className="button button-primary" onClick={saveAdmin}><Save size={15} /> 儲存變更</button></div></div><div className="admin-layout"><aside className="admin-sidebar"><div className="admin-status"><span className="pulse-dot" /> LOCAL PREVIEW</div><h1>內容控制台</h1><p>編輯文字、圖片、作品與網站狀態。儲存後會保留在此瀏覽器。</p><div className="admin-menu"><a className="active"><Pencil size={15} /> 個人資料</a><a><Layers3 size={15} /> 作品集 <span>{draft.projects.length}</span></a><a><ImagePlus size={15} /> 媒體素材</a><a><Cloud size={15} /> Firebase 同步</a></div><div className="firebase-card"><span className="firebase-icon"><Cloud size={16} /></span><strong>Firebase ready</strong><p>已預留同步入口。上線前請在 Firebase 設定 Auth 與 Firestore Rules。</p><button onClick={syncFirebase}>立即同步 <ArrowUpRight size={14} /></button></div></aside><div className="admin-main"><div className="admin-heading"><div><div className="section-kicker">CONTENT / 01</div><h2>你的數位身份</h2></div><span className="saved-chip"><Check size={14} /> Autosave local</span></div><section className="editor-card"><div className="editor-card-head"><div><span className="card-number">01</span><h3>首頁主視覺</h3></div><span>PUBLIC / HERO</span></div><div className="field-grid"><label>眉標文字<input value={draft.heroEyebrow} onChange={(event) => setDraft((previous) => ({ ...previous, heroEyebrow: event.target.value }))} /></label><label>可接案狀態<input value={draft.availability} onChange={(event) => setDraft((previous) => ({ ...previous, availability: event.target.value }))} /></label></div><label>主標題<textarea rows={2} value={draft.heroTitle} onChange={(event) => setDraft((previous) => ({ ...previous, heroTitle: event.target.value }))} /></label><label>自我介紹<textarea rows={4} value={draft.heroDescription} onChange={(event) => setDraft((previous) => ({ ...previous, heroDescription: event.target.value }))} /></label><div className="portrait-editor"><img src={draft.portrait} alt="目前個人照" /><div><span className="field-label">個人照 / GitHub 檔名</span><p>輸入 GitHub repo 內的檔名，前台會自動組合 raw URL。</p><div className="filename-row"><input value={newImageName} onChange={(event) => setNewImageName(event.target.value)} placeholder="portrait-2026.webp" /><button className="button button-outline" onClick={() => addImageByName(newImageName)}>套用 <ArrowUpRight size={14} /></button></div></div></div><div className={`dropzone ${dragging ? "dragging" : ""}`} onDragOver={(event) => { event.preventDefault(); setDragging(true); }} onDragLeave={() => setDragging(false)} onDrop={handleDrop}><Upload size={20} /><strong>拖曳照片到這裡</strong><span>或輸入檔名連接 GitHub 素材</span></div></section><section className="editor-card"><div className="editor-card-head"><div><span className="card-number">02</span><h3>作品集管理</h3></div><span>{draft.projects.length} PROJECTS</span></div><div className="project-editor-list">{draft.projects.map((project) => <div className="project-editor" key={project.id}><img src={project.images[0]} alt="" /><div className="project-editor-copy"><span>{project.category} · {project.year}</span><input value={project.title} onChange={(event) => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, title: event.target.value } : item) }))} /><textarea value={project.description} onChange={(event) => setDraft((previous) => ({ ...previous, projects: previous.projects.map((item) => item.id === project.id ? { ...item, description: event.target.value } : item) }))} rows={2} /><div className="tag-list">{project.tags.map((tag) => <span key={tag}>{tag}</span>)}</div></div><button className="delete-button" onClick={() => deleteProject(project.id)} aria-label={`刪除 ${project.title}`}><Trash2 size={17} /></button></div>)}</div><div className="new-project-form"><div className="new-project-head"><Plus size={17} /><strong>新增作品卡片</strong></div><div className="field-grid"><input value={newProject.title} onChange={(event) => setNewProject((previous) => ({ ...previous, title: event.target.value }))} placeholder="作品名稱" /><select value={newProject.category} onChange={(event) => setNewProject((previous) => ({ ...previous, category: event.target.value as Exclude<Category, "全部"> }))}><option>建築圖面</option><option>互動體驗</option><option>研究實作</option></select></div><textarea value={newProject.description} onChange={(event) => setNewProject((previous) => ({ ...previous, description: event.target.value }))} placeholder="一句話作品簡介" rows={2} /><button className="button button-outline" onClick={addProject}>建立作品草稿 <Plus size={15} /></button></div></section><section className="editor-card"><div className="editor-card-head"><div><span className="card-number">03</span><h3>經歷與筆記</h3></div><span>PUBLIC / CONTENT</span></div><div className="admin-subhead">經歷時間軸</div>{draft.experiences.map((experience) => <div className="repeat-editor" key={experience.id}><input value={experience.year} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, year: event.target.value } : item) }))} /><input value={experience.title} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, title: event.target.value } : item) }))} /><textarea value={experience.detail} rows={2} onChange={(event) => setDraft((previous) => ({ ...previous, experiences: previous.experiences.map((item) => item.id === experience.id ? { ...item, detail: event.target.value } : item) }))} /></div>)}<div className="admin-subhead notes-head">筆記卡片</div>{draft.notes.map((note) => <div className="repeat-editor note-editor" key={note.id}><input value={note.type} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, type: event.target.value } : item) }))} /><input value={note.readTime} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, readTime: event.target.value } : item) }))} /><input value={note.title} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, title: event.target.value } : item) }))} /><textarea value={note.description} rows={2} onChange={(event) => setDraft((previous) => ({ ...previous, notes: previous.notes.map((item) => item.id === note.id ? { ...item, description: event.target.value } : item) }))} /></div>)}</section><section className="editor-card"><div className="editor-card-head"><div><span className="card-number">04</span><h3>背景與社群</h3></div><span>PUBLIC / LINKS</span></div><label>Hero 背景圖片網址<input value={draft.heroBackground} onChange={(event) => setDraft((previous) => ({ ...previous, heroBackground: event.target.value }))} /></label><div className="field-grid"><label>Email<input value={draft.email} onChange={(event) => setDraft((previous) => ({ ...previous, email: event.target.value }))} /></label><label>Instagram 連結<input value={draft.instagram} onChange={(event) => setDraft((previous) => ({ ...previous, instagram: event.target.value }))} /></label></div></section><section className="editor-card mini-editor"><div className="editor-card-head"><div><span className="card-number">05</span><h3>聯絡資訊</h3></div><span>PUBLIC / CONTACT</span></div><label>Email<input value={draft.email} onChange={(event) => setDraft((previous) => ({ ...previous, email: event.target.value }))} /></label><div className="editor-note"><Sparkles size={17} /><span>這個後台是可運作的前端示範：內容會先保存在 localStorage，Firebase 同步按鈕已接好設定入口，適合接續加入登入保護與 Firestore Rules。</span></div></section></div></div></main>;
}
