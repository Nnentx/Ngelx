"""Patch only deployed message cleanup/hide permissions; preserve all other rules."""
import json,re,urllib.request,os
import google.auth
from google.auth.transport.requests import Request
creds,project=google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform']);creds.refresh(Request())
project=project or json.load(open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']))['project_id']
base='https://firebaserules.googleapis.com/v1/'
def api(path,payload=None,method=None):
 req=urllib.request.Request(base+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Authorization':'Bearer '+creds.token,'Content-Type':'application/json'},method=method)
 return json.load(urllib.request.urlopen(req,timeout=30))
release=api('projects/'+project+'/releases/cloud.firestore');rules=api(release['rulesetName'])
from build435_rules import patch_rules
files=[{'name':f['name'],'content':f['content']} for f in rules['source']['files']]
changed=False
for f in files:
 if 'match /chats/{chatId}' not in f['content']:continue
 updated=patch_rules(f['content'])
 changed=changed or updated!=f['content'];f['content']=updated
if not changed:
 print('Build435 scoped message cleanup permissions already deployed.');raise SystemExit(0)
result=api('projects/'+project+'/rulesets',{'source':{'files':files}})
api('projects/'+project+'/releases/cloud.firestore',{'release':{'name':release['name'],'rulesetName':result['name']},'updateMask':'rulesetName'},'PATCH')
print('Deployed scoped message cleanup/hide permissions; all other production rules preserved.')
