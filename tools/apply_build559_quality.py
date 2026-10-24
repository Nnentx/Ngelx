"""Apply the follow-up to the exact assembled Build558 source; repeat-safe."""
from pathlib import Path
import hashlib,json,subprocess
from build559_rules import patch_rules
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def apply():
 tools=ROOT/'tools';manifest=json.loads((tools/'build559_manifest.json').read_text());states=[]
 for path,expected in manifest.items():
  actual=digest(ROOT/path)
  if actual not in expected.values():raise RuntimeError('Build559 source drift: '+path)
  states.append('before' if actual==expected['before'] else 'after')
 if len(set(states))!=1:raise RuntimeError('Partial Build559 source')
 helper=tools/'build559_quality.dart';target=ROOT/'app/lib/build559_quality.dart'
 if target.exists() and target.read_bytes()!=helper.read_bytes():raise RuntimeError('Conflicting Build559 helper')
 rule_path=ROOT/'firestore.rules';rules=patch_rules(rule_path.read_text())
 if states[0]=='before':
  subprocess.run(['git','apply','--check',str(tools/'build559_quality.patch')],cwd=ROOT,check=True)
  subprocess.run(['git','apply',str(tools/'build559_quality.patch')],cwd=ROOT,check=True)
 target.write_bytes(helper.read_bytes());rule_path.write_text(rules)
 for path,expected in manifest.items():
  if digest(ROOT/path)!=expected['after']:raise RuntimeError('Build559 output mismatch: '+path)
 print('Build559 applied; no deployment or account mutation performed')
if __name__=='__main__':apply()
