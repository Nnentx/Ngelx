import os,json,base64,sys
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession

raw=os.environ.get('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED') or os.environ.get('FIREBASE_SERVICE_ACCOUNT')
if not raw:raise RuntimeError('Deployment identity missing')
try:info=json.loads(raw)
except json.JSONDecodeError:info=json.loads(base64.b64decode(raw))
assert info['project_id']=='ngelx-44eed'
s=AuthorizedSession(Credentials.from_service_account_info(info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
base='https://firebaserules.googleapis.com/v1/';release='projects/ngelx-44eed/releases/cloud.firestore';state=Path('build593-rules-state.json')
def get(path):
 r=s.get(base+path,timeout=30);r.raise_for_status();return r.json()
def point(name):
 r=s.patch(base+release,params={'updateMask':'rulesetName'},json={'release':{'name':release,'rulesetName':name}},timeout=30);r.raise_for_status()
 assert get(release)['rulesetName']==name
def transform(old):
 start=old.index('      match /guest_requests/{uid} {')
 end=old.index('      allow read: if true;',start)
 block=old[start:end]
 old_guard="host() && request.resource.data.status == 'invited'"
 new_guard="host() && acceptsLiveInvites() && request.resource.data.status == 'invited'"
 anchor="        allow get: if signedIn() && (request.auth.uid == uid || host());"
 helper="""        function acceptsLiveInvites() {
          let profile = /databases/$(database)/documents/users/$(uid);
          return !exists(profile) || get(profile).data.get('allowLiveInvites', true) != false;
        }
"""
 if block.count(new_guard)==2 and helper in block:
  return old
 assert block.count(anchor)==1 and block.count(old_guard)==2 and 'acceptsLiveInvites' not in block
 return old[:start]+block.replace(anchor,helper+anchor).replace(old_guard,new_guard)+old[end:]
if sys.argv[1]=='prepare':
 previous=get(release)['rulesetName']
 files=get(previous)['source']['files'];assert len(files)==1
 old=files[0]['content']
 Path('build593-current.rules').write_text(old)
 Path('firestore.rules').write_text(transform(old))
 print('Prepared scoped guest invitation rule changes')
elif sys.argv[1]=='publish':
 old=Path('build593-current.rules').read_text();new=Path('firestore.rules').read_text();assert transform(old)==new
 previous=get(release)['rulesetName'];files=get(previous)['source']['files'];assert len(files)==1 and files[0]['content']==old,'Production changed since emulator tests'
 if new==old:print('Scoped rules are already active');sys.exit(0)
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
