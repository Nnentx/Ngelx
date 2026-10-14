"""Apply Build455 after the verified Build454 source-generation chain."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]

def replace(path, old, new):
    target = root / path
    source = target.read_text()
    if old not in source:
        raise RuntimeError(f"Build455 source anchor missing: {path}: {old[:70]}")
    target.write_text(source.replace(old, new))

replace('app/lib/main.dart', "part 'build454_widgets.dart';", "part 'build454_widgets.dart';\npart 'build455_widgets.dart';")
replace('app/lib/main.dart', "profilAdi=(p['displayName']??p['username']??'NgelX').toString()", "profilAdi=ngelx455ProfileName(p, fallback:'Kişi bilgisi yükleniyor…')")
# Build457: the editor persists nicknames under the viewer's own UID:
# 'nicknames.$me'. Keep the original viewer-scoped reader in the inbox.
# Mapping to takmalar[other] leaks another viewer's nickname into this row.
# Never rewrite this expression to the other participant's UID.
replace('app/lib/main.dart', "title:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_chatAkisi,builder:(_,s){", "title:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('users').doc(widget.digerUid).snapshots(),builder:(_,profile455){return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:_chatAkisi,builder:(_,s){")
# Close this additional builder only at the private-chat title boundary.
path = root / 'app/lib/main.dart'
source = path.read_text()
start = source.index("title:StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(stream:FirebaseFirestore.instance.collection('users').doc(widget.digerUid).snapshots(),builder:(_,profile455)")
end = source.index('actions:', start)
section = source[start:end]
section = section.replace('gorunenAd=takma.isNotEmpty?takma:widget.ad;', "gorunenAd=takma.isNotEmpty?takma:ngelx455ProfileName(profile455.data?.data()??{},fallback:widget.ad=='NgelX'?'Kişi bilgisi yükleniyor…':widget.ad);\n        final photo455=(profile455.data?.data()?['photoUrl']??widget.foto).toString();")
section = section.replace('widget.foto.isEmpty', 'photo455.isEmpty').replace('NgelXAgImageProvider(widget.foto)', 'NgelXAgImageProvider(photo455)')
last = section.rfind('}),')
if last < 0: raise RuntimeError('Build455 private title closure missing')
section = section[:last] + '});}),' + section[last+3:]
path.write_text(source[:start]+section+source[end:])
replace('app/lib/main.dart', 'class _SohbetPageState extends State<SohbetPage> with Ngelx437MessageJump<SohbetPage> {', "class _SohbetPageState extends State<SohbetPage> with Ngelx437MessageJump<SohbetPage> {\n  late final Stream<DocumentSnapshot<Map<String,dynamic>>> _peerProfile455=FirebaseFirestore.instance.collection('users').doc(widget.digerUid).snapshots();")
replace('app/lib/main.dart', "stream:FirebaseFirestore.instance.collection('users').doc(widget.digerUid).snapshots(),builder:(_,profile455)", "stream:_peerProfile455,builder:(_,profile455)")
replace('app/lib/build445_inbox_model.dart', 'SizedBox(height:132,child:ListView.builder(', 'SizedBox(height:148,child:ListView.builder(')
replace('app/lib/build445_inbox_model.dart', 'itemExtent:84,', 'itemExtent:104,')
replace('app/lib/build445_inbox_model.dart', "name=self?_ngelx438Ui('Sen'):(p['displayName']??p['username']??'').toString().split(' ').first", "name=self?_ngelx438Ui('Sen'):ngelx455ProfileName(p,fallback:'Kişi').split(' ').first")
replace('app/lib/build445_inbox_model.dart', 'fontSize:13,fontWeight:FontWeight.w700', 'fontSize:15,fontWeight:FontWeight.w700')
replace('app/lib/build445_inbox_model.dart', "if(!self)Ngelx436PresenceAccess(other:id,target:p,child:Text(ngelx434Aktiflik(p),maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Color(0xFF52735F),fontSize:11,fontWeight:FontWeight.w600)))", "if(!self)SizedBox(width:92,child:Ngelx436PresenceAccess(other:id,target:p,child:Text(ngelx434Aktiflik(p),maxLines:2,overflow:TextOverflow.ellipsis,textAlign:TextAlign.center,style:const TextStyle(color:Color(0xFF52735F),fontSize:12,height:1.1,fontWeight:FontWeight.w600))))")

replace('app/lib/community450.dart', 'fontSize: 11)', 'fontSize: 13)')
replace('app/lib/community450.dart', 'fontSize: 11,', 'fontSize: 13,')
replace('app/lib/community450.dart', 'fontSize: 12)', 'fontSize: 14)')
replace('app/lib/community450.dart', 'padding:const EdgeInsets.all(16),margin:const EdgeInsets.only(bottom:16)', 'padding:const EdgeInsets.symmetric(horizontal:12,vertical:9),margin:const EdgeInsets.only(bottom:10)')
replace('app/lib/community450.dart', "Text(_stage454,style:const TextStyle(color:Color(0xFF43326C),fontWeight:FontWeight.w700)),const SizedBox(height:10)", "Text(_stage454,style:const TextStyle(color:Color(0xFF6744C8),fontSize:12,fontWeight:FontWeight.w700)),const SizedBox(height:6)")
replace('app/lib/community450.dart', "style:const TextStyle(color:Color(0xFF43326C))", "style:const TextStyle(color:Color(0xFF6744C8),fontSize:12,fontWeight:FontWeight.w600)")
replace('app/lib/community450.dart', "ScaffoldMessenger.of(context).showSnackBar(SnackBar(content:Text(pending?'Gönderin yönetici onayına gönderildi.':'Gönderin paylaşıldı.')))", "ngelx455Status(context,pending?'Yönetici onayına gönderildi':type=='video'?'Video paylaşıldı':type=='image'?'Fotoğraf paylaşıldı':'Gönderi paylaşıldı')")
path = root / 'app/lib/community450.dart'
source = path.read_text()
start = source.index('  Future<void> comments(BuildContext c) async {')
end = source.index('\n  @override', start)
source = source[:start] + '''  Future<void> comments(BuildContext c) async {
    await showModalBottomSheet(context:c,isScrollControlled:true,
      backgroundColor:Colors.white,showDragHandle:true,
      builder:(_)=>Ngelx455Comments(post:ref,member:member,admin:admin));
  }
''' + source[end:]
# Show counts from the existing collections rather than fabricated counters.
anchor = '        const Divider(),\n        Row('
count_ui = '''        Padding(padding:const EdgeInsets.only(top:10),child:Wrap(spacing:16,children:[
          StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:ref.collection('likes').snapshots(),builder:(_,s)=>Text(s.hasError?'Beğeniler yüklenemedi':'${s.data?.size??0} beğeni',style:const TextStyle(fontSize:13,color:Color(0xFF697386)))),
          StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:ref.collection('comments').snapshots(),builder:(_,s)=>Text(s.hasError?'Yorumlar yüklenemedi':'${s.data?.size??0} yorum',style:const TextStyle(fontSize:13,color:Color(0xFF697386)))),
        ])),
        const Divider(),
        Row('''
if anchor not in source: raise RuntimeError('Build455 community post actions anchor missing')
source = source.replace(anchor, count_ui)
start = source.index('            Expanded(\n              child: StreamBuilder<DocumentSnapshot<Map<String, dynamic>>>(', source.index('class NgelXCommunityPost450'))
end = source.index('            Expanded(\n              child: TextButton.icon(\n                onPressed: () => comments(c)', start)
source = source[:start] + "            Expanded(child:Ngelx455Reactions(ref:ref.collection('likes'),enabled:member)),\n" + source[end:]
source = source.replace("text: '${value['text']}\\nNgelX topluluk: $communityId'", "text: '${value['text']}\\n${value['mediaUrl']??''}\\nNgelX gönderi: $communityId/$id'")
source = source.replace('    scaffoldBackgroundColor: Colors.white,', '''    scaffoldBackgroundColor: Colors.white,
    textTheme:ThemeData.light().textTheme.copyWith(
      bodyMedium:const TextStyle(fontSize:15,height:1.4,color:Color(0xFF172033)),
      bodyLarge:const TextStyle(fontSize:16,height:1.4,color:Color(0xFF172033)),
      titleMedium:const TextStyle(fontSize:17,fontWeight:FontWeight.w700,color:Color(0xFF172033)),
      labelLarge:const TextStyle(fontSize:14,fontWeight:FontWeight.w700),
    ),
    inputDecorationTheme:InputDecorationTheme(filled:true,fillColor:const Color(0xFFF5F4F9),
      contentPadding:const EdgeInsets.symmetric(horizontal:16,vertical:14),
      border:OutlineInputBorder(borderSide:BorderSide.none,borderRadius:BorderRadius.circular(16)),
      hintStyle:const TextStyle(fontSize:14,color:Color(0xFF697386))),
    outlinedButtonTheme:OutlinedButtonThemeData(style:OutlinedButton.styleFrom(
      minimumSize:const Size(48,44),side:const BorderSide(color:Color(0xFFE2D9F3)),
      shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)))),
    filledButtonTheme:FilledButtonThemeData(style:FilledButton.styleFrom(
      minimumSize:const Size(48,44),shape:RoundedRectangleBorder(borderRadius:BorderRadius.circular(16)))),
    chipTheme:ChipThemeData(backgroundColor:const Color(0xFFF5F4F9),selectedColor:const Color(0xFFEDE4FF),
      labelStyle:const TextStyle(fontSize:14,fontWeight:FontWeight.w600)),''',1)
source = source.replace('fontSize: 11.5,','fontSize: 14,')
source = source.replace('builder: (c) => AlertDialog(', 'builder: (c) => AlertDialog(backgroundColor:Colors.white,')
source = source.replace("title: const Text('Topluluk önizlemesi'),", "title: const Text('Topluluk önizlemesi'),")
# Include chosen visuals in the existing creation confirmation.
start = source.index("'Topluluk önizlemesi'")
end = source.index('    if (confirmed != true',start)
segment=source[start:end]
segment=segment.replace('children: [', "children: [\n            if(cover!=null)Ngelx454LocalMedia(file:cover!,video:false),\n            if(photo!=null)Padding(padding:const EdgeInsets.symmetric(vertical:12),child:SizedBox(height:80,width:80,child:Ngelx454LocalMedia(file:photo!,video:false))),",1)
source=source[:start]+segment+source[end:]
start = source.index('class NgelXCommunityPost450')
end = source.index('class NgelXCommunityAdmin450', start)
post = source[start:end]
count_start = post.index('        Padding(padding:const EdgeInsets.only(top:10),child:Wrap(')
count_end = post.index('        const Divider(),', count_start)
post = post[:count_start] + '        Ngelx455PostCounts(ref:ref),\n' + post[count_end:]
share_start = post.index('                onPressed: () => SharePlus.instance.share(')
share_end = post.index('                icon: const Icon(Icons.share_outlined', share_start)
post = post[:share_start] + '                onPressed:()=>ngelx455SharePost(c,ref,value),\n' + post[share_end:]
post = post.replace('Widget build(BuildContext c) => Container(', 'Widget build(BuildContext c) => Ngelx455PostView(ref:ref,child:Container(',1)
close = post.rfind('  );')
if close < 0: raise RuntimeError('Community post closure missing')
post = post[:close]+'  ));'+post[close+4:]
source = source[:start]+post+source[end:]
source = source.replace('AlertDialog(', 'Ngelx455WhiteDialog(')
error_start=source.index('void _communityError450(')
error_end=source.index('Widget _communityImage450(',error_start)
source=source[:error_start]+'''void _communityError450(BuildContext c,Object e){
  ngelx455Status(c,'İşlem tamamlanamadı. ${_ngelxKisaHata(e)}',error:true);
}

'''+source[error_end:]
path.write_text(source)
replace('app/lib/build446_call_lifecycle.dart', '  bool _observing=false,_foreground=true;', '''  bool _observing=false,_foreground=true;
  Future<void> clearForAccount455()async{
    final pending=ngelxCallSession444.room;
    final generation455=ngelxCallSession444.generation;
    for(final item in _calls.entries.toList()){
      await detach(item.value.room);
      try{await item.value.room.disconnect();}catch(_){}
      if(ngelxCallSession444.current(item.key,generation455)&&_ngelxArkaPlanAramaOdalari.containsKey(item.key))await ngelxArkaPlanAramayiTemizle(item.key);
      if(ngelxCallSession444.current(item.key,generation455))ngelxCallSession444.release(item.key);
    }
    if(pending!=null&&ngelxCallSession444.current(pending,generation455))ngelxCallSession444.release(pending);
  }''')
replace('app/lib/build448_incoming_calls.dart', '      await _stop();\n      if(epoch!=_authEpoch454)return;', '      await _stop();\n      await ngelx446Calls.clearForAccount455();\n      if(epoch!=_authEpoch454)return;')
replace('app/lib/build448_incoming_calls.dart', '  String? _ringing,_handling;', '  String? _ringing,_handling,_account455;')
replace('app/lib/build448_incoming_calls.dart', '      final epoch=++_authEpoch454;', '      final epoch=++_authEpoch454;\n      final accountChanged455=_account455!=null&&_account455!=user?.uid;')
replace('app/lib/build448_incoming_calls.dart', '      await ngelx446Calls.clearForAccount455();', '      if(accountChanged455)await ngelx446Calls.clearForAccount455();')
replace('app/lib/build448_incoming_calls.dart', '      if(epoch!=_authEpoch454||user==null||user.isAnonymous)return;', '      if(epoch!=_authEpoch454)return;\n      _account455=user?.uid;\n      if(user==null||user.isAnonymous)return;')
replace('app/lib/build448_incoming_calls.dart', "final ref=FirebaseFirestore.instance.collection('chats').doc(chat),d=await ref.get();", "final ref=FirebaseFirestore.instance.collection('chats').doc(chat),d=await ref.get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:8));\n      if(FirebaseAuth.instance.currentUser?.uid!=me)return;")
replace('app/lib/main.dart', '      await kontrol.initialize();', '      await kontrol.initialize().timeout(const Duration(seconds:15));')
replace('app/lib/main.dart', 'final Expando<bool> _ngelx444Watched=Expando<bool>();', 'final Expando<bool> _ngelx444Watched=Expando<bool>();\nfinal Expando<double> _ngelx455CallVideoVolume=Expando<double>();')
replace('app/lib/main.dart', '  if(ngelxCallSession444.busy){try{await player.pause();}catch(_){}return;}', '''  if(ngelxCallSession444.busy&&player is! VideoPlayerController){try{await player.pause();}catch(_){}return;}
  if(player is VideoPlayerController){
    if(ngelxCallSession444.busy){
      _ngelx455CallVideoVolume[player]??=player.value.volume;
      await player.setVolume(0);
    }else if(_ngelx455CallVideoVolume[player]!=null){
      final previous=_ngelx455CallVideoVolume[player]!;_ngelx455CallVideoVolume[player]=null;
      await player.setVolume(previous);
    }
  }''')
replace('app/lib/main.dart', '      if(ngelxCallSession444.busy){unawaited(player.pause());}', '''      if(ngelxCallSession444.busy){
        if(player.value.volume>0){_ngelx455CallVideoVolume[player]??=player.value.volume;unawaited(player.setVolume(0));}
      }else if(_ngelx455CallVideoVolume[player]!=null){
        final previous=_ngelx455CallVideoVolume[player]!;_ngelx455CallVideoVolume[player]=null;unawaited(player.setVolume(previous));
      }''')
replace('app/lib/community450.dart', '      await p.initialize();', '      await p.initialize().timeout(const Duration(seconds:15));')
replace('app/lib/main.dart', "          final docs=_inboxBelgeleri438(s.data?.docs??[]).where((d){", "          if(!s.hasData&&!s.hasError)return const Center(child:CircularProgressIndicator(color:mor));\n          final docs=_inboxBelgeleri438(s.data?.docs??[]).where((d){")
replace('app/lib/main.dart', '              if(satirlar.isEmpty)return ListView(', "              if(satirlar.isEmpty&&s.data?.metadata.isFromCache==true)return const Center(child:Text('Sohbetler eşitleniyor…',style:TextStyle(color:mor,fontSize:14)));\n              if(satirlar.isEmpty)return ListView(")
print('Build455 profile names, comments, counters and compact upload presentation applied')
