#!/usr/bin/env python3
from pathlib import Path

p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '412'","defaultValue: '413'"),
                ("defaultValue: '1.0.187'","defaultValue: '1.0.188'")]:
    if s.count(old)!=1:raise SystemExit('Build 413 version drift: '+old)
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
old='version: 1.0.187+412'
if s.count(old)!=1:raise SystemExit('Build 413 pubspec drift')
p.write_text(s.replace(old,'version: 1.0.188+413',1),encoding='utf-8')
print('Build 413 v1.0.188+413 version set.')
