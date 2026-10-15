#!/usr/bin/env python3
"""Deploy only the previously emulator-tested, minimal Build457 community COVER rule.

Safety:
 - Requires exact candidate generated from live production before emulator tests.
 - Re-reads production immediately before deploy and aborts on any concurrent change.
 - Refuses unrelated data/rule mutations and verifies exact read-back.
 - Writes no Firestore user, community or media documents.
"""
import os
import json
import base64
import hashlib
import subprocess
import tempfile
from pathlib import Path

import google.oauth2.service_account
import google.auth.transport.requests
from apply_build457_cover_rules import transform as cover_only, OLD as OLD_RULE_BLOCK, NEW as NEW_RULE_BLOCK

PROJECT="ngelx-44eed"
API="https://firebaserules.googleapis.com/v1/"

def credentials():
    raw=next((os.environ.get(k) for k in (
        "FIREBASE_SERVICE_ACCOUNT_NGELX_44EED","FIREBASE_SERVICE_ACCOUNT"
    ) if os.environ.get(k)),None)
    if not raw: raise RuntimeError("Deployment service credential unavailable")
    try: info=json.loads(raw)
    except json.JSONDecodeError: info=json.loads(base64.b64decode(raw))
    if info.get("project_id")!=PROJECT: raise RuntimeError("Incorrect Firebase project")
    session=google.auth.transport.requests.AuthorizedSession(
      google.oauth2.service_account.Credentials.from_service_account_info(
        info,scopes=["https://www.googleapis.com/auth/cloud-platform"]))
    return info, session

def live(session):
    release=session.get(API+"projects/"+PROJECT+"/releases/cloud.firestore",timeout=30)
    release.raise_for_status()
    name=release.json().get("rulesetName","")
    if not name.startswith("projects/"+PROJECT+"/rulesets/"):
        raise RuntimeError("Unexpected active ruleset reference")
    ruleset=session.get(API+name,timeout=30)
    ruleset.raise_for_status()
    files=ruleset.json().get("source",{}).get("files",[])
    if len(files)!=1 or not isinstance(files[0].get("content"),str):
        raise RuntimeError("Unexpected active rules files")
    return name, files[0]["content"]

def digest(value):return hashlib.sha256(value.encode()).hexdigest()

def main():
    info,session=credentials()
    before_name,original=live(session)
    candidate=Path("firestore.rules").read_text(encoding="utf-8")
    expected=cover_only(original)
    # A workflow rerun after successful deployment is harmless.
    if expected==original:
        print("DEPLOY463_STATUS=ALREADY_PRESENT")
        return
    if candidate!=expected:
        raise RuntimeError("Candidate differs from precisely scoped cover-only change to live baseline")
    if candidate.count("// Build457 legacy founder cover-only repair")!=1:
        raise RuntimeError("Candidate missing single cover repair")
    # Check preserved untouched sections and absence of broad rule edits.
    if "// Build456 community moderation" in candidate and "// Build456 community moderation" not in original:
        raise RuntimeError("Unexpected broad Build456 rules included")
    # Exact textual replacement guard: absolutely no other rules change.
    if original.count(OLD_RULE_BLOCK)!=1 or candidate!=original.replace(OLD_RULE_BLOCK,NEW_RULE_BLOCK,1):
        raise RuntimeError("Expected exactly one approved cover-only rule insertion")
    if len(candidate)-len(original)>1600:
        raise RuntimeError("Rule patch unexpectedly large")
    # Confirm production hasn't been changed by another administrator since tests.
    confirmation_name,confirmation=live(session)
    if confirmation_name!=before_name or confirmation!=original:
        raise RuntimeError("Production rules changed during approval/test window; deploy aborted")
    fd,credential_path=tempfile.mkstemp(prefix="ngelx463-deploy-",suffix=".json")
    os.chmod(credential_path,0o600)
    try:
        with os.fdopen(fd,"w") as handle:json.dump(info,handle)
        environment=dict(os.environ)
        environment["GOOGLE_APPLICATION_CREDENTIALS"]=credential_path
        # Scope strictly to Firestore RULES: no indexes/functions/storage/hosting.
        subprocess.run(
            ["npx","--no-install","firebase","deploy","--only","firestore:rules",
             "--project",PROJECT,"--non-interactive"],check=True,env=environment)
        final_name,final_content=live(session)
        if final_content != candidate:
            raise RuntimeError("DEPLOY463_VERIFICATION_FAILED: active rules differ from approved candidate")
        print("DEPLOY463_STATUS=VERIFIED_SUCCESS")
        print("DEPLOY463_PREVIOUS_RULES_HASH="+digest(original)[:16])
        print("DEPLOY463_CURRENT_RULES_HASH="+digest(final_content)[:16])
        print("DEPLOY463_CHANGE=LEGACY_FOUNDER_COVER_ONLY")
    finally:
        Path(credential_path).unlink(missing_ok=True)

if __name__=="__main__":main()
