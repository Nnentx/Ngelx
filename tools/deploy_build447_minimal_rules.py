"""Deploy only the tested additions, retaining the inspected production baseline."""
import os,json,base64,subprocess,hashlib,tempfile
from pathlib import Path
import google.auth.transport.requests
import google.oauth2.service_account
expected='08dcd247ef3fc1087e238594993c53f5dd595ad8ea844cce89899cbaa6036493'
raw=next((os.environ.get(k,'') for k in ('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED','FIREBASE_SERVICE_ACCOUNT','GOOGLE_APPLICATION_CREDENTIALS_JSON') if os.environ.get(k)),None)
if not raw:raise RuntimeError('Existing deployment credential unavailable')
try:info=json.loads(raw)
except json.JSONDecodeError:info=json.loads(base64.b64decode(raw))
if info.get('project_id')!='ngelx-44eed':raise RuntimeError('Unexpected project')
http=google.auth.transport.requests.AuthorizedSession(google.oauth2.service_account.Credentials.from_service_account_info(info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
base='https://firebaserules.googleapis.com/v1/'
def current():
 r=http.get(base+'projects/ngelx-44eed/releases/cloud.firestore',timeout=30);r.raise_for_status();release=r.json()
 r=http.get(base+release['rulesetName'],timeout=30);r.raise_for_status();files=r.json()['source']['files']
 if len(files)!=1:raise RuntimeError('Unexpected rules source')
 return files[0]['content']
text=current()
if hashlib.sha256(text.encode()).hexdigest()!=expected:raise RuntimeError('Deployed rules changed since inspection; refusing to overwrite')
Path('build447-deployed.rules').write_text(text)
subprocess.run(['git','apply','--check','tools/build447_live_rules.patch'],check=True)
subprocess.run(['git','apply','tools/build447_live_rules.patch'],check=True)
proposed=Path('build447-deployed.rules').read_text();Path('firestore.rules').write_text(proposed)
subprocess.run(['npx','firebase','emulators:exec','--project','demo-ngelx','--only','firestore','--non-interactive','node tools/build446_rules_test.mjs && node tools/build447_live_member_test.mjs'],check=True)
if hashlib.sha256(current().encode()).hexdigest()!=expected:raise RuntimeError('Rules changed during validation; refusing deployment')
fd,path=tempfile.mkstemp(prefix='ngelx447-credentials-',suffix='.json');os.chmod(path,0o600)
try:
 with os.fdopen(fd,'w')as f:json.dump(info,f)
 env=dict(os.environ,GOOGLE_APPLICATION_CREDENTIALS=path)
 subprocess.run(['npx','firebase','deploy','--only','firestore:rules','--project','ngelx-44eed','--non-interactive'],env=env,check=True)
 if current()!=proposed:raise RuntimeError('Deployed-rule readback does not match tested content')
 print('Build447 minimal production rule additions verified by readback:',hashlib.sha256(proposed.encode()).hexdigest())
finally:Path(path).unlink(missing_ok=True)
