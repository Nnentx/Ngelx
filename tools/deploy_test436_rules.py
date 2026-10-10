"""Stage the exact production patch for emulator validation, then publish it."""
import json,os,sys,urllib.request
from pathlib import Path
import google.auth
from google.auth.transport.requests import Request
creds,project=google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform']);creds.refresh(Request())
project=project or json.loads(Path(os.environ['GOOGLE_APPLICATION_CREDENTIALS']).read_text())['project_id']
def api(path,payload=None,method=None):
 r=urllib.request.Request('https://firebaserules.googleapis.com/v1/'+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Authorization':'Bearer '+creds.token,'Content-Type':'application/json'},method=method)
 return json.load(urllib.request.urlopen(r,timeout=30))
release=api('projects/'+project+'/releases/cloud.firestore')
if sys.argv[-1]=='prepare':
 source=api(release['rulesetName'])['source']['files']
 from build435_rules import patch_rules as cleanup
 from build436_rules import patch_rules
 canonical=Path('firestore.rules').read_text()
 for f in source:
  if 'match /chats/{chatId}' not in f['content']:continue
  text=patch_rules(cleanup(f['content']))
  # Replace only canonical social request functions/routes. Existing unrelated rules survive.
  start=text.index('    function validSocialRequestCreate(');end=text.index('    match /notifications/',start)
  cs=canonical.index('    function validSocialRequestCreate(');ce=canonical.index('    match /notifications/',cs)
  text=text[:start]+canonical[cs:ce]+text[end:]
  f['content']=text
  Path('firestore.rules').write_text(f['content'])
 Path('rules436-staged.json').write_text(json.dumps({'original':release['rulesetName'],'files':source}))
 print('Exact production rule patch staged for emulator checks.')
else:
 staged=json.loads(Path('rules436-staged.json').read_text())
 if release['rulesetName']!=staged['original']:raise RuntimeError('Production rules changed during validation; refusing stale deployment')
 result=api('projects/'+project+'/rulesets',{'source':{'files':staged['files']}})
 api('projects/'+project+'/releases/cloud.firestore',{'release':{'name':release['name'],'rulesetName':result['name']},'updateMask':'rulesetName'},'PATCH')
 print('Emulator-tested exact production rule patch deployed.')
