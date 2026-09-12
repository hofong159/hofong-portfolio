from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
s=p.read_text().replace('.admin-menu, .firebase-card { display: none; }', '.firebase-card { display: none; }')
p.write_text(s)
