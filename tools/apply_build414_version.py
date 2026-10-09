#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for a,b in [("defaultValue: '413'","defaultValue: '414'"),
            ("defaultValue: '1.0.188'","defaultValue: '1.0.189'")]:
    if s.count(a)!=1:raise SystemExit('Build414 version anchor drift: '+a)
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.188+413')!=1:
    raise SystemExit('Build414 pubspec version anchor drift')
p.write_text(s.replace('version: 1.0.188+413','version: 1.0.189+414',1),encoding='utf-8')
print('Build 414 v1.0.189+414 version set.')
