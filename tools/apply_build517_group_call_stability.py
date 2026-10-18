#!/usr/bin/env python3
"""Build517 QA: member-scoped group departure, real group camera publication,
compact group controls and tap-to-hide; generated Flutter code, no deploy."""
from pathlib import Path
import re

MAIN=Path('app/lib/main.dart')
MARK='// Build517: group members leave independently and controls toggle on tap'

def once(s,old,new,label):
    count=s.count(old)
    if count!=1:
        raise RuntimeError(f'Build517 {label}: expected one anchor, found {count}')
    return s.replace(old,new,1)

CAMERA=r"""  // Build517: group members leave independently and controls toggle on tap.
  bool _voiceGroupCameraBusy517=false;
  Future<void> _toggleVoiceGroupVideo494()async{
    final room=oda,local=oda?.localParticipant;
    if(!grupAramasi||widget.goruntulu||bitiyor||kucultuluyor||
       _voiceGroupCameraBusy517||room==null||local==null)return;
    final enable=!_voiceGroupVideoOn494;
    if(mounted)setState(()=>_voiceGroupCameraBusy517=true);
    try{
      if(enable){
        final permission=await Permission.camera.request();
        if(!permission.isGranted){
          if(mounted)ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content:Text('Kamera izni gerekli. Sesli görüşme devam ediyor.')));
          return;
        }
      }
      if(!mounted||bitiyor||!identical(oda,room))return;
      await local.setCameraEnabled(enable,
        cameraCaptureOptions:const lk.CameraCaptureOptions(
          params:lk.VideoParametersPresets.h360_169,maxFrameRate:20.0,
          stopCameraCaptureOnMute:true));
      final trackPublished=local.videoTrackPublications.any(
        (p)=>!p.muted&&p.track is lk.VideoTrack);
      if(enable&&(!local.isCameraEnabled()||!trackPublished)){
        try{await local.setCameraEnabled(false);}catch(_){}
        throw StateError('group_camera_track_not_published');
      }
      if(!enable&&(local.isCameraEnabled()||trackPublished)){
        throw StateError('group_camera_not_stopped');
      }
      if(mounted&&identical(oda,room)){
        setState(()=>_voiceGroupVideoOn494=enable);
      }
    }catch(_){
      if(mounted&&identical(oda,room)){
        setState(()=>_voiceGroupVideoOn494=local.isCameraEnabled()&&
          local.videoTrackPublications.any((p)=>!p.muted&&p.track is lk.VideoTrack));
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content:Text('Kamera değiştirilemedi. Sesli görüşme devam ediyor.')));
      }
    }finally{
      if(mounted)setState(()=>_voiceGroupCameraBusy517=false);
    }
  }

"""

CONFIRM=r"""  Future<void> _confirmGroupExit517()async{
    if(!grupAramasi){await bitir();return;}
    final confirmed=await showDialog<bool>(context:context,builder:(dialog)=>AlertDialog(
      title:const Text('Görüşmeden ayrıl?'),
      content:const Text('Yalnız sen ayrılacaksın. Diğer katılımcıların görüşmesi devam edecek.'),
      actions:[
        TextButton(onPressed:()=>Navigator.pop(dialog,false),child:const Text('Vazgeç')),
        TextButton(onPressed:()=>Navigator.pop(dialog,true),child:const Text('Ayrıl')),
      ],
    ));
    if(confirmed==true&&mounted&&!bitiyor)await bitir();
  }

"""

def transform(src):
    if MARK in src:return src
    src=once(src,"part 'build509_floating_call.dart';",
      "part 'build509_floating_call.dart';\npart 'build517_group_leave.dart';",
      'independent group-leave source')
    a=src.index('class _NgelXAramaPageState')
    b=src.index('class GrupBilgiPage',a)
    body=src[a:b]
    # An initiator who leaves must NOT end a group call for everyone.
    start=body.index('        if(grup&&me!=null){')
    end=body.index("        }else{\n          final participants=List<String>.from(data['callParticipants']??const[]);",start)
    previous=body[start:end]
    if 'baslatan==me||kalan.isEmpty' not in previous:
        raise RuntimeError('Build517 old group-initiator ends-everyone condition changed')
    replacement="""        if(grup&&me!=null){
          await ngelx517LeaveGroupCall(
            widget.aramaRef,widget.roomName,me,
            video:widget.goruntulu,
            displayName:FirebaseAuth.instance.currentUser?.displayName);
"""
    body=body[:start]+replacement+body[end:]

    camera_a=body.index('  bool _voiceGroupVideoOn494=false;')
    camera_b=body.index('  Widget _grupSesliKatilimci(',camera_a)
    old_camera=body[camera_a:camera_b]
    if 'Future<void> _toggleVoiceGroupVideo494()async' not in old_camera:
        raise RuntimeError('Build517 previous group camera method unavailable')
    body=body[:camera_a]+'  bool _voiceGroupVideoOn494=false;\n'+CAMERA+body[camera_b:]

    # A reconnect is still to the SAME group LiveKit room. Restore camera only
    # if this member previously elected to show it.
    start=body.index('  Future<void> baglan(')
    stop=body.index('  lk.VideoTrack? _katilimciVideosu(',start)
    conn=body[start:stop]
    anchor='      await yerel.setMicrophoneEnabled(true);'
    conn=once(conn,anchor,anchor+"""
      if(!widget.goruntulu&&grupAramasi&&_voiceGroupVideoOn494){
        await yerel.setCameraEnabled(true,
          cameraCaptureOptions:const lk.CameraCaptureOptions(
            params:lk.VideoParametersPresets.h360_169,
            maxFrameRate:20.0,stopCameraCaptureOnMute:true));
      }""",'restore opted-in group camera on reconnect')
    body=body[:start]+conn+body[stop:]

    # Existing video-call tap-to-hide was restricted to calls STARTED as
    # video. Audio-originated group calls need the exact same toggle.
    body=once(body,
      'if(widget.goruntulu&&bitisDurumu==null&&hata==null&&mounted){',
      'if((widget.goruntulu||grupAramasi)&&bitisDurumu==null&&hata==null&&mounted){',
      'tap toggle applies to group audio')
    body=once(body,
      'if(bitisDurumu==null&&hata==null&&(!widget.goruntulu||_videoCallControlsVisible493))Padding(',
      'if(bitisDurumu==null&&hata==null&&(!grupAramasi&&!widget.goruntulu||_videoCallControlsVisible493))Padding(',
      'hide group voice controls')

    group_a=body.index('  Widget _grupAramaAlani(){')
    group_b=body.index('  Widget _videoAlani(){',group_a)
    group=body[group_a:group_b]
    group=once(group,'if(!widget.goruntulu){\n      return Expanded(child:Column(children:[\n        Padding(',
      'if(!widget.goruntulu){\n      return Expanded(child:Column(children:[\n        if(_videoCallControlsVisible493)Padding(',
      'hide group voice title')
    group=once(group,'padding:const EdgeInsets.fromLTRB(22,18,22,8)',
      'padding:const EdgeInsets.fromLTRB(16,4,16,4)',
      'move voice title upward')
    group=once(group,'fontSize:29,fontWeight:FontWeight.w900',
      'fontSize:20,fontWeight:FontWeight.w800',
      'smaller group voice title')
    # Tapping vacant space toggles controls; a drag still scrolls members.
    group=once(group,'Expanded(child:Center(child:SingleChildScrollView(',
      'Expanded(child:GestureDetector(behavior:HitTestBehavior.translucent,\n          onTap:_toggleVideoCallControls493,child:Center(child:SingleChildScrollView(',
      'group voice background tap')
    group=once(group,'child:Wrap(alignment:WrapAlignment.center,spacing:18,runSpacing:24,children:katilimcilar.map((x)=>_grupSesliKatilimci(x.p,yerel:x.yerel)).toList()),\n        ))),',
      'child:Wrap(alignment:WrapAlignment.center,spacing:12,runSpacing:14,children:katilimcilar.map((x)=>_grupSesliKatilimci(x.p,yerel:x.yerel)).toList()),\n        )))),',
      'compact participant cards and close tap wrapper')
    # Group-video grid consumes taps on cards; background taps still work.
    group=once(group,'Expanded(child:GridView.builder(',
      'Expanded(child:GestureDetector(behavior:HitTestBehavior.translucent,\n          onTap:_toggleVideoCallControls493,child:GridView.builder(',
      'group video background tap')
    group=once(group,'itemBuilder:(_,i)=>_katilimciKutusu(katilimcilar[i].p,yerel:katilimcilar[i].yerel),\n      )),',
      'itemBuilder:(_,i)=>_katilimciKutusu(katilimcilar[i].p,yerel:katilimcilar[i].yerel),\n      ))),',
      'group video tap wrapper close')
    body=body[:group_a]+group+body[group_b:]
    # Ensure the system back/minimize button is hidden with other chrome.
    header='if(bitisDurumu==null&&hata==null&&oda!=null)Padding('
    body=once(body,header,
      'if(bitisDurumu==null&&hata==null&&oda!=null&&(!grupAramasi||_videoCallControlsVisible493))Padding(',
      'hide mini header')

    body=once(body,'  Widget _ngelx465HangupControl()=>',
      CONFIRM+'  Widget _ngelx465HangupControl()=>','confirm group-only exit')
    hangup=body.index('  Widget _ngelx465HangupControl()=>')
    controls=body.index('  Widget _aramaKontrol(',hangup)
    row=body[hangup:controls]
    row=once(row,'onTap:()=>bitir(),','onTap:()=>unawaited(_confirmGroupExit517()),','safe leave control')
    row=row.replace('width:60,height:60,','width:48,height:48,')
    row=row.replace('color:Colors.white,size:30','color:Colors.white,size:23')
    body=body[:hangup]+row+body[controls:]
    # No touch target is smaller than 48x48 logical pixels.
    controls=body.index('  Widget _aramaKontrol(')
    lower=body[controls:]
    lower=once(lower,'width:58,height:58,','width:48,height:48,','compact circular controls')
    lower=once(lower,'size:27),','size:21),','control icon')
    lower=once(lower,'const SizedBox(height:7),','const SizedBox(height:4),','control label gap')
    lower=once(lower,'fontSize:10.5,fontWeight:FontWeight.w700',
      'fontSize:10,fontWeight:FontWeight.w700','control label')
    body=body[:controls]+lower
    # A single row on common phone widths, scrollable on narrow screens:
    # existing Wrap retains access to every action including camera/mute.
    body=once(body,'child:Wrap(alignment:WrapAlignment.center,spacing:14,runSpacing:12,children:[',
      'child:Wrap(alignment:WrapAlignment.center,spacing:7,runSpacing:5,children:[',
      'responsive compact action row')
    src=src[:a]+body+src[b:]
    if src.count(MARK)!=1:raise RuntimeError('Build517 marker must be unique')
    return src

if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if after!=before:MAIN.write_text(after,encoding='utf-8')
    print('Build517 patched generated group call: atomic member leave, camera publication, compact tap-to-hide')
