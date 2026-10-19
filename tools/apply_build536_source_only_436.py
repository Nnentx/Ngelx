#!/usr/bin/env python3
"""QA ONLY: run Build436 Flutter changes without replaying obsolete rules migration.

The generated Android source needs the Build436 widget changes. The Build436
rules migration assumes pre-Build4xx social-request fields that are absent
from the Build484 baseline. Re-running it is not an authorization mechanism.
All candidate Build533–535 rules are restored from the QA checkout before
any separate Firestore security emulator checks; nothing is deployed.
"""
from pathlib import Path
from hashlib import sha256
import runpy
import sys

RULES=Path('firestore.rules')
before=RULES.read_bytes()
sys.path.insert(0,str(Path('tools').resolve()))
import build436_rules

original=build436_rules.patch_rules
def preserve_rules(src: str) -> str:
    if src.encode('utf-8')!=before:
        raise RuntimeError('Unexpected Firestore rule rewrite during Build436 source-only QA')
    return src
try:
    build436_rules.patch_rules=preserve_rules
    runpy.run_path('tools/apply_build436_details.py',run_name='__main__')
finally:
    build436_rules.patch_rules=original
after=RULES.read_bytes()
assert sha256(before).digest()==sha256(after).digest(), 'Build436 source-only path changed Firestore authorization'
assert "class Ngelx436PresenceAccess" in Path('app/lib/main.dart').read_text(encoding='utf-8')
print('Build536 QA: historic Build436 Flutter changes applied, obsolete rules migration skipped, Firestore bytes unchanged')
