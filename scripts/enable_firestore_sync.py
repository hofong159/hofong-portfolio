from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/lib/firebase.ts')
s=p.read_text()
s=s.replace('import { doc, getFirestore, setDoc } from "firebase/firestore";', 'import { doc, getDoc, getFirestore, setDoc } from "firebase/firestore";')
old='''export async function syncSiteContent(content: unknown): Promise<boolean> {
  try {
    const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
    const database = getFirestore(app);
    await setDoc(doc(database, "portfolio", "siteContent"), { content, updatedAt: new Date().toISOString() }, { merge: true });
    return true;
  } catch (error) {
    console.warn("Firebase sync is not available yet. Check Firestore rules and network.", error);
    return false;
  }
}
'''
new='''export async function syncSiteContent(content: unknown): Promise<boolean> {
  try {
    const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
    const database = getFirestore(app);
    await setDoc(doc(database, "portfolio", "siteContent"), { content, updatedAt: new Date().toISOString() }, { merge: true });
    return true;
  } catch (error) {
    console.warn("Firebase sync failed. Check Firestore rules and network.", error);
    return false;
  }
}

export async function loadSiteContent<T>(): Promise<T | null> {
  try {
    const app = getApps().length ? getApp() : initializeApp(firebaseConfig);
    const database = getFirestore(app);
    const snapshot = await getDoc(doc(database, "portfolio", "siteContent"));
    if (!snapshot.exists()) return null;
    const data = snapshot.data()?.content;
    return (data ?? null) as T | null;
  } catch (error) {
    console.warn("Firebase content read failed. Falling back to local content.", error);
    return null;
  }
}
'''
if old not in s: raise SystemExit('firebase sync block missing')
p.write_text(s.replace(old,new))

p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
s=s.replace('import { auth, syncSiteContent } from "@/lib/firebase";', 'import { auth, loadSiteContent, syncSiteContent } from "@/lib/firebase";')
s=s.replace('''  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    return onAuthStateChanged(auth, setAdminUser);
  }, [theme]);''','''  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    return onAuthStateChanged(auth, setAdminUser);
  }, [theme]);

  useEffect(() => {
    let cancelled = false;
    loadSiteContent<SiteContent>().then((remote) => {
      if (!cancelled && remote && typeof remote === "object") {
        const merged = loadContentFromValue(remote);
        setContent(merged);
        setAdminDraft(merged);
        localStorage.setItem("hofong-site-content", JSON.stringify(merged));
      }
    });
    return () => { cancelled = true; };
  }, []);''')
# Add helper after loadContent function.
anchor='''function loadComments(): Comment[] {'''
helper='''function loadContentFromValue(value: SiteContent): SiteContent {
  const parsed = value as Partial<SiteContent>;
  return {
    ...DEFAULT_CONTENT,
    ...parsed,
    categories: Array.isArray(parsed.categories) && parsed.categories.length ? parsed.categories.filter((item): item is string => typeof item === "string" && item.trim().length > 0) : DEFAULT_CONTENT.categories,
    certificates: Array.isArray(parsed.certificates) ? parsed.certificates : DEFAULT_CONTENT.certificates,
    stats: Array.isArray(parsed.stats) ? parsed.stats : DEFAULT_CONTENT.stats,
    skills: Array.isArray(parsed.skills) ? parsed.skills : DEFAULT_CONTENT.skills,
    projects: (Array.isArray(parsed.projects) ? parsed.projects : DEFAULT_CONTENT.projects).map((project) => ({ ...project, imageFiles: Array.isArray(project.imageFiles) ? project.imageFiles : project.images, pdfFile: project.pdfFile || project.pdf || "" })),
    experiences: (Array.isArray(parsed.experiences) ? parsed.experiences : DEFAULT_CONTENT.experiences).map((item) => ({ ...item, link: item.link || "" })),
    notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,
  };
}

'''
if anchor not in s: raise SystemExit('comments anchor missing')
s=s.replace(anchor,helper+anchor,1)
# Save to Firestore from the actual draft.
s=s.replace('''  const saveAdmin = () => {
    setContent(adminDraft);
    setNotice("內容已儲存至本機預覽資料");
  };''','''  const saveAdmin = async () => {
    setContent(adminDraft);
    const ok = await syncSiteContent(adminDraft);
    setNotice(ok ? "內容已儲存並同步到 Firebase" : "內容已儲存到本機；Firebase 同步失敗，請檢查 Firestore Rules");
  };''')
s=s.replace('''  const syncFirebase = async () => {
    const ok = await syncSiteContent(content);''','''  const syncFirebase = async () => {
    const ok = await syncSiteContent(adminDraft);''')
p.write_text(s)
