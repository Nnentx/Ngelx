#!/usr/bin/env python3
"""Build483: preserve every unrelated live Firestore rule.

Only add bounded community-avatar/legacy-founder management permissions after
Build456 moderation and Build469 founder guards have been applied. No live
Firebase mutation or user-data mutation takes place here.
"""
from pathlib import Path

MARK = "// Build483 legacy community management and avatar compatibility"
ANCHOR = "      allow delete: if false;\n      match /requests/{uid} {"

INSERT = """      // Build483 legacy community management and avatar compatibility.\n      // Build483 legacy founder/admin photo-only patch. No role promotion.
      allow update: if communitySigned450()
        && request.auth.uid in resource.data.get('members', [])
        && (request.auth.uid == resource.data.get('founderId', '')
           || request.auth.uid in resource.data.get('admins', []))
        && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['photoUrl'])
        && request.resource.data.get('photoUrl', '') is string
        && request.resource.data.get('photoUrl', '').size() <= 2048;

      // Build483: legacy founder role permissions are independent from the
      // old validator requiring the founder to be listed in 'admins'.
      // Normal members and moderators never receive these extra rights.
      function communityLegacyRoles483() {
        let v = request.resource.data;
        let members = v.get('members', []);
        let admins = v.get('admins', []);
        let mods = v.get('moderators', []);
        let muted = v.get('muted', []);
        let banned = v.get('banned', []);
        let approval = v.get('approvalMembers', []);
        return members is list && members.size() >= 1 && members.size() <= 500
          && members.toSet().size() == members.size()
          && resource.data.get('founderId', '') in members
          && admins is list && admins.size() <= 10
          && admins.toSet().size() == admins.size()
          && admins.toSet().difference(members.toSet()).size() == 0
          && mods is list && mods.size() <= 30
          && mods.toSet().difference(members.toSet()).size() == 0
          && mods.toSet().intersection(admins.toSet()).size() == 0
          && muted is list && muted.size() <= 500
          && muted.toSet().difference(members.toSet()).size() == 0
          && banned is list && banned.size() <= 500
          && banned.toSet().intersection(members.toSet()).size() == 0
          && approval is list && approval.size() <= 500;
      }
      allow update: if communitySigned450()
        && request.auth.uid == resource.data.get('founderId', '')
        && request.auth.uid in resource.data.get('members', [])
        && request.resource.data.diff(resource.data).affectedKeys().hasOnly([
             'members','admins','moderators','muted','banned','approvalMembers'
           ])
        && communityLegacyRoles483();
"""

def transform(source: str) -> str:
    if MARK in source:
        return source
    start = source.index("    match /communities450/{cid} {")
    end = source.index("      match /requests/{uid} {", start) + len("      match /requests/{uid} {")
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
