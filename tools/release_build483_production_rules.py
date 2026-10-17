#!/usr/bin/env python3
"""Build483 production Firestore RULES-only staged release with rollback.

Stage: read immutable deployed ruleset; save rollback bundle and tested candidate.
Publish: check exact previous version, create immutable candidate ruleset, patch
the SINGLE cloud.firestore release and verify; roll back on verification failure.
Never reads or modifies Firestore user documents, Storage, or authentication data.
"""
import base64
import hashlib
import json
import os
import sys
import time
from pathlib import Path

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.service_account import Credentials
from apply_build483_community_permissions import prepare_production_candidate

PROJECT = "ngelx-44eed"
RELEASE = f"projects/{PROJECT}/releases/cloud.firestore"
RULE_API = "https://firebaserules.googleapis.com/v1/"
BASE_HASH = "0307f035ad68f047"  # Existing production rules, checked read-only.
QA_HASH = "56bf091f7940bd4f"  # Emulator-tested exact community-only candidate.
BUNDLE = Path("build483-rollback")
ORIGINAL = BUNDLE / "previous.rules"
CANDIDATE = BUNDLE / "candidate.rules"
META = BUNDLE / "release-metadata.json"


def digest(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def session():
    encoded = next((os.getenv(k) for k in (
        "FIREBASE_SERVICE_ACCOUNT_NGELX_44EED", "FIREBASE_SERVICE_ACCOUNT"
    ) if os.getenv(k)), "")
    if not encoded:
        raise RuntimeError("Firebase credential unavailable; no release")
    try:
        account = json.loads(encoded)
    except json.JSONDecodeError:
        account = json.loads(base64.b64decode(encoded))
    if account.get("project_id") != PROJECT:
        raise RuntimeError("Firebase project ID mismatch; no release")
    return AuthorizedSession(Credentials.from_service_account_info(
        account, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    ))


def read_release(http):
    resp = http.get(RULE_API + RELEASE, timeout=30)
    if not resp.ok:
        raise RuntimeError(f"Read release failed (HTTP {resp.status_code})")
    data = resp.json()
    path = data.get("rulesetName", "")
    if data.get("name") != RELEASE or not path.startswith(f"projects/{PROJECT}/rulesets/"):
        raise RuntimeError("Unexpected release resource")
    return data


def read_ruleset(http, name):
    if not name.startswith(f"projects/{PROJECT}/rulesets/"):
        raise RuntimeError("Unexpected ruleset source")
    result = http.get(RULE_API + name, timeout=30)
    if not result.ok:
        raise RuntimeError(f"Read ruleset failed (HTTP {result.status_code})")
    files = result.json().get("source", {}).get("files", [])
    if len(files) != 1 or not isinstance(files[0].get("content"), str):
        raise RuntimeError("Unexpected ruleset source files")
    return files[0]["content"]


def patch_release(http, ruleset):
    if not ruleset.startswith(f"projects/{PROJECT}/rulesets/"):
        raise RuntimeError("Refusing unknown ruleset")
    # Firebase Rules API's UpdateReleaseRequest contains a 'release' object.
    payload = {"release": {"name": RELEASE, "rulesetName": ruleset}}
    result = http.patch(RULE_API + RELEASE, json=payload, timeout=30)
    if not result.ok:
        raise RuntimeError(f"Firebase release PATCH failed (HTTP {result.status_code})")
    return result.json()


def validate_bundle():
    meta = json.loads(META.read_text(encoding="utf-8"))
    old = ORIGINAL.read_text(encoding="utf-8")
    new = CANDIDATE.read_text(encoding="utf-8")
    if meta.get("project") != PROJECT or meta.get("release") != RELEASE:
        raise RuntimeError("Unexpected release metadata")
    if meta.get("rulesetName", "").startswith(f"projects/{PROJECT}/rulesets/") is False:
        raise RuntimeError("Unexpected backup ruleset")
    if meta.get("originalSha256") != digest(old) or digest(old)[:16] != BASE_HASH:
        raise RuntimeError("Original rollback bundle checksum mismatch")
    if meta.get("candidateSha256") != digest(new) or digest(new)[:16] != QA_HASH:
        raise RuntimeError("Candidate rollback bundle checksum mismatch")
    if prepare_production_candidate(old) != new:
        raise RuntimeError("Candidate differs from the independently generated rules")
    return meta, old, new


def stage():
    http = session()
    live = read_release(http)
    before = read_ruleset(http, live["rulesetName"])
    if digest(before)[:16] != BASE_HASH:
        raise RuntimeError("Production rules changed; aborting before backup")
    candidate = prepare_production_candidate(before)
    if digest(candidate)[:16] != QA_HASH:
        raise RuntimeError("Candidate differs from emulator-tested policy; stop")
    if candidate == before:
        raise RuntimeError("No candidate rule change; stop")
    BUNDLE.mkdir(exist_ok=True)
    ORIGINAL.write_text(before, encoding="utf-8")
    CANDIDATE.write_text(candidate, encoding="utf-8")
    META.write_text(json.dumps({
        "project": PROJECT, "release": RELEASE,
        "rulesetName": live["rulesetName"],
        "originalSha256": digest(before),
        "candidateSha256": digest(candidate),
    }, indent=2), encoding="utf-8")
    validate_bundle()
    Path("firestore.rules").write_text(candidate, encoding="utf-8")
    print("BUILD483_STAGE=ROLLBACK_READY;EMULATOR_NEXT")
    print("BUILD483_OLD_SHA_PREFIX=" + digest(before)[:16])
    print("BUILD483_TESTED_SHA_PREFIX=" + digest(candidate)[:16])
    print("BUILD483_ORIGINAL_RULESET=" + live["rulesetName"])


def publish():
    meta, original, candidate = validate_bundle()
    http = session()
    live = read_release(http)
    if live["rulesetName"] != meta["rulesetName"]:
        raise RuntimeError("Current release changed after QA; refusing deployment")
    if digest(read_ruleset(http, live["rulesetName"])) != digest(original):
        raise RuntimeError("Production rule contents changed; refusing deployment")
    # Immutable ruleset creation checks Firestore rules syntax before releasing.
    reply = http.post(RULE_API + f"projects/{PROJECT}/rulesets", json={
        "source": {"files": [{"name": "firestore.rules", "content": candidate}]}
    }, timeout=45)
    if not reply.ok:
        raise RuntimeError(f"Create validated candidate ruleset failed (HTTP {reply.status_code}); release unchanged")
    new_name = reply.json().get("name", "")
    if not new_name.startswith(f"projects/{PROJECT}/rulesets/"):
        raise RuntimeError("New ruleset path invalid; release unchanged")
    if digest(read_ruleset(http, new_name)) != digest(candidate):
        raise RuntimeError("Immutable candidate differs from test; release unchanged")
    if read_release(http)["rulesetName"] != meta["rulesetName"]:
        raise RuntimeError("Release changed during candidate creation; refusing publish")
    print("BUILD483_IMMUTABLE_RULESET_CREATED=" + new_name)
    try:
        patch_release(http, new_name)
        for _ in range(4):
            current = read_release(http)
            if current["rulesetName"] == new_name and (
                digest(read_ruleset(http, new_name)) == digest(candidate)
            ):
                print("BUILD483_PRODUCTION_PUBLISHED_AND_VERIFIED=TRUE")
                print("BUILD483_ROLLBACK_RULESET=" + meta["rulesetName"])
                print("BUILD483_ACTIVE_SHA_PREFIX=" + digest(candidate)[:16])
                return
            time.sleep(2)
        raise RuntimeError("Release read-back mismatch after publication")
    except Exception as error:
        # Only undo our own update; never clobber another actor's new ruleset.
        live_now = read_release(http)
        if live_now["rulesetName"] == new_name:
            try:
                patch_release(http, meta["rulesetName"])
                restored = read_release(http)
                if restored["rulesetName"] != meta["rulesetName"] or (
                    digest(read_ruleset(http, meta["rulesetName"])) != digest(original)
                ):
                    raise RuntimeError("Rollback verification mismatch")
                print("BUILD483_AUTOMATIC_ROLLBACK=SUCCESS")
            except Exception as rollback_error:
                raise RuntimeError(
                    "URGENT: live rules may have changed and automatic rollback failed"
                ) from rollback_error
        raise RuntimeError("Build483 deploy verification failed; see rollback status") from error


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2 or sys.argv[1] not in ("stage", "publish"):
            raise RuntimeError("Usage: release_build483_production_rules.py stage|publish")
        if sys.argv[1] == "stage":
            stage()
        else:
            publish()
    except Exception as exc:
        # Deliberately avoid displaying credentials, original rules, or PII.
        print("BUILD483_RELEASE_ERROR=" + str(exc))
        sys.exit(1)
