#!/usr/bin/env python3
"""Build 424: authoritative story owner; independent message delivery before preview."""
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
start=s.index('  Future<void> _yanitGonder(String ham,{bool tepki=false})async{',s.index('class _HikayeGosterPageState'))
end=s.index('\n  Widget _medya(){',start)
old=s[start:end]
for required in ("'type':'story_reply'","batch.update(chat","asama='mesaj'"):
    if required not in old:raise SystemExit('Build424 story source drift: '+required)
new=r'''  Future<void> _yanitGonder(String ham,{bool tepki=false})async{
    final ben=FirebaseAuth.instance.currentUser;
    final metin=ham.trim();
    if(ben==null||metin.isEmpty||gonderiliyor)return;
    setState(()=>gonderiliyor=true);
    _duraklat();
    String asama='hikaye';
    try{
      final db=FirebaseFirestore.instance;
      var hedef=widget.ownerUid.trim();
      // The story record, not a possibly stale UI avatar, determines who
      // receives this private response across account switches.
      if(widget.storyId.isNotEmpty){
        final story=await db.collection('videos').doc(widget.storyId)
          .get(const GetOptions(source:Source.server))
          .timeout(const Duration(seconds:10));
        if(!story.exists)throw StateError('Hikâye artık bulunamıyor.');
        final gercekSahip=(story.data()?['ownerId']??'').toString().trim();
        if(gercekSahip.isNotEmpty)hedef=gercekSahip;
      }
      if(hedef.isEmpty)throw StateError('Hikâye sahibine ulaşılamadı.');
      if(hedef==ben.uid)throw StateError('Kendi hikâyene mesaj gönderemezsin.');
      asama='gizlilik';
      final users=db.collection('users');
      final profiller=await Future.wait([
        users.doc(ben.uid).get(const GetOptions(source:Source.server))
          .timeout(const Duration(seconds:10)),
        users.doc(hedef).get(const GetOptions(source:Source.server))
          .timeout(const Duration(seconds:10)),
      ]);
      final benim=profiller[0].data()??<String,dynamic>{};
      final diger=profiller[1].data()??<String,dynamic>{};
      List<String> liste(dynamic raw)=>raw is Iterable
        ?raw.map((x)=>x.toString()).toList(growable:false):<String>[];
      if(!profiller[1].exists||diger['deactivated']==true){
        throw StateError('Hikâye sahibinin hesabına ulaşılamıyor.');
      }
      if(liste(benim['blocked']).contains(hedef)||
         liste(diger['blocked']).contains(ben.uid)||
         liste(diger['restrictedUsers']).contains(ben.uid)){
        throw StateError('Bu hesaba mesaj gönderme iznin yok.');
      }
      final chats=db.collection('chats');
      DocumentReference<Map<String,dynamic>>? sohbet;
      // Looking up old random-ID chats is optional: unavailable or denied
      // queries must not prevent a permitted deterministic DM creation.
      asama='sohbet-arama';
      try{
        final mevcut=await chats.where('members',arrayContains:ben.uid)
          .limit(200).get(const GetOptions(source:Source.server))
          .timeout(const Duration(seconds:9));
        for(final d in mevcut.docs){
          final v=d.data(),uyeler=liste(v['members']);
          if(v['isGroup']!=true&&uyeler.length==2&&
             uyeler.contains(ben.uid)&&uyeler.contains(hedef)){
            final reddedildi=v['requestRejected_'+hedef]==true;
            final onaylandi=v['requestAccepted_'+hedef]==true||
              v['requestAccepted_'+ben.uid]==true;
            final arkadas=liste(benim['friends']).contains(hedef)||
              liste(diger['friends']).contains(ben.uid);
            if(reddedildi&&!onaylandi&&!arkadas){
              throw StateError('Mesaj isteğin reddedildi. Yanıt gönderilemiyor.');
            }
            sohbet=d.reference;
            break;
          }
        }
      }on StateError{
        rethrow;
      }on FirebaseException catch(e){
        debugPrint('ngelx_story_reply_lookup: '+e.code);
      }on TimeoutException{
        debugPrint('ngelx_story_reply_lookup: timeout');
      }
      if(sohbet==null){
        asama='sohbet-olusturma';
        final arkadas=liste(benim['friends']).contains(hedef)||
          liste(diger['friends']).contains(ben.uid);
        final izin=(diger['messagePermission']??
          (diger['friendsOnlyMessages']==true?'friends':'all')).toString();
        final takipIzin=liste(diger['following']).contains(ben.uid);
        if(!(izin=='all'||(izin=='friends'&&arkadas)||
          (izin=='following'&&takipIzin))){
          throw StateError('Hikâye sahibi yeni mesaj isteği kabul etmiyor.');
        }
        final ids=<String>[ben.uid,hedef]..sort();
        final belge=<String,dynamic>{
          'members':ids,'isGroup':false,
          'peerA':ids.first,'peerB':ids.last,
          if(arkadas)'requestAccepted_'+ben.uid:true,
          if(arkadas)'requestAccepted_'+hedef:true,
          if(!arkadas)'requestSenderUid':ben.uid,
          if(!arkadas)'requestRecipientUid':hedef,
          if(!arkadas)'requestRejected_'+hedef:false,
          'updatedAt':FieldValue.serverTimestamp(),
        };
        try{
          final sabit=chats.doc(ids.join('_'));
          await sabit.set(belge,SetOptions(merge:true))
            .timeout(const Duration(seconds:12));
          sohbet=sabit;
        }on FirebaseException catch(e){
          if(e.code!='permission-denied'&&e.code!='failed-precondition')rethrow;
          final yeni=chats.doc();
          await yeni.set(belge).timeout(const Duration(seconds:12));
          sohbet=yeni;
        }
      }

      // Core reply is committed BEFORE the non-essential chat preview.
      // A bad metadata write must no longer roll back the message.
      asama='mesaj-gonderimi';
      final chat=sohbet!;
      await chat.collection('messages').doc().set({
        'senderId':ben.uid,'text':metin,'type':'story_reply',
        'storyId':widget.storyId,'storyUrl':widget.url,
        'storyOwnerId':hedef,'storyMediaType':widget.mediaType,
        'reaction':tepki,'createdAt':FieldValue.serverTimestamp(),
        'clientCreatedAt':Timestamp.now(),
      }).timeout(const Duration(seconds:15));

      asama='sohbet-onizleme';
      try{
        await chat.update({
          'lastMessage':tepki?'$metin Hikâye tepkisi':'↩ Hikâye yanıtı: $metin',
          'lastSenderId':ben.uid,
          'updatedAt':FieldValue.serverTimestamp(),
          'unread_$hedef':FieldValue.increment(1),
        }).timeout(const Duration(seconds:8));
      }catch(e){
        debugPrint('ngelx_story_reply_preview: '+e.runtimeType.toString());
      }
      unawaited(uygulamaBildirimiGonder(
        toUid:hedef,fromUid:ben.uid,tur:'message',
        metin:tepki?'Hikâyene tepki verdi':'Hikâyene yanıt verdi',
        belgeId:chat.id,
      ).catchError((_){ }));
      cevap.clear();
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:Text(tepki?'Tepkin gönderildi.':'Yanıtın gönderildi.')));
    }on StateError catch(e){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:Text(e.message.toString())));
    }on FirebaseException catch(e){
      debugPrint('ngelx_story_reply: '+asama+' / '+e.code);
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:Text('Hikâye yanıtı: '+asama+' ('+e.code+').')));
    }on TimeoutException{
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:Text('Hikâye yanıtı zaman aşımı: '+asama+'.')));
    }catch(e){
      debugPrint('ngelx_story_reply: '+asama+' / '+e.runtimeType.toString());
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:Text('Hikâye yanıtı tamamlanamadı ('+asama+').')));
    }finally{
      if(mounted){setState(()=>gonderiliyor=false);_devam();}
    }
  }
'''
s=s[:start]+new+s[end:]
p.write_text(s,encoding='utf-8')
p=Path('app/lib/main.dart');s=p.read_text(encoding='utf-8')
for a,b in [("defaultValue: '423'","defaultValue: '424'"),
            ("defaultValue: '1.0.198'","defaultValue: '1.0.199'")]:
    if s.count(a)!=1:raise SystemExit('Build424 version drift: '+a)
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml');s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.198+423')!=1:
    raise SystemExit('Build424 pubspec drift')
p.write_text(s.replace('version: 1.0.198+423','version: 1.0.199+424',1),encoding='utf-8')
print('Build424: story owner verified, message delivered before chat preview, explicit failure stage.')
