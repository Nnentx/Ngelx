from pathlib import Path
import sys

TAG = '// Build554 account-scoped live cleanup and reference comments'

def once(s, old, new):
    if s.count(old) != 1:
        raise RuntimeError(f'Build554 anchor count {s.count(old)}: {old[:100]}')
    return s.replace(old, new, 1)

def apply(root=Path('app')):
    p=root/'lib/main.dart';s=p.read_text()
    if TAG in s:return
    s=once(s, 'String? _media448;', '''String? _media448;
int _mediaEpoch554=0;
bool _mediaChangingAccount554=false;
Future<void> Function()? _mediaClose554;
void ngelx554ReleaseMedia(int epoch){
  if(epoch!=_mediaEpoch554)return;
  _media448=null;_media448Stop=null;_mediaClose554=null;
}
Future<void> ngelx554BeforeAccountChange()async{
  final epoch=_mediaEpoch554;
  final close=_mediaClose554;
  if(_media448!=null&&close==null&&_media448Stop==null){
    throw StateError('Hesap değiştirmeden önce açık sesli odadan ayrıl.');
  }
  if(close!=null)await close().timeout(const Duration(seconds:20));
  final stopping=_media448Stop;
  if(stopping!=null)await stopping.timeout(const Duration(seconds:12));
  ngelx554ReleaseMedia(epoch);
  if(epoch==_mediaEpoch554)_mediaEpoch554++;
}
''')
    s=once(s, '''  _media448=name;_media448Stop=null;
  try{await action();}finally{try{await _media448Stop;}catch(_){}if(_media448==name){_media448=null;_media448Stop=null;}}''', '''  final epoch=++_mediaEpoch554;
  _media448=name;_media448Stop=null;_mediaClose554=null;
  try{await action();}finally{
    if(epoch==_mediaEpoch554){
      try{await _media448Stop;}catch(_){}
      ngelx554ReleaseMedia(epoch);
    }
  }''')
    s=once(s,'Future<void> ngelx544BeforeAccountChange()async{','Future<void> ngelx544BeforeAccountChange()async{\n  await ngelx554BeforeAccountChange();')
    s=once(s,"Future<void> ngelx439SignOut()=>_ngelx439AuthOperations.signOut(()async{", "Future<void> ngelx439SignOut()=>_ngelx439AuthOperations.signOut(()async{\n  await ngelx554BeforeAccountChange();")
    s=once(s,"  _ngelx439AuthOperations.signIn(()async{", "  _ngelx439AuthOperations.signIn(()async{\n    _mediaChangingAccount554=true;\n    try{")
    s=once(s,"    return FirebaseAuth.instance.signInWithEmailAndPassword(email:email,password:password);", "    return await FirebaseAuth.instance.signInWithEmailAndPassword(email:email,password:password);\n    }finally{_mediaChangingAccount554=false;}")
    s=once(s,"Future<void> ngelx439SignOut()=>_ngelx439AuthOperations.signOut(()async{\n  await", "Future<void> ngelx439SignOut()=>_ngelx439AuthOperations.signOut(()async{\n  _mediaChangingAccount554=true;\n  try{\n  await")
    s=once(s,"  ngelxKokRotayaDon();\n});", "  ngelxKokRotayaDon();\n  }finally{_mediaChangingAccount554=false;}\n});")
    s=once(s,"  if(_media448!=null||ngelxCallSession444.busy){", "  if(_mediaChangingAccount554){ngelxDurumMesaji(context,'Hesap değiştiriliyor, lütfen bekle.',tip:'uyari');return;}\n  if(_media448!=null||ngelxCallSession444.busy){")
    s=once(s,"bool ngelx444ReserveCall(BuildContext context,String name){", "bool ngelx444ReserveCall(BuildContext context,String name){\n  if(_mediaChangingAccount554){ngelxDurumMesaji(context,'Hesap değiştiriliyor, lütfen bekle.',tip:'uyari');return false;}")
    # Admission can finish after a user has switched accounts. Never mount that room.
    s=once(s,"    final kimlik='${user.uid}-${DateTime.now().millisecondsSinceEpoch}';", "    final kimlik=user.uid;")
    a=s.index('Future<void> _ngelxCanliYayinaKatil448(');b=s.index('\nbool ngelxAktivite',a)
    section=s[a:b]
    section=once(section,'  lk.Room? oda;', '  final admissionEpoch554=_mediaEpoch554;\n  lk.Room? oda;')
    section=once(section,'    oda=lk.Room(roomOptions:', '''    if(FirebaseAuth.instance.currentUser?.uid!=user.uid||admissionEpoch554!=_mediaEpoch554)return;
    oda=lk.Room(roomOptions:''')
    section=once(section,'    await oda.connect(cevap.serverUrl,cevap.participantToken);', '''    _mediaClose554=()async{if(oda!=null)await ngelx444CloseRoom(oda!);};
    await oda.connect(cevap.serverUrl,cevap.participantToken).timeout(const Duration(seconds:18));''')
    section=once(section,'    if(!context.mounted){','    if(!context.mounted||FirebaseAuth.instance.currentUser?.uid!=user.uid||admissionEpoch554!=_mediaEpoch554){')
    # Room cleanup is unconditional, including Navigator errors and ordinary pops.
    section=once(section,"    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Canlı yayına şu anda bağlanılamadı.')));\n  }", "    if(context.mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Canlı yayına şu anda bağlanılamadı.')));\n  }finally{\n    if(oda!=null){try{await oda.disconnect();await oda.dispose();}catch(_){}}\n  }")
    s=s[:a]+section+s[b:];p.write_text(s+'\n'+TAG+'\n')

    p=root/'lib/build540_reference_ui.dart';s=p.read_text()
    s=once(s,'    color: const Color(0xC01A1721),','    color: Colors.transparent,')
    a=s.index('      child: LayoutBuilder');b=s.index('\n    ),\n  );',a)
    s=s[:a]+'''      child: LayoutBuilder(builder:(_,box) {
        if(MediaQuery.viewInsetsOf(context).bottom>0)return composer;
        // Reference layout: one row at ordinary phone widths. On extremely
        // narrow screens only the actions scroll; the text input keeps its width.
        final actionWidth=actions.length*44.0;
        final available=math.max(0.0,box.maxWidth-116.0);
        final railWidth=math.min(actionWidth,available);
        return Row(crossAxisAlignment:CrossAxisAlignment.center,children:[
          Expanded(child:composer),
          SizedBox(width:railWidth,child:SingleChildScrollView(
            scrollDirection:Axis.horizontal,child:Row(children:actions))),
        ]);
      }),'''+s[b:];p.write_text(s)

    p=root/'lib/live_broadcast_studio.dart';s=p.read_text()
    s=once(s,'  StreamSubscription<User?>? _auth541;', '''  StreamSubscription<User?>? _auth541;
  late final int _mediaLease554;
  Future<void> _accountExit554()async{
    kapatildi=true;yayinBitti=true;
    sayac?.cancel();heartbeat?.cancel();_videoWatch554?.cancel();_guestRetry546?.cancel();
    _guestWanted448=false;_guestRevision546++;
    await _keepLiveScreen553(false);
    final stopping=_stopRoom448();ngelx448HoldMediaUntil(stopping);
    await stopping;
    // End server presence while the original account still owns its token.
    if(widget.yayinSahibi&&FirebaseAuth.instance.currentUser?.uid==widget.ownerId){
      await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).set({
        'active':false,'status':'ended','endReason':'host_ended','cameraEnabled':false,
        'endedAt':FieldValue.serverTimestamp()},SetOptions(merge:true)).timeout(const Duration(seconds:6));
      await FirebaseFirestore.instance.collection('users').doc(widget.ownerId).set({
        'isLive':false,'currentLiveId':FieldValue.delete(),'liveTitle':FieldValue.delete(),
        'liveEndedAt':FieldValue.serverTimestamp()},SetOptions(merge:true)).timeout(const Duration(seconds:6));
    }
    ngelx554ReleaseMedia(_mediaLease554);
    if(mounted)setState((){});
  }
  Timer? _videoWatch554;
  int _videoRetries554=0;
  bool _videoRecovering554=false;
  Future<void> _recoverVideo554({bool manual=false})async{
    if(widget.yayinSahibi||kapatildi||yayinBitti||_guestWanted448||
      _guestConnecting448||_videoRecovering554||yenidenBaglaniyor||
      !manual&&(_goruntu()!=null||_videoRetries554>=2))return;
    final uid=FirebaseAuth.instance.currentUser?.uid;
    if(uid==null)return;
    _videoRecovering554=true;
    try{
      final doc=await FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId)
        .get(const GetOptions(source:Source.server)).timeout(const Duration(seconds:6));
      if(!mounted||kapatildi||yayinBitti||FirebaseAuth.instance.currentUser?.uid!=uid)return;
      final live=doc.data()??<String,dynamic>{};
      if(!ngelxCanliKaydiTaze(live)){await _izleyicideYayinBitti('host_ended');return;}
      if(live['cameraEnabled']==false)return;
      _videoRetries554++;
      final token=await NgelXLiveKitSource441().fetch(lk.TokenRequestOptions(
        roomName:_liveRoom546,participantIdentity:uid)).timeout(const Duration(seconds:12));
      if(!mounted||kapatildi||yayinBitti||FirebaseAuth.instance.currentUser?.uid!=uid)return;
      yenidenBaglaniyor=true;
      await widget.oda.disconnect().timeout(const Duration(seconds:5));
      if(kapatildi||yayinBitti||FirebaseAuth.instance.currentUser?.uid!=uid)return;
      _liveServer453=token.serverUrl;_liveToken453=token.participantToken;
      await widget.oda.connect(_liveServer453,_liveToken453).timeout(const Duration(seconds:15));
      if(kapatildi||yayinBitti||FirebaseAuth.instance.currentUser?.uid!=uid){
        try{await widget.oda.disconnect();}catch(_){}
      }
    }catch(_){}finally{
      _videoRecovering554=false;yenidenBaglaniyor=false;
      if(mounted)setState((){});
    }
  }''')
    s=once(s,'    final ownerSession541=FirebaseAuth.instance.currentUser?.uid;', '''    _mediaLease554=_mediaEpoch554;
    _mediaClose554=_accountExit554;
    _videoWatch554=Timer.periodic(const Duration(seconds:15),(_){
      if(_goruntu()!=null){_videoRetries554=0;return;}
      unawaited(_recoverVideo554());
    });
    final ownerSession541=FirebaseAuth.instance.currentUser?.uid;''')
    # Rendering must observe actual track/subscription arrival, not just SID/mute.
    s=s.replace("${t.sid}:${t.muted}').join(',')", "${t.sid}:${t.muted}:${t.track!=null}').join(',')")
    s=once(s, 'if(widget.oda.connectionState==lk.ConnectionState.disconnected&&!kapatildi&&!yayinBitti&&!_guestConnecting448)', 'if(widget.oda.connectionState==lk.ConnectionState.disconnected&&!kapatildi&&!yayinBitti&&!_guestConnecting448&&!_videoRecovering554)')
    s=once(s,"values.where((p)=>widget.ownerId.isEmpty||p.identity==widget.ownerId)","values.where((p)=>_izleyiciUid(p)==widget.ownerId)")
    # Release the media lease on physical disconnect, even when the summary route remains.
    s=once(s,'    try{await widget.oda.dispose().timeout(const Duration(seconds:4));}catch(_){}', '    try{await widget.oda.dispose().timeout(const Duration(seconds:4));}catch(_){}\n    ngelx554ReleaseMedia(_mediaLease554);')
    s=once(s,'    _auth541?.cancel();','    _auth541?.cancel();\n    _videoWatch554?.cancel();')
    s=s.replace('ngelx448HoldMediaUntil(stopping);', 'if(_mediaLease554==_mediaEpoch554)ngelx448HoldMediaUntil(stopping);')
    s=once(s,'''        await widget.oda.disconnect();
        if (kapatildi || yayinBitti) return;
        await _otomatikYenidenBaglan();''', '''        await _recoverVideo554(manual:true);''')
    s=once(s,'maxHeight:keyboard?56:112','maxHeight:keyboard?76:148')
    # Preserve compact panel but align status and controls in a single row.
    a=s.index('  Widget _guestStatus546(){');b=s.index('\n\n  void _yenile()',a)
    s=s[:a]+'''  Widget _guestStatus546(){
    if(widget.yayinSahibi||_guestStage546.isEmpty)return const SizedBox.shrink();
    Widget toggle(IconData icon,String label,VoidCallback action)=>IconButton(
      tooltip:label,onPressed:_guestMediaBusy546||_guestConnecting448?null:action,
      visualDensity:VisualDensity.compact,icon:Icon(icon,color:Colors.white,size:22));
    return Container(margin:const EdgeInsets.only(bottom:5),
      padding:const EdgeInsets.symmetric(horizontal:9,vertical:2),
      decoration:BoxDecoration(color:const Color(0xBB211D2F),borderRadius:BorderRadius.circular(16)),
      child:Row(children:[
        Icon(_guestActive448?Icons.check_circle:Icons.sync,color:Colors.greenAccent,size:16),
        const SizedBox(width:6),Expanded(child:Text(_guestStage546,maxLines:2,
          overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:11))),
        if(_guestActive448)...[
          toggle(_guestMicWanted546&&!_guestAudioMuted489?Icons.mic:Icons.mic_off,
            'Mikrofon',()=>unawaited(_guestToggle546(false))),
          toggle(_guestCameraWanted546?Icons.videocam:Icons.videocam_off,
            'Kamera',()=>unawaited(_guestToggle546(true))),
          if(_guestCameraWanted546)toggle(Icons.cameraswitch,'Kamerayı çevir',()=>unawaited(_guestFlip548())),
        ]else if(_guestWanted448&&!_guestConnecting448&&_guestConsent548)
          IconButton(tooltip:'Tekrar bağlan',onPressed:(){_guestRetries546=0;unawaited(_guestSync448(true));},
            icon:const Icon(Icons.refresh,color:Colors.white)),
      ]));
  }
'''+s[b:]
    # A rebuild can occur while reconnecting: the periodic watcher is not a build side effect.
    s=s.replace("onPressed:_otomatikYenidenBaglan", "onPressed:()=>unawaited(_recoverVideo554(manual:true))")
    # Pending host admission must also be cancellable before the live route exists.
    s=once(s,'  Future<void> _baslat448() async {', '  Future<void> _baslat448() async {\n    final admissionEpoch554=_mediaEpoch554;')
    s=once(s,'      oda = lk.Room(roomOptions: lk.RoomOptions(', '''      if(FirebaseAuth.instance.currentUser?.uid!=user.uid||admissionEpoch554!=_mediaEpoch554)return;
      oda = lk.Room(roomOptions: lk.RoomOptions(''')
    s=once(s,'      await oda.connect(cevap.serverUrl, cevap.participantToken);', '''      _mediaClose554=()async{if(oda!=null)await ngelx444CloseRoom(oda!);};
      await oda.connect(cevap.serverUrl, cevap.participantToken).timeout(const Duration(seconds:18));
      if(!mounted||FirebaseAuth.instance.currentUser?.uid!=user.uid||admissionEpoch554!=_mediaEpoch554){await ngelx444CloseRoom(oda);return;}''')
    s=once(s,"      final belge = await FirebaseFirestore.instance.collection('live_streams').add({", "      if(!mounted||FirebaseAuth.instance.currentUser?.uid!=user.uid){await ngelx444CloseRoom(oda);return;}\n      final belge = await FirebaseFirestore.instance.collection('live_streams').add({")
    s=once(s,'''      if (!mounted) return;
      await Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => CanliYayinPage(''', '''      if (!mounted||FirebaseAuth.instance.currentUser?.uid!=user.uid||admissionEpoch554!=_mediaEpoch554){await ngelx444CloseRoom(oda);return;}
      await Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => CanliYayinPage(''')
    p.write_text(s+'\n'+TAG+'\n')

    # Strengthen motion without claiming that bitmap assets are rigged 3D models.
    p=root/'lib/build553_gift_effect.dart';s=p.read_text()
    s=once(s,"offset:Offset(0,reduced?0:math.sin(t*math.pi*5)*5)","offset:Offset(reduced?0:math.sin(t*math.pi*4)*9,reduced?0:math.sin(t*math.pi*5)*14)")
    s=once(s,".78+.22*Curves.easeOutCubic.transform((t/.22).clamp(0.0,1.0))", ".58+.42*Curves.easeOutBack.transform((t/.24).clamp(0.0,1.0))+math.sin(t*math.pi*6)*.025")
    s=once(s,"final distance=radius*(.3+(i%13)/10);", "final distance=radius*(.18+((i%13)/13+t*1.6)%1.35);")
    p.write_text(s)

if __name__=='__main__':apply(Path(sys.argv[1]) if len(sys.argv)>1 else Path('app'))
