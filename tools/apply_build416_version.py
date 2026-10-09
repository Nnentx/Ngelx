#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for a,b in [("defaultValue: '415'","defaultValue: '416'"),
            ("defaultValue: '1.0.190'","defaultValue: '1.0.191'")]:
    if s.count(a)!=1:raise SystemExit('Build416 version drift: '+a)
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.190+415')!=1:
    raise SystemExit('Build416 pubspec version drift')
p.write_text(s.replace('version: 1.0.190+415','version: 1.0.191+416',1),encoding='utf-8')
print('Build 416 v1.0.191+416 version set.')
