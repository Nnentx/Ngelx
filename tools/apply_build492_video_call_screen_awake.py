#!/usr/bin/env python3
"""Build492 QA: foreground video calls request Android screen-on temporarily.

Applies after prior Build491 Flutter/native transformations. Does not change
global brightness, proximity behavior on voice-only calls, or OS power key.
"""
from pathlib import Path

FLUTTER=Path("app/lib/main.dart")
ANDROID=Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt")
MARK="// Build492: keep foreground video-call screen awake only"

METHOD=r"""
  // Build492: keep foreground video-call screen awake only.
  Future<void> _videoCallKeepScreen492(bool enabled)async{
    if(!Platform.isAndroid||!widget.goruntulu)return;
    try{
      await const MethodChannel('com.nnentx.ngelx_app/call_screen')
        .invokeMethod<void>('keepScreenOn',<String,bool>{'enabled':enabled});
    }catch(_){}
  }
  @override
  void didChangeAppLifecycleState(AppLifecycleState state){
    unawaited(_videoCallKeepScreen492(
      state==AppLifecycleState.resumed&&!kucultuluyor&&!bitiyor&&bitisDurumu==null));
  }

"""


def once(s,a,b,label):
    count=s.count(a)
    if count!=1:raise RuntimeError(f"Build492 {label}: expected 1, got {count}")
    return s.replace(a,b,1)


def flutter_transform(src):
    if MARK in src:return src
    begin=src.index("class _NgelXAramaPageState extends State<NgelXAramaPage>")
    end=src.index("class GrupBilgiPage",begin)
    head,chunk,tail=src[:begin],src[begin:end],src[end:]
    chunk=once(chunk,
      "class _NgelXAramaPageState extends State<NgelXAramaPage>{",
      "class _NgelXAramaPageState extends State<NgelXAramaPage> with WidgetsBindingObserver{",
      "video call route lifecycle observer")
    import re
    init_pattern=r"@override\s+void initState\(\)\s*\{\s*super\.initState\(\);"
    if len(re.findall(init_pattern,chunk))!=1:
        raise RuntimeError("Build492 expected one video-call initState")
    chunk=re.sub(init_pattern,
      lambda m:m.group(0)+"\n    WidgetsBinding.instance.addObserver(this);\n    unawaited(_videoCallKeepScreen492(true));",
      chunk,count=1)
    chunk=once(chunk,
      "  Widget _efektliVideo(lk.VideoTrack track)",
      METHOD+"  Widget _efektliVideo(lk.VideoTrack track)",
      "scoped native bridge")
    # Actual call-screen route may be minimized but underlying LiveKit room
    # remains in the app, so clear FLAG_KEEP_SCREEN_ON on minimization.
    chunk=once(chunk,
      "  Future<void> _aramaEkraniniKucult()async{\n    if(kucultuluyor||!mounted)return;\n    kucultuluyor=true;",
      "  Future<void> _aramaEkraniniKucult()async{\n    if(kucultuluyor||!mounted)return;\n    kucultuluyor=true;\n    await _videoCallKeepScreen492(false);",
      "call minimized")
    chunk=once(chunk,
      "  @override void dispose(){\n    aramaSureZamanlayici?.cancel();",
      "  @override void dispose(){\n    WidgetsBinding.instance.removeObserver(this);\n    unawaited(_videoCallKeepScreen492(false));\n    aramaSureZamanlayici?.cancel();",
      "call route cleanup")
    return head+chunk+tail


def native_transform(src):
    if MARK in src:return src
    needle="""        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, mediaChannel)"""
    injected="""        super.configureFlutterEngine(flutterEngine)
        // Build492: keep foreground video-call screen awake only.
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, "com.nnentx.ngelx_app/call_screen")
            .setMethodCallHandler { call, result ->
                if (call.method != "keepScreenOn") {
                    result.notImplemented()
                } else {
                    val enabled = call.argument<Boolean>("enabled") == true
                    runOnUiThread {
                        if (enabled) window.addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                        else window.clearFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
                        result.success(null)
                    }
                }
            }
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, mediaChannel)"""
    return once(src,needle,injected,"native foreground window flag bridge")


def main():
    for file,fn in ((FLUTTER,flutter_transform),(ANDROID,native_transform)):
        src=file.read_text(encoding="utf-8")
        out=fn(src)
        if out!=src:file.write_text(out,encoding="utf-8")
    print("Build492 video-call screen on/off lifecycle guarded; brightness and audio-only unchanged")


if __name__=="__main__":main()
