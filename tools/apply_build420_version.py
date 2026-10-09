#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '419'","defaultValue: '420'"),
                ("defaultValue: '1.0.194'","defaultValue: '1.0.195'")]:
 if s.count(old)!=1:raise SystemExit('Build420 version drift: '+old)
 s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
old='version: 1.0.194+419'
if s.count(old)!=1:raise SystemExit('Build420 pubspec drift')
p.write_text(s.replace(old,'version: 1.0.195+420',1),encoding='utf-8')
print('Build420 v1.0.195+420 set.')
