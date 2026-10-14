"""Test an additive patch against current production rules, then deploy exactly it."""
import os, json, base64, hashlib, tempfile, subprocess
from pathlib import Path
import google.auth.transport.requests
import google.oauth2.service_account
from apply_build456_rules import transform

raw=next((os.environ.get(k) for k in ('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED','FIREBASE_SERVICE_ACCOUNT') if os.environ.get(k)),None)
if not raw: raise RuntimeError('Existing Firebase deployment credential unavailable')
try: info=json.loads(raw)
except json.JSONDecodeError: info=json.loads(base64.b64decode(raw))
if info.get('project_id') != 'ngelx-44eed': raise RuntimeError('Unexpected Firebase project')
http=google.auth.transport.requests.AuthorizedSession(google.oauth2.service_account.Credentials.from_service_account_info(info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
base='https://firebaserules.googleapis.com/v1/'
def current():
    r=http.get(base+'projects/ngelx-44eed/releases/cloud.firestore',timeout=30);r.raise_for_status()
    r=http.get(base+r.json()['rulesetName'],timeout=30);r.raise_for_status()
    files=r.json()['source']['files']
    if len(files)!=1: raise RuntimeError('Unexpected production rules source')
    return files[0]['content']
original=current()
proposed=transform(original)
if proposed == original:
    print('Exact Build456 community rules already present and verified');raise SystemExit(0)
Path('build456-production-before.rules').write_text(original)
Path('firestore.rules').write_text(proposed)
subprocess.run(['npx','firebase','emulators:exec','--project','demo-ngelx','--only','firestore','--non-interactive','node tools/build450_rules_test.mjs && node tools/build455_rules_test.mjs && node tools/build456_rules_test.mjs'],check=True)
if current()!=original: raise RuntimeError('Production rules changed during verification; refusing to overwrite')
fd,path=tempfile.mkstemp(prefix='ngelx456-credential-',suffix='.json');os.chmod(path,0o600)
try:
    with os.fdopen(fd,'w') as f: json.dump(info,f)
    subprocess.run(['npx','firebase','deploy','--only','firestore:rules','--project','ngelx-44eed','--non-interactive'],env=dict(os.environ,GOOGLE_APPLICATION_CREDENTIALS=path),check=True)
    if current()!=proposed: raise RuntimeError('Production read-back differs from verified rules')
    print('Build456 rules deployed and verified:',hashlib.sha256(proposed.encode()).hexdigest())
finally: Path(path).unlink(missing_ok=True)
