"""Presentation-only follow-up to the exact assembled Build558 application."""
from pathlib import Path
import hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def apply():
 tools=ROOT/'tools';manifest=json.loads((tools/'build560_manifest.json').read_text());states=[]
 for path,expected in manifest.items():
  actual=digest(ROOT/path)
  if actual not in expected.values():raise RuntimeError('Build560 source drift: '+path)
  states.append('before' if actual==expected['before'] else 'after')
 if len(set(states))!=1:raise RuntimeError('Partial Build560 source')
 helper=tools/'build560_inbox.dart';target=ROOT/'app/lib/build560_inbox.dart'
 if target.exists() and target.read_bytes()!=helper.read_bytes():raise RuntimeError('Conflicting inbox helper')
 if states[0]=='before':
  subprocess.run(['git','apply','--check',str(tools/'build560_inbox.patch')],cwd=ROOT,check=True)
  subprocess.run(['git','apply',str(tools/'build560_inbox.patch')],cwd=ROOT,check=True)
 target.write_bytes(helper.read_bytes())
 for path,expected in manifest.items():
  if digest(ROOT/path)!=expected['after']:raise RuntimeError('Build560 output mismatch: '+path)
 print('Build560 inbox presentation applied; no rules, data, auth or service configuration touched')
if __name__=='__main__':apply()
