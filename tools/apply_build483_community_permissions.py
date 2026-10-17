#!/usr/bin/env python3
"""Build483: preserve every unrelated live Firestore rule.

Only add bounded community-avatar/legacy-founder management permissions after
Build456 moderation and Build469 founder guards have been applied. No live
Firebase mutation or user-data mutation takes place here.
"""
from pathlib import Path

MARK = "// Build483 legacy community management and avatar compatibility"
ANCHOR = "      allow delete: if false;\n      match /requests/{uid} {"

INSERT = """      // Build483 legacy community management and avatar compatibility.
      // Firestore remains authoritative: existing verified founder ID, current
      // membership and the already-approved admin list are the only roots of trust.
      // No client can modify a community founder ID, creation time or join code.
      allow update: if communitySigned450()
        && request.auth.uid in resource.data.get('members', [])
        && (
          request.auth.uid == resource.data.get('founderId', '')
          || (request.auth.uid in resource.data.get('admins', [])
              && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['photoUrl']))
        )
        && request.resource.data.diff(resource.data).affectedKeys().hasOnly([
          'photoUrl','members','admins','moderators','muted','banned','approvalMembers'
        ])
        && request.resource.data.get('photoUrl','') is string
        && request.resource.data.get('photoUrl','').size() <= 2048
        && request.resource.data.get('members',[]) is list
        && request.resource.data.get('members',[]).size() >= 1
        && request.resource.data.get('members',[]).size() <= 500
        && resource.data.get('founderId','') in request.resource.data.get('members',[])
        && request.resource.data.get('members',[]).toSet().size()
           == request.resource.data.get('members',[]).size()
        && request.resource.data.get('admins',[]) is list
        && request.resource.data.get('admins',[]).size() <= 10
        && request.resource.data.get('admins',[]).toSet().size()
           == request.resource.data.get('admins',[]).size()
        && request.resource.data.get('admins',[]).toSet()
          .difference(request.resource.data.get('members',[]).toSet()).size() == 0
        && request.resource.data.get('moderators',[]) is list
        && request.resource.data.get('moderators',[]).size() <= 30
        && request.resource.data.get('moderators',[]).toSet()
          .difference(request.resource.data.get('members',[]).toSet()).size() == 0
        && request.resource.data.get('moderators',[]).toSet()
          .intersection(request.resource.data.get('admins',[]).toSet()).size() == 0
        && request.resource.data.get('muted',[]) is list
        && request.resource.data.get('muted',[]).size() <= 500
        && request.resource.data.get('muted',[]).toSet()
          .difference(request.resource.data.get('members',[]).toSet()).size() == 0
        && request.resource.data.get('banned',[]) is list
        && request.resource.data.get('banned',[]).size() <= 500
        && request.resource.data.get('banned',[]).toSet()
          .intersection(request.resource.data.get('members',[]).toSet()).size() == 0
        && request.resource.data.get('approvalMembers',[]) is list
        && request.resource.data.get('approvalMembers',[]).size() <= 500;
"""

def transform(source: str) -> str:
    if MARK in source:
        return source
    start = source.index("    match /communities450/{cid} {")
    end = source.index("      match /requests/{uid} {", start)
    before, region, after = source[:start], source[start:end], source[end:]
    if region.count(ANCHOR) != 1:
        raise ValueError("Build483 refuses unexpected community root boundary")
    if "communityModerator456(cid)" not in source or "Build469:" not in region:
        raise ValueError("Build483 requires verified Build456/469 rule guards")
    # Copy and leave outside-community rules byte-identical.
    return before + region.replace(ANCHOR, INSERT + ANCHOR, 1) + after

def prepare_production_candidate(live: str) -> str:
    """Apply existing tested Build456 + Build469 first, then Build483."""
    if "Build450 communities" not in live or "Build457 legacy founder cover-only repair" not in live:
        raise ValueError("Unknown live rules; refuse to extend them")
    if "match /users/{uid}" not in live or "match /chats/{chatId}" not in live:
        raise ValueError("Existing user/chat rules missing; refuse to proceed")
    if "reactionVisible455" not in live:
        raise ValueError("Build455 comment/reaction rules not deployed as expected")
    from apply_build456_rules import transform as add456
    from apply_build469_founder_rules_qa import transform as add469
    newer = add456(live)
    if "Build469:" not in newer:
        newer = add469(newer)
    newer = transform(newer)
    for name in ("match /chats/{chatId}", "match /users/{uid}",
                 "match /communities450/{cid}", "communityModerator456",
                 "commentLimits456", MARK):
        if name not in newer:
            raise ValueError("Missing expected rules section: " + name)
    if "allow write: if true" in newer:
        raise ValueError("Unsafe unconditional write detected")
    return newer

if __name__ == "__main__":
    path = Path("firestore.rules")
    raw = path.read_text(encoding="utf-8")
    proposed = transform(raw)
    if proposed != raw:
        path.write_text(proposed, encoding="utf-8")
    print("Build483 emulator-only community permissions generated; NO LIVE DEPLOY")
