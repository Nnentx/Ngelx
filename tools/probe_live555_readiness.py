"""Read-only check of the existing deployment identity; never print credentials."""
import base64
import json
import os
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials

PROJECT='ngelx-44eed'
raw=next((os.environ.get(k) for k in (
    'FIREBASE_SERVICE_ACCOUNT_NGELX_44EED','FIREBASE_SERVICE_ACCOUNT')
    if os.environ.get(k)),None)
if not raw:
    raise RuntimeError('Existing deployment identity unavailable')
try:
    info=json.loads(raw)
except json.JSONDecodeError:
    info=json.loads(base64.b64decode(raw))
if info.get('project_id')!=PROJECT:
    raise RuntimeError('Refusing a different Firebase project')
# Explicit credentials only. Do not probe the host metadata service or use ADC.
session=AuthorizedSession(Credentials.from_service_account_info(
    info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
permissions=[
    'cloudfunctions.functions.get','cloudfunctions.functions.list',
    'cloudfunctions.functions.create','cloudfunctions.functions.update',
    'cloudfunctions.functions.setIamPolicy','secretmanager.secrets.get',
    'secretmanager.versions.access','serviceusage.services.use',
]
response=session.post(
    f'https://cloudresourcemanager.googleapis.com/v1/projects/{PROJECT}:testIamPermissions',
    json={'permissions':permissions},timeout=20)
print('Deployment permission check HTTP:',response.status_code)
if response.ok:
    allowed=set(response.json().get('permissions',[]))
    for permission in permissions:
        print(permission, 'ALLOWED' if permission in allowed else 'NOT_GRANTED')
for label,url in [
    ('Function administration',f'https://cloudfunctions.googleapis.com/v2/projects/{PROJECT}/locations/europe-west1/functions'),
    ('LiveKit configuration metadata',f'https://secretmanager.googleapis.com/v1/projects/{PROJECT}/secrets'),
]:
    response=session.get(url,timeout=20)
    print(label+' HTTP:',response.status_code)
    if not response.ok:
        # Only structured public error codes, never arbitrary response bodies.
        try:
            error=response.json().get('error',{})
            print(label+' error status:',error.get('status','UNKNOWN'))
            for detail in error.get('details',[]):
                if detail.get('@type','').endswith('ErrorInfo'):
                    print(label+' reason:',detail.get('reason','UNKNOWN'))
                    metadata=detail.get('metadata',{})
                    for key in ('service','permission'):
                        if key in metadata:print(label+' '+key+':',metadata[key])
        except (ValueError,AttributeError,TypeError):
            print(label+' error details unavailable')
print('Read-only checks complete; no service, IAM, secret, rule, billing or data changes.')
