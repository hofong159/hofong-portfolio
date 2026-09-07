from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
needle='''  notes: [
    { id: 1, type: 'FIELD NOTE / 01', title: '為什麼我還在拍\\n城市的背面？', description: '那些沒有被拍進旅遊指南的邊角，往往更接近一座城市真正的呼吸。', readTime: '06 MIN READ' },
    { id: 2, type: 'PROCESS / 02', title: '從一張紙開始的\\n互動原型', description: '在螢幕之前，先讓手和眼睛一起想。', readTime: '04 MIN READ' },
  ],
  categories:'''
if 'categories: [\'建築圖面\'' not in s:
    s=s.replace(needle, needle.replace('  categories:', '''  categories: ['建築圖面', '互動體驗', '研究實作'],
  certificates: [
    { id: 1, title: '建築師資格證書', issuer: '台灣建築師公會', year: '2025', credential: 'TW-ARCH-2025-001', description: '建築專業資格與執業相關證明。', imageFile: '', pdfFile: '', link: '' },
    { id: 2, title: '互動媒體設計證書', issuer: 'Digital Futures Lab', year: '2024', credential: 'DFL-IM-2024-018', description: '互動設計與數位敘事實務認證。', imageFile: '', pdfFile: '', link: '' },
  ],
  categories:'''))
# pass reorder into AdminPanel invocation
s=s.replace('''deleteProject={deleteProject} moveProject={moveProject} moveExperience={moveExperience} moveNote={moveNote} saveAdmin''','''deleteProject={deleteProject} moveProject={moveProject} moveExperience={moveExperience} moveNote={moveNote} reorder={reorder} saveAdmin''')
# add reorder in AdminPanel args and type
s=s.replace('''moveProject, moveExperience, moveNote, adminUser,''','''moveProject, moveExperience, moveNote, reorder, adminUser,''')
s=s.replace('''moveNote: (id: number, direction: -1 | 1) => void; saveAdmin:''','''moveNote: (id: number, direction: -1 | 1) => void; reorder: <T,>(items: T[], index: number, direction: -1 | 1) => T[]; saveAdmin:''')
p.write_text(s)
