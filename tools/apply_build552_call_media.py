from pathlib import Path
import sys
TAG='// Build552 call lifecycle media and unread clarity'
def once(s,a,b):
 if s.count(a)!=1:raise RuntimeError(f'Build552 anchor {s.count(a)}: {a[:100]}')
 return s.replace(a,b,1)
def apply(root=Path('app/lib')):
 p=root/'main.dart';s=p.read_text()
 if TAG in s:return
 s=once(s,"import 'build551_media.dart';","import 'build551_media.dart';\nimport 'build552_policy.dart';")
 s=once(s,'  Future<void> _videoCallKeepScreen492(bool enabled)async{','  bool? _keepScreen552;\n  Future<void> _videoCallKeepScreen492(bool enabled)async{')
 s=once(s,"    try{\n      await const MethodChannel('com.nnentx.ngelx_app/call_screen')","    if(_keepScreen552==enabled)return;\n    _keepScreen552=enabled;\n    try{\n      await const MethodChannel('com.nnentx.ngelx_app/call_screen')")
 s=once(s,'  void _odaDegisti(){\n    if(!_alive444)return;','  void _odaDegisti(){\n    if(!_alive444)return;\n    unawaited(_videoCallKeepScreen492(true));')
 s=once(s,'    if(!Platform.isAndroid||!widget.goruntulu)return;','''    if(!Platform.isAndroid)return;
    final state=WidgetsBinding.instance.lifecycleState;
    final r=oda;
    final people=<lk.Participant>[if(r?.localParticipant!=null)r!.localParticipant!,
      ...?r?.remoteParticipants.values];
    final video=widget.goruntulu||people.any((p)=>p.videoTrackPublications.any(
      (t)=>!t.muted&&t.track is lk.VideoTrack));
    enabled=enabled&&video&&!bitiyor&&!kucultuluyor&&bitisDurumu==null&&
      (state==null||ngelx552Visible(state));''')
 s=once(s,'state==AppLifecycleState.resumed&&!kucultuluyor&&!bitiyor&&bitisDurumu==null','ngelx552Visible(state)&&!kucultuluyor&&!bitiyor&&bitisDurumu==null')
 s=once(s,'final sutun=katilimcilar.length<=1?1:katilimcilar.length>=7?3:2;','final sutun=ngelx552Columns(katilimcilar.length);')
 s=once(s,'else Center(child:Ngelx446SpeakingRing(participant:p,child:_katilimciAvatar(p,yerel:yerel,radius:oda!.remoteParticipants.length>=6?18:45))),','''else LayoutBuilder(builder:(_,box){
          final label=_videoCallControlsVisible493?48.0:0.0;
          final radius=math.min((box.maxHeight-label-8)/2,(box.maxWidth-16)/2).clamp(8.0,45.0).toDouble();
          return Padding(padding:EdgeInsets.only(bottom:label),child:Center(
            child:Ngelx446SpeakingRing(participant:p,child:_katilimciAvatar(p,yerel:yerel,radius:radius))));
        }),''')

 s=once(s,'final normal=TextStyle(fontWeight:okundu?FontWeight.w400:FontWeight.w600);\n    const kalin=TextStyle(color:mor,fontWeight:FontWeight.w900);\n    const grupStil=TextStyle(color:ngelxGroupGreen,fontWeight:FontWeight.w900);','''final normal=TextStyle(color:okundu?Colors.black54:const Color(0xFF18131F),fontWeight:okundu?FontWeight.w400:FontWeight.w700);
    final kalin=TextStyle(color:okundu?const Color(0xFF8B789F):const Color(0xFF60309A),fontWeight:okundu?FontWeight.w500:FontWeight.w900);
    final grupStil=TextStyle(color:okundu?const Color(0xFF638775):const Color(0xFF08763C),fontWeight:okundu?FontWeight.w500:FontWeight.w900);''')
 a=s.index('// Only mark rows intersecting the viewport');b=s.index('\nbool ngelxBildirimKaydiGecerli',a)
 s=s[:a]+'''// Read status changes only on explicit open or mark-all action.
class NgelXGorulenBildirim extends StatelessWidget{
 final QueryDocumentSnapshot<Map<String,dynamic>> bildirim;
 final Widget child;
 const NgelXGorulenBildirim({super.key,required this.bildirim,required this.child});
 @override Widget build(BuildContext context)=>child;
}
'''+s[b:]
 s=once(s,'        _ngelx464BellegeAl(url,bytes);\n        return bytes;','''        ui.Codec? codec;
        try{
          codec=await ui.instantiateImageCodec(bytes);
          final frame=await codec.getNextFrame();frame.image.dispose();
          _ngelx464BellegeAl(url,bytes);return bytes;
        }catch(_){await _ngelx464GenelResimCache.removeFile(url);}
        finally{codec?.dispose();}''')
 s=once(s,'  await ready.future;','''  try{await ready.future.timeout(const Duration(seconds:8));}
  catch(_){
    // A timed-out queued image must not occupy a download slot later.
    if(!_ngelx464BeklemeSirasi.remove(ready))_ngelx464IndirmeSirasiBirak();
    rethrow;
  }''')
 # Disk persistence is optional and must not delay first paint.
 s=once(s,'''          try{await _ngelx464GenelResimCache.putFile(
              url,bytes,maxAge:const Duration(days:3));}catch(_){}''','''          unawaited(_ngelx464GenelResimCache.putFile(
              url,bytes,maxAge:const Duration(days:3)).then<void>((_){}).catchError((_){ }));''')
 p.write_text(s+'\n'+TAG+'\n')
 p=root/'build446_call_lifecycle.dart';s=p.read_text()
 s=s.replace('WidgetsBinding.instance.lifecycleState==AppLifecycleState.resumed','ngelx552Visible(WidgetsBinding.instance.lifecycleState!)')
 s=once(s,'    _foreground=state==AppLifecycleState.resumed;\n    final foreground=_foreground;','''    // Android volume panels are transient inactive overlays.
    if(state==AppLifecycleState.inactive)return;
    final next=ngelx552Visible(state);
    if(next==_foreground)return;
    _foreground=next;
    final foreground=_foreground;''');p.write_text(s)
 p=root/'build551_widgets.dart';p.write_text(p.read_text().replace('.clamp(130.0,1200.0)','.clamp(1.0,1200.0)'))
 p=root/'build548_widgets.dart';s=p.read_text();a=s.index('class _Ngelx548ChatPhotoState');b=s.index('// Private prejoin preview',a)
 p.write_text(s[:a]+Path('tools/build552_photo_state.dart').read_text()+'\n'+s[b:])
 p=root/'build543_pip_participants.dart';s=p.read_text()
 s=once(s,'final columns=count>=10?4:count>=5?3:count==1?1:2;','final columns=ngelx552Columns(count);')
 s=s.replace('final lk.Room room;final String title;','final lk.Room room;final String title;final VoidCallback? onExpand;').replace('required this.room,required this.title});','required this.room,required this.title,this.onExpand});')
 s=once(s,"        Text('$title · ${people.length} kişi',maxLines:1,overflow:TextOverflow.ellipsis,\n          style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w700)),","""        Row(children:[Expanded(child:Text('$title · ${people.length} kişi',maxLines:1,overflow:TextOverflow.ellipsis,
          style:const TextStyle(color:Colors.white,fontSize:11,fontWeight:FontWeight.w700))),
          if(onExpand!=null)Semantics(label:'Aramayı büyüt',button:true,child:InkWell(onTap:onExpand,
            child:const Padding(padding:EdgeInsets.all(3),child:Icon(Icons.open_in_full,size:15,color:Colors.white))))]),""")
 s=s.replace('padding:const EdgeInsets.all(5)','padding:const EdgeInsets.all(2)')
 s=once(s,'borderRadius:BorderRadius.circular(6),child:Column(children:[\n        Expanded(child:video!=null?', 'borderRadius:BorderRadius.circular(6),child:Stack(fit:StackFit.expand,children:[\n        video!=null?')
 s=once(s,"          })),\n        Text(name,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:9)),","""          }),
        Positioned(left:2,right:2,bottom:2,child:Container(padding:const EdgeInsets.symmetric(horizontal:3,vertical:1),
          decoration:BoxDecoration(color:Colors.black54,borderRadius:BorderRadius.circular(4)),
          child:Text(name,maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:9)))),""");p.write_text(s)
 p=root/'build445_inbox_model.dart';s=p.read_text()
 s=once(s,'final width=(screen.width-16).clamp(112.0,156.0).toDouble();','''final width=(screen.width-16).clamp(112.0,180.0).toDouble();
    final seats=room.remoteParticipants.length+(room.localParticipant==null?0:1);
    final previewHeight=seats>4?220.0:seats>2?165.0:130.0;
    final cardHeight=previewHeight+56;''')
 s=once(s,'Offset bounded(Offset p)=>ngelx540BoundMini(p,screen,padding,keyboard,width);','''Offset bounded(Offset p){
      final base=ngelx540BoundMini(p,screen,padding,keyboard,width);
      final top=padding.top+8;
      final bottom=math.max(top,screen.height-padding.bottom-keyboard-cardHeight-8);
      return Offset(base.dx,base.dy.clamp(top,bottom).toDouble());
    }''')
 s=s.replace('child:Container(padding:const EdgeInsets.all(10),decoration:BoxDecoration(color:const Color(0xFF39206F)','child:Container(padding:const EdgeInsets.all(3),decoration:BoxDecoration(color:const Color(0xFF39206F)')
 s=once(s,'SizedBox(height:130,width:double.infinity','SizedBox(height:previewHeight,width:double.infinity')
 s=once(s,'child:Ngelx543MiniCall(room:room,title:detail.title)','child:Ngelx543MiniCall(room:room,title:detail.title,onExpand:()=>ngelx445ReturnCall(name))')
 s=once(s,'const SizedBox(height:7),Text(duration','const SizedBox(height:2),Text(duration');p.write_text(s)
 (root/'build552_policy.dart').write_text(Path('tools/build552_policy.dart').read_text())
if __name__=='__main__':apply(Path(sys.argv[1]) if len(sys.argv)>1 else Path('app/lib'))
