#!/usr/bin/env python3
from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
for old,new in [("defaultValue: '411'","defaultValue: '412'"),("defaultValue: '1.0.186'","defaultValue: '1.0.187'")]:
 if s.count(old)!=1:raise SystemExit('Build 412 version drift: '+old)
 s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml');s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.186+411')!=1:raise SystemExit('Build 412 pubspec version drift')
p.write_text(s.replace('version: 1.0.186+411','version: 1.0.187+412',1),encoding='utf-8')
print('Build 412 v1.0.187+412 version applied.')
