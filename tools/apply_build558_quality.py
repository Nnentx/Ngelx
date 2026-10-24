"""Apply Build558 only to the exact verified assembled Build557 application.

Historical generators and app sources stay untouched in the repository. This
step runs after apply_build557_quality.py in an assembled working tree.
"""
from pathlib import Path
import hashlib,json,subprocess
from build558_rules import patch_rules
ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def apply():
    manifest=json.loads((TOOLS/'build558_manifest.json').read_text())
    states=[]
    for relative,expected in manifest.items():
        actual=digest(ROOT/relative)
        if actual not in expected.values():raise RuntimeError('Build558 requires exact assembled Build557 source: '+relative)
        states.append('before' if actual==expected['before'] else 'after')
    if len(set(states))!=1:raise RuntimeError('Partial Build558 source; restore baseline before retrying')
    helper=TOOLS/'build558_chat_quality.dart';target=ROOT/'app/lib/build558_chat_quality.dart'
    if target.exists() and target.read_bytes()!=helper.read_bytes():raise RuntimeError('Conflicting Build558 helper')
    rules=ROOT/'firestore.rules'
    rules_after=patch_rules(rules.read_text()) # Validate before any source mutation.
    if states[0]=='before':
        subprocess.run(['git','apply','--check',str(TOOLS/'build558_quality.patch')],cwd=ROOT,check=True)
        subprocess.run(['git','apply',str(TOOLS/'build558_quality.patch')],cwd=ROOT,check=True)
    target.write_bytes(helper.read_bytes());rules.write_text(rules_after)
    for relative,expected in manifest.items():
        if digest(ROOT/relative)!=expected['after']:raise RuntimeError('Build558 result mismatch: '+relative)
    print('Build558 applied: prior source, backend membership checks and Android identity preserved')
if __name__=='__main__':apply()
