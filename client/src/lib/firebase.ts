import { getApp, getApps, initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { doc, getDoc, getFirestore, setDoc } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDQYxxFHc8iXa7MKBgyXfzNE8EgxjZqJdk",
  authDomain: "hofong-portfolio.firebaseapp.com",
  databaseURL: "https://hofong-portfolio-default-rtdb.firebaseio.com",
  projectId: "hofong-portfolio",
  storageBucket: "hofong-portfolio.firebasestorage.app",
  messagingSenderId: "254096787618",
  appId: "1:254096787618:web:a90e48def9dbe696a7affb",
  measurementId: "G-GHH3G5YRWP",
};

export const auth = getAuth(getApps().length ? getApp() : initializeApp(firebaseConfig));

export async function syncSiteContent(content: unknown): Promise<boolean> {
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
