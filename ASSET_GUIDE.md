# 照片與 PDF 素材使用方式

網站後台預設會從 GitHub repository `hofong159/portfolio-assets` 的 `main` 分支讀取素材。

## 放置位置

可以直接放在 repository 根目錄，也可以建立資料夾分類，例如：

```text
portfolio-assets/
├── images/
│   ├── portrait-2026.webp
│   ├── lightwell-01.webp
│   └── lightwell-02.webp
└── pdf/
    └── lightwell-case-study.pdf
```

## 後台輸入方式

若檔案在根目錄，輸入：

```text
portrait-2026.webp
```

若檔案在資料夾內，輸入包含相對路徑的檔名：

```text
images/portrait-2026.webp
pdf/lightwell-case-study.pdf
```

**副檔名要完整保留**，例如 `.jpg`、`.png`、`.webp`、`.pdf`。檔名與大小寫必須完全一致。不要輸入 GitHub 網址、前綴或後綴；後台會自動把檔名組成 GitHub Raw URL。

## 建議檔名規則

建議使用英文、數字、連字號或底線，不要使用空格或中文，避免網址編碼問題：

```text
portrait-2026.webp
lightwell-01.webp
common-ground-cover.jpg
lightwell-case-study.pdf
```

## 更新流程

1. 把照片或 PDF 上傳到 `hofong159/portfolio-assets`。
2. 等 GitHub 完成檔案更新。
3. 到個人網站的「後台」登入。
4. 在照片或 PDF 欄位輸入檔名／相對路徑。
5. 按「儲存變更」。
6. 若修改的是網站程式或 GitHub Pages 設定，才需要等待網站重新部署；單純更換素材通常不需要改程式。

照片會以完整比例顯示，不會被裁切；PDF 會在案例視窗內預覽，也可以開新分頁查看。
