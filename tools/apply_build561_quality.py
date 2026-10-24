"""Apply only the verified Build560-to-Build561 app delta."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def apply():
 tools=ROOT/'tools';manifest=json.loads((tools/'build561_manifest.json').read_text())
 states=[]
 for path,expected in manifest.items():
  actual=digest(ROOT/path)
  if actual not in expected.values():raise RuntimeError('Build561 source drift: '+path)
  states.append('before' if actual==expected['before'] else 'after')
 if len(set(states))!=1:raise RuntimeError('Partial Build561 source')
 helper=tools/'build561_quality.dart';target=ROOT/'app/lib/build561_quality.dart'
 if target.exists() and target.read_bytes()!=helper.read_bytes():raise RuntimeError('Conflicting Build561 helper')
 if states[0]=='before':
  subprocess.run(['git','apply','--check',str(tools/'build561_quality.patch')],cwd=ROOT,check=True)
  subprocess.run(['git','apply',str(tools/'build561_quality.patch')],cwd=ROOT,check=True)
 target.write_bytes(helper.read_bytes())
 for path,expected in manifest.items():
  if digest(ROOT/path)!=expected['after']:raise RuntimeError('Build561 output mismatch: '+path)
 print('Build561 applied to exact Build560 source; existing rules and inbox layout preserved')
if __name__=='__main__':apply()
