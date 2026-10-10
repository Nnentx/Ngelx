"""Patch only deployed live child-delete permissions; preserve production rules."""
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
files=[{'name':f['name'],'content':f['content']} for f in rules['source']['files']];changed=False
for f in files:
 text=f['content'];start=text.find('match /live_streams/{streamId}')
 if start<0:continue
 # Find matching block rather than changing unrelated matches.
 brace=text.index('{',text.index('}',start)+1);depth=1;i=brace+1
 while depth:
  depth+=(text[i]=='{')-(text[i]=='}');i+=1
 block=text[start:i]
 if '// Build433 host cleanup' in block:continue
 owner='(signedIn() && get(/databases/$(database)/documents/live_streams/$(streamId)).data.ownerId == request.auth.uid)'
 for child,var in [('comments','commentId'),('reactions','uid')]:
  pat=r'(match /'+child+r'/\{'+var+r'\}\s*\{)'
  block,count=re.subn(pat,lambda m:m.group(0)+'\n        allow delete: if '+owner+';',block,count=1)
  if count!=1:raise RuntimeError('Unexpected deployed live child layout: '+child)
 block=block[:block.index('{',block.index('}')+1)+1]+'\n      // Build433 host cleanup'+block[block.index('{',block.index('}')+1)+1:]
 block=block[:-1]+'\n      match /viewers/{viewerId} { allow delete: if '+owner+'; }\n    }'
 f['content']=text[:start]+block+text[i:];changed=True
if not changed:
 if any('// Build433 host cleanup' in f['content'] for f in files):
  print('Live child cleanup permissions already deployed.');raise SystemExit(0)
 raise RuntimeError('No live-stream rule block found; refusing replacement')
result=api('projects/'+project+'/rulesets',{'source':{'files':files}})
api('projects/'+project+'/releases/cloud.firestore',{'release':{'name':release['name'],'rulesetName':result['name']},'updateMask':'rulesetName'},'PATCH')
print('Deployed live child-delete permissions; all other production rules preserved.')
