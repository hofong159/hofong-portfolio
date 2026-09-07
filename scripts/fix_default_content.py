from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
needle='''  projects: [
'''
insert='''  categories: ['建築圖面', '互動體驗', '研究實作'],
  certificates: [
    { id: 1, title: '建築師資格證書', issuer: '台灣建築師公會', year: '2025', credential: 'TW-ARCH-2025-001', description: '建築專業資格與執業相關證明。', imageFile: '', pdfFile: '', link: '' },
    { id: 2, title: '互動媒體設計證書', issuer: 'Digital Futures Lab', year: '2024', credential: 'DFL-IM-2024-018', description: '互動設計與數位敘事實務認證。', imageFile: '', pdfFile: '', link: '' },
  ],
  projects: [
'''
if s.count(needle) < 1: raise SystemExit('default projects anchor missing')
s=s.replace(needle, insert, 1)
p.write_text(s)
