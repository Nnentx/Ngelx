#!/usr/bin/env python3
"""Build492 scope: foreground video-only keep-awake lifecycle invariants."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("b492","tools/apply_build492_video_call_screen_awake.py")
assert spec and spec.loader
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
a=Path("app/lib/main.dart").read_text(encoding="utf-8")
b=Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt").read_text(encoding="utf-8")
assert m.flutter_transform(a)==a
assert m.native_transform(b)==b
start=a.index("class _NgelXAramaPageState")
end=a.index("class GrupBilgiPage",start)
c=a[start:end]
for text in (
 "with WidgetsBindingObserver",
 "WidgetsBinding.instance.addObserver(this)",
 "WidgetsBinding.instance.removeObserver(this)",
 "unawaited(_videoCallKeepScreen492(true));",
 "unawaited(_videoCallKeepScreen492(false));",
 "await _videoCallKeepScreen492(false);",
 "state==AppLifecycleState.resumed&&!kucultuluyor&&!bitiyor",
 "if(!Platform.isAndroid||!widget.goruntulu)return",
 "MethodChannel('com.nnentx.ngelx_app/call_screen')",
 "bitisDurumu==null",
):
 assert text in c,text
assert b.count('android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON')==2
assert b.count('call.method != "keepScreenOn"')==1
print("Build492 foreground video keep-screen-on native bridge and full cleanup PASS")
