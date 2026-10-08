#!/usr/bin/env python3
"""Build 407 source safety regression: old users may NOT self-admit with an invite."""
from pathlib import Path
def rd(p):return Path(p).read_text(encoding="utf-8")
m=rd("app/lib/main.dart");r=rd("firestore.rules");t=rd("tools/firestore_rules_test.mjs");p=rd("app/pubspec.yaml")
g=m[m.index("class _GrubaKatilPageState extends State<GrubaKatilPage>"):m.index("\nclass ",m.index("class _GrubaKatilPageState extends State<GrubaKatilPage>")+9)]
j=r[r.index("match /joinRequests/{requestUid}"):r.index("match /group_archives")]
checks={
 "version 407":"version: 1.0.183+407" in p and "defaultValue: '407'" in m,
 "invite creates pending request":"'status':'pending'" in g and "Katılma isteğin kurucu veya yönetici onayına gönderildi" in g,
 "invite does not self-add":"await chat.update({" not in g and "'status':'autojoin'" not in g,
 "invite preserves expired/revoked check":"iv['revoked']==true" in g and "iv['active']==false" in g,
 "link requests list available to admin":"allow list: if isGroupAdmin(chatId)" in j,
 "join request client only pending":"request.resource.data.get('status', '') == 'pending'" in j,
 "link self-add prohibited":"validSelfJoin(chatId) ||" not in r and "function validSelfJoin(chatId) { return false; }" in r,
 "legacy reapply must still be pending":"resource.data.get('status', '') in ['autojoin', 'cancelled', 'rejected']" in j,
 "admin can accept/reject":"allow update: if isGroupAdmin(chatId)" in j,
 "emulator rejects autojoin":"await assertFails(setDoc(doc(bob, 'chats/group_open/joinRequests/bob')" in t,
 "emulator tests admin approval":"const approvedByAdmin=await assertSucceeds" in t,
 "new tabs preserve selection":"'followingTab': {'tr':'Çevrem'" in m and "'forYou': {'tr':'Radar'" in m,
 "feed video seek on drag no re-seek": "void _videoSarmayiGuncelle" in m and "await kontrol.seekTo(Duration(milliseconds:hedef));" in m,
 "toast actionable short":"duration:const Duration(seconds:3)" in m and "label:'Akışa git'" in m,
 "old audio/live/inbox intact": "live_broadcast_studio" in m and "gelenKutusuIsteginiSonuclandir" in m,
}
for n,ok in checks.items():print(("OK   " if ok else "FAIL ")+n,flush=True)
if not all(checks.values()):raise SystemExit("Build 407 check failed")
print("Build 407 source checks passed. Android device test still pending.",flush=True)
