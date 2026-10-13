"""Add only community rules to the current deployed baseline, then test and verify."""
import os,json,base64,subprocess,hashlib,tempfile
from pathlib import Path
import google.auth.transport.requests
import google.oauth2.service_account
raw=next((os.environ.get(k,'') for k in ('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED','FIREBASE_SERVICE_ACCOUNT','GOOGLE_APPLICATION_CREDENTIALS_JSON') if os.environ.get(k)),None)
if not raw:raise RuntimeError('Existing deployment credential unavailable')
try:info=json.loads(raw)
except json.JSONDecodeError:info=json.loads(base64.b64decode(raw))
if info.get('project_id')!='ngelx-44eed':raise RuntimeError('Unexpected project')
http=google.auth.transport.requests.AuthorizedSession(google.oauth2.service_account.Credentials.from_service_account_info(info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
base='https://firebaserules.googleapis.com/v1/'
def current():
 r=http.get(base+'projects/ngelx-44eed/releases/cloud.firestore',timeout=30);r.raise_for_status()
 r=http.get(base+r.json()['rulesetName'],timeout=30);r.raise_for_status();files=r.json()['source']['files']
 if len(files)!=1:raise RuntimeError('Unexpected rules source')
 return files[0]['content']
original=current();before=hashlib.sha256(original.encode()).hexdigest();fragment=Path('tools/community450.rules.fragment').read_text()
if 'match /communities450/' in original:
 if fragment.strip() not in original:raise RuntimeError('Different community rules already deployed; review required')
 print('Identical community rules already deployed');raise SystemExit(0)
pos=original.index('    match /');proposed=original[:pos]+fragment+'\n'+original[pos:]
Path('build450-production-before.rules').write_text(original);Path('firestore.rules').write_text(proposed)
subprocess.run(['npx','firebase','emulators:exec','--project','demo-ngelx','--only','firestore','--non-interactive','node tools/build448_rules_test.mjs && node tools/build450_rules_test.mjs'],check=True)
if hashlib.sha256(current().encode()).hexdigest()!=before:raise RuntimeError('Rules changed during validation; refusing to overwrite')
fd,path=tempfile.mkstemp(prefix='ngelx450-credential-',suffix='.json');os.chmod(path,0o600)
try:
 with os.fdopen(fd,'w')as f:json.dump(info,f)
 env=dict(os.environ,GOOGLE_APPLICATION_CREDENTIALS=path)
 subprocess.run(['npx','firebase','deploy','--only','firestore:rules','--project','ngelx-44eed','--non-interactive'],env=env,check=True)
 if current()!=proposed:raise RuntimeError('Deployed rules differ from verified content')
 print('Build450 community rules deployed and read back:',hashlib.sha256(proposed.encode()).hexdigest())
finally:Path(path).unlink(missing_ok=True)
