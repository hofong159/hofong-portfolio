from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
s=s.replace('''const GITHUB_ASSET_BASE = "https://raw.githubusercontent.com/hofong159/portfolio-assets/main/";
const assetUrl = (value: string) => value.startsWith("http") ? value : `${GITHUB_ASSET_BASE}${value.replace(/^\\/+/, "")}`;''','''const GITHUB_ASSET_BASE = "https://raw.githubusercontent.com/hofong159/hofong-portfolio/main/";
const assetUrl = (value: string) => {
  if (value.startsWith("http")) return value;
  const clean = value.trim().replace(/^\\/+/, "");
  const encoded = clean.split("/").map((part) => encodeURIComponent(part)).join("/");
  return `${GITHUB_ASSET_BASE}${encoded}`;
};''')
# Update visible guidance in admin
s=s.replace('''輸入 GitHub repo 內的檔名，前台會自動組合 raw URL。''','''輸入網站 GitHub repository 第一層的檔名，前台會自動組合 Raw URL；支援中文檔名。''')
s=s.replace('''直接放素材 repo 第一層''','''直接放網站 repo 第一層''')
s=s.replace('''直接放素材 repository 第一層''','''直接放網站 repository 第一層''')
p.write_text(s)

for guide_path in [Path('/home/ubuntu/hofong-portfolio/ASSET_GUIDE.md'), Path('/home/ubuntu/portfolio-assets-repo/ASSET_GUIDE.md')]:
    if not guide_path.exists(): continue
    text=guide_path.read_text()
    text += '''\n## 目前網站實際讀取位置\n\n網站目前會讀取 `hofong159/hofong-portfolio` repository 的第一層檔案。若要使用 `個人照.jpg`，請把檔案放在該 repository 根目錄，後台只輸入 `個人照.jpg`。中文檔名可以使用，但英文檔名仍較不容易出錯。\n'''
    guide_path.write_text(text)
