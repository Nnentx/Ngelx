#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '417'","defaultValue: '418'"),
                ("defaultValue: '1.0.192'","defaultValue: '1.0.193'")]:
 if s.count(old)!=1:raise SystemExit('Build418 version drift: '+old)
 s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.192+417')!=1:raise SystemExit('Build418 pubspec drift')
p.write_text(s.replace('version: 1.0.192+417','version: 1.0.193+418',1),encoding='utf-8')
print('Build418 v1.0.193+418 set.')
