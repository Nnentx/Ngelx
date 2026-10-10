from pathlib import Path
import re
p=Path('app/lib/main.dart');s=p.read_text()
def rep(a,b,n=1):
 global s
 assert s.count(a)==n,(a[:110],s.count(a),n)
 s=s.replace(a,b)
# These are automatic now; old false flags must not suppress behavior.
rep("final okunduPaylas=d.data()?['readReceipts_$ben']!=false;",'const okunduPaylas=true;')
rep("final izin=veri['readReceipts_$ben']!=false;",'const izin=true;')
rep("if(grupVerisi!['readReceipts_'+id]==false)continue;",'// Read receipts are automatic for every member.')
rep("_typingGostergesiAcik=tv['typingIndicator_$uid']!=false;",'_typingGostergesiAcik=true;')
rep("shareReadReceipt:tv['readReceipts_'+me]!=false,",'shareReadReceipt:true,')
rep("if(_mesajHazirlikSohbet['typingIndicator_$ben']!=false){",'if(mounted){')
rep("final okundu=cv['readReceipts_${widget.digerUid}']!=false;",'const okundu=true;')
rep("final digerOkuma=veri['readReceipts_${widget.digerUid}']!=false?veri['lastReadAt_${widget.digerUid}']:null;","final digerOkuma=veri['lastReadAt_${widget.digerUid}'];")
rep("          final read=v['readReceipts_'+uid]!=false;\n          final typing=v['typingIndicator_'+uid]!=false;\n",'')
for label in ('Okundu bilgisi','Yazma göstergesi'):
 s,count=re.subn(r"^.*_satir\([^\n]*'"+label+r"'[^\n]*\n",'',s,flags=re.M);assert count==1
start=s.index('              if(me!=null)SwitchListTile(\n',s.index('class SohbetBilgiPage'))
end=s.index('              const SizedBox(height:18),',start)
assert 'Okundu bilgisi' in s[start:end] and 'Yazma göstergesi' in s[start:end]
s=s[:start]+s[end:]
# Use the shared field, falling back to the last globally selected legacy value.
rep("(veri['quickEmoji_$uid']??'👍').toString()","ngelx437SharedEmoji(veri)")
rep("(mevcut['quickEmoji_$me']??'👍').toString()","ngelx437SharedEmoji(mevcut)")
rep("await ref.set({'quickEmoji_$me':emoji},SetOptions(merge:true));","await ref.set({'quickEmoji':emoji,'quickEmojiUpdatedBy':me,'quickEmojiUpdatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));")
rep("'quickEmoji_$me':'👍'","'quickEmoji':'👍'")
# Refresh group timestamp during continuous typing; an old timestamp must not expire mid-sentence.
rep('  bool _typingYazildi=false,_typingGostergesiAcik=true;','  bool _typingYazildi=false,_typingGostergesiAcik=true;\n  DateTime? _typingHeartbeat;')
rep("        _typingYazildi=true;\n        unawaited(chatRef.set", "        _typingYazildi=true;\n        _typingHeartbeat=DateTime.now();\n        unawaited(chatRef.set")
rep("    _typingZamanlayici=Timer(const Duration(milliseconds:2400),(){", """    if(_typingYazildi&&(_typingHeartbeat==null||DateTime.now().difference(_typingHeartbeat!).inSeconds>=3)){
      _typingHeartbeat=DateTime.now();
      unawaited(chatRef.set({'typing_'+me:FieldValue.serverTimestamp()},SetOptions(merge:true)).catchError((_){ }));
    }
    _typingZamanlayici=Timer(const Duration(milliseconds:2400),(){""")
# Only a foreground, current chat at the newest message can mark the thread read.
rep('    if(ben==null||_okunduYaziliyor)return;',"    if(ben==null||_okunduYaziliyor||!mounted||!ngelx437ReceiptVisible(foreground:WidgetsBinding.instance.lifecycleState==AppLifecycleState.resumed,currentRoute:ModalRoute.of(context)?.isCurrent==true,listReady:liste.hasClients,atBottom:liste.hasClients&&liste.position.maxScrollExtent-liste.position.pixels<=120,searching:_jumpMoving))return;",2)
rep('if(me!=null&&uyeMi&&docs.isNotEmpty){','if(me!=null&&uyeMi&&docs.isNotEmpty&&liste.hasClients&&_enAltta&&!_jumpMoving&&ModalRoute.of(context)?.isCurrent==true&&WidgetsBinding.instance.lifecycleState==AppLifecycleState.resumed){')
rep('    if(yeni!=_enAltta)setState(()=>_enAltta=yeni);','    if(yeni!=_enAltta)setState(()=>_enAltta=yeni);\n    if(yeni)unawaited(_okunduIsaretle());')
# Add private scroll read updates without marking messages while an info/search page covers the chat.
rep('  void sonaGit({bool zorla=false}){WidgetsBinding.instance.addPostFrameCallback((_){','  void sonaGit({bool zorla=false}){if(jumpActive&&!zorla)return;WidgetsBinding.instance.addPostFrameCallback((_){',2)
# When initial scrolling has materialized the bottom, perform the read update.
s=s.replace('      if(hedef>0)liste.jumpTo(hedef);','      if(hedef>0)liste.jumpTo(hedef);\n      unawaited(_okunduIsaretle());',1)
a=s.index('class _SohbetPageState');head=s[:a];tail=s[a:].replace('      if(hedef>0)liste.jumpTo(hedef);','      if(hedef>0)liste.jumpTo(hedef);\n      unawaited(_okunduGuncelle());',1);s=head+tail
# State mixin: preserve existing chat rows and fetch old search context independently.
rep('class _GrupSohbetPageState extends State<GrupSohbetPage>{','''class _GrupSohbetPageState extends State<GrupSohbetPage> with Ngelx437MessageJump<GrupSohbetPage>{
  @override String get jumpChatId=>widget.chatId;
  @override ScrollController get jumpScroll=>liste;
  Future<void> _grupBilgiAc()async{
    final result=await Navigator.push<Object?>(context,MaterialPageRoute(builder:(_)=>GrupBilgiPage(chatId:widget.chatId)));
    if(mounted)await jumpToMessage(result);
  }''')
rep('class _SohbetPageState extends State<SohbetPage> {','''class _SohbetPageState extends State<SohbetPage> with Ngelx437MessageJump<SohbetPage> {
  @override String get jumpChatId=>widget.chatId;
  @override ScrollController get jumpScroll=>liste;
  void _private437Scroll(){if(liste.hasClients&&liste.position.maxScrollExtent-liste.position.pixels<120)unawaited(_okunduGuncelle());}''')
rep('  void bilgi()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetBilgiPage(uid:widget.digerUid,ad:widget.ad,foto:widget.foto,chatId:widget.chatId)));','''  Future<void> bilgi()async{
    final result=await Navigator.push<Object?>(context,MaterialPageRoute(builder:(_)=>SohbetBilgiPage(uid:widget.digerUid,ad:widget.ad,foto:widget.foto,chatId:widget.chatId)));
    if(mounted)await jumpToMessage(result);
  }''')
rep('()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>GrupBilgiPage(chatId:widget.chatId)))','_grupBilgiAc',2)
rep("()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetMesajAramaPage(chatId:widget.chatId,groupMode:true)))","()async{final result=await Navigator.push<String>(context,MaterialPageRoute(builder:(_)=>SohbetMesajAramaPage(chatId:widget.chatId,groupMode:true)));if(mounted&&result!=null)Navigator.pop(context,result);}")
rep("()=>Navigator.push(context,MaterialPageRoute(builder:(_)=>SohbetMesajAramaPage(chatId:chatId,participantName:ad)))","()async{final result=await Navigator.push<String>(context,MaterialPageRoute(builder:(_)=>SohbetMesajAramaPage(chatId:chatId,participantName:ad)));if(context.mounted&&result!=null)Navigator.pop(context,result);}")
a=s.index('  Future<void> _aramaSonucuAc(');b=s.index('\n  @override',a)
# Replace the entire preview-sheet handler; keep following helpers intact.
end=s.index('\n  }',a)+len('\n  }')
s=s[:a]+"  Future<void> _aramaSonucuAc(QueryDocumentSnapshot<Map<String,dynamic>> d)async{Navigator.pop(context,d.id);}"+s[end:]
rep('final docs=<QueryDocumentSnapshot<Map<String,dynamic>>>[...hamDocs].where','final docs=jumpMerge(hamDocs).where')
rep('final tumDocs=s.data?.docs??List<QueryDocumentSnapshot<Map<String,dynamic>>>.from(_mesajOnbellek);','final tumDocs=jumpMerge(s.data?.docs??List<QueryDocumentSnapshot<Map<String,dynamic>>>.from(_mesajOnbellek));')
rep('key:ValueKey(d.id),','key:jumpRowKey(d.id),')
rep("key:ValueKey('private_${d.id}'),","key:jumpRowKey(d.id),")
rep('              return Column(children:[\n                if(gunGoster&&gunEtiketi.isNotEmpty)', '              return Column(children:[\n                if(d.id==_jumpId)const Text(\'Arama sonucu\',style:TextStyle(color:Color(0xFF2478FF),fontWeight:FontWeight.w800)),\n                if(gunGoster&&gunEtiketi.isNotEmpty)')
# Highlight target using existing repaint boundary's child without changing renderer structure.
rep('child:Column(children:[\n                          if(gunAyir)',"child:Column(children:[\n                          if(d.id==_jumpId)const Text('Arama sonucu',style:TextStyle(color:Color(0xFF2478FF),fontWeight:FontWeight.w800)),\n                          if(gunAyir)")
# Scroll listener registration in the private state only.
a=s.index('class _SohbetPageState');b=s.index('class SohbetBilgiPage',a);part=s[a:b]
anchor='    super.initState();';assert part.count(anchor)==1
part=part.replace(anchor,anchor+'\n    liste.addListener(_private437Scroll);')
s=s[:a]+part+s[b:]
# Inbox clears unread counters before navigation; receipt state must follow actual visible messages instead.
rep('  bool _okunduYaziliyor=false;', '  bool _okunduYaziliyor=false;\n  Timestamp? _read437Stamp,_read437Written;')
rep('  final List<QueryDocumentSnapshot<Map<String,dynamic>>> _grupMesajOnbellek=[];', '  Timestamp? _read437Stamp,_read437Written;\n  final List<QueryDocumentSnapshot<Map<String,dynamic>>> _grupMesajOnbellek=[];')
rep('      if(okunmamis<=0)return;', "      final stamp=_read437Stamp;if(stamp==null)return;\n      final previous=d.data()?['lastReadAt_$ben'];\n      if(okunmamis<=0&&previous is Timestamp&&previous.millisecondsSinceEpoch>=stamp.millisecondsSinceEpoch){_read437Written=stamp;return;}",2)
rep("if(okunduPaylas)'lastReadAt_$ben':FieldValue.serverTimestamp(),", "if(okunduPaylas)'lastReadAt_$ben':stamp,")
rep("if(izin)'lastReadAt_$ben':FieldValue.serverTimestamp(),", "if(izin)'lastReadAt_$ben':stamp,")
rep('    _okunduYaziliyor=true;', '    if(_read437Stamp==null||(_read437Written!=null&&_read437Written!.millisecondsSinceEpoch>=_read437Stamp!.millisecondsSinceEpoch))return;\n    _okunduYaziliyor=true;',2)
# Assign the completed timestamp only on success, never after failed writes.
rep("},SetOptions(merge:true)).timeout(const Duration(seconds:5));\n    }catch(_){\n    }finally{\n      _okunduYaziliyor=false;", "},SetOptions(merge:true)).timeout(const Duration(seconds:5));\n      _read437Written=stamp;\n    }catch(_){\n    }finally{\n      _okunduYaziliyor=false;")
rep("},SetOptions(merge:true));\n    }catch(_){\n    }finally{\n      _okunduYaziliyor=false;", "},SetOptions(merge:true));\n      _read437Written=stamp;\n    }catch(_){\n    }finally{\n      _okunduYaziliyor=false;")
read_loop="""for(final item in docs){final value=item.data(),stamp=value['createdAt'];if(value['senderId']!=uid&&value['type']!='system'&&stamp is Timestamp&&(_read437Stamp==null||stamp.millisecondsSinceEpoch>_read437Stamp!.millisecondsSinceEpoch))_read437Stamp=stamp;}"""
rep('                  if(snap.hasData){\n                    if(docs.isNotEmpty', '                  if(snap.hasData){\n                    '+read_loop+'\n                    if(docs.isNotEmpty')
rep('          sureliMesajTakvimi(docs);\n          final okunmamis=', '          sureliMesajTakvimi(docs);\n          if(s.hasData){'+read_loop+'}\n          final okunmamis=')
# Group info fallback must also ignore the retired switch.
p2=Path('app/lib/group_quality.dart');g=p2.read_text();g=g.replace("      if (data['readReceipts_' + id] == false) continue;",'      // Automatic read receipts; old preference is retired.');p2.write_text(g)

# Bound image disk cache to seven days while keeping originals and upload drafts.
rep("import 'package:cached_network_image/cached_network_image.dart';","import 'package:cached_network_image/cached_network_image.dart';\nimport 'package:flutter_cache_manager/flutter_cache_manager.dart';")
s=s.replace('CachedNetworkImage(', 'CachedNetworkImage(cacheManager:ngelx437ImageCache,')
s=s.replace('CachedNetworkImage.evictFromCache(raw)', 'CachedNetworkImage.evictFromCache(raw,cacheManager:ngelx437ImageCache)')
# Shared media list expires separately from original 14-day chat messages.
a=s.index('class _GrupMedyaPageState');b=s.index('class NgelXMedyaGaleriPage',a);part=s[a:b]
part=part.replace(".collection('messages').orderBy('createdAt',descending:true).limit(300)",".collection('messages').where('createdAt',isGreaterThan:Timestamp.fromDate(DateTime.now().subtract(const Duration(hours:48)))).orderBy('createdAt',descending:true).limit(300)")
part=part.replace("'Medya ve bağlantılar',style:","'Son 48 saat · Medya ve bağlantılar',style:")
s=s[:a]+part+s[b:]
# Network media viewer had an unbounded initialize and no usable retry.
a=s.index('class NgelXGrupVideoMesaj extends StatefulWidget');b=s.index('class TamEkranVideoPage',a)
s=s[:a]+Path('tools/build437_video_message.dart').read_text()+'\n'+s[b:]
# Root query links work on the actual static host, where /u/ currently returns 404.
rep("$ngelxWebAdresi/u/$profilUid", "$ngelxWebAdresi/?profile=$profilUid")
rep("$ngelxWebAdresi/u/$uid", "$ngelxWebAdresi/?profile=$uid")
s=s.replace('unawaited(ngelxMarkGroupMessagesSeen(', 'unawaited(ngelx437MarkGroupMessagesSeen(')
rep('        if(uri!=null){',"        if(uri!=null){\n          final profile=uri.queryParameters['profile'];\n          if(profile!=null&&profile.isNotEmpty)return MaterialPageRoute(builder:(_)=>KullaniciProfilPage(uid:profile));")
manifest=Path('app/android/app/src/main/AndroidManifest.xml');m=manifest.read_text();anchor='<data android:scheme="https" android:host="ngelxsocial.com" android:pathPrefix="/u/" />';assert anchor in m;m=m.replace(anchor,anchor+'\n                <data android:scheme="https" android:host="ngelxsocial.com" android:path="/" />');manifest.write_text(m)

s+='\n'+Path('tools/build437_message_jump.dart').read_text()+'\n'+Path('tools/build437_retention_client.dart').read_text()
rep('    await Firebase.initializeApp();','    await Firebase.initializeApp();\n    unawaited(ngelx437TrimDownloads());')
# Apply retention to cache snapshots too, without discarding server originals early.
rep('              if(!ngelx435MesajErisilebilir(d.data(),FirebaseAuth.instance.currentUser?.uid))return false;\n              final t=', '              if(!ngelx435MesajErisilebilir(d.data(),FirebaseAuth.instance.currentUser?.uid)||!ngelx437MediaInList(d.data()[\'createdAt\'],DateTime.now()))return false;\n              final t=')
# Hide expired originals in live and cached message/search snapshots while the server removes files.
rep("return x is! Timestamp||x.toDate().isAfter(simdi);", "return !ngelx437MessageExpired(d.data()['createdAt'],simdi)&&(x is! Timestamp||x.toDate().isAfter(simdi));")
rep("jumpMerge(hamDocs).where((d)=>(d.data()['type']??'').toString()!='poll')", "jumpMerge(hamDocs).where((d)=>!ngelx437MessageExpired(d.data()['createdAt'],DateTime.now())&&(d.data()['type']??'').toString()!='poll')")
rep("              if(!ngelx435MesajErisilebilir(v,FirebaseAuth.instance.currentUser?.uid))return false;", "              if(!ngelx435MesajErisilebilir(v,FirebaseAuth.instance.currentUser?.uid)||ngelx437MessageExpired(v['createdAt'],DateTime.now()))return false;")

# Every newly marked notification gets an explicit read time for its 30-day retention window.
s=s.replace("{'read':true}","{'read':true,'readAt':FieldValue.serverTimestamp()}")

rep("defaultValue: '1.0.211'", "defaultValue: '1.0.212'")
rep("defaultValue: '436'", "defaultValue: '437'")
p.write_text(s)
test=Path('tools/firestore_rules_test.mjs');v=test.read_text();anchor="  console.log('Firestore rules testleri başarılı.');";assert anchor in v;test.write_text(v.replace(anchor,Path('tools/build437_rules_test.mjs').read_text()+'\n'+anchor))
p=Path('app/pubspec.yaml');p.write_text(p.read_text().replace('version: 1.0.211+436','version: 1.0.212+437'))
p.write_text(p.read_text().replace('  cached_network_image:', '  flutter_cache_manager: ^3.4.1\n  cached_network_image:'))
print('Build437 automatic receipts, typing, shared emoji and search-to-message applied')
