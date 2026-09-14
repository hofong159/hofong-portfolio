from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
needle="""  ],
  categories: ['建築圖面', '互動體驗', '研究實作'],"""
replace="""  ],
  nowKicker: 'NOW / 2026.09',
  nowTitle: '目前正在研究',
  nowItems: ['城市聲景與移動中的記憶', '小型展覽的可重複系統', '一個還在長大的作品集後台'],
  nowFooter: '更新於今天，保持開放。',
  categories: ['建築圖面', '互動體驗', '研究實作'],"""
if needle not in s: raise SystemExit('default insertion point missing')
s=s.replace(needle,replace,1)
block='''      nowKicker: typeof parsed.nowKicker === "string" ? parsed.nowKicker : DEFAULT_CONTENT.nowKicker,
      nowTitle: typeof parsed.nowTitle === "string" ? parsed.nowTitle : DEFAULT_CONTENT.nowTitle,
      nowItems: Array.isArray(parsed.nowItems) ? parsed.nowItems.filter((item): item is string => typeof item === "string") : DEFAULT_CONTENT.nowItems,
      nowFooter: typeof parsed.nowFooter === "string" ? parsed.nowFooter : DEFAULT_CONTENT.nowFooter,
'''
s=s.replace(block+block,block,1)
# Add remote loader fields if absent.
anchor='''    notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,
  };
}

function loadComments'''
replacement='''    notes: Array.isArray(parsed.notes) ? parsed.notes : DEFAULT_CONTENT.notes,
    nowKicker: typeof parsed.nowKicker === "string" ? parsed.nowKicker : DEFAULT_CONTENT.nowKicker,
    nowTitle: typeof parsed.nowTitle === "string" ? parsed.nowTitle : DEFAULT_CONTENT.nowTitle,
    nowItems: Array.isArray(parsed.nowItems) ? parsed.nowItems.filter((item): item is string => typeof item === "string") : DEFAULT_CONTENT.nowItems,
    nowFooter: typeof parsed.nowFooter === "string" ? parsed.nowFooter : DEFAULT_CONTENT.nowFooter,
  };
}

function loadComments'''
if anchor not in s: raise SystemExit('remote loader anchor missing')
s=s.replace(anchor,replacement,1)
p.write_text(s)
