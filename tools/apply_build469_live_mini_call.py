#!/usr/bin/env python3
"""Build469: show actual remote video in the already-working minimized call overlay.
No new LiveKit session, no camera permission changes and no call transport changes.
Keep panel draggable and clamp to visible Android safe width.
"""
from pathlib import Path
FILE=Path('app/lib/build445_inbox_model.dart')
START='class _Ngelx445CallOverlayState extends State<Ngelx445CallOverlay>{'
END='class Ngelx445InboxCallBanner extends StatelessWidget'
TAG='// Build469: Messenger-style live thumbnail in the EXISTING mini call'
def once(s,old,new,what):
    if s.count(old)!=1:raise RuntimeError(f'Build469 mini overlay {what}: {s.count(old)}')
    return s.replace(old,new,1)

METHOD="""  // Build469: Messenger-style live thumbnail in the EXISTING mini call.
  // Reuse the attached room; do not create another call or start the camera.
  Widget _ngelx469Preview(lk.Room active, String fallbackPhoto){
    lk.VideoTrack? remote;
    for(final p in active.remoteParticipants.values){
      for(final pub in p.videoTrackPublications){
        if(!pub.muted&&pub.track is lk.VideoTrack){
          remote=pub.track as lk.VideoTrack;break;
        }
      }
      if(remote!=null)break;
    }
    if(remote==null){
      return CircleAvatar(radius:26,backgroundColor:const Color(0xFF6F4AB2),
        backgroundImage:fallbackPhoto.isEmpty?null:NgelXAgImageProvider(fallbackPhoto),
        child:fallbackPhoto.isEmpty?const Icon(Icons.videocam,color:Colors.white):null);
    }
    return ClipRRect(
      borderRadius:BorderRadius.circular(12),
      child:SizedBox(width:116,height:92,child:lk.VideoTrackRenderer(remote,fit:lk.VideoViewFit.cover)),
    );
  }
"""
def transform(src):
    if TAG in src:return src
    a=src.index(START);b=src.index(END,a)
    r=src[a:b]
    r=once(r,
      '  Timer? _tick;StreamSubscription<User?>? _auth;',
      METHOD+'  Timer? _tick;StreamSubscription<User?>? _auth;','preview helper')
    r=once(r,
      'final x=(_left??screen.width-128).clamp(8.0,(screen.width-120).clamp(8.0,double.infinity)).toDouble();',
      '''// Keep the whole mini call panel inside the actual screen width.
    final maxX=math.max(8.0,screen.width-152.0);
    final x=(_left??screen.width-152).clamp(8.0,maxX).toDouble();''',
      'safe draggable x clamp')
    r=once(r,
      'return Positioned(left:x,top:y,width:112,child:Material(',
      'return Positioned(left:x,top:y,width:144,child:Material(',
      'bounded mini call width')
    r=once(r,
      '''CircleAvatar(radius:20,backgroundColor:const Color(0xFF6F4AB2),backgroundImage:detail.photo.isEmpty?null:NgelXAgImageProvider(detail.photo),child:detail.photo.isEmpty?Icon(detail.video?Icons.videocam:Icons.call,color:Colors.white,size:20):null),''',
      '''if(detail.video)_ngelx469Preview(room.room,detail.photo)
            else CircleAvatar(radius:20,backgroundColor:const Color(0xFF6F4AB2),backgroundImage:detail.photo.isEmpty?null:NgelXAgImageProvider(detail.photo),child:detail.photo.isEmpty?const Icon(Icons.call,color:Colors.white,size:20):null),''',
      'live video in minimized call')
    for guard in ("onTap:()=>ngelx445ReturnCall(name)",
                  "onEnd:()=>ngelx445EndBackground(name)",
                  "onPanUpdate:(delta)=>setState",
                  "FirebaseAuth.instance.currentUser?.uid!=detail.uid"):
      if guard not in r:raise RuntimeError('minimized call safety contract missing '+guard)
    return src[:a]+r+src[b:]
if __name__=='__main__':
    old=FILE.read_text(encoding='utf-8')
    new=transform(old)
    if new!=old:FILE.write_text(new,encoding='utf-8')
    print('Build469: minimized video call previews live remote track and remains inside screen')
