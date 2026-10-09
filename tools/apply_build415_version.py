#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '414'","defaultValue: '415'"),
                ("defaultValue: '1.0.189'","defaultValue: '1.0.190'")]:
    if s.count(old)!=1:raise SystemExit('Build 415 version drift: '+old)
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.189+414')!=1:raise SystemExit('Build 415 pubspec version drift')
p.write_text(s.replace('version: 1.0.189+414','version: 1.0.190+415',1),encoding='utf-8')
print('Build 415 v1.0.190+415 version set.')
