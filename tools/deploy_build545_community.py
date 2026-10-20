"""Owner-authorized community-only release; never deploy unrelated functions/rules."""
import base64, json, os, shutil, subprocess, tempfile
from pathlib import Path
from prepare_build483_live_rules_qa import retrieve, EXPECTED_LIVE_PREFIX
from apply_build483_community_permissions import prepare_production_candidate
from prepare_build543_community_rules import transform
import hashlib

original = retrieve()
if hashlib.sha256(original.encode()).hexdigest()[:16] != EXPECTED_LIVE_PREFIX:
    raise RuntimeError('Live rules changed since audit; refusing deployment')
proposed = transform(prepare_production_candidate(original))
assert original.split('    // Build450 communities',1)[0] == proposed.split('    // Build450 communities',1)[0]
assert original.split('    match /users/{uid}',1)[1] == proposed.split('    match /users/{uid}',1)[1]
# The exact candidate must have passed all emulator gates earlier in this job.
assert Path('firestore.rules').read_text() == proposed
raw = next(os.environ[k] for k in ('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED','FIREBASE_SERVICE_ACCOUNT') if os.environ.get(k))
try: info = json.loads(raw)
except json.JSONDecodeError: info = json.loads(base64.b64decode(raw))
assert info['project_id'] == 'ngelx-44eed'
fd, credential = tempfile.mkstemp(prefix='community545-',suffix='.json')
os.chmod(credential,0o600)
try:
    with os.fdopen(fd,'w') as f: json.dump(info,f)
    env = dict(os.environ, GOOGLE_APPLICATION_CREDENTIALS=credential)
    source = Path('community-delete543-service')
    (source/'community543').mkdir(parents=True,exist_ok=True)
    (source/'livekit443').mkdir(exist_ok=True)
    for name in ['index.mjs','delete-policy.mjs']:
        shutil.copyfile('server/community543/'+name,source/'community543'/name)
    for name in ['firestore-adapters.mjs','room-policy.mjs']:
        shutil.copyfile('server/livekit443/'+name,source/'livekit443'/name)
    (source/'package.json').write_text(json.dumps({'name':'ngelx-community-delete543','private':True,'type':'module','main':'community543/index.mjs','engines':{'node':'22'},'dependencies':{'firebase-admin':'^13.6.0','firebase-functions':'^6.4.0'}}))
    config = Path('firebase545-community.json')
    config.write_text(json.dumps({'functions':[{'source':str(source),'codebase':'community-delete543','runtime':'nodejs22'}],'firestore':{'rules':'firestore.rules'}}))
    subprocess.run(['npm','install','--no-package-lock'],cwd=source,check=True)
    # Guard immediately before release. Only the prepared community rule region changes.
    if retrieve() != original: raise RuntimeError('Concurrent rules change; refusing overwrite')
    subprocess.run(['npx','firebase','deploy','--only','firestore:rules','--config',str(config),'--project','ngelx-44eed','--non-interactive'],env=env,check=True)
    if retrieve() != proposed: raise RuntimeError('Deployed rules readback mismatch')
    print('Community-only rules deployed and read back:',hashlib.sha256(proposed.encode()).hexdigest())
    subprocess.run(['npx','firebase','deploy','--only','functions:community-delete543:communityDelete543','--config',str(config),'--project','ngelx-44eed','--non-interactive'],env=env,check=True)
    # Authentication must be enforced without touching any community records.
    import requests
    url='https://europe-west1-ngelx-44eed.cloudfunctions.net/communityDelete543'
    result=requests.post(url,json={'communityId':'probe-no-write545','confirmDelete':True,'confirmName':'probe'},timeout=30)
    assert result.status_code==401, (result.status_code,result.text[:200])
    print('Community delete endpoint deployed; unauthenticated request correctly denied')
finally:
    Path(credential).unlink(missing_ok=True)
