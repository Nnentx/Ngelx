#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
for a,b in [("defaultValue: '421'","defaultValue: '422'"),
            ("defaultValue: '1.0.196'","defaultValue: '1.0.197'")]:
    if s.count(a)!=1:raise SystemExit('Build422 version drift: '+a)
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml');s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.196+421')!=1:raise SystemExit('Build422 pubspec version drift')
p.write_text(s.replace('version: 1.0.196+421','version: 1.0.197+422',1),encoding='utf-8')
print('Build422 NgelX v1.0.197+422 version set.')
