"""Read the active rule source with an explicit credential; no production writes."""
import base64
import hashlib
import json
import os
import urllib.request
from pathlib import Path
from google.oauth2 import service_account
from google.auth.transport.requests import Request

raw = os.environ.get('NGELX_SERVICE_JSON', '')
if not raw:
    raise RuntimeError('Existing Firebase service credential unavailable')
try:
    info = json.loads(raw)
except json.JSONDecodeError:
    info = json.loads(base64.b64decode(raw))
project = info['project_id']
if project != 'ngelx-44eed':
    raise RuntimeError('Unexpected Firebase project; refusing diagnostic')
creds = service_account.Credentials.from_service_account_info(
    info, scopes=['https://www.googleapis.com/auth/cloud-platform'])
creds.refresh(Request())
def read(path):
    request = urllib.request.Request(
        'https://firebaserules.googleapis.com/v1/' + path,
        headers={'Authorization': 'Bearer ' + creds.token}, method='GET')
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)
release = read('projects/' + project + '/releases/cloud.firestore')
files = read(release['rulesetName'])['source']['files']
rules = [f['content'] for f in files if 'match /databases/' in f['content']]
if len(rules) != 1:
    raise RuntimeError('Expected one active Firestore rule source')
Path('firestore.rules').write_text(rules[0])
print('Read-only production rules snapshot SHA256: ' + hashlib.sha256(rules[0].encode()).hexdigest())
