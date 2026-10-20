#!/usr/bin/env python3
"""Guarded incremental changes to the fully assembled, working Build541 app."""
from pathlib import Path
MARK='// Build542 call refinements'
def once(s,a,b):
    if s.count(a)!=1: raise RuntimeError('Build542 anchor mismatch: '+a[:100])
    return s.replace(a,b,1)
def main(s):
    s=once(s,"part 'build517_group_leave.dart';","part 'build517_group_leave.dart';\npart 'build542_pending_leave.dart';")
    s=once(s,'const Ngelx445InboxCallBanner(),','// Build542: the group row already provides KATIL.')
    s=once(s,"        'emailVerificationRequired': true,","        'emailVerificationRequired': true,\n        'allowProfileCapture': true,")
    a=s.index('              if(uyeMi&&ngelx440CallJoinable(tv,DateTime.now()))');b=s.index("              if(List<String>.from(tv['admins']",a)
    s=s[:a]+s[b:]
    # Keep the original guarded route and the group row's independently sized trailing column.
    a=s.index('                  if(grup){');b=s.index('                  }',a)
    part=s[a:b]
    part=once(part,'trailing:ngelx445CallTrailing(v,SizedBox(width:64', 'trailing:ngelx542GroupTrailing(v,()=>sohbetiAc(d.id,GrupSohbetPage(chatId:d.id,ad:ad,foto:foto,joinOnOpen542:true)),SizedBox(width:64')
    s=s[:a]+part+s[b:]
    s=once(s,"this.foto='',this.aktifAramadanAcildi=false});\n  @override State<GrupSohbetPage>","this.foto='',this.aktifAramadanAcildi=false,this.joinOnOpen542=false});\n  final bool joinOnOpen542;\n  @override State<GrupSohbetPage>")
    a=s.index('class _GrupSohbetPageState');b=s.index('  @override void initState(){',a)+len('  @override void initState(){')
    s=s[:b]+"\n    if(widget.joinOnOpen542)WidgetsBinding.instance.addPostFrameCallback((_)async{\n      try{\n        final snap=await chatRef.get(const GetOptions(source:Source.server));\n        if(mounted&&snap.exists)await aktifGrupAramasinaKatil(snap.data()!);\n      }catch(_){if(mounted)ngelxDurumMesaji(context,'Aramaya katılınamadı. Tekrar dene.',tip:'hata');}\n    });\n"+s[b:]
    a=s.index('  Future<void> aktifGrupAramasinaKatil(');b=s.index('  Future<void>',a+20)
    part=s[a:b]
    part=once(part,"    final grupBelgesi=await chatRef.get();", "    if(!await ngelx542PrepareManualJoin(oda,ben)){if(mounted)ngelxDurumMesaji(context,'Önceki ayrılma kaydı gönderilemedi. Bağlantını kontrol edip tekrar dene.',tip:'hata');return;}\n    final grupBelgesi=await chatRef.get(const GetOptions(source:Source.server));\n    if(!mounted)return;\n    v=grupBelgesi.data()??<String,dynamic>{};\n    if(v['callRoomName']!=oda)return;")
    part=once(part,'    try{\n      await chatRef.set({', "    try{\n      if(v['callExitedRoomName']==oda&&List<String>.from(v['callExitedUids']??const[]).contains(ben)){\n        if(!await ngelx534ConfirmAndRejoinGroupCall(context,chatRef,oda,cancelled:()=>!mounted))return;\n      }\n      if(!mounted||FirebaseAuth.instance.currentUser?.uid!=ben)return;\n      await chatRef.set({")
    s=s[:a]+part+s[b:]
    a=s.index('  Future<void> _confirmGroupExit517()async{');b=s.index('  Widget _ngelx465HangupControl()',a)
    s=s[:a]+'''  Future<void> _confirmGroupExit517()async{
    if(!bitiyor)await bitir();
  }

'''+s[b:]
    a=s.index('              // Build520: system PiP uses');b=s.index('            ]),',a)
    s=s[:a]+s[b:]
    s=once(s,'child:Wrap(alignment:WrapAlignment.center,spacing:7,runSpacing:5,children:[','child:Wrap(alignment:WrapAlignment.center,spacing:12,runSpacing:10,children:[')
    s=once(s,"              if(widget.goruntulu&&kamera)_aramaKontrol(Icons.cameraswitch_rounded,'Çevir',kameraCevir,true),",'')
    # Preserve camera flipping as a long press on the video control, keeping five buttons.
    a=s.index('  Widget _ngelx465HangupControl()');b=s.index('\nclass GrupBilgiPage',a)
    body=s[a:b].replace('width:48,height:48','width:44,height:44')
    body=body.replace("Text(_ngelx438Ui(label),style:","Text(_ngelx438Ui(label),maxLines:1,overflow:TextOverflow.ellipsis,style:")
    body=body.replace('onTap:()=>onTap(),','onTap:()=>onTap(),\n      onLongPress:label==\'Kamera\'?()=>unawaited(kameraCevir()):null,')
    s=s[:a]+body+s[b:]
    old='mainAxisExtent:katilimcilar.length>=7?((constraints.maxHeight-42)/4).clamp(88.0,140.0).toDouble():null,childAspectRatio:katilimcilar.length<=2?1.02:.82'
    s=once(s,old,'mainAxisExtent:((constraints.maxHeight-18-10*((katilimcilar.length/sutun).ceil()-1))/(katilimcilar.length/sutun).ceil()).clamp(130.0,1200.0).toDouble()')
    # A publication can arrive after setCameraEnabled completes: wait for the real track,
    # rather than immediately disabling a camera that is still starting.
    s=once(s,'  // Build507: explicit private voice-call camera opt-in;', '''  Future<void> _waitCamera542(lk.LocalParticipant local,bool enabled)async{
    final deadline=DateTime.now().add(const Duration(seconds:3));
    while(mounted&&!bitiyor&&identical(oda?.localParticipant,local)){
      final published=local.videoTrackPublications.any((p)=>!p.muted&&p.track is lk.VideoTrack);
      if(local.isCameraEnabled()==enabled&&published==enabled)return;
      if(DateTime.now().isAfter(deadline))return;
      await Future<void>.delayed(const Duration(milliseconds:80));
    }
  }
  // Build507: explicit private voice-call camera opt-in;''')
    s=once(s,'      final published=local.videoTrackPublications.any(\n', '      await _waitCamera542(local,turnOn);\n      if(!mounted||bitiyor||!identical(oda?.localParticipant,local))return;\n      final published=local.videoTrackPublications.any(\n')
    s=once(s,'      final trackPublished=local.videoTrackPublications.any(', '      await _waitCamera542(local,enable);\n      if(!mounted||bitiyor||!identical(oda,room))return;\n      final trackPublished=local.videoTrackPublications.any(')
    # Preserve the busy guards until the actual platform operation settles. Never race
    # an abandoned timeout with another camera mutation or touch the microphone.
    a=s.index('  Future<void> kameraDegistir()async{');b=s.index('  Future<void> kameraCevir()',a)
    s=s[:a]+'''  bool _videoCameraBusy542=false;
  Future<void> kameraDegistir()async{
    final local=oda?.localParticipant;
    if(local==null||_videoCameraBusy542||bitiyor||kucultuluyor)return;
    final yeni=!local.isCameraEnabled();
    setState(()=>_videoCameraBusy542=true);
    try{
      if(yeni&&!(await Permission.camera.request()).isGranted)return;
      if(!mounted||bitiyor||!identical(oda?.localParticipant,local))return;
      await local.setCameraEnabled(yeni,cameraCaptureOptions:const lk.CameraCaptureOptions(params:lk.VideoParametersPresets.h720_169,maxFrameRate:24.0,stopCameraCaptureOnMute:true));
      await _waitCamera542(local,yeni);
      if(mounted&&identical(oda?.localParticipant,local))setState(()=>kamera=local.isCameraEnabled());
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content:Text('Kamera açılamadı. Görüşme devam ediyor. Tekrar deneyebilirsin.')));
    }finally{if(mounted)setState(()=>_videoCameraBusy542=false);}
  }
'''+s[b:]
    a=s.index('  Future<void> bitir({bool geriDon=true})async{');b=s.index('  @override void dispose()',a)
    body=s[a:b].replace('await ngelx517LeaveGroupCall(', 'await ngelx542LeaveGroupCall(')
    body=body.replace("Arama kapandı. Sunucu kaydı güncellenemedi; yeniden dene.","Aramadan çıktın. Ayrılma kaydı bağlantı gelince tekrar gönderilecek.")
    s=s[:a]+body+s[b:]
    # Local camera quality follows the existing network adaptation / subscription rules.
    a=s.index('class _NgelXAramaPageState');b=s.index('class GrupBilgiPage',a)
    body=s[a:b].replace('lk.VideoParametersPresets.h360_169','lk.VideoParametersPresets.h720_169')
    body=body.replace("_voiceGroupVideoOn494?'Görüntüyü kapat':'Görüntüyü aç'", "_voiceGroupCameraBusy517?'Açılıyor…':_voiceGroupVideoOn494?'Görüntüyü kapat':'Görüntüyü aç'")
    body=body.replace("_privateVoiceCameraOn507?'Görüntüyü kapat':'Görüntüyü aç'", "_privateVoiceCameraBusy507?'Açılıyor…':_privateVoiceCameraOn507?'Görüntüyü kapat':'Görüntüyü aç'")
    s=s[:a]+body+s[b:]
    return s

def rejoin(s):
    a=s.index('  final approved=await showDialog<bool>(');b=s.index('  return ngelx534ExplicitRejoinGroupCall(',a)
    s=s[:a]+'''  // The deliberate KATIL tap is the user's join intent. Automatic reconnect
  // remains rejected by baglan(yeniden:true), before this wrapper is called.
  const approved=true;
  if(!context.mounted||cancelled?.call()==true)return false;
'''+s[b:]
    return s

def model(s):
    # Both historical friendship records and current profile arrays are authoritative.
    # Restore peers even when a legacy account's mirrored friends array is missing.
    s=once(s,'super.initState();_noteClock=','super.initState();unawaited(ngelx542RetryPendingLeaves());_noteClock=')
    s=once(s,"  late final _stories=", "  late final _friendships=FirebaseFirestore.instance.collection('friendships').where('members',arrayContains:widget.uid).snapshots();\n  late final _stories=")
    a=s.index('      final friends=Set<String>');b=s.index('      return StreamBuilder<QuerySnapshot',a)
    s=s[:a]+'''      return StreamBuilder<QuerySnapshot<Map<String,dynamic>>>(stream:_friendships,builder:(_,relationships){
      final friends=<String>{...List<String>.from(data['friends']??const[])};
      for(final relation in relationships.data?.docs??<QueryDocumentSnapshot<Map<String,dynamic>>>[]){
        final record=relation.data();
        if(record['active']==true)friends.addAll(List<String>.from(record['members']??const[]));
      }
      friends.remove(widget.uid);
      final ids=<String>{widget.uid,...friends}
        .where((id)=>id.isNotEmpty&&!blocked.contains(id)).toList();
'''+s[b:]
    a=s.index('class Ngelx445FriendsStrip');b=s.index('class ',s.index('  @override Widget build(BuildContext context)=>StreamBuilder',a)+1) if False else s.index('class Ngelx445CallOverlay')
    # Close the additional relationship stream just before the original user stream.
    end=s.index('\n}\n',s.index("key:PageStorageKey('inbox-friends-"))
    part=s[:end];pos=part.rfind('    });');assert pos!=-1
    s=s[:pos]+'      });\n'+s[pos:]
    s=once(s,'left:0,right:0,height:40','left:0,right:0,height:64')
    s=once(s,'top:visible?40:0','top:visible?64:0')
    s=once(s,"Expanded(child:Text('${detail.title} · Aramaya dönmek için dokun',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:12,fontWeight:FontWeight.w700)))", "Expanded(child:Column(mainAxisAlignment:MainAxisAlignment.center,crossAxisAlignment:CrossAxisAlignment.start,children:[Text(detail.title,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:14,fontWeight:FontWeight.w700)),const Text('Aramaya dönmek için dokun',style:TextStyle(color:Colors.white,fontSize:12))]))")
    s+="""
Widget ngelx542GroupTrailing(Map<String,dynamic> chat,VoidCallback join,Widget usual){
  final me=FirebaseAuth.instance.currentUser?.uid;
  if(me==null||chat['isGroup']!=true||
     !List<String>.from(chat['members']??const[]).contains(me)||
     !ngelx440CallJoinable(chat,DateTime.now()))return usual;
  return SizedBox(width:100,child:Column(mainAxisSize:MainAxisSize.min,children:[
    FilledButton.icon(style:FilledButton.styleFrom(backgroundColor:const Color(0xFF21852C),foregroundColor:Colors.white,padding:const EdgeInsets.symmetric(horizontal:10,vertical:8)),
      onPressed:join,icon:const Icon(Icons.call,size:16),label:const Text('KATIL',style:TextStyle(fontSize:12,fontWeight:FontWeight.w800))),
  ]));
}
"""
    return s

def leave(s):
    for marker in ["call_end_$roomName","call_leave_${roomName}_$uid"]:
        a=s.index("await ref.collection('messages').doc('"+marker+"').set(<String,dynamic>{")
        b=s.index('},SetOptions(merge:true));',a)+len('},SetOptions(merge:true));')
        part=s[a:b].replace("await ref.collection('messages').doc('","await ngelx542QueueReceipt(ref.collection('messages').doc('",1).replace("').set(<String,dynamic>{","'),<String,dynamic>{",1).replace('},SetOptions(merge:true));','});')
        s=s[:a]+part+s[b:]
    return s

TRANSFORMS={'main.dart':main,'build445_inbox_model.dart':model,'build534_explicit_group_rejoin.dart':rejoin,'build517_group_leave.dart':leave}
def transform(s,fn):return s if MARK in s else fn(s)+'\n'+MARK+'\n'
if __name__=='__main__':
    changes=[]
    for name,fn in TRANSFORMS.items():
        p=Path('app/lib')/name;s=p.read_text();out=transform(s,fn);assert transform(out,fn)==out;changes.append((p,out))
    for p,s in changes:p.write_text(s)
    print('Build542 call refinements applied atomically')
