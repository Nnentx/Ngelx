#!/usr/bin/env python3
"""Read-only planning for community rules patch against ACTUAL production rules.
Fetches only rule text (no app records); never deploys or prints rule contents.
"""
import os, json, base64, hashlib
from pathlib import Path
import google.oauth2.service_account,google.auth.transport.requests
from apply_build457_cover_rules import transform as rules457

def main():
    raw=next((os.environ.get(k) for k in ('FIREBASE_SERVICE_ACCOUNT_NGELX_44EED',
                                            'FIREBASE_SERVICE_ACCOUNT') if os.environ.get(k)),'')
    if not raw:raise RuntimeError('No existing project deployment credentials')
    try:info=json.loads(raw)
    except json.JSONDecodeError:info=json.loads(base64.b64decode(raw))
    if info.get('project_id')!='ngelx-44eed':raise RuntimeError('Wrong project')
    session=google.auth.transport.requests.AuthorizedSession(
        google.oauth2.service_account.Credentials.from_service_account_info(
            info,scopes=['https://www.googleapis.com/auth/cloud-platform']))
    base='https://firebaserules.googleapis.com/v1/'
    release=session.get(base+'projects/ngelx-44eed/releases/cloud.firestore',timeout=30)
    release.raise_for_status()
    ruleset_name=release.json().get('rulesetName','')
    if not ruleset_name.startswith('projects/ngelx-44eed/rulesets/'):
        raise RuntimeError('Unexpected release ruleset ref')
    reply=session.get(base+ruleset_name,timeout=30);reply.raise_for_status()
    files=reply.json()['source']['files']
    if len(files)!=1:raise RuntimeError('Unexpected number of rules files')
    original=files[0]['content']
    if '// Build456 community moderation' in original or '// Build457 legacy founder cover-only repair' in original:
        raise RuntimeError('Markers changed unexpectedly; require manual review')
    if original.count('    // Build450 communities')!=1:
        raise RuntimeError('Expected single Build450 community block')
    updated=rules457(original)
    for marker in ('// Build457 legacy founder cover-only repair',):
        if updated.count(marker)!=1:raise RuntimeError('Missing expected new marker: '+marker)
    # Critical invariants: no rewriting unrelated auth/chat/user read/update rules.
    for segment in ('    match /chats/{chatId} {', '    match /videos/{videoId} {',
                    '    match /users/{uid} {'):
        if segment not in original or segment not in updated:
            raise RuntimeError('Rule section absent in before/after: '+segment)
    def entire(start, stop):
        a=original.index(start);b=original.index(stop,a)
        c=updated.index(start);d=updated.index(stop,c)
        return original[a:b]==updated[c:d]
    for start,stop in [('    match /videos/{videoId} {','    match /chats/{chatId} {')]:
        if not entire(start,stop):
            raise RuntimeError('Unrelated production video rules would change')
    Path('firestore.rules').write_text(updated,encoding='utf-8')
    print('DRY463_STATUS=MINIMAL_COVER_ONLY_PROPOSAL_NO_DEPLOY')
    print('DRY463_BASE_HASH='+hashlib.sha256(original.encode()).hexdigest()[:16])
    print('DRY463_PATCH_HASH='+hashlib.sha256(updated.encode()).hexdigest()[:16])
    print('DRY463_COVER_ONLY_PATCH_BYTES='+str(len(updated)-len(original)))
    print('DRY463_AUTH_CHAT_VIDEO_RULES=PRESERVED')

if __name__=='__main__':main()
