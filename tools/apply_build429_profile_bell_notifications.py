#!/usr/bin/env python3
"""Build 429: profile bell opens notifications-only activity, not unified inbox."""
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
a=s.index('class _ProfilPageState extends State<ProfilPage>')
b=s.index('\nclass _ProfilEtkilesimRozeti',a)
owner=s[a:b]
old="const MesajPage(initialFilter:'Bildirimler')"
count=owner.count(old)
if count<1:
 raise SystemExit(f'Build429 profile bell route missing: {count}')
owner=owner.replace(old,'const AktivitePage()')
s=s[:a]+owner+s[b:]
p.write_text(s,encoding='utf-8')
print(f'Build429: restored notifications-only Activity page for {count} profile bell route(s); inbox remains separate')
