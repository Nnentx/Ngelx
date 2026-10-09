#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for a,b in [("defaultValue: '420'","defaultValue: '421'"),
            ("defaultValue: '1.0.195'","defaultValue: '1.0.196'")]:
    if s.count(a)!=1:raise SystemExit('Build421 version drift: '+a)
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.195+420')!=1:
    raise SystemExit('Build421 pubspec version drift')
p.write_text(s.replace('version: 1.0.195+420','version: 1.0.196+421',1),encoding='utf-8')
print('Build421 v1.0.196+421 version set.')
