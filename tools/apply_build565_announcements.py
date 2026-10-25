from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def apply():
 tools=ROOT/'tools';manifest=json.loads((tools/'build565_manifest.json').read_text());states=[]
 for path,expected in manifest.items():
  actual=digest(ROOT/path)
  if actual not in expected.values():raise RuntimeError('Build565 source drift: '+path)
  states.append('before' if actual==expected['before'] else 'after')
 if len(set(states))!=1:raise RuntimeError('Partial Build565 source')
 for name in ['build565_announcements.dart','build565_ludo.dart']:
  target=ROOT/'app/lib'/name
  if target.exists() and target.read_bytes()!=(tools/name).read_bytes():raise RuntimeError('Conflicting Build565 helper')
 if states[0]=='before':
  subprocess.run(['git','apply','--check',str(tools/'build565_announcements.patch')],cwd=ROOT,check=True)
  subprocess.run(['git','apply',str(tools/'build565_announcements.patch')],cwd=ROOT,check=True)
 for name in ['build565_announcements.dart','build565_ludo.dart']:(ROOT/'app/lib'/name).write_bytes((tools/name).read_bytes())
 for path,expected in manifest.items():
  if digest(ROOT/path)!=expected['after']:raise RuntimeError('Build565 output mismatch: '+path)
 print('Build565 applied to exact Build564 source; inbox, privacy and send paths preserved.')
if __name__=='__main__':apply()
