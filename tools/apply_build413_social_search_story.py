#!/usr/bin/env python3
"""Build 413: minimal fixes on top of the fully generated Build 412 Flutter file.

Preserve the approved cover/coverless profile, actions, navigation, privacy and
Firestore rules. Fail closed when an expected anchor changes.
"""
from pathlib import Path

p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')

def one(old,new,label):
    global s
    hits=s.count(old)
    if hits!=1:
        raise SystemExit(f'Build 413 {label}: expected one anchor, found {hits}')
    s=s.replace(old,new,1)

# Friend list: show actual relationship before mutual-friend information.
one("""      final alt=ortak>0
        ? ortak.toString()+' ortak arkadaş'
        : (arkadas?'Arkadaşın':(takipte?'Takip ediyorsun':'NgelX’te keşfet'));""",
"""      final alt=arkadas
        ? (ortak>0?'Arkadaşın · '+ortak.toString()+' ortak arkadaş':'Arkadaşın')
        : (ortak>0?ortak.toString()+' ortak arkadaş'
          :(takipte?'Takip ediyorsun':'NgelX’te keşfet'));""",
"friend list relationship label")

# The month name in "Eylül 2026’te katıldı" cannot take a fixed suffix.
if "’te katıldı" not in s:
    raise SystemExit('Build 413 join-date grammar anchor missing')
s=s.replace("’te katıldı", " tarihinde katıldı")

# Visitor controls should not claim no follow/friend relationship while the
# current account's relationship document is still loading.
one("""                    builder:(_,benSnap){
                      final benimTakipEttiklerim=List<String>.from(benSnap.data?.data()?['following']??const[]);""",
"""                    builder:(_,benSnap){
                      if(me!=null&&!benSnap.hasData){
                        return const SizedBox(height:46,child:Center(
                          child:CircularProgressIndicator(strokeWidth:2,color:mor)));
                      }
                      final benimTakipEttiklerim=List<String>.from(benSnap.data?.data()?['following']??const[]);""",
"follow loading state")
one("""                  builder:(_,benSnap){
                    final benimArkadaslarim=List<String>.from(benSnap.data?.data()?['friends']??const[]);""",
"""                  builder:(_,benSnap){
                    if(me!=null&&!benSnap.hasData){
                      return const SizedBox(height:46,child:Center(
                        child:CircularProgressIndicator(strokeWidth:2,color:mor)));
                    }
                    final benimArkadaslarim=List<String>.from(benSnap.data?.data()?['friends']??const[]);""",
"friend loading state")

# Global search previously searched just 60 arbitrary users. Search server
# prefixes, and explicitly include real friends/following, without widening
# Firestore permissions or bypassing discoverability and block filters.
a=s.index('class _AramaPageState extends State<AramaPage>')
b=s.index('\nclass HikayeSeridi',a)
v=s[a:b]
old="""  Future<List<QuerySnapshot<Map<String,dynamic>>>>? _aramaVerisi;

  Future<List<QuerySnapshot<Map<String,dynamic>>>> _aramaVerisiniHazirla(){
    // Trafik tasarrufu: her harfte 60 kullanici + 100 icerigi yeniden indirme.
    return _aramaVerisi??=Future.wait([
      FirebaseFirestore.instance.collection('users').limit(60).get(),
      FirebaseFirestore.instance.collection('videos').limit(100).get(),
    ]);
  }
"""
new=r"""  Future<List<QuerySnapshot<Map<String,dynamic>>>>? _aramaVerisi;
  String _aramaOnbellekAnahtari='';
  String arananSorgu='';
  Timer? _aramaBekleme;

  Future<List<QuerySnapshot<Map<String,dynamic>>>> _aramaVerisiniHazirla(){
    final uid=FirebaseAuth.instance.currentUser?.uid??'';
    final q=arananSorgu.trim().toLowerCase();
    final anahtar=uid+'|'+q;
    if(_aramaVerisi!=null&&_aramaOnbellekAnahtari==anahtar)return _aramaVerisi!;
    _aramaOnbellekAnahtari=anahtar;
    return _aramaVerisi=()async{
      final db=FirebaseFirestore.instance;
      final users=db.collection('users');
      final sorgular=<Future<QuerySnapshot<Map<String,dynamic>>>>[
        users.limit(60).get(),
        db.collection('videos').limit(100).get(),
      ];
      // Standard single-field Firestore range searches; retain the existing
      // client-side blocked/discoverable/deactivated safeguards below.
      if(q.length>=2){
        final bicimler=<String>{
          q,
          q[0].toUpperCase()+q.substring(1),
          q.toUpperCase(),
        };
        for(final metin in bicimler){
          for(final alan in <String>['displayName','username']){
            sorgular.add(users.orderBy(alan)
              .startAt([metin]).endAt([metin+'\uf8ff']).limit(35).get());
          }
        }
      }
      if(uid.isNotEmpty){
        try{
          final belge=await users.doc(uid).get();
          final veri=belge.data()??<String,dynamic>{};
          final ids=<String>{};
          for(final key in <String>['friends','following']){
            final raw=veri[key];
            if(raw is Iterable){
              for(final value in raw){
                final id=value.toString();
                if(id.isNotEmpty&&id!=uid)ids.add(id);
                if(ids.length>=120)break;
              }
            }
            if(ids.length>=120)break;
          }
          final liste=ids.toList();
          for(var i=0;i<liste.length;i+=30){
            final son=(i+30<liste.length)?i+30:liste.length;
            sorgular.add(users.where(FieldPath.documentId,
              whereIn:liste.sublist(i,son)).get());
          }
        }catch(_){
          // Optional relationship enrichment must not break all search results.
        }
      }
      return Future.wait(sorgular);
    }();
  }
"""
if v.count(old)!=1:
    raise SystemExit(f'Build 413 global search source anchor drift: {v.count(old)}')
v=v.replace(old,new,1)
old="""  void _sorguDegisti(String v){
    final yeni=v.trim().toLowerCase();
    if(yeni.isNotEmpty)unawaited(_aramaVerisiniHazirla());
    setState(()=>sorgu=yeni);
  }
"""
new="""  void _sorguDegisti(String v){
    final yeni=v.trim().toLowerCase();
    _aramaBekleme?.cancel();
    if(yeni.isEmpty){
      setState((){sorgu='';arananSorgu='';});
      return;
    }
    setState(()=>sorgu=yeni);
    _aramaBekleme=Timer(const Duration(milliseconds:320),(){
      if(mounted)setState(()=>arananSorgu=yeni);
    });
  }
"""
if v.count(old)!=1:raise SystemExit('Build 413 debounce anchor drift')
v=v.replace(old,new,1)
old="""      sorgu=ilk.toLowerCase();
      unawaited(_aramaVerisiniHazirla());"""
new="""      sorgu=ilk.toLowerCase();
      arananSorgu=sorgu;"""
if v.count(old)!=1:raise SystemExit('Build 413 initial search anchor drift')
v=v.replace(old,new,1)
old="  void dispose() { ara.dispose(); super.dispose(); }"
new="  void dispose() { _aramaBekleme?.cancel(); ara.dispose(); super.dispose(); }"
if v.count(old)!=1:raise SystemExit('Build 413 search disposal anchor drift')
v=v.replace(old,new,1)
old="onPressed: () { ara.clear(); setState(() => sorgu = ''); }"
new="onPressed: () { ara.clear(); _sorguDegisti(''); }"
if v.count(old)!=1:raise SystemExit('Build 413 clear search anchor drift')
v=v.replace(old,new,1)
old="          : FutureBuilder<List<QuerySnapshot<Map<String, dynamic>>>>("
new="""          : arananSorgu!=sorgu
            ? const Center(child:CircularProgressIndicator(color:mor))
            : FutureBuilder<List<QuerySnapshot<Map<String, dynamic>>>>("""
if v.count(old)!=1:raise SystemExit('Build 413 search loading anchor drift')
v=v.replace(old,new,1)
old="                final kullanicilar = snap.data![0].docs.where((d) {"
new="""                final adayKullanicilar=<String,QueryDocumentSnapshot<Map<String,dynamic>>>{};
                for(var i=0;i<snap.data!.length;i++){
                  if(i==1)continue; // videos occupy the second query
                  for(final d in snap.data![i].docs){adayKullanicilar[d.id]=d;}
                }
                final kullanicilar = adayKullanicilar.values.where((d) {"""
if v.count(old)!=1:raise SystemExit('Build 413 search results anchor drift')
v=v.replace(old,new,1)
s=s[:a]+v+s[b:]

# Story replies: a viewer is not authorized to mutate the story owner's
# replyCount/reactionCount. Doing so atomically rolled back the whole message.
# Create the private chat first (respecting message privacy and blocks), then
# atomically write chat metadata and message; no unauthorized story write.
a=s.index('  Future<void> _yanitGonder(String ham,{bool tepki=false})async{')
b=s.index('\n  Widget _medya(){',a)
old=s[a:b]
new="""  Future<void> _yanitGonder(String ham,{bool tepki=false})async{
    final ben=FirebaseAuth.instance.currentUser;
    final hedef=widget.ownerUid.trim();
    final metin=ham.trim();
    if(ben==null||metin.isEmpty||gonderiliyor)return;
    if(hedef.isEmpty||hedef==ben.uid){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Bu hikâyeye yanıt gönderilemiyor.')));
      return;
    }
    setState(()=>gonderiliyor=true);
    _duraklat();
    try{
      final db=FirebaseFirestore.instance;
      final ids=<String>[ben.uid,hedef]..sort();
      final chatId=ids.join('_');
      final chat=db.collection('chats').doc(chatId);
      final belge=await chat.get().timeout(const Duration(seconds:8));
      if(!belge.exists){
        final belgeler=await Future.wait([
          db.collection('users').doc(ben.uid).get(),
          db.collection('users').doc(hedef).get(),
        ]);
        final benim=belgeler[0].data()??<String,dynamic>{};
        final diger=belgeler[1].data()??<String,dynamic>{};
        List<String> liste(dynamic v)=>v is Iterable
          ?v.map((x)=>x.toString()).toList():<String>[];
        if(diger['deactivated']==true||
            liste(benim['blocked']).contains(hedef)||
            liste(diger['blocked']).contains(ben.uid)||
            liste(diger['restrictedUsers']).contains(ben.uid)){
          throw StateError('Bu kişiyle mesajlaşmaya izin verilmiyor.');
        }
        final arkadas=liste(benim['friends']).contains(hedef)||
          liste(diger['friends']).contains(ben.uid);
        final izin=(diger['messagePermission']??
          (diger['friendsOnlyMessages']==true?'friends':'all')).toString();
        final takipci=liste(diger['following']).contains(ben.uid);
        if(!(izin=='all'||(izin=='friends'&&arkadas)||
          (izin=='following'&&takipci))){
          throw StateError('Bu kişi mesaj gizliliği nedeniyle yeni sohbet kabul etmiyor.');
        }
        await chat.set({
          'members':ids,'isGroup':false,'peerA':ids.first,'peerB':ids.last,
          if(arkadas)'requestAccepted_'+ben.uid:true,
          if(arkadas)'requestAccepted_'+hedef:true,
          if(!arkadas)'requestSenderUid':ben.uid,
          if(!arkadas)'requestRecipientUid':hedef,
          if(!arkadas)'requestRejected_'+hedef:false,
          'updatedAt':FieldValue.serverTimestamp(),
        }).timeout(const Duration(seconds:10));
      }else{
        final bilgi=belge.data()??<String,dynamic>{};
        final uyeler=List<String>.from(bilgi['members']??const[]);
        if(bilgi['isGroup']==true||uyeler.length!=2||
          !uyeler.contains(ben.uid)||!uyeler.contains(hedef)){
          throw StateError('Özel sohbet açılamadı.');
        }
      }
      final mesajRef=chat.collection('messages').doc();
      final batch=db.batch();
      batch.update(chat,{
        'lastMessage':tepki?'$metin Hikâye tepkisi':'↩ Hikâye yanıtı: $metin',
        'lastSenderId':ben.uid,
        'updatedAt':FieldValue.serverTimestamp(),
        'unread_$hedef':FieldValue.increment(1),
      });
      batch.set(mesajRef,{
        'senderId':ben.uid,'text':metin,'type':'story_reply',
        'storyId':widget.storyId,'storyUrl':widget.url,
        'storyOwnerId':hedef,'storyMediaType':widget.mediaType,
        'reaction':tepki,'createdAt':FieldValue.serverTimestamp(),
        'clientCreatedAt':Timestamp.now(),
      });
      await batch.commit().timeout(const Duration(seconds:12));
      unawaited(uygulamaBildirimiGonder(
        toUid:hedef,fromUid:ben.uid,tur:'message',
        metin:tepki?'$metin hikâyene tepki verdi':'Hikâyene yanıt verdi',
        belgeId:chatId,
      ).catchError((_){ }));
      cevap.clear();
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content:Text(tepki?'Tepkin gönderildi.':'Yanıtın gönderildi.')));
    }catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content:Text(e is StateError?e.message.toString():
          'Hikâye yanıtı gönderilemedi. Bağlantını ve mesaj izinlerini kontrol et.')));
    }finally{
      if(mounted){setState(()=>gonderiliyor=false);_devam();}
    }
  }
"""
if old.count("batch.set(story,")!=1:
    raise SystemExit('Build 413 story reply contract drift')
s=s[:a]+new+s[b:]

p.write_text(s,encoding='utf-8')
print('Build 413 safe social/search/story fixes applied; Firestore rules unchanged.')
