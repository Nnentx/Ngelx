import os,json,base64
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
raw=os.environ.get('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED') or os.environ.get('FIREBASE_SERVICE_ACCOUNT')
if not raw: raise RuntimeError('Deployment identity missing')
try: info=json.loads(raw)
except json.JSONDecodeError: info=json.loads(base64.b64decode(raw))
assert info['project_id']=='ngelx-44eed'
s=AuthorizedSession(Credentials.from_service_account_info(info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
base='https://firebaserules.googleapis.com/v1/'
r=s.get(base+'projects/ngelx-44eed/releases/cloud.firestore',timeout=30);r.raise_for_status()
release=r.json()
r=s.get(base+release['rulesetName'],timeout=30);r.raise_for_status()
files=r.json()['source']['files'];assert len(files)==1
Path('build588-current.rules').write_text(files[0]['content'])
Path('build588-rules-checkpoint.json').write_text(json.dumps({'rulesetName':release['rulesetName']}))
print('Current production rules read successfully; no changes made.')
