#!/usr/bin/env python3
"""Build530: read-only structural checks for group exit protection."""
from pathlib import Path
leave=Path("app/lib/build517_group_leave.dart").read_text(encoding="utf-8")
join=Path("app/lib/build527_group_join_transaction.dart").read_text(encoding="utf-8")
policy=Path("server/livekit443/room-policy.mjs").read_text(encoding="utf-8")
tests=Path("server/livekit443/room-policy.test.mjs").read_text(encoding="utf-8")
assert "runTransaction<Map<String,dynamic>>" in leave
assert "data['callRoomName']!=roomName" in leave
assert "'callParticipants':FieldValue.arrayRemove([uid])" in leave
assert "'callExitedRoomName':roomName" in leave
assert "'callExitedUids':exits" in leave
assert "previousExitRoom==roomName" in leave
assert "FieldValue.arrayUnion([uid])" in leave
assert ":<String>[uid]" in leave
assert "runTransaction<bool>" in join
assert "data['callRoomName']!=roomName" in join
assert "data['callExitedRoomName']==roomName" in join
assert "List<String>.from(data['callExitedUids']??const <String>[])" in join
assert ".contains(uid))return false;" in join
assert "room.callExitedRoomName === currentRoom" in policy
assert "list(room.callExitedUids).includes(uid)) return null;" in policy
assert "room.callExitedRoomName === currentRoom" in policy.split("if (room.isGroup === true) {",1)[1]
assert "Build530: voluntary group exit blocks fresh token only for that call room" in tests
for forbidden in ("removeParticipant(", "deleteRoom(", "disconnect(", "DevelopmentTokenSource("):
    assert forbidden not in leave+join, forbidden
print("Build530 SOURCE PASS: atomic voluntary exit and same-room stale rejoin rejection")
print("Build530 SOURCE PASS: future group rooms remain eligible; no LiveKit admin call/deploy")
print("Build530 DEVICE GATE: manual rejoin policy and three-device call longevity require acceptance")
