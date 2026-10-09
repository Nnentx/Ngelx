#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '418'","defaultValue: '419'"),
                ("defaultValue: '1.0.193'","defaultValue: '1.0.194'")]:
    if s.count(old)!=1:raise SystemExit('Build419 version drift: '+old)
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
old='version: 1.0.193+418'
if s.count(old)!=1:raise SystemExit('Build419 pubspec version drift')
p.write_text(s.replace(old,'version: 1.0.194+419',1),encoding='utf-8')
print('Build419 v1.0.194+419 set.')
