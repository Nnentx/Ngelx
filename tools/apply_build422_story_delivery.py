#!/usr/bin/env python3
"""Build 422: safe DM creation and delivery for story replies. Firestore rules unchanged."""
from pathlib import Path
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
a=s.index('  Future<void> _yanitGonder(String ham,{bool tepki=false})async{',s.index('class _HikayeGosterPageState'))
b=s.index('\n  Widget _medya(){',a)
old=s[a:b]
for key in ('await chat.get()', "'type':'story_reply'", 'batch.update(chat'):
    if key not in old:raise SystemExit('Build422 story source drift: '+key)
new="""  Future<void> _yanitGonder(String ham,{bool tepki=false})async{
    final ben=FirebaseAuth.instance.currentUser;
    final hedef=widget.ownerUid.trim();
    final metin=ham.trim();
    if(ben==null||hedef.isEmpty||hedef==ben.uid||metin.isEmpty||gonderiliyor)return;
    setState(()=>gonderiliyor=true);
    _duraklat();
    String asama='profil';
    try{
      final db=FirebaseFirestore.instance;
      final profiller=await Future.wait([
        db.collection('users').doc(ben.uid).get().timeout(const Duration(seconds:8)),
        db.collection('users').doc(hedef).get().timeout(const Duration(seconds:8)),
      ]);
      final benim=profiller[0].data()??<String,dynamic>{};
      final diger=profiller[1].data()??<String,dynamic>{};
      List<String> liste(dynamic raw)=>raw is Iterable
        ?raw.map((x)=>x.toString()).toList(growable:false):<String>[];
      if(!profiller[1].exists||diger['deactivated']==true){
        throw StateError('Hikâye sahibi hesabına ulaşılamıyor.');
      }
      if(liste(benim['blocked']).contains(hedef)||
          liste(diger['blocked']).contains(ben.uid)||
          liste(diger['restrictedUsers']).contains(ben.uid)){
        throw StateError('Bu kullanıcıya mesaj gönderme iznin yok.');
      }
      asama='sohbet-arama';
      final chats=db.collection('chats');
      String chatId='';
      // A missing chat document cannot be read by a non-member. Query ONLY
      // existing chats where current user is a member, like Profile -> Mesaj.
      final mevcut=await chats.where('members',arrayContains:ben.uid)
        .limit(200).get().timeout(const Duration(seconds:8));
      for(final d in mevcut.docs){
        final v=d.data(),uyeler=liste(v['members']);
        if(v['isGroup']!=true&&uyeler.length==2&&
            uyeler.contains(ben.uid)&&uyeler.contains(hedef)){
          chatId=d.id;break;
        }
      }
      if(chatId.isEmpty){
        asama='sohbet-olusturma';
        final arkadas=liste(benim['friends']).contains(hedef)||
          liste(diger['friends']).contains(ben.uid);
        final izin=(diger['messagePermission']??
          (diger['friendsOnlyMessages']==true?'friends':'all')).toString();
        final takipEdiyor=liste(diger['following']).contains(ben.uid);
        if(!(izin=='all'||(izin=='friends'&&arkadas)||
            (izin=='following'&&takipEdiyor))){
          throw StateError('Hikâye sahibi yeni mesaj isteği kabul etmiyor.');
        }
        final ids=<String>[ben.uid,hedef]..sort();
        final veri=<String,dynamic>{
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
          await sabit.set(veri,SetOptions(merge:true))
            .timeout(const Duration(seconds:10));
          chatId=sabit.id;
        }on FirebaseException catch(e){
          if(e.code!='permission-denied'&&e.code!='failed-precondition')rethrow;
          final temiz=chats.doc();
          await temiz.set(veri).timeout(const Duration(seconds:10));
          chatId=temiz.id;
        }
      }
      asama='mesaj';
      final chat=chats.doc(chatId);
      final batch=db.batch();
      batch.update(chat,{
        'lastMessage':tepki?'$metin Hikâye tepkisi':'↩ Hikâye yanıtı: $metin',
        'lastSenderId':ben.uid,
        'updatedAt':FieldValue.serverTimestamp(),
        'unread_$hedef':FieldValue.increment(1),
      });
      batch.set(chat.collection('messages').doc(),{
        'senderId':ben.uid,'text':metin,'type':'story_reply',
        'storyId':widget.storyId,'storyUrl':widget.url,
        'storyOwnerId':hedef,'storyMediaType':widget.mediaType,
        'reaction':tepki,'createdAt':FieldValue.serverTimestamp(),
        'clientCreatedAt':Timestamp.now(),
      });
      await batch.commit().timeout(const Duration(seconds:12));
      unawaited(uygulamaBildirimiGonder(
        toUid:hedef,fromUid:ben.uid,tur:'message',
        metin:tepki?'Hikâyene tepki verdi':'Hikâyene yanıt verdi',
        belgeId:chatId,
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
        content:Text(e.code=='permission-denied'
          ?'Hikâye yanıtı izin hatası ('+asama+').'
          :'Hikâye yanıtı gönderilemedi ('+asama+').')));
    }on TimeoutException{
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Hikâye yanıtında zaman aşımı. Tekrar dene.')));
    }catch(e){
      debugPrint('ngelx_story_reply stage='+asama+' error='+e.runtimeType.toString());
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content:Text('Hikâye yanıtı tamamlanamadı ('+asama+').')));
    }finally{
      if(mounted){setState(()=>gonderiliyor=false);_devam();}
    }
  }
"""
s=s[:a]+new+s[b:]
p.write_text(s,encoding='utf-8')
print('Build422 story reply: member-query, privacy-preserving chat create, proper message write.')
