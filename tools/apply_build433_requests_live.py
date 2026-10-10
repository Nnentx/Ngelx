from pathlib import Path
p=Path('app/lib/main.dart');s=p.read_text()
def rep(a,b):
 global s
 assert a in s,a[:100]
 s=s.replace(a,b)
rep("  final String initialFilter;\n  const AktivitePage({super.key,this.initialFilter='all'});","  final String initialFilter;\n  final bool notificationOnly;\n  const AktivitePage({super.key,this.initialFilter='all',this.notificationOnly=false});")
rep('class _AktivitePageState extends State<AktivitePage> {','''class _AktivitePageState extends State<AktivitePage> {
  bool get _istekSayfasi=>widget.initialFilter=='follow_requests'||widget.initialFilter=='friend_requests';
  String get _sayfaBasligi=>_istekSayfasi?(widget.initialFilter=='follow_requests'?'Takip istekleri':'Arkadaşlık istekleri'):'Bildirimler';
  final Set<String> _islenenIstekler={};
  late final _uid=FirebaseAuth.instance.currentUser?.uid;
  late final _notificationCache=NgelxSnapshotCache(()=>FirebaseFirestore.instance.collection('notifications').where('toUid',isEqualTo:_uid).limit(200).snapshots());
  @override void dispose(){_notificationCache.dispose();super.dispose();}
''')
rep("final ben=FirebaseAuth.instance.currentUser?.uid;if(ben==null||_aktiviteYenileniyor)return;","final ben=FirebaseAuth.instance.currentUser?.uid;if(ben==null||_aktiviteYenileniyor)return;\n    _notificationCache.retry();")
rep("(_secilenBildirimler.length.toString()+' seçildi'):t('activity')","(_secilenBildirimler.length.toString()+' seçildi'):_sayfaBasligi")
rep("stream: uid == null ? null : FirebaseFirestore.instance.collection('notifications').where('toUid', isEqualTo: uid).limit(200).snapshots(),","stream:uid==null?null:_notificationCache.stream,")
rep("          final docs=tumDocs.where((d)=>_filtreUyar(d.data())).toList();","          final docs=_istekSayfasi?ngelx433SosyalIstekler(tumDocs,uid??'').where((d)=>_filtreUyar(d.data())).toList():tumDocs.where((d)=>_filtreUyar(d.data())).toList();")
rep('''          return Column(children:[
            Container(
              color:Colors.white,
              padding:const EdgeInsets.fromLTRB(12,7,0,10),''','''          return Column(children:[
            if(_istekSayfasi)Padding(padding:const EdgeInsets.all(16),child:Align(alignment:Alignment.centerLeft,child:Text('${docs.length} bekleyen istek',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)))),
            if(!_istekSayfasi&&!widget.notificationOnly)Container(
              color:Colors.white,
              padding:const EdgeInsets.fromLTRB(12,7,0,10),''')
rep("?Center(child:Text(t('noActivityInFilter'),style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)))","?Center(child:Text(_istekSayfasi?'Bekleyen istek yok.':'Yeni bildirim yok.',style:const TextStyle(color:Colors.black54,fontWeight:FontWeight.w700)))")
anchor="            final secili=_secilenBildirimler.contains(d.id);"
rep(anchor,anchor+'''
            if(_istekSayfasi)return Padding(padding:const EdgeInsets.symmetric(horizontal:6,vertical:14),child:Row(crossAxisAlignment:CrossAxisAlignment.start,children:[
              CircleAvatar(radius:36,backgroundColor:const Color(0xFFE5E7EB),backgroundImage:gonderenFoto.isEmpty?null:NgelXAgImageProvider(gonderenFoto),child:gonderenFoto.isEmpty?const Icon(Icons.person,color:Colors.grey,size:44):null),
              const SizedBox(width:14),
              Expanded(child:Column(crossAxisAlignment:CrossAxisAlignment.start,children:[
                Text((v['senderName']??v['fromName']??'Kullanıcı').toString(),style:const TextStyle(fontSize:18,fontWeight:FontWeight.w800)),
                const SizedBox(height:10),
                Row(children:[
                  for(final kabul in [true,false])Expanded(child:Padding(padding:EdgeInsets.only(right:kabul?8:0),child:FilledButton(
                    style:FilledButton.styleFrom(backgroundColor:kabul?const Color(0xFF0866FF):const Color(0xFFE5E7EB),foregroundColor:kabul?Colors.white:Colors.black,shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(12))),
                    onPressed:_islenenIstekler.contains(d.id)?null:()async{
                      setState(()=>_islenenIstekler.add(d.id));
                      try{await istegiSonuclandir(context,d,kabul);}finally{if(mounted)setState(()=>_islenenIstekler.remove(d.id));}
                    },child:Text(kabul?'Onayla':'Sil'),
                  ))),
                ]),
              ])),
            ]));
''')
rep('builder:(_)=>const AktivitePage()','builder:(_)=>const AktivitePage(notificationOnly:true)')
rep("      return IconButton(\n        tooltip:'Bildirimler',","      return IconButton(\n        style:IconButton.styleFrom(backgroundColor:Colors.white,padding:const EdgeInsets.all(12)),\n        tooltip:'Bildirimler',")
rep("title:Text(metin,maxLines:2,overflow:TextOverflow.ellipsis,style:TextStyle(color:const Color(0xFF111827),fontWeight:v['read']==true?FontWeight.w600:FontWeight.w900)),","title:ngelx433RenkliBildirim(v),")
# One shared newest-state predicate for both counter and dedicated lists.
a=s.index('          final hamSosyal=',s.index('    Widget isteklerIcerigi()'));b=s.index('          return ListView(',a)
s=s[:a]+"          final sosyal=ngelx433SosyalIstekler(snap.data?.docs??const <QueryDocumentSnapshot<Map<String,dynamic>>>[],ben);\n"+s[b:]
rep("for(final d in q.docs){b.set(d.reference,{'read':true},SetOptions(merge:true));}","for(final d in q.docs){b.update(d.reference,{'read':true});}")
s+='\n'+Path('tools/build433_helpers.dart').read_text()
p.write_text(s)
# Child cleanup by the authenticated host, without weakening unrelated collections.
f=Path('firestore.rules');r=f.read_text();a=r.index('    match /live_streams/{streamId}');q=r[a:]
q=q.replace('allow update, delete: if signedIn() && (resource.data.userId == request.auth.uid || resource.data.uid == request.auth.uid);',"allow update: if signedIn() && (resource.data.userId == request.auth.uid || resource.data.uid == request.auth.uid);\n        allow delete: if signedIn() && (resource.data.userId == request.auth.uid || resource.data.uid == request.auth.uid || get(/databases/$(database)/documents/live_streams/$(streamId)).data.ownerId == request.auth.uid);")
q=q.replace('allow delete: if isMe(uid);',"allow delete: if isMe(uid) || (signedIn() && get(/databases/$(database)/documents/live_streams/$(streamId)).data.ownerId == request.auth.uid);")
q=q.replace('      match /comments/{commentId}',"      match /viewers/{viewerId} {\n        allow read: if signedIn();\n        allow delete: if signedIn() && get(/databases/$(database)/documents/live_streams/$(streamId)).data.ownerId == request.auth.uid;\n      }\n      match /comments/{commentId}")
f.write_text(r[:a]+q)
# Retain history only when explicitly saved; saved records expire 30 days after end.
p=Path('app/lib/main.dart');s=p.read_text();a=s.index('class CanliYayinGecmisiPage');b=s.index('class NgelXKapakKonumlandirPage',a)
s=s[:a]+'''class CanliYayinGecmisiPage extends StatefulWidget{
  const CanliYayinGecmisiPage({super.key});
  @override State<CanliYayinGecmisiPage> createState()=>_CanliYayinGecmisiPageState();
}
class _CanliYayinGecmisiPageState extends State<CanliYayinGecmisiPage>{
  late final _uid=FirebaseAuth.instance.currentUser?.uid;
  late final _cache=NgelxSnapshotCache(()=>FirebaseFirestore.instance.collection('live_streams').where('ownerId',isEqualTo:_uid).limit(100).snapshots());
  final Set<String> _pending={};
  String? _error;
  @override void dispose(){_cache.dispose();super.dispose();}
  Future<void> _delete(String id)async{
    if(!_pending.add(id))return;
    if(mounted)setState(()=>_error=null);
    try{await ngelx433CanliSil(id);}catch(_){if(mounted)setState(()=>_error='Yayın temizlenemedi. Yenile ile tekrar deneyebilirsin.');}
    finally{_pending.remove(id);if(mounted)setState((){});}
  }
  Future<void> _refresh()async{
    _cache.retry();
    if(_uid==null)return;
    try{
      final q=await FirebaseFirestore.instance.collection('live_streams').where('ownerId',isEqualTo:_uid).limit(100).get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:12));
      for(final d in q.docs){if(ngelx433CanliTemizlenir(d.data(),DateTime.now()))await _delete(d.id);}
    }catch(_){if(mounted)setState(()=>_error='Geçmiş yenilenemedi. Tekrar dene.');}
  }
  @override Widget build(BuildContext context)=>Theme(data:ThemeData.light(),child:Scaffold(
    backgroundColor:Colors.white,
    appBar:AppBar(title:const Text('Canlı yayın geçmişi'),actions:[IconButton(tooltip:'Yenile',onPressed:_refresh,icon:const Icon(Icons.refresh,color:mor))]),
    body:_uid==null?const Center(child:Text('Oturum bulunamadı.')):StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(
      stream:_cache.stream,builder:(_,snap){
        if(snap.hasError)return ngelx432YuklemeHatasi(()=>unawaited(_refresh()),'Geçmiş yüklenemedi.');
        if(!snap.hasData)return const Center(child:CircularProgressIndicator(color:mor));
        final all=snap.data!.docs,now=DateTime.now();
        final expired=all.where((d)=>ngelx433CanliTemizlenir(d.data(),now)).toList();
        // Start cleanup once per route snapshot, keep durable deleting marker on failure.
        final signature=expired.map((d)=>d.id).join('|');
        if(signature!=_cleanupSignature){
          _cleanupSignature=signature;
          WidgetsBinding.instance.addPostFrameCallback((_){if(mounted)unawaited(_cleanup(expired));});
        }
        final docs=all.where((d)=>!ngelxCanliKaydiTaze(d.data())&&d.data()['active']!=true&&!ngelx433CanliTemizlenir(d.data(),now)).toList()
          ..sort((a,b){int ms(Map<String,dynamic> v){final t=v['endedAt']??v['startedAt'];return t is Timestamp?t.millisecondsSinceEpoch:0;}return ms(b.data()).compareTo(ms(a.data()));});
        return Column(children:[
          const Padding(padding:EdgeInsets.all(16),child:Text('Kaydedilmiş yayınlar 30 gün saklanır. Kaydedilmemiş yayınlar geçmişte tutulmaz.',style:TextStyle(color:Colors.black54))),
          if(_error!=null)Padding(padding:const EdgeInsets.all(12),child:Text(_error!,style:const TextStyle(color:Colors.red))),
          Expanded(child:docs.isEmpty?const Center(child:Text('Kaydedilmiş canlı yayın geçmişin yok.')):ListView.builder(
            itemCount:docs.length,itemBuilder:(_,i){final d=docs[i],v=d.data();return ListTile(
              title:Text((v['title']??'Canlı yayın').toString()),subtitle:Text(zamanKisa(v['endedAt']??v['startedAt'])),
              trailing:IconButton(tooltip:'Kalıcı sil',icon:const Icon(Icons.delete_outline,color:Colors.red),onPressed:_pending.contains(d.id)?null:()async{
                final yes=await showDialog<bool>(context:context,builder:(_)=>AlertDialog(title:const Text('Yayın kaydı silinsin mi?'),content:const Text('Yayın kaydı, ilişkili medya ve yorumlar kalıcı olarak silinecek.'),actions:[TextButton(onPressed:()=>Navigator.pop(context,false),child:const Text('Vazgeç')),FilledButton(onPressed:()=>Navigator.pop(context,true),child:const Text('Sil'))]));
                if(yes==true)await _delete(d.id);
              }),
            );},
          )),
        ]);
      },
    ),
  ));
  String _cleanupSignature='';
  Future<void> _cleanup(List<QueryDocumentSnapshot<Map<String,dynamic>>> docs)async{for(final d in docs){if(!mounted)return;await _delete(d.id);}}
}

'''+s[b:];p.write_text(s)
# Ended host-owned unsaved streams clean up after the existing summary/disconnect.
f=Path('app/lib/live_broadcast_studio.dart');r=f.read_text();anchor='    await widget.oda.disconnect();\n    await widget.oda.dispose();\n    if(mounted)setState(()=>bitisOzetiHazir=true);';assert anchor in r
r=r.replace(anchor,anchor+'''\n    if(widget.yayinSahibi){
      unawaited(()async{
        try{
          final snap=await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).get(const GetOptions(source:Source.server));
          if(snap.exists&&ngelx433CanliTemizlenir(snap.data()!,DateTime.now()))await ngelx433CanliSil(widget.belgeId);
        }catch(_){/* Durable deleting marker is retried by history refresh. */}
      }());
    }''',1);f.write_text(r)
f=Path('app/pubspec.yaml');r=f.read_text();r=r.replace('version: 1.0.207+432','version: 1.0.208+433');f.write_text(r)
print('Build433 dedicated requests, notifications, and live history applied')
f=Path('tools/firestore_rules_test.mjs');r=f.read_text();anchor="  console.log('Firestore rules testleri başarılı.');";assert anchor in r
f.write_text(r.replace(anchor,Path('tools/build433_rules_test.mjs').read_text()+'\n'+anchor))
# In-flight heartbeat/PK writes must not recreate a record after cleanup.
f=Path('app/lib/live_broadcast_studio.dart');r=f.read_text()
r=r.replace('unawaited(ngelxCanliPkYayindanCik(widget.belgeId));','try{await ngelxCanliPkYayindanCik(widget.belgeId).timeout(const Duration(seconds:10));}catch(_){}')
r=r.replace("      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set(yama,SetOptions(merge:true));","      if(kapatildi)return;\n      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).update(yama);")
f.write_text(r)
f=Path('app/lib/live_pk.dart');r=f.read_text().replace('await liveRef.set(_ngelxPkTemizleAlanlari(),SetOptions(merge:true));','await liveRef.update(_ngelxPkTemizleAlanlari());');f.write_text(r)
