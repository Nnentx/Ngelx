"""Publish only the tested live-stream rule delta, preserving the current baseline."""
import os,json,base64,hashlib
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
from apply_build553_live_rules import transform
old=Path('live553-current.rules').read_text();new=Path('live553-candidate.rules').read_text()
assert transform(old)==new and transform(new)==new
assert old[:old.index('    match /live_streams/{streamId} {')]==new[:new.index('    match /live_streams/{streamId} {')]
assert old[old.index('      match /reactions/{uid} {',old.index('    match /live_streams/{streamId} {')):]==new[new.index('      match /reactions/{uid} {',new.index('    match /live_streams/{streamId} {')):]
raw=next((os.environ[k] for k in ['FIREBASE_SERVICE_ACCOUNT_NGELX_44EED','FIREBASE_SERVICE_ACCOUNT'] if os.environ.get(k)),None)
if not raw:raise RuntimeError('Deployment identity missing')
try:info=json.loads(raw)
except json.JSONDecodeError:info=json.loads(base64.b64decode(raw))
assert info['project_id']=='ngelx-44eed'
s=AuthorizedSession(Credentials.from_service_account_info(info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
base='https://firebaserules.googleapis.com/v1/';release='projects/ngelx-44eed/releases/cloud.firestore'
r=s.get(base+release,timeout=30);r.raise_for_status();previous=r.json()['rulesetName']
r=s.get(base+previous,timeout=30);r.raise_for_status();files=r.json()['source']['files'];assert len(files)==1
if files[0]['content']!=old:raise RuntimeError('Live rules changed after testing; refusing publication')
r=s.post(base+'projects/ngelx-44eed/rulesets',json={'source':{'files':[{'name':'firestore.rules','content':new}]}},timeout=30)
r.raise_for_status();ruleset=r.json()['name'];assert ruleset.startswith('projects/ngelx-44eed/rulesets/')
r=s.patch(base+release,params={'updateMask':'rulesetName'},json={'release':{'name':release,'rulesetName':ruleset}},timeout=30)
r.raise_for_status()
r=s.get(base+release,timeout=30);r.raise_for_status();assert r.json()['rulesetName']==ruleset
out={'previous':previous,'current':ruleset,'sha256':hashlib.sha256(new.encode()).hexdigest(),'scope':'live comments gifts and moderator-only viewer bans'}
Path('live553-publication.json').write_text(json.dumps(out,indent=2))
print('Scoped live-stream rules published and verified:',out['sha256'])
