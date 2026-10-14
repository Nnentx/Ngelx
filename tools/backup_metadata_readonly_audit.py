#!/usr/bin/env python3
"""Read-only NgelX Firestore backup / R2 lifecycle metadata audit.

This program never fetches user documents, enumerates R2 objects, exports files,
runs deployment commands, creates backups, or mutates any remote service.
Output includes only aggregate backup/lifecycle status, safe for CI logs.
"""
import base64
import datetime as dt
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

PROJECT = "ngelx-44eed"
R2_BUCKET = "ngelx-media"
UTC = dt.timezone.utc


def summarize_backups(payload, now=None):
    now = now or dt.datetime.now(UTC)
    backups = payload.get("backups") or []
    unreachable = payload.get("unreachable") or []
    ready = [x for x in backups if x.get("state") == "READY"
             and x.get("database") == f"projects/{PROJECT}/databases/(default)"]
    dates = []
    for item in ready:
        stamp = item.get("snapshotTime")
        try:
            if stamp:
                dates.append(dt.datetime.fromisoformat(stamp.replace("Z", "+00:00")))
        except (ValueError, TypeError):
            pass
    latest = max(dates) if dates else None
    return {
        "state": "PARTIAL" if unreachable else ("READY" if ready else "NONE"),
        "ready_count": len(ready),
        "latest_snapshot_age_days": round(max(0, (now-latest).total_seconds())/86400, 1) if latest else None,
        "unreachable_location_count": len(unreachable),
    }


def summarize_lifecycle(payload):
    rules = (payload.get("result") or {}).get("rules") or []
    active = [x for x in rules if x.get("enabled") is True]
    deletes = [x for x in active if x.get("deleteObjectsTransition") is not None]
    return {
        "state": "READ",
        "enabled_rule_count": len(active),
        "enabled_object_deletion_rules": len(deletes),
        "separate_media_backup_verified": False,
    }


def fetch_json(url, bearer):
    request = Request(url, headers={"Authorization": "Bearer " + bearer,
                                    "Accept": "application/json"},
                      method="GET")
    try:
        with urlopen(request, timeout=25) as response:
            return json.load(response), None
    except HTTPError as error:
        return None, "HTTP_" + str(error.code)
    except (URLError, TimeoutError):
        return None, "NETWORK_UNAVAILABLE"
    except (ValueError, TypeError):
        return None, "BAD_RESPONSE"



def summarize_pitr(database):
    enabled = database.get("pointInTimeRecoveryEnablement") == "POINT_IN_TIME_RECOVERY_ENABLED"
    start = database.get("earliestVersionTime")
    target = dt.datetime(2026, 10, 14, 13, 46, tzinfo=UTC)
    inside = False
    if start:
        try:
            inside = dt.datetime.fromisoformat(start.replace("Z", "+00:00")) <= target
        except (ValueError, TypeError):
            pass
    return {
        "state": "ENABLED" if enabled else "DISABLED",
        "pre_cleanup_read_time_in_window": bool(enabled and inside),
        "note": "Historical-read window is not proof the specific deleted records exist.",
    }


def firebase_backup_status():
    raw = (os.getenv("FIREBASE_SERVICE_ACCOUNT_NGELX_44EED") or
           os.getenv("FIREBASE_SERVICE_ACCOUNT") or
           os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"))
    if not raw:
        return {"state": "NO_CREDENTIAL"}, {"state": "NO_CREDENTIAL"}, {"state": "NO_CREDENTIAL"}
    try:
        try:
            info = json.loads(raw)
        except (ValueError, TypeError):
            info = json.loads(base64.b64decode(raw, validate=True))
        if info.get("project_id") != PROJECT:
            return {"state": "PROJECT_MISMATCH"}, {"state": "PROJECT_MISMATCH"}, {"state": "PROJECT_MISMATCH"}
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request as GoogleRequest
        creds = service_account.Credentials.from_service_account_info(
            info, scopes=["https://www.googleapis.com/auth/cloud-platform"])
        creds.refresh(GoogleRequest())
    except Exception:
        # Do not leak credentials, token endpoints or exception content to public logs.
        return {"state": "AUTH_UNAVAILABLE"}, {"state": "AUTH_UNAVAILABLE"}, {"state": "AUTH_UNAVAILABLE"}
    base = "https://firestore.googleapis.com/v1/projects/" + PROJECT
    listed, error = fetch_json(base + "/locations/-/backups", creds.token)
    if error:
        backup_status = {"state": error}
    else:
        backup_status = summarize_backups(listed)
    schedules, error = fetch_json(base + "/databases/(default)/backupSchedules", creds.token)
    if error:
        schedule_status = {"state": error}
    else:
        schedule_status = {
            "state": "READ",
            "schedule_count": len(schedules.get("backupSchedules") or []),
        }
    database, error = fetch_json(base + '/databases/(default)', creds.token)
    pitr_status = {'state': error} if error else summarize_pitr(database)
    return backup_status, schedule_status, pitr_status


def r2_lifecycle_status():
    account = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    token = os.getenv("CLOUDFLARE_API_TOKEN")
    if not account or not token:
        return {"state": "NO_CREDENTIAL"}
    if not all(c.isalnum() or c in "-_" for c in account):
        return {"state": "BAD_ACCOUNT_ID"}
    url = (f"https://api.cloudflare.com/client/v4/accounts/{account}"
           f"/r2/buckets/{R2_BUCKET}/lifecycle")
    response, error = fetch_json(url, token)
    if error:
        return {"state": error}
    if response.get("success") is not True:
        return {"state": "API_UNVERIFIED"}
    return summarize_lifecycle(response)


def main():
    backups, schedules, pitr = firebase_backup_status()
    lifecycle = r2_lifecycle_status()
    result = {
        "mode": "READ_ONLY_NO_USER_DATA",
        "firestore_backups": backups,
        "firestore_backup_schedules": schedules,
        "firestore_pitr": pitr,
        "r2_lifecycle": lifecycle,
        "note": "Existence of a Firestore backup does not verify restore or independent R2 backup.",
    }
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as out:
            out.write("## NgelX read-only backup inventory\n")
            out.write("- Firestore backup metadata: **" + backups["state"] + "**\n")
            out.write("- Firestore backup schedule metadata: **" + schedules["state"] + "**\n")
            out.write("- Firestore PITR metadata: **" + pitr["state"] + "**\n")
            out.write("- R2 lifecycle metadata: **" + lifecycle["state"] + "**\n")
            out.write("- This is not a backup restore test; no user data or objects were accessed.\n")
    return 0 if backups["state"] == "READY" and schedules["state"] == "READ" and lifecycle["state"] == "READ" else 2


if __name__ == "__main__":
    sys.exit(main())
