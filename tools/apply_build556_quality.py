"""Apply only Build556 deltas after the complete Build555 source generation.

All existing source hashes are checked before the first mutation. This prevents
applying the package to the raw Build399 checkout or another generated version.
"""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/'tools'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def apply():
    manifest=json.loads((TOOLS/'build556_manifest.json').read_text())
    states=[]
    for relative,expected in manifest.items():
        path=ROOT/relative
        actual=digest(path)
        if actual not in expected.values():raise RuntimeError('Build556 requires exact assembled Build555 source: '+relative)
        states.append('before' if actual==expected['before'] else 'after')
    if len(set(states))!=1:raise RuntimeError('Partial Build556 source state; restore the assembled baseline before retrying')
    assets=['build556_quality.dart','build556_policy.dart','build556_delete.dart']
    for name in assets:
        target=ROOT/'app/lib'/name
        if target.exists() and target.read_bytes()!=(TOOLS/name).read_bytes():raise RuntimeError('Conflicting helper: '+name)
    if states[0]=='before':
        subprocess.run(['git','apply','--check',str(TOOLS/'build556_quality.patch')],cwd=ROOT,check=True)
        subprocess.run(['git','apply',str(TOOLS/'build556_quality.patch')],cwd=ROOT,check=True)
    for name in assets:(ROOT/'app/lib'/name).write_bytes((TOOLS/name).read_bytes())
    for relative,expected in manifest.items():
        if digest(ROOT/relative)!=expected['after']:raise RuntimeError('Build556 result mismatch: '+relative)
    print('Build556 applied; existing routes, backend rules, Android identity and prior source preserved')
if __name__=='__main__':apply()
