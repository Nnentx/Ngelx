"""Deploy isolated incoming-call push; retain existing working media transport."""
import os,json,base64,tempfile,subprocess,shutil
from pathlib import Path
raw=next((os.environ.get(k,'')for k in ('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED','FIREBASE_SERVICE_ACCOUNT','GOOGLE_APPLICATION_CREDENTIALS_JSON')if os.environ.get(k)),None)
if not raw:raise RuntimeError('Existing deployment credential unavailable')
try:info=json.loads(raw)
except json.JSONDecodeError:info=json.loads(base64.b64decode(raw))
if info.get('project_id')!='ngelx-44eed':raise RuntimeError('Unexpected project')
fd,path=tempfile.mkstemp(prefix='ngelx448-',suffix='.json');os.chmod(path,0o600)
try:
 with os.fdopen(fd,'w')as f:json.dump(info,f)
 env=dict(os.environ,GOOGLE_APPLICATION_CREDENTIALS=path)
 source=Path('callpush448');source.mkdir(exist_ok=True)
 policy=Path('server/calls448/push-policy.mjs').read_text()
 policy=policy.replace("import {fresh, millis} from '../livekit443/room-policy.mjs';", "const millis=v=>typeof v?.toMillis==='function'?v.toMillis():v instanceof Date?v.getTime():NaN;\nconst fresh=(v,now,max)=>Number.isFinite(millis(v))&&now-millis(v)>=-30000&&now-millis(v)<=max;")
 (source/'push-policy.mjs').write_text(policy)
 index=Path('server/calls448/index.mjs').read_text()
 (source/'index.mjs').write_text("import {initializeApp,getApps} from 'firebase-admin/app';\nif(!getApps().length)initializeApp();\n"+index)
 (source/'package.json').write_text(json.dumps({'name':'ngelx-callpush448','private':True,'type':'module','main':'index.mjs','engines':{'node':'22'},'dependencies':{'firebase-admin':'^13.6.0','firebase-functions':'^6.4.0'}}))
 config={'functions':{'source':'callpush448','codebase':'calls448','runtime':'nodejs22'}}
 Path('firebase448.json').write_text(json.dumps(config))
 subprocess.run(['npm','install','--no-package-lock'],cwd=source,check=True)
 subprocess.run(['npx','firebase','deploy','--only','functions:calls448:incomingCall448','--config','firebase448.json','--project','ngelx-44eed','--non-interactive'],env=env,check=True)
 print('Build448 incoming-call push deployed; media token transport preserved')
finally:Path(path).unlink(missing_ok=True)
