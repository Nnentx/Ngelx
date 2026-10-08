#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
for a,b in [("defaultValue: '409'","defaultValue: '411'"),("defaultValue: '1.0.185'","defaultValue: '1.0.186'")]:
 if s.count(a)!=1:raise SystemExit('Version drift: '+a)
 s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml');s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.185+409')!=1:raise SystemExit('Pubspec version drift')
p.write_text(s.replace('version: 1.0.185+409','version: 1.0.186+411',1),encoding='utf-8')
print('Build 411 version 1.0.186+411 set.')