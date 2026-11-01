import os,json,base64,time,secrets,concurrent.futures,hashlib
from pathlib import Path
import requests
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
raw=os.environ.get('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED') or os.environ.get('FIREBASE_SERVICE_ACCOUNT')
try:info=json.loads(raw)
except json.JSONDecodeError:info=json.loads(base64.b64decode(raw))
assert info['project_id']=='ngelx-44eed'
creds=Credentials.from_service_account_info(info,scopes=['https://www.googleapis.com/auth/cloud-platform']);admin=AuthorizedSession(creds)
cfg=json.loads(Path('tested/app/android/app/google-services.json').read_text());key=next(c['api_key'][0]['current_key'] for c in cfg['client'] if c['client_info']['android_client_info']['package_name']=='com.nnentx.ngelx_app')
root='https://firestore.googleapis.com/v1/projects/ngelx-44eed/databases/(default)/documents/';endpoint='https://ngelx-live-moderation.alihancaglar76.workers.dev/pk/finish'
nonce=secrets.token_hex(10);prefix='qa_pk588_'+nonce;users=[];paths=[]
def b64(b):return base64.urlsafe_b64encode(b).rstrip(b'=').decode()
def login(i):
 uid=prefix+'_'+str(i);now=int(time.time());head=b64(json.dumps({'alg':'RS256','typ':'JWT'}).encode());body=b64(json.dumps({'iss':info['client_email'],'sub':info['client_email'],'aud':'https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit','iat':now,'exp':now+600,'uid':uid}).encode());value=head+'.'+body;token=value+'.'+b64(creds.sign_bytes(value.encode()))
 r=requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken',params={'key':key},json={'token':token,'returnSecureToken':True},timeout=30);r.raise_for_status();users.append((uid,r.json()['idToken']));return users[-1]
def field(v):
 if v is None:return {'nullValue':None}
 if isinstance(v,bool):return {'booleanValue':v}
 if isinstance(v,int):return {'integerValue':str(v)}
 if isinstance(v,str):return {'stringValue':v}
 if isinstance(v,list):return {'arrayValue':{'values':[field(x) for x in v]}}
 return {'mapValue':{'fields':{k:field(x) for k,x in v.items()}}}
def put(path,v):
 paths.append(path);r=admin.patch(root+path,params={'currentDocument.exists':'false'},json={'fields':{k:field(x) for k,x in v.items()}},timeout=30);r.raise_for_status()
def call(user):
 r=requests.post(endpoint,headers={'Authorization':'Bearer '+user[1]},json={'sessionId':prefix},timeout=30)
 if r.status_code!=200:raise RuntimeError('PK smoke HTTP '+str(r.status_code))
 return r.json()
try:
 a=login(0);b=login(1);now=int(time.time()*1000);ra=prefix+'_a';rb=prefix+'_b'
 put('calls/'+prefix,{'type':'live_pk','status':'active','members':[a[0],b[0]],'inviterUid':a[0],'inviteeUid':b[0],'inviterLiveId':ra,'inviteeLiveId':rb,'clientStartedAt':now-181000,'endsAt':now-1000,'startLikeA':0,'startLikeB':0,'startGiftA':0,'startGiftB':0})
 # Inactive private fixtures cannot appear in live discovery or send invitations.
 for room,user,likes in [(ra,a,12),(rb,b,2)]:put('live_streams/'+room,{'ownerId':user[0],'active':False,'visibility':'private','pkSessionId':prefix,'pkActive':True,'likeCount':likes,'giftPoints':0})
 paths.extend(['live_pk_stats588/'+a[0],'live_pk_stats588/'+b[0]]+['_livekit_rate_limits/free_'+hashlib.sha256(('pk588:'+u[0]).encode()).hexdigest() for u in [a,b]])
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(call,[a,b]))
 assert all(r['winnerUid']==a[0] and r['streakByUid'][a[0]]==1 and r['streakByUid'][b[0]]==0 for r in results)
 assert call(a)['streakByUid'][a[0]]==1
 r=admin.get(root+'live_pk_stats588/'+a[0],timeout=30);r.raise_for_status();assert int(r.json()['fields']['streak']['integerValue'])==1
 r=requests.get(root+'live_pk_stats588/'+a[0],headers={'Authorization':'Bearer '+a[1]},timeout=30);assert r.status_code==200
 r=requests.patch(root+'live_pk_stats588/'+a[0],headers={'Authorization':'Bearer '+a[1]},json={'fields':{'streak':{'integerValue':'999'}}},timeout=30);assert r.status_code==403
 print('Real authenticated PK: concurrent finish, shared winner, WIN x1 and idempotent retry verified')
finally:
 failures=0
 for path in paths:
  try:
   r=admin.delete(root+path,timeout=30);assert r.status_code in [200,404]
  except Exception:failures+=1
 for uid,token in users:
  try:
   r=requests.post('https://identitytoolkit.googleapis.com/v1/accounts:delete',params={'key':key},json={'idToken':token},timeout=30);r.raise_for_status()
  except Exception:failures+=1
 if failures:raise RuntimeError('Temporary fixture cleanup failures: '+str(failures))
 print('All temporary PK documents and test accounts removed')
