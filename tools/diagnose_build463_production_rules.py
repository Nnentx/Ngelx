#!/usr/bin/env python3
"""Read-only NgelX production Firestore rule-version check. Never print rules, credentials or user data."""
import os, json, base64, hashlib, sys
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession

def main():
    raw=next((os.environ.get(k) for k in (
        'FIREBASE_SERVICE_ACCOUNT_NGELX_44EED','FIREBASE_SERVICE_ACCOUNT')
        if os.environ.get(k)),None)
    if not raw:
        print("DIAG463_STATUS=NO_CREDENTIAL_AVAILABLE")
        return 2
    try:
        info=json.loads(raw)
    except json.JSONDecodeError:
        info=json.loads(base64.b64decode(raw))
    if info.get('project_id')!='ngelx-44eed':
        print("DIAG463_STATUS=PROJECT_MISMATCH")
        return 2
    creds=Credentials.from_service_account_info(info,
        scopes=['https://www.googleapis.com/auth/cloud-platform'])
    http=AuthorizedSession(creds)
    base="https://firebaserules.googleapis.com/v1/"
    release=http.get(base+"projects/ngelx-44eed/releases/cloud.firestore",timeout=30)
    if release.status_code != 200:
        print("DIAG463_STATUS=RELEASE_READ_FAILED;HTTP="+str(release.status_code))
        return 2
    ruleset_name=release.json().get('rulesetName','')
    if not ruleset_name.startswith('projects/ngelx-44eed/rulesets/'):
        print("DIAG463_STATUS=UNKNOWN_RULESET")
        return 2
    response=http.get(base+ruleset_name,timeout=30)
    if response.status_code != 200:
        print("DIAG463_STATUS=RULESET_READ_FAILED;HTTP="+str(response.status_code))
        return 2
    files=response.json().get('source',{}).get('files',[])
    if len(files)!=1:
        print("DIAG463_STATUS=UNEXPECTED_RULE_FILES;COUNT="+str(len(files)))
        return 2
    rules=files[0].get('content','')
    if not isinstance(rules,str) or not rules:
        print("DIAG463_STATUS=EMPTY_RULE_FILE")
        return 2
    checks={
        'COMMUNITY_ROOT':"match /communities450/{cid}" in rules,
        'COMMUNITY_POSTS':"match /posts/{pid}" in rules and "communityMember450" in rules,
        'COMMUNITY_COMMENTS':"match /comments/{commentId}" in rules and "communityVisible450" in rules,
        'COMMUNITY_COVER_LEGACY_FIX':"Build457 legacy founder cover-only repair" in rules,
        'COMMUNITY_COMMENT_455':"reactionVisible455" in rules or "communityMetric" in rules or "commentCount455" in rules,
        'COMMUNITY_COMMENT_456_SLOWMODE':"commentLimits456" in rules,
        'COMMUNITY_456_MODERATION':"communityPosting456" in rules,
        'CHAT_COLLECTION':"match /chats/{chatId}" in rules,
        'USER_COLLECTION':"match /users/{uid}" in rules,
    }
    print("DIAG463_STATUS=OK")
    print("DIAG463_RULESET_FINGERPRINT="+hashlib.sha256(rules.encode()).hexdigest()[:16])
    for label,value in checks.items():
        print("DIAG463_"+label+"="+str(value).lower())
    if not checks['COMMUNITY_ROOT']:
        print("DIAG463_CONCLUSION=COMMUNITY_RULES_MISSING")
    elif not checks['COMMUNITY_COVER_LEGACY_FIX']:
        print("DIAG463_CONCLUSION=LEGACY_COVER_FIX_MISSING")
    elif not checks['COMMUNITY_COMMENT_456_SLOWMODE']:
        print("DIAG463_CONCLUSION=COMMENT_RULES_OUTDATED")
    else:
        print("DIAG463_CONCLUSION=KEY_RULE_MARKERS_PRESENT")
    return 0

if __name__=='__main__':
    sys.exit(main())
