"""Publish only the NgelX Android update manifest by cloning all active Hosting assets.

DO NOT deploy website sources here: they may differ from the active website.
"""
import gzip,hashlib,json,os,time
from pathlib import Path
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request

site='ngelx-44eed'
base='https://firebasehosting.googleapis.com/v1beta1/'
feed_bytes=Path('android-update.json').read_bytes()
feed=json.loads(feed_bytes)
assert feed['build']==585 and feed['version']=='1.0.355'
assert feed['package']=='com.nnentx.ngelx_app' and feed['abi']=='arm64-v8a'
assert feed['url'].startswith('https://github.com/Nnentx/Ngelx/releases/download/v1.0.355-build585/')
service=os.environ.get('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED')
if not service:
    raise RuntimeError('Firebase Hosting secret unavailable; live updater has NOT been changed')
auth=service_account.Credentials.from_service_account_info(json.loads(service),scopes=['https://www.googleapis.com/auth/cloud-platform'])
auth.refresh(Request())
session=requests.Session()
session.headers.update({'Authorization':'Bearer '+auth.token,'Accept':'application/json'})
def api(method,path,payload=None,params=None):
    res=session.request(method,base+path,json=payload,params=params,timeout=45)
    if not res.ok: raise RuntimeError(f'{method} {path}: HTTP {res.status_code}: {res.text[:350]}')
    return res.json()
def current():
    releases=api('GET',f'sites/{site}/releases',params={'pageSize':1}).get('releases',[])
    assert releases,'Cannot find current hosting release'
    version=releases[0].get('version')
    name=version.get('name') if isinstance(version,dict) else version
    assert isinstance(name,str) and name.startswith(f'sites/{site}/versions/')
    return name
live=requests.get('https://ngelxsocial.com/android-update.json',params={'t':str(time.time_ns())},timeout=30,headers={'Cache-Control':'no-cache'})
live.raise_for_status()
active_feed=live.json()
assert isinstance(active_feed.get('build'),int) and active_feed['build']<=585,'Newer updater exists; refusing downgrade'
if active_feed['build']==585:
    assert active_feed['sha256']==feed['sha256'],'Different Build585 is already published'
old=current()
Path('hosting585-checkpoint.json').write_text(json.dumps({'previousVersion':old,'previousFeed':active_feed},ensure_ascii=False,indent=2)+'\n')
config=api('GET',old).get('config')
assert isinstance(config,dict),'Existing Hosting config unavailable'
files={}
token=None
while True:
    params={'pageSize':1000,'status':'ACTIVE'}
    if token: params['pageToken']=token
    page=api('GET',old+'/files',params=params)
    for f in page.get('files',[]):
        assert f['path'].startswith('/') and len(f['hash'])==64
        files[f['path']]=f['hash']
    token=page.get('nextPageToken')
    if not token: break
assert '/index.html' in files and len(files)>=3,'Cannot preserve active site content'
existing={path:hash for path,hash in files.items() if path!='/android-update.json'}
packed=gzip.compress(feed_bytes,compresslevel=9,mtime=0)
sha=hashlib.sha256(packed).hexdigest()
files['/android-update.json']=sha
print('Keeping',len(existing),'current web assets and all Hosting rules unchanged')
new=api('POST',f'sites/{site}/versions',{'config':config})['name']
needed=set()
upload_url=None
pairs=list(files.items())
for i in range(0,len(pairs),1000):
    out=api('POST',new+':populateFiles',{'files':dict(pairs[i:i+1000])})
    needed.update(out.get('uploadRequiredHashes',[]))
    upload_url=out.get('uploadUrl')
assert needed.issubset({sha}),f'Existing assets unexpectedly need upload: {needed}'
if sha in needed:
    uploaded=session.post(upload_url+'/'+sha,data=packed,headers={'Content-Type':'application/octet-stream'},timeout=45)
    uploaded.raise_for_status()
assert not api('GET',new+'/files',params={'status':'EXPECTED'}).get('files',[]),'Unuploaded web files'
api('PATCH',new,{'status':'FINALIZED'},params={'update_mask':'status'})
checkpoint={'previousVersion':old,'previousFeed':active_feed,'candidateVersion':new,'publishedBuild':585}
Path('hosting585-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n')
keys=['schema','package','abi','version','build','size','sha256','url']
try:
    assert current()==old,'Another website release was deployed; refusing to overwrite'
    api('POST',f'sites/{site}/releases',{},params={'versionName':new})
    for attempt in range(8):
        try:
            resp=requests.get('https://ngelxsocial.com/android-update.json',params={'t':str(time.time_ns())},timeout=15,headers={'Cache-Control':'no-cache'})
            value=resp.json() if resp.ok else {}
            canonical=requests.get('https://ngelxsocial.com/android-update.json',timeout=15,headers={'Cache-Control':'no-cache'})
            current_feed=canonical.json() if canonical.ok else {}
            if all(value.get(key)==feed[key] and current_feed.get(key)==feed[key] for key in keys):
                checkpoint['verified']=True
                Path('hosting585-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n')
                print('Verified in-app Android update feed: 1.0.355 / 585')
                break
        except (requests.RequestException,ValueError):
            pass
        time.sleep(5)
    else:
        raise RuntimeError('Custom-domain update feed could NOT be verified')
except Exception:
    # Restore only our own release; never overwrite a concurrent site release.
    if current()==new:
        api('POST',f'sites/{site}/releases',{},params={'versionName':old})
        checkpoint['rolledBack']=current()==old
        Path('hosting585-checkpoint.json').write_text(json.dumps(checkpoint,ensure_ascii=False,indent=2)+'\n')
    raise

