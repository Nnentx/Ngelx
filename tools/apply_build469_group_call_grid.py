#!/usr/bin/env python3
"""Build469: consistent all-participant call controls and real active-speaker highlights.
Patch the finished generated call widget, not the LiveKit transport or Firestore ACL.
"""
from pathlib import Path
MAIN=Path("app/lib/main.dart")
START="class _NgelXAramaPageState extends State<NgelXAramaPage>{"
END="class GrupBilgiPage extends StatefulWidget"
TAG="// Build469: every participant has one scoped actions menu"

def once(s,old,new,why):
    if s.count(old)!=1:
        raise RuntimeError(f"Build469 {why}: expected one anchor, found {s.count(old)}")
    return s.replace(old,new,1)

MENU="""  // Build469: every participant has one scoped actions menu. Visibility is
  // role-independent. Changing somebody else's room state still uses the
  // existing role-checked moderation flow, never a direct Firestore write.
  Widget _ngelx469ParticipantMenu(lk.Participant person,{bool yerel=false}){
    final remote=person is lk.RemoteParticipant?person:null;
    final tracks=remote?.audioTrackPublications;
    final locallyMuted=tracks!=null&&tracks.isNotEmpty&&tracks.every((p)=>!p.subscribed);
    final canModerate=_isAdmin446&&!yerel;
    return PopupMenuButton<String>(
      key:ValueKey('call_participant_actions_'+person.identity.toString()),
      tooltip:'Katılımcı seçenekleri',
      color:const Color(0xFF2C2142),
      icon:const Icon(Icons.more_vert_rounded,color:Colors.white,size:22),
      onSelected:(choice){
        if(choice=='self_mute'){unawaited(mikrofonDegistir());return;}
        if(choice=='listen'&&remote!=null){
          unawaited(_ngelx465SetRemoteAudio(remote,locallyMuted));
          return;
        }
        if(choice=='moderate'&&canModerate){
          unawaited(ngelx446MuteMenu(context,widget.aramaRef,widget.roomName,person.identity.toString()));
        }
      },
      itemBuilder:(_)=>[
        if(yerel)PopupMenuItem<String>(value:'self_mute',
          child:Text(mikrofon?'Mikrofonumu sustur':'Mikrofonumu aç',
            style:const TextStyle(color:Colors.white))),
        if(!yerel)PopupMenuItem<String>(value:'listen',
          enabled:tracks?.isNotEmpty==true,
          child:Text(locallyMuted?'Sesini aç (benim için)':'Sustur (benim için)',
            style:const TextStyle(color:Colors.white))),
        PopupMenuItem<String>(value:'moderate',enabled:canModerate,
          child:Row(children:[
            Icon(Icons.person_remove_alt_1_rounded,
              color:canModerate?Colors.white:Colors.white38,size:19),
            const SizedBox(width:8),
            Text('Sesten at',style:TextStyle(
              color:canModerate?Colors.white:Colors.white38)),
          ])),
      ],
    );
  }

"""
def transform(src):
    if TAG in src:return src
    a=src.index(START);b=src.index(END,a)
    r=src[a:b]
    r=once(r,'  Widget _ngelx465SquareCallAvatar(lk.Participant p,{bool yerel=false,double size=86}){',
           MENU+'  Widget _ngelx465SquareCallAvatar(lk.Participant p,{bool yerel=false,double size=86}){','participant menu')
    r=once(r,
      'return GestureDetector(onTap:yerel?null:()=>ngelx446MuteMenu(context,widget.aramaRef,widget.roomName,p.identity.toString()),child:Container(\n      clipBehavior:Clip.antiAlias,',
      'return Container(\n      clipBehavior:Clip.antiAlias,','call participant grid gesture')
    r=once(r,
      'border:Border.all(color:!widget.goruntulu&&mic446?const Color(0xFFB88BFF):Colors.white.withValues(alpha:.12),width:widget.goruntulu?1:2),',
      'border:Border.all(color:p.isSpeaking&&mic446?const Color(0xFF23DC7A):Colors.white.withValues(alpha:.12),width:p.isSpeaking&&mic446?3.5:1.5),','real speaker border')
    r=once(r,
      'boxShadow:const [BoxShadow(color:Color(0x28000000),blurRadius:18,offset:Offset(0,8))],',
      'boxShadow:p.isSpeaking&&mic446?const [BoxShadow(color:Color(0xBB1FCF70),blurRadius:22,spreadRadius:2)]:const [BoxShadow(color:Color(0x28000000),blurRadius:18,offset:Offset(0,8))],',
      'real speaker glow')
    r=once(r,
      'if(_isAdmin446&&!yerel)Positioned(top:2,right:2,child:IconButton(icon:const Icon(Icons.more_vert,color:Colors.white),onPressed:()=>ngelx446MuteMenu(context,widget.aramaRef,widget.roomName,p.identity.toString()))),',
      'Positioned(top:2,right:2,child:_ngelx469ParticipantMenu(p,yerel:yerel)),',
      'one menu in video/grid tile')
    r=once(r,
      '''      ]),
    ));
  }

  // Build465: only this listener can mute''',
      '''      ]),
    );
  }

  // Build465: only this listener can mute''','tile close')
    r=once(r,
      'final aktif=yerel&&mikrofon;',
      'final aktif=p.isSpeaking&&(yerel?mikrofon:p.audioTrackPublications.any((track)=>!track.muted));',
      'square avatar real speaking state')
    r=once(r,
      'gradient:aktif?const LinearGradient(colors:[Color(0xFFB479FF),Color(0xFF6F49E8)]):null,',
      'gradient:aktif?const LinearGradient(colors:[Color(0xFF26EC85),Color(0xFF0C9D55)]):null,',
      'square avatar green border')
    r=once(r,
      'boxShadow:aktif?const [BoxShadow(color:Color(0x557A50E8),blurRadius:22,spreadRadius:3)]:null,',
      'boxShadow:aktif?const [BoxShadow(color:Color(0xAA20E378),blurRadius:22,spreadRadius:3)]:null,',
      'square avatar green glow')
    r=once(r,
      'if(_isAdmin446&&!yerel)Positioned(top:-8,right:-10,child:IconButton(icon:const Icon(Icons.more_vert,color:Colors.white),onPressed:()=>ngelx446MuteMenu(context,widget.aramaRef,widget.roomName,p.identity.toString()))),\n            if(!yerel)Positioned(right:-10,top:-14,child:_ngelx465RemoteAudioMenu(p)),',
      'Positioned(right:-10,top:-14,child:_ngelx469ParticipantMenu(p,yerel:yerel)),',
      'single menu on voice/avatar tile')
    if 'Ngelx446SpeakingRing(participant:p' not in r:
      raise RuntimeError('LiveKit participant speaking ring lost')
    if 'on<lk.RoomReconnectedEvent>' not in r:
      raise RuntimeError('existing LiveKit connection events lost')
    return src[:a]+r+src[b:]
if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if after!=before:MAIN.write_text(after,encoding='utf-8')
    print('Build469: 3-dot menu for ALL callers, green speaking glow, existing role-gated moderation')
