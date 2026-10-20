from pathlib import Path
TAG='// Build548 device and live follow-ups'
def once(s,a,b):
 if s.count(a)!=1:raise RuntimeError(f'Build548 expected unique anchor {a[:100]!r}, found {s.count(a)}')
 return s.replace(a,b,1)
def snippet(name):return Path('tools/build548_'+name+'.dart').read_text()
def main_source(s):
 if TAG in s:return s
 s=once(s,"import 'build546_guest_policy.dart';","import 'build546_guest_policy.dart';\nimport 'build548_policy.dart';")
 s=once(s,"part 'build453_widgets.dart';","part 'build453_widgets.dart';\npart 'build548_widgets.dart';")
 a=s.index('class _YeniYuklePageState ');b=s.index('\nclass ',a+15)
 create=s[a:b]
 create=once(create,'  String tur=\'video\';',snippet('create_gallery')+"\n  String tur='video';")
 create=once(create,'    unawaited(_taslagiYukle());\n    unawaited(_kayipMedyaKurtar());','''    _createBusy548=true;
    unawaited(()async{
      try{await _taslagiYukle();if(mounted)await _kayipMedyaKurtar();}
      finally{_createBusy548=false;if(mounted)setState((){});}
    }());''')
 create=once(create,'  Future<void> medyaSec()async{','''  Future<void> medyaSec()=>_createMediaAction548(_medyaSec548);
  Future<void> _medyaSec548()async{''')
 create=once(create,'  Future<void> kamerayiAc({required bool video})async{','''  Future<void> kamerayiAc({required bool video})=>_createMediaAction548(()=>_kamerayiAc548(video:video));
  Future<void> _kamerayiAc548({required bool video})async{''')
 create=create.replace('    if(yukleniyor)return;\n    setState((){tur=yeni;', '    if(yukleniyor||_createBusy548||DateTime.now().isBefore(_createReady548))return;\n    setState((){tur=yeni;')
 create=once(create,'onPressed:yukleniyor?null:medyaSec,','onPressed:yukleniyor||_createBusy548?null:genelGaleri548,')
 # Generic top gallery icon must use mixed media as well; photo/video tool
 # callbacks still call mediaSec after an explicit content-type selection.
 create=once(create,"_finalUstUretIkon(Icons.photo_library_outlined,(){_turDegistir('photo');unawaited(medyaSec());})","_finalUstUretIkon(Icons.photo_library_outlined,()=>unawaited(genelGaleri548()))")
 create=create.replace('  Future<void> _uretiYenile() async {\n    if(yukleniyor)return;', '  Future<void> _uretiYenile() async {\n    if(yukleniyor||_createBusy548)return;')
 s=s[:a]+create+s[b:]
 a=s.index('class NgelXSohbetFotoOnizleme ');b=s.index('\nclass NgelXSohbetVideoOnizleme ',a)
 s=s[:a]+'''class NgelXSohbetFotoOnizleme extends StatelessWidget{
  final String url;
  const NgelXSohbetFotoOnizleme({super.key,required this.url});
  @override Widget build(BuildContext context)=>Ngelx548ChatPhoto(url:url);
}
''' +s[b:]
 a=s.index('class _NgelXAramaPageState ');b=s.index('\nclass GrupBilgiPage ',a)
 call=s[a:b]
 # Resolve peer from signed-in UID + members, never shared callTitle.
 call=call.replace('widget.baslik','_callTitle548').replace('widget.foto','_callPhoto548')
 call=once(call,'  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _aramaProfilCache={};',snippet('call_peer')+'\n  final Map<String,Future<DocumentSnapshot<Map<String,dynamic>>>> _aramaProfilCache={};')
 call=once(call,"      final status446=d.data()??<String,dynamic>{};","      final status446=d.data()??<String,dynamic>{};\n      _syncPeer548(status446);")
 call=once(call,'    Ngelx543PipCall.clear(widget.roomName);\n    _controlsTimer540?.cancel();','    _peerSub548?.cancel();\n    Ngelx543PipCall.clear(widget.roomName);\n    _controlsTimer540?.cancel();')
 start=call.index('  Future<void> hoparlorDegistir()async{');end=call.index('\n  Future<void> bitir(',start)
 call=call[:start]+'''  Future<void> hoparlorDegistir()async{
    if(_speakerBusy548||bitiyor)return;
    _speakerBusy548=true;
    final next=!lk.AudioManager.instance.isSpeakerOutputPreferred;
    try{
      await lk.AudioManager.instance.setSpeakerOutputPreferred(next,force:next);
      if(mounted)setState(()=>hoparlor=lk.AudioManager.instance.isSpeakerOutputPreferred);
    }catch(_){if(mounted)ngelxDurumMesaji(context,'Ses çıkışı değiştirilemedi.',tip:'hata');}
    finally{_speakerBusy548=false;}
  }
''' +call[end:]
 call=once(call,'color:acik?Colors.white12:Colors.white,shape:BoxShape.circle','color:(label==\'Hoparlör\'||label==\'Ses\'?acik:!acik)?Colors.white:Colors.white12,shape:BoxShape.circle')
 call=once(call,'child:Icon(icon,color:acik?Colors.white:ngelxCallBg,size:21),',"child:Icon(icon,color:(label=='Hoparlör'||label=='Ses'?acik:!acik)?ngelxCallBg:Colors.white,size:21),")
 s=s[:a]+call+s[b:]
 return s+'\n'+TAG+'\n'
def studio_source(s):
 if TAG in s:return s
 s=once(s,'  bool _guestMicWanted546=true,_guestCameraWanted546=true;', '  bool _guestMicWanted546=true,_guestCameraWanted546=false;\n'+snippet('guest_stage'))
 s=once(s,'  Future<void> _guestSync448(bool accepted)async{','''  Future<void> _guestSync448(bool accepted)async{
    if(accepted&&!_guestConsent548){
      _guestWanted448=true;
      _guestStageSet546('Katılım türünü seçip yayına bağlan.');
      return;
    }
    if(!accepted&&_guestActive448)_guestConsent548=false;''')
 s=s.replace("_guestCameraWanted546?'Konuk bağlantısı hazır':'Yayındasın · kamera kapalı'","_guestCameraWanted546?'Konuk olarak bağlı · görüntülü':'Konuk olarak bağlı · sesli'")
 a=s.index('  Widget _guestStatus546(){');b=s.index('\n  void _yenile()',a)
 s=s[:a]+snippet('guest_status')+'\n'+s[b:]
 # Rebuild local and remote audio/video state, including mic mute and speaking.
 s=once(s,"|${widget.oda.localParticipant?.videoTrackPublications.map((t)=>'${t.sid}:${t.muted}').join(',')}'", "|${widget.oda.localParticipant?.videoTrackPublications.map((t)=>'${t.sid}:${t.muted}').join(',')}|${widget.oda.localParticipant?.audioTrackPublications.map((t)=>'${t.sid}:${t.muted}').join(',')}|${widget.oda.remoteParticipants.values.map((p)=>'${p.identity}:${p.isSpeaking}').join(',')}|${widget.oda.localParticipant?.isSpeaking}'")
 # The compact toolbar previously omitted the local camera preference callback.
 s=once(s,'          host:widget.yayinSahibi,compact:true,','''          host:widget.yayinSahibi,compact:true,connected548:_guestActive448,onLeaving548:()=>unawaited(_guestSync448(false)),
          cameraPreferred:_guestCameraWanted546,onCameraPreference:_chooseGuestMedia548,''')
 s=once(s,'host:host,cameraPreferred:_guestCameraWanted546,onCameraPreference:(value){if(mounted)setState(()=>_guestCameraWanted546=value);},','host:host,connected548:_guestActive448,onLeaving548:()=>unawaited(_guestSync448(false)),cameraPreferred:_guestCameraWanted546,onCameraPreference:_chooseGuestMedia548,')
 # A single guest stage owns both remote and local previews. Remove both old,
 # overlapping rails and keep header/comments/controls outside its bounds.
 start=s.index('          if(widget.oda.remoteParticipants.values.where((p)=>p.videoTrackPublications.any(')
 end=s.index('\n',start)
 s=s[:start]+s[end:]
 old="          if(!yayinBitti)Positioned(right:9,bottom:MediaQuery.viewInsetsOf(context).bottom+math.min(MediaQuery.sizeOf(context).height*.33,190.0),child:_guestRail488()),"
 s=once(s,old,'')
 s=once(s,'              const Spacer(),\n              _commentSection490(),','              Expanded(child:_stage548()),\n              _commentSection490(),')
 s=once(s,'              child:track==null\n                ?_goruntuYokEkrani()','''              child:ngelx548UseGrid(_stageGuests548().length)&&!pkAktifYerel
                ?const ColoredBox(color:Color(0xFF16121E))
                :track==null
                ?_goruntuYokEkrani()''')
 # Explicitly activate free non-financial gifts. Existing transaction IDs,
 # retry idempotency and local duplicate-send lock remain intact.
 start=s.index('    // Stage-only gate:');end=s.index('    final user = FirebaseAuth.instance.currentUser;',start)
 s=s[:start]+"    if(!ngelx548ValidGift(ad,puan,adet)||kapatildi||yayinBitti)return;\n"+s[end:]
 s=once(s,"        final current=await tx.get(giftDoc);","""        final live=await tx.get(FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId));
        if(live.data()?['active']!=true||List<String>.from(live.data()?['bannedUsers']??const[]).contains(user.uid))throw StateError('live_unavailable');
        final current=await tx.get(giftDoc);""")
 s=s.replace('QA sanal hediye · gerçek para/coin ödemesi yok','Ücretsiz sanal hediyeler · para veya coin harcanmaz')
 s=s.replace("Text('${h['puan']} N',", "Text('Ücretsiz · ${h['puan']} puan',")
 return s+'\n'+TAG+'\n'
def guest_source(s):
 if TAG in s:return s
 s=once(s,'  final bool cameraPreferred;final ValueChanged<bool>? onCameraPreference;','  final bool connected548;final VoidCallback? onLeaving548;\n  final bool cameraPreferred;final ValueChanged<bool>? onCameraPreference;')
 s=once(s,'this.cameraPreferred=true,this.onCameraPreference','this.cameraPreferred=false,this.connected548=false,this.onLeaving548,this.onCameraPreference')
 a=s.index('  Future<void> _viewerJoinPanel497(');b=s.index('\n  @override Widget build(',a)
 s=s[:a]+snippet('guest_panel')+s[b:]
 return s+'\n'+TAG+'\n'
if __name__=='__main__':
 for file,transform in [('main.dart',main_source),('live_broadcast_studio.dart',studio_source),('build448_live_guests.dart',guest_source)]:
  p=Path('app/lib')/file;p.write_text(transform(p.read_text()))
 for name in ['widgets','policy']:(Path('app/lib')/('build548_'+name+'.dart')).write_text(snippet(name))
