import os,json,base64,tempfile,subprocess
import google.auth.transport.requests
import google.oauth2.service_account
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
 http=google.auth.transport.requests.AuthorizedSession(google.oauth2.service_account.Credentials.from_service_account_info(info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
 response=http.get('https://cloudfunctions.googleapis.com/v2/projects/ngelx-44eed/locations/europe-west1/functions/livekitToken',timeout=30);response.raise_for_status()
 current=response.json();url=current.get('serviceConfig',{}).get('environmentVariables',{}).get('LIVEKIT_SERVER_URL')
 if not url or not url.startswith('wss://'):raise RuntimeError('Current LiveKit server configuration unavailable; refusing replacement')
 Path('server/.env.ngelx-44eed').write_text('LIVEKIT_SERVER_URL='+url+'\n')
 config={'functions':{'source':'server','codebase':'default','runtime':'nodejs22'}}
 Path('firebase448.json').write_text(json.dumps(config))
 subprocess.run(['npm','install','--no-package-lock'],cwd='server',check=True)
 subprocess.run(['npx','firebase','deploy','--only','functions:livekitToken,functions:incomingCall448','--config','firebase448.json','--project','ngelx-44eed','--non-interactive'],env=env,check=True)
 print('Build448 live guest token policy and incoming-call push deployed')
finally:Path(path).unlink(missing_ok=True)
