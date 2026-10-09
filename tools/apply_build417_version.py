#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '416'","defaultValue: '417'"),
                ("defaultValue: '1.0.191'","defaultValue: '1.0.192'")]:
    if s.count(old)!=1:raise SystemExit('Build417 version drift: '+old)
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.191+416')!=1:raise SystemExit('Build417 pubspec drift')
p.write_text(s.replace('version: 1.0.191+416','version: 1.0.192+417',1),encoding='utf-8')
print('Build417 1.0.192+417 set.')
