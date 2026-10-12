from pathlib import Path
import re, math, wave, struct
p=Path('app/lib/main.dart');s=p.read_text()
assert "import 'build444_call_session.dart';" not in s
s="import 'build444_call_session.dart';\n"+s
marker='final Map<String,lk.Room> _ngelxArkaPlanAramaOdalari'
global_code='''final ngelxCallSession444=NgelxCallSession444();
final Set<dynamic> _ngelx444MediaPlayers=<dynamic>{};
final Expando<bool> _ngelx444Watched=Expando<bool>();
Future<void> ngelx444MediaPlay(dynamic player)async{
  if(player==null)return;
  if(ngelxCallSession444.busy){try{await player.pause();}catch(_){}return;}
  _ngelx444MediaPlayers.add(player);
  if(player is VideoPlayerController && _ngelx444Watched[player]!=true){
    _ngelx444Watched[player]=true;
    player.addListener((){
      if(!player.value.isPlaying){_ngelx444MediaPlayers.remove(player);return;}
      if(ngelxCallSession444.busy){unawaited(player.pause());}
      else{_ngelx444MediaPlayers.add(player);}
    });
  }
  try{await player.play();}finally{if(player is! VideoPlayerController)_ngelx444MediaPlayers.remove(player);}
}
bool ngelx444ReserveCall(BuildContext context,String name){
  if(!ngelxCallSession444.reserve(name)){
    ngelxDurumMesaji(context,_ngelx438Ui('Önce devam eden aramayı bitir.'),tip:'uyari');
    return false;
  }
  for(final p in _ngelx444MediaPlayers.toList()){
    unawaited(Future<void>(()async{try{await p.pause();}catch(_){} }));
  }
  return true;
}
Future<void> ngelx444CloseRoom(lk.Room r)async{
  // Disconnect closes incoming audio immediately, independently of Firestore.
  try{await r.disconnect();}catch(_){}
  try{await r.dispose();}catch(_){}
}

'''
s=s.replace(marker,global_code+marker,1)
# Reserve before any outgoing call record is written; release failed launch.
for signature in ['  Future<void> aramaBaslat(bool goruntulu)async{','  Future<void> grupAramasiBaslat(bool goruntulu,String grupAdi,String foto)async{']:
 start=0
 while True:
  a=s.find(signature,start)
  if a<0:break
  b=s.index('\n  }',a)+5;region=s[a:b]
  marker='    try{';assert marker in region
  region=region.replace(marker,"    if(!ngelx444ReserveCall(context,odaAdi)){if(mounted)setState(()=>aramaBaslatiliyor=false);return;}\n"+marker,1)
  if '}finally{' in region:
   region=region.replace('}finally{','}finally{\n      ngelxCallSession444.releasePending(odaAdi);',1)
  else:
   last=region.rfind('\n    }');region=region[:last]+region[last:].replace('\n    }','\n    }finally{ngelxCallSession444.releasePending(odaAdi);}',1)
  s=s[:a]+region+s[b:];start=a+len(region)
# Incoming acceptance must reserve before setting active.
s=s.replace('                        if(acilanAramaId==d.id)return;',"                        if(acilanAramaId==d.id)return;\n                        final callRoom444=(v['callRoomName']??'').toString();\n                        if(!ngelx444ReserveCall(context,callRoom444))return;",1)
s=s.replace('                        }finally{\n                          if(mounted)setState(()=>acilanAramaId=null);','                        }finally{\n                          ngelxCallSession444.releasePending(callRoom444);\n                          if(mounted)setState(()=>acilanAramaId=null);',1)
a=s.index('  Future<void> aktifGrupAramasinaKatil');b=s.index('\n  Future<void> aramaBaslat',a);region=s[a:b]
region=region.replace('    try{',"    if(ngelxCallSession444.room!=oda&&!ngelx444ReserveCall(context,oda))return;\n    if(ngelxCallSession444.attached){ngelxDurumMesaji(context,_ngelx438Ui('Önce devam eden aramayı bitir.'),tip:'uyari');return;}\n    try{",1)
region=region.replace('\n    }\n  }','\n    }finally{ngelxCallSession444.releasePending(oda);}\n  }',1);s=s[:a]+region+s[b:]
# Background cleanup owns the session until disconnect completes.
s=s.replace('Future<void> ngelxArkaPlanAramayiTemizle(String roomName)async{','Future<void> ngelxArkaPlanAramayiTemizle(String roomName)async{',1)
s=s.replace("    try{await room.dispose();}catch(_){}\n  }\n}","    try{await room.dispose();}catch(_){}\n    ngelxCallSession444.release(roomName);\n  }\n}",1)
a=s.index('class _NgelXAramaPageState');b=s.index('\nclass ',a+10);region=s[a:b]
region=region.replace('  lk.Room? oda;', '''  lk.Room? oda;
  lk.Room? _connecting444;
  bool _connectInFlight444=false;
  bool _owns444=false;
  int _epoch444=0;
  AudioPlayer? _ringback444;
  bool get _alive444=>mounted&&!bitiyor&&!kucultuluyor&&_owns444&&ngelxCallSession444.current(widget.roomName,_epoch444);
  Future<void> _tone444(bool play)async{
    if(!play){final p=_ringback444;_ringback444=null;if(p!=null){try{await p.dispose();}catch(_){}}return;}
    if(!_alive444||_ringback444!=null)return;
    final p=AudioPlayer(handleAudioSessionActivation:false,handleInterruptions:false);
    _ringback444=p;
    try{
      await p.setAsset('assets/call_ringback444.wav');
      await p.setLoopMode(LoopMode.one);
      if(!_alive444||!identical(p,_ringback444)){await p.dispose();return;}
      unawaited(p.play().catchError((_){ }));
    }catch(_){if(identical(p,_ringback444))_ringback444=null;try{await p.dispose();}catch(_){} }
  }
  Future<void> _stopLocal444()async{
    unawaited(_tone444(false));
    odaOlaylari?.dispose();odaOlaylari=null;
    final r=oda;oda=null;
    final pending=_connecting444;_connecting444=null;
    if(r!=null)r.removeListener(_odaDegisti);
    if(pending!=null)pending.removeListener(_odaDegisti);
    await Future.wait([
      if(r!=null)ngelx444CloseRoom(r),
      if(pending!=null&&!identical(pending,r))ngelx444CloseRoom(pending),
      ngelxArkaPlanAramayiTemizle(widget.roomName),
    ]);
    if(_owns444){ngelxCallSession444.release(widget.roomName);_owns444=false;}
  }
  Future<void> _writeCurrent444(Map<String,dynamic> values)async{
    if(!_alive444)return;
    await FirebaseFirestore.instance.runTransaction((tx)async{
      final d=await tx.get(widget.aramaRef);
      if(!_alive444||d.data()?['callRoomName']!=widget.roomName)return;
      final status=d.data()?['callStatus'];
      if(status!='ringing'&&status!='active')return;
      final update=Map<String,dynamic>.from(values);
      if(status=='active'&&update['callStatus']=='ringing')update['callStatus']='active';
      tx.set(widget.aramaRef,update,SetOptions(merge:true));
    });
  }
''',1)
region=region.replace('    super.initState();','''    super.initState();
    _owns444=ngelxCallSession444.attach(widget.roomName);
    _epoch444=ngelxCallSession444.generation;
    if(!_owns444){
      bitiyor=true;baglaniyor=false;
      hata=_ngelx438Ui('Önce devam eden aramayı bitir.');
      WidgetsBinding.instance.addPostFrameCallback((_){if(mounted)Navigator.pop(context);});
      return;
    }
    hoparlor=widget.goruntulu;
''',1)
region=region.replace('  void _odaDegisti(){','  void _odaDegisti(){\n    if(!_alive444)return;',1)
region=region.replace('    if(r?.remoteParticipants.isNotEmpty==true){','    if(r?.remoteParticipants.isNotEmpty==true){\n      unawaited(_tone444(false));',1)
region=region.replace("unawaited(widget.aramaRef.set({\n          'callStatus':'active',\n          'callConnectedAt':FieldValue.serverTimestamp(),\n        },SetOptions(merge:true)).catchError((_){ }));","unawaited(_writeCurrent444({'callStatus':'active','callConnectedAt':FieldValue.serverTimestamp()}).catchError((_){ }));",1)
# Stop ringback as soon as acceptance arrives, even before remote audio is published.
region=region.replace("      final durum=(d.data()?['callStatus']??'').toString();","      final durum=(d.data()?['callStatus']??'').toString();\n      if(durum=='active'||durum=='ended'||durum=='rejected'||durum=='missed')unawaited(_tone444(false));",1)
region=region.replace('    if(bitiyor||yenidenBaglanmaDenemesi>=3)return;','    if(!_alive444||yenidenBaglanmaDenemesi>=3)return;',1)
# End remote and local media before any network waits.
a=region.index('  Future<void> _uzaktanBitirildi');z=region.index('    if(!mounted)return;',a)
old=region[a:z];i=old.index('    final r=oda;');old=old[:i]+'    await _stopLocal444();\n';region=region[:a]+old+region[z:]
a=region.index('  Future<void> bitir(');z=region.index('    try{',a)
region=region[:z]+'    await _stopLocal444();\n'+region[z:]
a=region.index('    await ngelxArkaPlanAramayiTemizle(widget.roomName);',region.index('  Future<void> bitir('));z=region.index('    if(geriDon&&mounted)',a)
region=region[:a]+region[z:]
# Always dispose resources, including during pending connection. Preserve intentional minimize.
a=region.index('  @override void dispose(){');z=region.index('\n  Widget _efektliVideo',a)
region=region[:a]+'''  @override void dispose(){
    bitiyor=true;
    aramaSureZamanlayici?.cancel();cevapsizZamanlayici?.cancel();yenidenBaglanmaZamanlayici?.cancel();
    aramaDurumAboneligi?.cancel();odaOlaylari?.dispose();odaOlaylari=null;
    if(!kucultuluyor)unawaited(_stopLocal444());
    super.dispose();
  }
'''+region[z:]
# Minimize only fully connected calls. Back during connection cancels instead of orphaning it.
region=region.replace('    kucultuluyor=true;',"    if(oda==null||_connectInFlight444){await bitir();return;}\n    kucultuluyor=true;\n    unawaited(_tone444(false));\n    ngelxCallSession444.minimize(widget.roomName);",1)
# Serialize explicit reconnects and invalidate every awaited connection boundary.
region=region.replace('    final u=FirebaseAuth.instance.currentUser;\n    if(u==null)', '    if(!_alive444||_connectInFlight444)return;\n    final u=FirebaseAuth.instance.currentUser;\n    if(u==null)',1)
region=region.replace('    lk.Room? r;\n    try{','    _connectInFlight444=true;\n    lk.Room? r;\n    try{',1)
region=region.replace('      await _izinleriIste();',"      final initial444=await widget.aramaRef.get().timeout(const Duration(seconds:8));\n      if(!_alive444)return;\n      if(initial444.data()?['callRoomName']!=widget.roomName||!['ringing','active'].contains(initial444.data()?['callStatus'])){await _uzaktanBitirildi('ended');return;}\n      await _izinleriIste();\n      if(!_alive444)return;",1)
region=region.replace("      r=lk.Room(roomOptions:","      if(!_alive444)return;\n      r=lk.Room(roomOptions:",1)
region=region.replace('      r.addListener(_odaDegisti);\n      _aramaOlaylariniBagla(r);\n      await r.connect','      _connecting444=r;\n      r.addListener(_odaDegisti);\n      _aramaOlaylariniBagla(r);\n      await r.connect',1)
region=region.replace('      oda=r;\n      final yerel',"      if(!_alive444){await ngelx444CloseRoom(r);return;}\n      _connecting444=null;\n      oda=r;\n      final yerel",1)
region=region.replace('await yerel.setMicrophoneEnabled(true);','await yerel.setMicrophoneEnabled(mikrofon);\n      if(!_alive444){await ngelx444CloseRoom(r);return;}',1)
region=region.replace('await yerel.setCameraEnabled(true,','await yerel.setCameraEnabled(kamera,',1)
region=region.replace('      await lk.AudioManager.instance.setSpeakerOutputPreferred(true,force:widget.goruntulu);\n      hoparlor=true;','      if(!_alive444){await ngelx444CloseRoom(r);return;}\n      await lk.AudioManager.instance.setSpeakerOutputPreferred(hoparlor);',1)
region=region.replace("      final kayitliOda=(aramaVerisi['callRoomName']??'').toString();","      if(!_alive444){await ngelx444CloseRoom(r);return;}\n      final kayitliOda=(aramaVerisi['callRoomName']??'').toString();\n      if(kayitliOda!=widget.roomName||!['ringing','active'].contains(aramaVerisi['callStatus'])){await _uzaktanBitirildi('ended');return;}",1)
region=region.replace('      if(aktif){\n        final baslangic','      if(aktif){\n        unawaited(_tone444(false));\n        final baslangic',1)
region=region.replace('      }else{\n        aramaSureZamanlayici?.cancel();','      }else{\n        unawaited(_tone444(true));\n        aramaSureZamanlayici?.cancel();',1)
region=region.replace('unawaited(widget.aramaRef.set(durumGuncelleme,SetOptions(merge:true)).timeout','unawaited(_writeCurrent444(durumGuncelleme).timeout',1)
region=region.replace('      if(yeniden&&yenidenBaglanmaDenemesi<3){','      if(_alive444&&yeniden&&yenidenBaglanmaDenemesi<3){',1)
region=region.replace('      }else if(mounted){\n        setState((){baglaniyor=false;yenidenBaglaniyor=false;hata=e.toString()', '      }else if(_alive444){\n        unawaited(_tone444(false));\n        setState((){baglaniyor=false;yenidenBaglaniyor=false;hata=e.toString()',1)
# finally on connection method only.
a=region.index('  Future<void> baglan');z=region.index('\n  lk.VideoTrack?',a);part=region[a:z];i=part.rfind('\n    }\n  }');assert i>=0
part=part[:i]+part[i:].replace('\n    }\n  }','\n    }finally{_connectInFlight444=false;if(identical(_connecting444,r))_connecting444=null;}\n  }',1);region=region[:a]+part+region[z:]
s=s[:a if False else s.index('class _NgelXAramaPageState')]+region+s[b:]
# Route all non-call media play through the same process ownership check.
# Call ringback lives in the call class and is deliberately excluded.
a=s.index('class _NgelXAramaPageState');b=s.index('\nclass ',a+10)
pattern=r'\b([A-Za-z_]\w*(?:\?|!)?)\.play\(\)'
def media(x):return re.sub(pattern,lambda m:'ngelx444MediaPlay('+m[1].replace('?','')+')',x)
s=media(s[:a])+s[a:b]+media(s[b:])
# Do not rewrite the helper into recursion.
s=s.replace('try{await ngelx444MediaPlay(player);}finally','try{await player.play();}finally',1)
p.write_text(s)
for file in Path('app/lib').glob('*.dart'):
 if file.name=='main.dart' or not file.read_text().startswith("part of "):continue
 text=file.read_text();file.write_text(media(text))
# Synthesized original ringback: 425 Hz, one second on, three off.
asset=Path('app/assets/call_ringback444.wav');asset.parent.mkdir(exist_ok=True)
with wave.open(str(asset),'wb') as w:
 w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000)
 frames=[]
 for i in range(64000):
  t=i/16000;edge=min(1,t/.02,(1-t)/.02) if t<1 else 0
  frames.append(struct.pack('<h',int(5500*max(0,edge)*math.sin(2*math.pi*425*t))))
 w.writeframes(b''.join(frames))
p=Path('app/pubspec.yaml');s=p.read_text();s=s.replace('  assets:\n','  assets:\n    - assets/call_ringback444.wav\n',1);p.write_text(s)
print('Build444 call ownership, immediate local teardown, connection cancellation, media priority and ringback applied')
