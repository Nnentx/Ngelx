#!/usr/bin/env python3
"""Build 400: fix cover photo upload by using the R2 Worker's allowed 'profiles' kind."""
from pathlib import Path

main_file = Path('app/lib/main.dart')
pubspec_file = Path('app/pubspec.yaml')
worker_file = Path('cloudflare/worker/src/index.js')
main = main_file.read_text(encoding='utf-8')
pubspec = pubspec_file.read_text(encoding='utf-8')
worker = worker_file.read_text(encoding='utf-8')

# Server rejects profile-covers with HTTP 400 invalid_kind. Profiles is allowed.
worker_allowed = worker.split('const ALLOWED_KINDS = new Set([', 1)[1].split(']);', 1)[0]
if "'profiles'" not in worker_allowed:
    raise SystemExit('Server must allow the profiles upload kind')
old = "kind:'profile-covers',ext:uzanti,legacyPath:'profile-covers/"
new = "kind:'profiles',ext:uzanti,legacyPath:'profile-covers/"
if main.count(old) != 1:
    raise SystemExit(f'Expected one legacy cover upload kind, found {main.count(old)}')
main = main.replace(old, new, 1)
for old, new in [
    ("defaultValue: '399'", "defaultValue: '400'"),
    ("defaultValue: '1.0.175'", "defaultValue: '1.0.176'"),
]:
    if main.count(old) != 1:
        raise SystemExit(f'Expected exactly one build identifier: {old}')
    main = main.replace(old, new, 1)
if pubspec.count('version: 1.0.175+399') != 1:
    raise SystemExit('Build 399 pubspec version not found')
pubspec = pubspec.replace('version: 1.0.175+399', 'version: 1.0.176+400', 1)
main_file.write_text(main, encoding='utf-8')
pubspec_file.write_text(pubspec, encoding='utf-8')
print('Build 400 hotfix applied: cover uploads use profiles; version 1.0.176+400.')
