from pathlib import Path
p=Path('/home/ubuntu/hofong-portfolio/client/src/index.css')
s=p.read_text()
old='''.site-shell.section-profile #about,\n.site-shell.section-timeline #about, .site-shell.section-timeline #timeline,'''
new='''.site-shell.section-profile #about,\n.site-shell.section-profile .guestbook-section,\n.site-shell.section-timeline #about, .site-shell.section-timeline #timeline,'''
if old not in s: raise SystemExit('visibility selector missing')
s=s.replace(old,new,1)
# Add guestbook to all non-profile active states' hidden content through the common hidden rule.
needle='''.site-shell.section-contact #about, .site-shell.section-contact #contact { opacity: 1;'''
replace='''.site-shell.section-contact #about, .site-shell.section-contact #contact { opacity: 1;'''
# Keep guestbook hidden for every section; it is not part of public navigation.
marker='''.site-shell.section-profile #about { padding-top: 138px; }'''
s=s.replace(marker,'''.site-shell.section-profile .guestbook-section, .site-shell.section-timeline .guestbook-section, .site-shell.section-work .guestbook-section, .site-shell.section-certificates .guestbook-section, .site-shell.section-journal .guestbook-section, .site-shell.section-contact .guestbook-section { opacity: 0; visibility: hidden; pointer-events: none; max-height: 0; overflow: hidden; padding-top: 0; padding-bottom: 0; }\n'''+marker,1)
p.write_text(s)
