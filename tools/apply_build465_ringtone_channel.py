#!/usr/bin/env python3
"""Build465 audible incoming-call notification channel post Build454 patch.

Run after older Git patches, not against the checked-in Android service:
Build454 intentionally verifies the historical channel source exactly.
"""
from pathlib import Path

SERVICE=Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallService.kt")
OLD='const val CHANNEL = "ngelx_incoming_calls448"'
NEW='const val CHANNEL = "ngelx_incoming_calls465"'

def transform(src):
    if src.count(NEW)==1:return src
    if src.count(OLD)!=1:
        raise RuntimeError("Build465 ringtone: expected exactly one legacy channel")
    if "NotificationManager.IMPORTANCE_HIGH" not in src or "setSound(ringtone" not in src:
        raise RuntimeError("Build465 ringtone: source no longer has high priority audible notifications")
    return src.replace(OLD,NEW,1)

def main():
    before=SERVICE.read_text(encoding="utf-8")
    after=transform(before)
    if before!=after:SERVICE.write_text(after,encoding="utf-8")
    print("Build465: new high-priority ringtone channel applied after older Git patches")

if __name__=="__main__":main()
