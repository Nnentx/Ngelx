"""Add the updater only after the exact verified Build563 assembled sources."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def apply():
 tools=ROOT/'tools';manifest=json.loads((tools/'build564_manifest.json').read_text());states=[]
 for path,expected in manifest.items():
  actual=digest(ROOT/path)
  if actual not in expected.values():raise RuntimeError('Build564 source drift: '+path)
  states.append('before' if actual==expected['before'] else 'after')
 if len(set(states))!=1:raise RuntimeError('Partial Build564 source')
 copies={'build564_update.dart':'app/lib/build564_update.dart','Ngelx564Updater.kt':'app/android/app/src/main/kotlin/com/nnentx/ngelx_app/Ngelx564Updater.kt','update_paths564.xml':'app/android/app/src/main/res/xml/update_paths564.xml'}
 for source,target in copies.items():
  p=ROOT/target
  if p.exists() and p.read_bytes()!=(tools/source).read_bytes():raise RuntimeError('Conflicting Build564 file: '+target)
 if states[0]=='before':
  subprocess.run(['git','apply','--check',str(tools/'build564_update.patch')],cwd=ROOT,check=True)
  subprocess.run(['git','apply',str(tools/'build564_update.patch')],cwd=ROOT,check=True)
 for source,target in copies.items():
  p=ROOT/target;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((tools/source).read_bytes())
 for path,expected in manifest.items():
  if digest(ROOT/path)!=expected['after']:raise RuntimeError('Build564 output mismatch: '+path)
 print('Build564 applied; existing app, inbox, call and comment code preserved.')
if __name__=='__main__':apply()
