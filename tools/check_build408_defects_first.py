#!/usr/bin/env python3
"""Build 408 source guard: defects before design, no data migration."""
from pathlib import Path
m=Path("app/lib/main.dart").read_text(encoding="utf-8")
p=Path("app/pubspec.yaml").read_text(encoding="utf-8")
r=Path("firestore.rules").read_text(encoding="utf-8")
a=m.index("class _KullaniciProfilPageState extends State<KullaniciProfilPage>")
b=m.index("class NgelXVideoKapakOnizleme",a)
u=m[a:b]
a=m.index("class _GrupSohbetPageState extends State<GrupSohbetPage>")
b=m.index("\nclass ",a+15)
g=m[a:b]
tests={
"build number":"version: 1.0.184+408" in p and "defaultValue: '408'" in m,
"live profile uses authoritative session":"collection('live_streams').doc(canliId).snapshots()" in u,
"live flag requires session document":"ngelxCanliKaydiTaze(yayinSnap.data!.data()" in u,
"stale isLive alone does not draw badge":"final canli=v['isLive']" not in u and "if(canli)Positioned" in u,
"owner stats/actions preserved":"'Arkadaşsınız'" in u and "'Ortak gruplar'" in u,
"group block dialog acknowledged per group and membership":"ngelx_group_block_dialog_" in g and "prefs.getString(anahtar)==imza" in g,
"block guard preserved":"_engellenenGrupUyeleri" in g and "Engellediğin kişilerin mesajları gizli" in g,
"group cancel still navigates back":"if(!gir&&mounted)Navigator.maybePop(context)" in g,
"group approval message reflects server request status":"adlı kullanıcının" in m and "joinRequests').doc(memberId).snapshots()" in m,
"all prior Build 407 inbox pathways remain":"bildirimGonderenIle" in m and "group_join_request" in m,
"permissions not weakened":"function validSelfJoin(chatId) { return false; }" in r,
"layout redesign not mixed into defect batch":"profileViewMode" not in u,
}
for name,ok in tests.items():print(("PASS " if ok else "FAIL ")+name,flush=True)
if not all(tests.values()):raise SystemExit("Build 408 source guard failed")
print("Build 408 critical bug source checks passed (device verification pending).",flush=True)
