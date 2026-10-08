#!/usr/bin/env python3
"""Verify Build 400 cover-upload fix against supported R2 Worker kind."""
from pathlib import Path

main = Path('app/lib/main.dart').read_text(encoding='utf-8')
pub = Path('app/pubspec.yaml').read_text(encoding='utf-8')
worker = Path('cloudflare/worker/src/index.js').read_text(encoding='utf-8')
allowed = worker.split('const ALLOWED_KINDS = new Set([', 1)[1].split(']);', 1)[0]

checks = {
    'build version': 'version: 1.0.176+400' in pub,
    'build code': "defaultValue: '400'" in main,
    'build name': "defaultValue: '1.0.176'" in main,
    'cover uploader uses supported kind': "kind:'profiles',ext:uzanti,legacyPath:'profile-covers/" in main,
    'unsupported cover kind absent from uploader': "kind:'profile-covers',ext:uzanti" not in main,
    'R2 Worker accepts profiles': "'profiles'" in allowed,
    'cover editor preserved': 'NgelXKapakKonumlandirPage' in main,
    'profile cover field preserved': 'coverPhotoUrl' in main,
    'inbox preserved': 'Widget tumIcerigi()' in main,
    'explore preserved': 'Yeni insanları, içerikleri ve grupları keşfet' in main,
    'create preserved': '_finalUretKart' in main,
}
for name, passed in checks.items():
    print(('OK   ' if passed else 'FAIL ')+name, flush=True)
if not all(checks.values()):
    raise SystemExit('Build 400 hotfix regression failed')
print('Build 400 cover upload regression checks passed.')
