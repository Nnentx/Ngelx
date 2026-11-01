import os,json,base64,sys
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
from build588_scope_rules import transform
raw=os.environ.get('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED') or os.environ.get('FIREBASE_SERVICE_ACCOUNT')
if not raw:raise RuntimeError('Deployment identity missing')
try:info=json.loads(raw)
except json.JSONDecodeError:info=json.loads(base64.b64decode(raw))
assert info['project_id']=='ngelx-44eed'
s=AuthorizedSession(Credentials.from_service_account_info(info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
base='https://firebaserules.googleapis.com/v1/';release='projects/ngelx-44eed/releases/cloud.firestore';state=Path('build588-rules-state.json')
def get(path):
 r=s.get(base+path,timeout=30);r.raise_for_status();return r.json()
def point(name):
 r=s.patch(base+release,params={'updateMask':'rulesetName'},json={'release':{'name':release,'rulesetName':name}},timeout=30);r.raise_for_status()
 assert get(release)['rulesetName']==name
if sys.argv[1]=='publish':
 old=Path('build588-current.rules').read_text();new=Path('firestore.rules').read_text();assert transform(old)==new
 previous=get(release)['rulesetName'];files=get(previous)['source']['files'];assert len(files)==1 and files[0]['content']==old,'Production changed since emulator tests'
 r=s.post(base+'projects/ngelx-44eed/rulesets',json={'source':{'files':[{'name':'firestore.rules','content':new}]}},timeout=30);r.raise_for_status();name=r.json()['name']
 assert name.startswith('projects/ngelx-44eed/rulesets/')
 state.write_text(json.dumps({'previous':previous,'current':name}));point(name)
 print('Scoped production rules published and verified')
else:
 if not state.exists():print('No rule publication to roll back');sys.exit(0)
 v=json.loads(state.read_text());current=get(release)['rulesetName']
 if current==v['previous']:print('Previous rules already active');sys.exit(0)
 assert current==v['current'],'Concurrent rule publication detected; no overwrite'
 point(v['previous']);print('Previous production rules restored')
