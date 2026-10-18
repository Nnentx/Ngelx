#!/usr/bin/env python3
"""Build497 guest join UI regression without changing permissions/transitions."""
from pathlib import Path
src=Path("app/lib/build448_live_guests.dart").read_text(encoding="utf-8")
assert src.count("Future<void> _viewerJoinPanel497(")==1
for expected in (
 "class Ngelx448GuestControls extends StatelessWidget",
 "showModalBottomSheet<void>(",
 "isScrollControlled:true,useSafeArea:true,showDragHandle:true",
 "Yayıncı onayladığında",
 "Daveti kabul et",
 "Daveti reddet",
 "Katılma isteği gönder",
 "İsteği iptal et",
 "Yayından ayrıl",
 "Navigator.of(sheetContext).pop()",
 "unawaited(ngelx448GuestAction(context,liveId,ownerUid,uid,mainAction))",
 "onPressed:()=>_viewerJoinPanel497(context,uid,'invited')",
 "onPressed:()=>_viewerJoinPanel497(context,uid,status is String ? status : null)",
 "stream:ngelx448GuestRef(liveId,uid).snapshots()",
 "if(host)return FilledButton.icon",
 ".collection('guest_requests').snapshots()",
 "if(status=='pending')IconButton",
 "if(status=='pending'||status=='invited')IconButton",
 "if(status=='accepted')const Tooltip",
 "MediaQuery.sizeOf(c).height*.48",
):assert expected in src,expected
# Build503: only pending/invited are rejected through client transactions.
# Accepted guest removal MUST use the server-admin live card menu.
assert "Konuk bağlantısını sonlandır" not in src
assert "if(status=='pending'||status=='invited')IconButton" in src
assert "if(status=='accepted')const Tooltip" in src
# Distinguish host-only collection enumeration from viewer-only doc subscription.
host_start=src.index("  Future<void> _panel(BuildContext context)async{")
viewer_start=src.index("  Future<void> _viewerJoinPanel497(",host_start)
build_start=src.index("  @override Widget build(BuildContext context)",viewer_start)
assert ".collection('guest_requests').snapshots()" in src[host_start:viewer_start]
assert ".collection('guest_requests').snapshots()" not in src[viewer_start:]
assert "if(host)return FilledButton.icon" in src[build_start:]
# All actual state mutations keep the pre-existing Firebase transaction guards.
for expected in (
 "me==guest)next='pending'",
 "status=='pending'&&me==owner",
 "status=='invited'&&me==guest",
 "me==owner||me==guest",
 "v['active']!=true||v['ownerId']!=owner||guest==owner",
): assert expected in src,expected
# Only the invited/requesting GUEST needs device permissions. A host who
# approves a pending guest must not be blocked by local camera/microphone.
assert "if(me==guest&&(action=='request'||action=='accept')){" in src
assert "if(action=='request'||action=='accept'){" not in src
print("Build497: guest-only permission prompt and host approval guard PASS")
print("Build497: compact role-safe join panel; unchanged Firestore transition checks PASS")
