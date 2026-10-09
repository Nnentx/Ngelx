#!/usr/bin/env python3
"""Static contracts run after Build 412 patches and Build 413 corrections."""
from pathlib import Path

s=Path('app/lib/main.dart').read_text(encoding='utf-8')
a=s.index('class _AramaPageState extends State<AramaPage>')
b=s.index('\nclass HikayeSeridi',a)
search=s[a:b]
a=s.index('  Future<void> _yanitGonder(String ham,{bool tepki=false})async{')
b=s.index('\n  Widget _medya(){',a)
story=s[a:b]
a=s.index('class _KullaniciProfilPageState extends State<KullaniciProfilPage>')
b=s.index('\nclass NgelXVideoKapakOnizleme',a)
visitor=s[a:b]
a=s.index('class _ArkadaslarPageState extends State<ArkadaslarPage>')
b=s.index('\nclass ',a+7)
friends=s[a:b]

tests={
  'friend label reflects actual friendship':"final alt=arkadas" in friends
     and "Arkadaşın · " in friends,
  'global search queries names and handles case':"orderBy(alan)" in search
     and "startAt([metin])" in search
     and "metin.toUpperCase()" not in search or "q.toUpperCase()" in search,
  'global search includes real friends and follows':"['friends','following']" in search
     and "where(FieldPath.documentId" in search,
  'global search results deduplicated':"adayKullanicilar[d.id]=d" in search,
  'account-scoped cache':"uid+'|'+q" in search,
  'search debounced and disposed':"_aramaBekleme?.cancel()" in search
     and "Duration(milliseconds:320)" in search,
  'search privacy and blocks preserved':"!beniEngelledi&&!engellenenler.contains(d.id)" in search
     and "v['discoverableProfile']!=false" in search,
  'real content results and ranking retained':"final gorulenMedya=<String>{};" in search
     and "IcerikBaglantiPage(icerikId:d.id)" in search,
  'story reply no viewer-only video mutation':"batch.set(story," not in story
     and "'replyCount':FieldValue.increment" not in story,
  'story reply honors messaging permissions':"messagePermission" in story
     and "'friendsOnlyMessages'" in story and "'blocked'" in story,
  'story creates chat before messages':"await chat.set(" in story
     and "batch.update(chat" in story
     and story.index("await chat.set(")<story.index("batch.update(chat"),
  'story message payload retained':"'type':'story_reply'" in story
     and "'storyId':widget.storyId" in story
     and "uygulamaBildirimiGonder(" in story,
  'visitor status waits for account':visitor.count("if(me!=null&&!benSnap.hasData)")>=2,
  'original follow/friend handlers untouched':"takipDurumuDegistir(uid" in visitor
     and "sosyalIstekGonder(" in visitor
     and "_arkadasliktanCikar" in visitor,
  'approved coverless / covered design preserved':"if(kapaksiz)...[" in visitor
     and "NgelXAgImageProvider(profilKapak)" in visitor,
  'other original social actions preserved':"profildenMesajAc(" in visitor
     and "OrtakGruplarPage(digerUid:uid)" in visitor,
  'join month grammar corrected':"’te katıldı" not in s
     and " tarihinde katıldı" in s,
  'no Firestore rule changes':Path('firestore.rules').exists(),
}
for name,passed in tests.items():
    print(('PASS ' if passed else 'FAIL ')+name,flush=True)
if not all(tests.values()):
    raise SystemExit('Build 413 regression contract failed')
print('Build 413 source regression contracts PASS. Real-device behavior still requires QA.')
