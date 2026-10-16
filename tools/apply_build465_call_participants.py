#!/usr/bin/env python3
"""Build465 call UI: reversible per-listener remote audio and full square avatars.

A remote participant's microphone cannot be forcibly re-enabled by a peer.
Instead, this menu unsubscribes/subscribes audio on the *local listener* and
explicitly labels that scope. It never modifies Firestore or another user's mic.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")
START="class _NgelXAramaPageState"
VOICE="  Widget _grupSesliKatilimci(lk.Participant p,{bool yerel=false}){"
NEXT="  Widget _grupAramaAlani(){"
VIDEO="  Widget _katilimciKutusu(lk.Participant p,{bool yerel=false}){"
VOICE_OLD="""            shape:BoxShape.circle,
            gradient:aktif?const LinearGradient(colors:[Color(0xFFB479FF),Color(0xFF6F49E8)]):null,"""
VOICE_NEW="""            // Build465: show the complete portrait within a rounded square.
            borderRadius:BorderRadius.circular(20),
            gradient:aktif?const LinearGradient(colors:[Color(0xFFB479FF),Color(0xFF6F49E8)]):null,"""

HELPERS="""  // Build465: only this listener can mute and restore a remote audio feed.
  Future<void> _ngelx465SetRemoteAudio(lk.Participant person,bool enable)async{
    if(person is! lk.RemoteParticipant)return;
    final audio=person.audioTrackPublications;
    if(audio.isEmpty){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Katılımcının ses bağlantısı henüz hazır değil.')),
      );
      return;
    }
    try{
      for(final publication in audio){
        if(enable){await publication.subscribe();}
        else{await publication.unsubscribe();}
      }
      if(mounted)setState((){});
    }catch(_){
      if(mounted)ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content:Text('Ses ayarı değiştirilemedi. Tekrar dene.')),
      );
    }
  }
  Widget _ngelx465RemoteAudioMenu(lk.Participant person){
    if(person is! lk.RemoteParticipant)return const SizedBox.shrink();
    final audio=person.audioTrackPublications;
    final locallyMuted=audio.isNotEmpty&&audio.every((p)=>!p.subscribed);
    return PopupMenuButton<bool>(
      tooltip:'Katılımcı sesi (yalnızca senin için)',
      icon:const Icon(Icons.more_vert_rounded,color:Colors.white,size:20),
      color:const Color(0xFF2C2142),
      onSelected:(enabled)=>_ngelx465SetRemoteAudio(person,enabled),
      itemBuilder:(_)=>[
        PopupMenuItem<bool>(
          value:locallyMuted,
          child:Row(mainAxisSize:MainAxisSize.min,children:[
            Icon(locallyMuted?Icons.volume_up_rounded:Icons.volume_off_rounded,color:Colors.white70,size:19),
            const SizedBox(width:10),
            Text(locallyMuted?'Sesi yeniden aç (benim için)':'Sustur (benim için)',
              style:const TextStyle(color:Colors.white)),
          ]),
        ),
      ],
    );
  }

  Widget _ngelx465SquareCallAvatar(lk.Participant p,{bool yerel=false,double size=86}){
    final id=p.identity.toString();
    final ad=_katilimciAdi(p,yerel:yerel);
    Widget content(String url)=>SizedBox(
      width:size,height:size,
      child:ClipRRect(
        borderRadius:BorderRadius.circular(17),
        child:url.isEmpty
          ?Container(color:const Color(0xFF332450),alignment:Alignment.center,
              child:Text(ad.isNotEmpty?ad[0].toUpperCase():'N',
                style:TextStyle(color:Colors.white,fontSize:size*.38,fontWeight:FontWeight.w800)))
          :Image(image:NgelXAgImageProvider(url),fit:BoxFit.contain,width:size,height:size,
              errorBuilder:(_,__,___)=>Container(color:const Color(0xFF332450),
                alignment:Alignment.center,child:const Icon(Icons.person_rounded,color:Colors.white70))),
      ),
    );
    if(yerel)return content(FirebaseAuth.instance.currentUser?.photoURL??'');
    return FutureBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      future:_aramaProfil(id),
      builder:(_,snapshot)=>content((snapshot.data?.data()?['photoUrl']??'').toString()),
    );
  }

"""

def once(s,old,new,label):
    n=s.count(old)
    if n!=1:raise RuntimeError(f"Build465 group call {label}: anchor count {n}")
    return s.replace(old,new,1)

def transform(src):
    if "// Build465: only this listener can mute" in src:return src
    # The call widget is before both the conversation pages in Build465.
    begin=src.index(VOICE)
    end=src.index(NEXT,begin)
    region=src[begin:end]
    region=once(region,VOICE_OLD,VOICE_NEW,"rounded square")
    region=once(region,"_katilimciAvatar(p,yerel:yerel,radius:43)",
                "_ngelx465SquareCallAvatar(p,yerel:yerel,size:86)",
                "unclipped voice avatar")
    region=once(region,
      "            Positioned(right:-2,bottom:2,child:CircleAvatar(",
      "            if(!yerel)Positioned(right:-10,top:-14,child:_ngelx465RemoteAudioMenu(p)),\n"
      "            Positioned(right:-2,bottom:2,child:CircleAvatar(",
      "voice menu")
    src=src[:begin]+HELPERS+region+src[end:]
    begin=src.index(VIDEO)
    end=src.index(VOICE,begin)
    region=src[begin:end]
    region=once(region,
      "       child:Stack(fit:StackFit.expand,children:[",
      "       child:Stack(fit:StackFit.expand,children:[",
      "video stack")
    region=once(region,
      "         Positioned(\n           left:10,right:10,bottom:10,",
      "         if(!yerel)Positioned(right:2,top:3,child:_ngelx465RemoteAudioMenu(p)),\n"
      "         Positioned(\n           left:10,right:10,bottom:10,",
      "video menu")
    src=src[:begin]+region+src[end:]
    return src

def main():
    before=MAIN.read_text(encoding="utf-8")
    after=transform(before)
    if before!=after:MAIN.write_text(after,encoding="utf-8")
    print("Build465: square call avatars and locally reversible remote-audio menu")

if __name__=="__main__":main()
