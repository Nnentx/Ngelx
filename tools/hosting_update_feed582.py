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
assert feed['build']==582 and feed['version']=='1.0.352'
assert feed['package']=='com.nnentx.ngelx_app' and feed['abi']=='arm64-v8a'
assert feed['size']==50180430
assert feed['sha256']=='c96c46216f0fc1021d07a3f940fc0daf808f774addf8044153a55f01e461dc47'
assert feed['url'].startswith('https://github.com/Nnentx/Ngelx/releases/download/v1.0.352-build582/')
service=os.environ.get('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED')
if not service:
    raise RuntimeError('Firebase Hosting secret unavailable; live updater has NOT been changed')
identity=json.loads(service)
assert identity.get('project_id')==site,'Wrong Firebase project'
auth=service_account.Credentials.from_service_account_info(identity,scopes=['https://www.googleapis.com/auth/cloud-platform'])
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
current_feed=requests.get('https://ngelxsocial.com/android-update.json',params={'check':str(time.time_ns())},headers={'Cache-Control':'no-cache'},timeout=20)
current_feed.raise_for_status()
previous=current_feed.json()
assert previous.get('package')==feed['package'] and previous.get('abi')==feed['abi']
assert isinstance(previous.get('build'),int) and previous['build']<=582,'Refusing to downgrade a newer live update'
if previous['build']==582:
    assert previous.get('sha256')==feed['sha256'] and previous.get('url')==feed['url'],'Existing Build582 differs'
    print('Build582 is already live and matches the verified APK')
    raise SystemExit(0)
old=current()
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
assert current()==old,'Another website release was deployed; refusing to overwrite'
api('POST',f'sites/{site}/releases',{},params={'versionName':new})
for attempt in range(8):
    try:
        resp=requests.get('https://ngelxsocial.com/android-update.json',params={'t':str(time.time_ns())},timeout=15,headers={'Cache-Control':'no-cache'})
        value=resp.json() if resp.ok else {}
        if value.get('build')==582 and value.get('sha256')==feed['sha256']:
            print('Verified in-app Android update feed: 1.0.352 / 582')
            break
    except (requests.RequestException,ValueError):
        pass
    time.sleep(5)
else:
    raise RuntimeError('Hosting version released, but custom-domain update feed could NOT be verified')
