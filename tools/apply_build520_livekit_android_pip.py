#!/usr/bin/env python3
"""Build520 no-deploy QA: opt-in Android PiP shows real existing LiveKit video.

The native OS-owned Picture-in-Picture surface is not the Build509 system-wide
free-drag TYPE_APPLICATION_OVERLAY; Android controls placement/size. This is
an honest media-backed fallback without a second LiveKit room or new tokens.
Apply after Build509, Build506 and Build507 generated Flutter/Android code.
"""
from pathlib import Path
MAIN=Path('app/lib/main.dart')
NATIVE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt')
MANIFEST=Path('app/android/app/src/main/AndroidManifest.xml')
MARK='// Build520: user-initiated Android PiP with actual Flutter LiveKit video'

def once(s,old,new,label):
    n=s.count(old)
    if n!=1:raise RuntimeError(f'Build520 {label}: expected one anchor, found {n}')
    return s.replace(old,new,1)

METHOD=r"""
  // Build520: user-initiated Android PiP with actual Flutter LiveKit video.
  void _pipChanged520(){if(mounted)setState((){});}
  Future<void> _enterPip520()async{
    if(bitiyor||oda==null)return;
    // Only a user gesture invokes the system PiP operation.
    final entered=await Ngelx520PipBridge.enter();
    if(entered){
      // One compact call surface at a time. Build509 still stays available
      // through its own user-approved cross-app permission.
      unawaited(Ngelx509FloatingCallBridge.hide());
    }else if(mounted){
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content:Text('Bu telefonda küçük video penceresi kullanılamıyor. Görüşme devam ediyor.')));
    }
  }
  Widget _ngelx520PipVideo(){
    final room=oda;
    lk.VideoTrack? remote;
    if(room!=null){
      for(final p in room.remoteParticipants.values){
        final candidate=_katilimciVideosu(p);
        if(candidate!=null){remote=candidate;break;}
      }
    }
    final local=_katilimciVideosu(room?.localParticipant);
    final primary=remote??local;
    return ColoredBox(color:const Color(0xFF14111C),
      child:Stack(fit:StackFit.expand,children:[
        if(primary!=null)
          lk.VideoTrackRenderer(primary,fit:lk.VideoViewFit.cover)
        else Center(child:Column(mainAxisSize:MainAxisSize.min,children:[
          const Icon(Icons.call_rounded,color:Colors.white70,size:28),
          const SizedBox(height:5),
          Text(widget.baslik,maxLines:1,overflow:TextOverflow.ellipsis,
            style:const TextStyle(color:Colors.white,fontSize:13)),
        ])),
        if(remote!=null&&local!=null)
          Positioned(right:6,top:6,width:74,height:88,
            child:ClipRRect(borderRadius:BorderRadius.circular(9),
              child:lk.VideoTrackRenderer(local,fit:lk.VideoViewFit.cover))),
      ]));
  }

"""

def dart_transform(src):
    if MARK in src:return src
    src=once(src,"part 'build509_floating_call.dart';",
      "part 'build509_floating_call.dart';\npart 'build520_livekit_pip.dart';",
      'PiP bridge Flutter part')
    a=src.index('class _NgelXAramaPageState')
    b=src.index('class GrupBilgiPage',a)
    body=src[a:b]
    body=once(body,'    super.initState();',
      '''    super.initState();
    Ngelx520PipBridge.install();
    Ngelx520PipBridge.active.addListener(_pipChanged520);''',
      'PiP state listener on init')
    body=once(body,'  @override void dispose(){',
      '''  @override void dispose(){
    Ngelx520PipBridge.active.removeListener(_pipChanged520);''',
      'PiP state listener disposal')
    body=once(body,'  Widget _efektliVideo(lk.VideoTrack track)',
      METHOD+'  Widget _efektliVideo(lk.VideoTrack track)',
      'media-backed mini surface')
    # Generated call screens may use a Container, Stack or custom Builder
    # for Scaffold.body. Wrap the stable Scaffold itself instead of relying
    # on an older body's exact widget type.
    body=once(body,'    child:Scaffold(',
      '''    child:Ngelx520PipBridge.active.value
      ?Scaffold(backgroundColor:Colors.black,body:_ngelx520PipVideo())
      :Scaffold(''','PiP replaces call chrome only while OS in PiP')
    anchor="""              IconButton(
                tooltip:'Diğer uygulamaların üzerinde göster',"""
    extra="""              // Build520: system PiP uses the existing LiveKit renderer.
              if(widget.goruntulu||_privateVoiceCameraOn507||_voiceGroupVideoOn494)
                IconButton(
                  tooltip:'Gerçek görüntülü küçük pencere (Android PiP)',
                  onPressed:()=>unawaited(_enterPip520()),
                  icon:const Icon(Icons.picture_in_picture_rounded,
                    color:Colors.white,size:23),
                ),
"""
    body=once(body,anchor,extra+anchor,'user-initiated PiP button')
    for term in (
      'lk.VideoTrackRenderer(primary,fit:lk.VideoViewFit.cover)',
      'Ngelx520PipBridge.active.removeListener',
      'if(widget.goruntulu||_privateVoiceCameraOn507||_voiceGroupVideoOn494)',
      'Ngelx509FloatingCallBridge',
      'Widget _grupAramaAlani()',
      'Future<void> bitir(',
      'on<lk.RoomReconnectedEvent>'
    ):
        if term not in body:raise RuntimeError('Build520 missing preserved '+term)
    return src[:a]+body+src[b:]

def native_transform(src):
    if '// Build520: explicitly requested system Picture-in-Picture' in src:return src
    src=once(src,'import android.app.Activity\n',
      '''import android.app.Activity
import android.app.PictureInPictureParams
import android.content.res.Configuration
import android.util.Rational
''','Android PiP imports')
    src=once(src,'    private val floatingChannel509 = "com.nnentx.ngelx_app/call_overlay_509"\n',
      '''    private val floatingChannel509 = "com.nnentx.ngelx_app/call_overlay_509"
    private val pipChannel520 = "com.nnentx.ngelx_app/call_pip_520"
    private var pipMethodChannel520: MethodChannel? = null
''','PiP Flutter channel')
    src=once(src,'        super.configureFlutterEngine(flutterEngine)\n',
      '''        super.configureFlutterEngine(flutterEngine)
        // Build520: explicitly requested system Picture-in-Picture, no extra
        // token or camera permission, and no automatic PiP activation.
        val pip520 = MethodChannel(flutterEngine.dartExecutor.binaryMessenger, pipChannel520)
        pipMethodChannel520=pip520
        pip520.setMethodCallHandler { call,result ->
            when(call.method){
                "enter" -> {
                    if(Build.VERSION.SDK_INT < Build.VERSION_CODES.O ||
                       !CallAudioService.active){
                        result.success(false)
                    }else try{
                        val params=PictureInPictureParams.Builder()
                            .setAspectRatio(Rational(16,9)).build()
                        result.success(enterPictureInPictureMode(params))
                    }catch(_:Exception){
                        result.success(false)
                    }
                }
                else -> result.notImplemented()
            }
        }
''','PiP call channel implementation')
    src=once(src,'    override fun onDestroy() {\n',
      '''    override fun onPictureInPictureModeChanged(
        isInPictureInPictureMode: Boolean,newConfig: Configuration
    ){
        super.onPictureInPictureModeChanged(isInPictureInPictureMode,newConfig)
        pipMethodChannel520?.invokeMethod("pipMode520",isInPictureInPictureMode)
    }

    override fun onDestroy() {
        pipMethodChannel520=null
''','native PiP exit event and cleanup')
    return src

def manifest_transform(src):
    if 'android:supportsPictureInPicture="true"' in src:return src
    return once(src,
      '            android:hardwareAccelerated="true"',
      '''            android:resizeableActivity="true"
            android:supportsPictureInPicture="true"
            android:hardwareAccelerated="true"''','Android activity PiP opt-in')

if __name__=='__main__':
    for path,fn in ((MAIN,dart_transform),(NATIVE,native_transform),(MANIFEST,manifest_transform)):
        old=path.read_text(encoding='utf-8')
        new=fn(old)
        if new!=old:path.write_text(new,encoding='utf-8')
    print('Build520: user opt-in real LiveKit Flutter renderer inside Android OS PiP, existing call room retained')
