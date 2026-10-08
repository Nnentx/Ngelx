#!/usr/bin/env python3
"""Bump Build 409 only after previous behavior patches pass."""
from pathlib import Path
p=Path("app/lib/main.dart")
s=p.read_text(encoding="utf-8")
for old,new in [("defaultValue: '408'","defaultValue: '409'"),("defaultValue: '1.0.184'","defaultValue: '1.0.185'")]:
    if s.count(old)!=1:raise SystemExit("version metadata drift: "+old)
    s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8")
p=Path("app/pubspec.yaml")
s=p.read_text(encoding="utf-8")
if s.count("version: 1.0.184+408")!=1:raise SystemExit("pubspec metadata drift")
p.write_text(s.replace("version: 1.0.184+408","version: 1.0.185+409",1),encoding="utf-8")
print("Build 409 version 1.0.185+409 set.")
