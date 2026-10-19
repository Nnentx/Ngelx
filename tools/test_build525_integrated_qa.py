#!/usr/bin/env python3
"""Build525 combined source-contract QA after Build517/518/519/520/521/524.
This is a regression gate, not a substitute for multiple physical phones.
"""
from pathlib import Path

def require(source,fragment,description):
    assert fragment in source, f'Build525 missing {description}: {fragment}'

main=Path('app/lib/main.dart').read_text(encoding='utf-8')
live=Path('app/lib/live_broadcast_studio.dart').read_text(encoding='utf-8')
search=Path('app/lib/live_feed_card.dart').read_text(encoding='utf-8')
native=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt').read_text(encoding='utf-8')
manifest=Path('app/android/app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
policy=Path('server/livekit443/room-policy.mjs').read_text(encoding='utf-8')
adapter=Path('server/livekit443/firestore-adapters.mjs').read_text(encoding='utf-8')
workflow=Path('.github/workflows/NgelX-BUILD511-GIFTS-QA.yml').read_text(encoding='utf-8')

for term in ("part 'build517_group_leave.dart';","part 'build520_livekit_pip.dart';",
             "await ngelx517LeaveGroupCall(", "_voiceGroupCameraBusy517",
             "_enterPip520()async","lk.VideoTrackRenderer(primary"):
    require(main,term,'group and real LiveKit PiP')
for term in ("// Build521: stable gift request ID","// Build524: preserve draft",
             "_pendingGiftId521", "_pendingCommentId524",
             "if(yorum.text.trim()==metin)yorum.clear()",
             "if(_sendingComment524)return"):
    require(live,term,'virtual gifts and comments')
for term in ("// Build518: paginated all-active live search", "query.startAfterDocument(cursor)",
             "Future<void> _openActiveRoom518(String roomId)async"):
    require(search,term,'live discovery search')
for term in ("// Build519: prefer supported system or backported photo picker",
             "PickVisualMediaRequest.Builder()", "pipChannel520",
             "enterPictureInPictureMode(params)"):
    require(native,term,'Android gallery + PiP')
require(manifest,'android:supportsPictureInPicture="true"','Android PiP manifest')
for term in ("list(room.callKickedUids).includes(uid)",
             "room.guestCapacityAllowed!==false"):
    require(policy,term,'combined LiveKit policy')
for term in ("guestCapacityAllowed","limit(11).get()"):
    require(adapter,term,'server guest capacity admission')
require(workflow,"run: |\n          echo 'Build511 virtual gifting",'valid legacy gift CI YAML')

assert live.count("_pendingGiftSignature521;")==1
assert live.count("_pendingCommentSignature524;")==1
assert main.count("part 'build520_livekit_pip.dart';")==1
assert main.count("part 'build517_group_leave.dart';")==1
print('Build525 PASS: all 7 patch streams co-exist and guest kick/10-publish policy both present')
print('Build525 PHYSICAL DEVICES PENDING: 3-person group A/B/C, 10 guests, PiP/live track, gallery, gifts, comments')
