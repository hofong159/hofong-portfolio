import { getApp, getApps, initializeApp } from "firebase/app";
import { doc, getFirestore, setDoc } from "firebase/firestore";

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

export async function syncSiteContent(content: unknown): Promise<boolean> {
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
