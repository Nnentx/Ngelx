#!/usr/bin/env python3
"""Assert all Build 406 user-facing fixes and Firestore link scope, without fake E2E claims."""
from pathlib import Path
def rd(path):return Path(path).read_text(encoding="utf-8")
m=rd("app/lib/main.dart")
l=rd("app/lib/live_broadcast_studio.dart")
rules=rd("firestore.rules")
tests=rd("tools/firestore_rules_test.mjs")
pub=rd("app/pubspec.yaml")
s=m[m.index("class _GrubaKatilPageState extends State<GrubaKatilPage>"):m.index("\nclass ",m.index("class _GrubaKatilPageState extends State<GrubaKatilPage>")+10)]
owner=m[m.index("class _ProfilPageState extends State<ProfilPage>"):m.index("\nclass _ProfilEtkilesimRozeti")]
act=m[m.index("Widget _bildirimBasligi(Map<String,dynamic>"):m.index("\nclass AktiflikDurumuYazisi")]
privacy=m[m.index("class _TercihlerPageState extends State<TercihlerPage>"):m.index("\nclass ",m.index("class _TercihlerPageState extends State<TercihlerPage>")+10)]
checks={
"build 406 version":"version: 1.0.182+406" in pub and "defaultValue: '406'" in m,
"live summary label black":"Text(etiket,style:const TextStyle(color:Colors.black87" in l,
"live summary metric black":"Text(deger,style:const TextStyle(color:Colors.black87" in l,
"live summary persistent":"if(yayinBitti)Positioned.fill(child:_bitisEkrani())" in l,
"notifications recipient-independent sender profile":"collection('users').doc(fromUid).snapshots()" in act,
"notifications real name":"v['senderName']=name" in act and "v['photoUrl']=picture" in act,
"notifications fallback not made-up person":"sender.connectionState==ConnectionState.waiting?'Gönderen yükleniyor':'Kullanıcı'" in act,
"notifications request accept/reject preserved":"istegiSonuclandir(context,d,true)" in act and "istegiSonuclandir(context,d,false)" in act,
"invite current-code validation": "validInvite(code, chatId)" in rules and "'inviteCode':invite" in s,
"invite self membership without manual approval":"// The current invitation code authorizes direct admission." in s and "final onayGerekli" not in s,
"invite immediate update":"await chat.update({" in s and "'status':'autojoin'" in s,
"invite clear screen help":"Geçerli davet bağlantısı veya kodu ile yönetici onayı beklemeden katılabilirsin." in s,
"invite rule ban and max":"bannedMembers" in rules and "resource.data.get('maxMembers', 60)" in rules,
"invite rule no approval veto":"resource.data.get('joinApproval', false) != true" not in rules[rules.index("function validSelfJoin"):rules.index("function validMemberAddition")],
"invite security tests":"const joinedByLink=await assertSucceeds(getDoc" in tests and "await assertFails(updateDoc(doc(carol" in tests,
"profile intro refreshed by key":"ProfilTanitimVideoKarti(key:ValueKey<String>(tanitimVideoUrl),url:tanitimVideoUrl)" in owner,
"avatar/cover stable provider":"_sabitProfilResmi(" in owner and "_sabitProfilGorselleri" in owner,
"saved title no splitting":"maxLines:1,softWrap:false" in owner and "SizedBox(width:67" in owner,
"privacy effective rules explained":"Gizli hesap açık: yeni takipçiler onay bekler" in privacy,
"media cover background stable":"Video önizlemesi" in m and "NgelXVideoKapakOnizleme(url:url)" in m,
"saved actual content intact":"collection('saved')" in m,
"messaging and create untouched":"gelenKutusuIsteginiSonuclandir" in m and "_finalUretKart" in m,
"voice rooms retained":"audio_live_rooms" in rd("app/lib/main.dart") or Path("app/lib/audio_live_rooms.dart").exists(),
"no fake users":"admin-approved fake member" not in m,
}
for name,passed in checks.items():print(("OK  " if passed else "FAIL")+ "  "+name,flush=True)
if not all(checks.values()):raise SystemExit("Build 406 regression failure")
print("Build 406 source checks passed; real-device and two-account tests remain distinct.",flush=True)
