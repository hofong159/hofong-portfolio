from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
s=p.read_text()
s=s.replace('.admin-menu a { display: flex; align-items: center; gap: 9px; color: var(--muted); padding: 11px 10px; font-size: 12px; }', '.admin-menu a, .admin-menu button { display: flex; align-items: center; gap: 9px; color: var(--muted); padding: 11px 10px; font-size: 12px; background: transparent; border: 0; width: 100%; text-align: left; }')
s=s.replace('.admin-menu a.active { color: var(--ink); background: var(--surface-2); }', '.admin-menu a.active, .admin-menu button.active, .admin-menu button:hover { color: var(--ink); background: var(--surface-2); }')
s=s.replace('.admin-menu a span { margin-left: auto; color: var(--accent); font: 10px \'DM Mono\',monospace; }', '.admin-menu a span, .admin-menu button span { margin-left: auto; color: var(--accent); font: 10px \'DM Mono\',monospace; }')
p.write_text(s)
