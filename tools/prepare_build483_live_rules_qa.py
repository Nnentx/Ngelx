#!/usr/bin/env python3
"""Read-only live-rule audit; create an emulator-only community candidate.

Never publishes rules or reads/writes any Firestore documents. Rejects any
unexpected live version before building a candidate.
"""
import os, json, base64, hashlib, difflib, sys
from pathlib import Path
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession
from apply_build483_community_permissions import prepare_production_candidate

PROJECT = "ngelx-44eed"
# Read-only probe observed on 2026-10-17; changes must trigger review.
EXPECTED_LIVE_PREFIX = "0307f035ad68f047"

def retrieve():
    raw = next((os.environ.get(k) for k in (
        "FIREBASE_SERVICE_ACCOUNT_NGELX_44EED", "FIREBASE_SERVICE_ACCOUNT"
    ) if os.environ.get(k)), None)
    if not raw:
        raise RuntimeError("A read-only Firebase service credential is missing")
    try:
        credentials = json.loads(raw)
    except json.JSONDecodeError:
        credentials = json.loads(base64.b64decode(raw))
    if credentials.get("project_id") != PROJECT:
        raise RuntimeError("Unexpected Firebase project")
    session = AuthorizedSession(Credentials.from_service_account_info(
        credentials, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    ))
    base = "https://firebaserules.googleapis.com/v1/"
    release = session.get(base + "projects/" + PROJECT + "/releases/cloud.firestore", timeout=30)
    release.raise_for_status()
    ruleset_name = release.json().get("rulesetName", "")
    if not ruleset_name.startswith("projects/" + PROJECT + "/rulesets/"):
        raise RuntimeError("Unexpected released ruleset")
    result = session.get(base + ruleset_name, timeout=30)
    result.raise_for_status()
    files = result.json().get("source", {}).get("files", [])
    if len(files) != 1 or not isinstance(files[0].get("content"), str):
        raise RuntimeError("Unexpected live rules source")
    return files[0]["content"]

def main():
    live = retrieve()
    digest = hashlib.sha256(live.encode()).hexdigest()
    print("BUILD483_LIVE_HASH_PREFIX=" + digest[:16])
    if digest[:16] != EXPECTED_LIVE_PREFIX:
        raise RuntimeError("Live rules changed since review; no candidate built")
    proposed = prepare_production_candidate(live)
    live_lines = live.splitlines()
    next_lines = proposed.splitlines()
    # Only inspect bounds, never emit a full live rules dump to CI output.
    delta = list(difflib.unified_diff(live_lines, next_lines))
    if not delta or len(proposed) < len(live):
        raise RuntimeError("Expected additive rule change not found")
    print("BUILD483_CANDIDATE_HASH_PREFIX=" + hashlib.sha256(proposed.encode()).hexdigest()[:16])
    print("BUILD483_RULES_ADDED_LINES=" + str(sum(1 for x in delta if x.startswith("+") and not x.startswith("+++"))))
    print("BUILD483_RULES_REMOVED_LINES=" + str(sum(1 for x in delta if x.startswith("-") and not x.startswith("---"))))
    # Overwrite only the ephemeral CI checkout for emulator validation.
    Path("firestore.rules").write_text(proposed, encoding="utf-8")
    print("BUILD483_STATUS=EMULATOR_CANDIDATE_ONLY;NO_DEPLOY")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("BUILD483_STATUS=FAILED_SAFELY;REASON=" + str(exc))
        sys.exit(1)
