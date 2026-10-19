#!/usr/bin/env python3
"""Incremental presentation fixes after540; keep existing media and role flows."""
from pathlib import Path
MARK='// Build541 continuity'
def once(s,a,b):
    if s.count(a)!=1:raise RuntimeError('Build541 anchor mismatch: '+a[:90])
    return s.replace(a,b,1)
def live(s):
    s=once(s,"const Text('● CANLI',style:TextStyle(color:Color(0xFFFF2851),fontWeight:FontWeight.w800,fontSize:11))", "Container(padding:const EdgeInsets.symmetric(horizontal:9,vertical:5),decoration:BoxDecoration(color:const Color(0xFFE91948),borderRadius:BorderRadius.circular(7)),child:const Text('● CANLI',style:TextStyle(color:Colors.white,fontWeight:FontWeight.w800,fontSize:11)))")
    s=once(s,"String yazi='Bağlı';", "String yazi=_goruntu()==null?'Görüntü bekleniyor':'Bağlı';")
    s=once(s,"Color renk=const Color(0xFF27D17F);", "Color renk=_goruntu()==null?const Color(0xFFFFB020):const Color(0xFF27D17F);")
    s=once(s,"label:'Gül',icon:const Text('🌹',style:TextStyle(fontSize:27)),\n          onPressed:widget.yayinSahibi?_giftHistory512:hediyeGonderiliyor?null:_hediyePaneli", "label:'Gül',icon:const Text('🌹',style:TextStyle(fontSize:27)),\n          onPressed:widget.yayinSahibi?_giftHistory512:hediyeGonderiliyor?null:()=>_hediyeGonder('Gül','🌹',1)")
    # Keep the existing roles and all callbacks; theme only the expanded tools.
    s=once(s,'if(_toolsOpen540) Container(', 'if(_toolsOpen540) Theme(data:ThemeData.dark(),child:Container(')
    a=s.index('if(_toolsOpen540) Theme(');b=s.index('    Ngelx540LiveBar',a)
    part=s[a:b].rstrip();assert part.endswith('),')
    part=part[:-2]+')),'
    part=part.replace('color:Colors.white','color:const Color(0xDD151C2B)').replace('Colors.black87','Colors.white').replace('Colors.black54','Colors.white70')
    s=s[:a]+part+'\n'+s[b:]
    return s

def main(s):
    # A minimize must show the in-app card, irrespective of native overlay permission.
    s=once(s,'    ngelx448HideCallCard(widget.roomName);','    ngelx448HiddenCallCard.value=null;')
    s=once(s,'const Ngelx445CallOverlay()', 'const Ngelx445CallOverlay(),const Ngelx541GlobalCallStrip()')
    return s

def model(s):
    a=s.index('class Ngelx445CallOverlay');b=s.index('class Ngelx445InboxCallBanner',a)
    body=s[a:b]
    avatar="CircleAvatar(radius:28,backgroundColor:const Color(0xFF6F4AB2),backgroundImage:detail.photo.isEmpty?null:NgelXAgImageProvider(detail.photo),child:detail.photo.isEmpty?Icon(detail.video?Icons.videocam:Icons.call,color:Colors.white,size:20):null)"
    body=once(body,avatar,"SizedBox(height:70,width:double.infinity,child:ClipRRect(borderRadius:BorderRadius.circular(12),child:_ngelx541MiniVideo(room)??"+avatar+"))")
    helper='''lk.VideoTrack? _ngelx541RemoteVideo(lk.Room room){
  for(final person in room.remoteParticipants.values){
    for(final publication in person.videoTrackPublications){
      if(publication.subscribed&&!publication.muted&&publication.track is lk.VideoTrack)return publication.track as lk.VideoTrack;
    }
  }
  return null;
}
Widget? _ngelx541MiniVideo(lk.Room room){
  final track=_ngelx541RemoteVideo(room);
  return track==null?null:lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover);
}
'''
    s=s[:a]+helper+body+s[b:]
    s+='''
class Ngelx541GlobalCallStrip extends StatelessWidget{
  const Ngelx541GlobalCallStrip({super.key});
  @override Widget build(BuildContext context)=>ValueListenableBuilder<int>(valueListenable:ngelx445CallRevision,builder:(_,revision,__){
    final name=ngelxCallSession444.room,detail=ngelx445CallDetails[name];
    if(name==null||detail==null||!ngelxCallSession444.background||!_ngelxArkaPlanAramaOdalari.containsKey(name)||detail.uid!=FirebaseAuth.instance.currentUser?.uid)return const SizedBox.shrink();
    return Positioned(top:MediaQuery.paddingOf(context).top,left:0,right:0,child:Material(color:const Color(0xFF21852C),child:InkWell(onTap:()=>ngelx445ReturnCall(name),child:Padding(padding:const EdgeInsets.symmetric(horizontal:12,vertical:7),child:Row(children:[Icon(detail.video?Icons.videocam:Icons.call,color:Colors.white,size:16),const SizedBox(width:7),Expanded(child:Text('${detail.title} · Aramaya dönmek için dokun',maxLines:1,overflow:TextOverflow.ellipsis,style:const TextStyle(color:Colors.white,fontSize:12,fontWeight:FontWeight.w700)))])))));
  });
}
''' 
    a=s.index('class Ngelx445InboxCallBanner');b=s.index('Future<void> ngelx445OpenCallChat',a)
    body=s[a:b].replace('Material(color:mor,','Material(color:const Color(0xFF21852C),')
    s=s[:a]+body+s[b:]
    return s

def audio(s):
    a=s.index('  Widget koltuk(String id)');b=s.index('  @override void dispose()',a)
    body=s[a:b]
    # Preserve data subscriptions, seat count, request and moderator callbacks.
    body=body.replace('Color(0xFFF8F6FA)','Color(0xFF263B49)').replace('Color(0xFFEDEAF0)','Color(0xFF344C59)').replace('Color(0xFFECE7F0)','Color(0xFF263B49)').replace('Color(0xFFF8F4FD)','Color(0x00000000)')
    body=body.replace('borderRadius:BorderRadius.circular(18)','borderRadius:BorderRadius.circular(70)')
    body=body.replace('CircleAvatar(radius:24,','CircleAvatar(radius:34,')
    body=body.replace("final rol=admin?'ADMIN'", "final rol=admin?'Davet sahibi'")
    body=body.replace('Colors.black87','Colors.white').replace('Colors.black54','Colors.white70').replace('Colors.black45','Colors.white60').replace('Colors.black38','Colors.white54').replace('Colors.black26','Colors.white54')
    body=body.replace('Scaffold(backgroundColor:Colors.white,appBar:AppBar(backgroundColor:Colors.white,foregroundColor:Colors.black,','Scaffold(backgroundColor:const Color(0xFF031923),appBar:AppBar(backgroundColor:const Color(0xFF031923),foregroundColor:Colors.white,')
    body=body.replace('Color(0xFFF6F0FF)','Color(0xFF102B39)').replace('color:Colors.black,fontSize:20','color:Colors.white,fontSize:20').replace('Color(0xFFFDFBFF)','Color(0xFF0C2430)').replace('Color(0xFFEDE8F2)','Color(0xFF173443)')
    body=body.replace('.clamp(3,ngelxSesliMaksKonusmaci)', '.clamp(9,ngelxSesliMaksKonusmaci)')
    body=body.replace('return koltuk(id);',"return id.isEmpty?InkWell(borderRadius:BorderRadius.circular(70),onTap:bitti?null:yoneticiyim?istekler:sozIste,child:koltuk(id)):koltuk(id);")
    body=body.replace('childAspectRatio:.92','childAspectRatio:.88')
    s=s[:a]+body+s[b:]
    return s

def chat(s):
    a=s.index('class _NgelxSesliInlineSohbetState');b=s.index('class NgelxYerlesikMuzik',a)
    body=s[a:b].replace('height:230','height:210')
    body=body.replace('Colors.white,border:Border','Color(0xFF031923),border:Border').replace('Color(0xFFEDE8F2)','Color(0xFF173443)')
    body=body.replace('Color(0xFFF0E8FF)','Color(0x332A3949)').replace('Color(0xFFF5F5F7)','Color(0x222A3949)').replace('Color(0xFFF5F5F8)','Color(0xFF233441)')
    body=body.replace('Colors.black87','Colors.white').replace('Colors.black38','Colors.white60')
    return s[:a]+body+s[b:]
TRANSFORMS={'live_broadcast_studio.dart':live,'main.dart':main,'build445_inbox_model.dart':model,'audio_live_rooms.dart':audio,'audio_live_rooms_pro.dart':chat}
def transform(s,fn):return s if MARK in s else fn(s)+'\n'+MARK+'\n'
if __name__=='__main__':
    changes=[]
    for name,fn in TRANSFORMS.items():
        p=Path('app/lib')/name;s=p.read_text();out=transform(s,fn);assert transform(out,fn)==out;changes.append((p,out))
    for p,s in changes:p.write_text(s)
    print('Build541 continuity applied atomically')
