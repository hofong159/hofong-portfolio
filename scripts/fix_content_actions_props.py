from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/pages/Home.tsx')
s=p.read_text()
s=s.replace('''moveProject, moveExperience, moveNote, reorder, adminUser''','''moveProject, moveExperience, deleteExperience, moveNote, addNote, deleteNote, reorder, adminUser''',1)
p.write_text(s)
