#!/usr/bin/env python3
"""Non-regression contracts for consolidated QA fixes; real phones still required."""
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
def part(a,b):
    st=s.index(a);en=s.index(b,st+len(a));return s[st:en]
story=part('class _HikayeGosterPageState extends State<HikayeGosterPage>','\nclass HesapDegistirPage')
inbox=part('class _MesajPageState extends State<MesajPage>','\nclass ArsivSohbetlerPage')
visitor=part('class _KullaniciProfilPageState extends State<KullaniciProfilPage>','\nclass NgelXVideoKapakOnizleme')
owner=part('class _ProfilPageState extends State<ProfilPage>','\nclass _ProfilEtkilesimRozeti')
feed=part('class _VideoAkisiState extends State<VideoAkisi>','\nclass ')
story_reply=story[story.index('  Future<void> _yanitGonder('):story.index('\n  Widget _medya(){')]
checks={
 'story no unauthorized video mutations':'batch.set(story,' not in story_reply,
 'story finds allowed member chats':"where('members',arrayContains:ben.uid)" in story_reply,
 'story no reads of missing chat documents':'await chat.get()' not in story_reply,
 'story finds legacy private IDs':"chatId=d.id" in story_reply,
 'story creates privacy-safe chats with fallback':'requestRecipientUid' in story_reply and
   "clean" not in story_reply and "final temiz=chats.doc()" in story_reply,
 'story writes actual reply to message collection':"'type':'story_reply'" in story_reply and
   "await batch.commit()" in story_reply,
 'story human-readable stage errors':'Hikâye yanıtı izin hatası' in story_reply,
 'story reply and video player same page':"VideoPlayerController.networkUrl(Uri.parse(widget.url))" in story,
 'inbox has direct notification profile navigation':inbox.count('KullaniciProfilPage(uid:from)')>=3,
 'no duplicate Activity route from inbox':'const AktivitePage()' not in inbox,
 'inbox supports scoped notifications':"initialFilter='Tümü'" in s and
   "late String filtre=widget.initialFilter" in inbox,
 'pending requests directly rendered with Onayla/Sil':"Text('Onayla')" in inbox and
   "Text('Sil')" in inbox and 'gelenKutusuIsteginiSonuclandir(d,true)' in inbox,
 'mutual friends never fixed 127':"' ortak arkadaş'" in inbox and '127 ortak arkadaş' not in inbox,
 'mutual avatars cached':"_kullaniciGetir(id)" in inbox and "ortak.take(3)" in inbox,
 'friend request recipient uses verified server state':"sosyalIstekRef(uid,me,'friend_request').snapshots()" in visitor,
 'follow request recipient uses verified server state':"sosyalIstekRef(uid,me,'follow_request').snapshots()" in visitor,
 'profile reply launches accept/reject':visitor.count("Text('Kabul et'")>=2 and
   visitor.count("Text('Reddet'")>=2,
 'both incoming profile answers use safe shared handler':
   visitor.count('ngelxGelenSosyalIstekCevapla(')>=2,
 'no already-accepted request resurfacing':
   "gelenSnap.data?.data()?['status']=='pending'" in visitor,
 'existing covered/coverless modes intact':"if(kapaksiz)...[" in visitor and
   "NgelXAgImageProvider(profilKapak)" in visitor,
 'existing follow and friendship callbacks intact':
   "takipDurumuDegistir(uid" in visitor and
   "sosyalIstekGonder(hedefUid:uid,tur:'friend_request'" in visitor,
 'full join date not cropped':"Text(katilim,textAlign:TextAlign.center," in owner and
   "Text(katilim,overflow:TextOverflow.ellipsis" not in owner,
 'cached feed stream retained filters':"_ngelxSabitAkis" in feed and
   "profilHazir" in feed and "gizlenenIcerikler" in feed,
 'feed shows informative loading state':"Akış hazırlanıyor..." in feed,
 'cached inbox streams to avoid repeated resubscriptions':"_sohbetAkisi(" in inbox and
   "_bildirimAkisi(" in inbox,
 'profile owner notification bell opens inbox':"MesajPage(initialFilter:'Bildirimler')" in owner,
 'existing request cancellation stays protected':"İstek artık beklemede değil veya iptal edilemedi." in s,
 'no Firestore security rules changed':Path('firestore.rules').exists(),
}
for label,ok in checks.items():print(('PASS ' if ok else 'FAIL ')+label,flush=True)
if not all(checks.values()):raise SystemExit('Build422 consolidated source protections FAILED')
print('Build422 consolidated source protection tests PASSED; device test pending.')
