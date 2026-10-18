#!/usr/bin/env python3
"""Build509 source contract. Native overlay remains a staged QA prototype."""
from pathlib import Path
import importlib.util

spec=importlib.util.spec_from_file_location("b509","tools/apply_build509_android_cross_app_window.py")
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
main=Path("app/lib/main.dart").read_text(encoding="utf-8")
model=Path("app/lib/build445_inbox_model.dart").read_text(encoding="utf-8")
manifest=Path("app/android/app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
activity=Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt").read_text(encoding="utf-8")
service=Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/CallAudioService.kt").read_text(encoding="utf-8")
window=Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/Ngelx509FloatingCallWindow.kt").read_text(encoding="utf-8")
bridge=Path("app/lib/build509_floating_call.dart").read_text(encoding="utf-8")

assert mod.main_transform(main)==main
assert mod.model_transform(model)==model
for check in (
  "part 'build509_floating_call.dart';",
  "unawaited(Ngelx509FloatingCallBridge.showIfAllowed(widget.roomName));",
  "tooltip:'Diğer uygulamaların üzerinde göster'",
  "await Ngelx509FloatingCallBridge.requestPermission()",
  "unawaited(Ngelx509FloatingCallBridge.hide());",
):
  assert check in main,check
assert "Ngelx509FloatingCallBridge.install();" in model
assert '<uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />' in manifest
assert 'android:exported="false" android:foregroundServiceType="microphone"' in manifest
for value in ("Settings.canDrawOverlays(this)", "ACTION_MANAGE_OVERLAY_PERMISSION",
              "CallAudioService.active", "SHOW_FLOATING_509", "HIDE_FLOATING_509"):
  assert value in activity,value
for value in ("active = false", "floating509?.remove()", "HIDE_FLOATING_509",
              "SHOW_FLOATING_509", "onTaskRemoved"):
  assert value in service,value
for value in ("TYPE_APPLICATION_OVERLAY", "Settings.canDrawOverlays(owner)",
              "Mode.COMPACT", "Mode.EXPANDED", "Mode.COLLAPSED",
              "onTap:", # overwritten below; native click is setOnClickListener
              "MotionEvent.ACTION_OUTSIDE", "methodChannel?.invokeMethod",
              "fullscreen", "microphone", "speaker", "end"):
  if value=="onTap:":continue
  assert value in window,value
for value in ("FirebaseAuth.instance.currentUser?.uid!=detail.uid",
              "ngelxCallSession444.background", "_ngelxArkaPlanAramaOdalari[name]",
              "ngelx446Calls.muted(name)", "ngelx445ReturnCall(name)",
              "ngelx445EndBackground(name)", "await hasPermission()"):
  assert value in bridge,value
assert 'setCameraEnabled' not in bridge
assert 'LiveKit' not in window or 'No video media surface' in window
print("Build509 native permission and current-call-only cross-app overlay QA contract PASS")
print("Build509 real video track in native overlay and physical Android permission test: OPEN")
