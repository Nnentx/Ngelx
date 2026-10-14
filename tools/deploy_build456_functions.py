"""Deploy isolated community services using the repository's existing Firebase identity."""
import os,json,base64,tempfile,subprocess,shutil
from pathlib import Path
raw=next((os.environ.get(k)for k in ('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED','FIREBASE_SERVICE_ACCOUNT')if os.environ.get(k)),None)
if not raw:raise RuntimeError('Existing Firebase deployment identity unavailable')
try:info=json.loads(raw)
except json.JSONDecodeError:info=json.loads(base64.b64decode(raw))
if info.get('project_id')!='ngelx-44eed':raise RuntimeError('Unexpected project')
fd,path=tempfile.mkstemp(prefix='ngelx456-',suffix='.json');os.chmod(path,0o600)
try:
 with os.fdopen(fd,'w')as f:json.dump(info,f)
 source=Path('community-services456');source.mkdir(exist_ok=True);shutil.copy('server/community456/index.mjs',source/'index.mjs');shutil.copy('server/community456/policy.mjs',source/'policy.mjs')
 (source/'package.json').write_text(json.dumps({'name':'ngelx-community456','private':True,'type':'module','main':'index.mjs','engines':{'node':'22'},'dependencies':{'firebase-admin':'^13.6.0','firebase-functions':'^6.4.0'}}))
 Path('firebase456-functions.json').write_text(json.dumps({'functions':{'source':str(source),'codebase':'community456','runtime':'nodejs22'}}))
 subprocess.run(['npm','install','--no-package-lock'],cwd=source,check=True)
 subprocess.run(['npx','firebase','deploy','--only','functions:community456','--config','firebase456-functions.json','--project','ngelx-44eed','--non-interactive'],env=dict(os.environ,GOOGLE_APPLICATION_CREDENTIALS=path),check=True)
 print('Community schedules, counters and opt-in notifications deployed')
finally:Path(path).unlink(missing_ok=True)
