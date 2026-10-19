#!/usr/bin/env python3
"""Build520 PiP source contract (device LiveKit acceptance still required)."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('b520','tools/apply_build520_livekit_android_pip.py')
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
dart=Path('app/lib/main.dart').read_text(encoding='utf-8')
native=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt').read_text(encoding='utf-8')
manifest=Path('app/android/app/src/main/AndroidManifest.xml').read_text(encoding='utf-8')
bridge=Path('app/lib/build520_livekit_pip.dart').read_text(encoding='utf-8')
assert mod.dart_transform(dart)==dart,'main Flutter patch must be idempotent'
assert mod.native_transform(native)==native,'Android native patch must be idempotent'
assert mod.manifest_transform(manifest)==manifest,'Android PiP manifest must be idempotent'

assert "part 'build520_livekit_pip.dart';" in dart
call=dart[dart.index('class _NgelXAramaPageState'):dart.index('class GrupBilgiPage')]
for k in (
  'void _pipChanged520()',
  '_enterPip520()async',
  'Ngelx520PipBridge.install()',
  'Ngelx520PipBridge.active.addListener',
  'Ngelx520PipBridge.active.removeListener',
  '?Scaffold(backgroundColor:Colors.black,body:_ngelx520PipVideo())',
  'lk.VideoTrackRenderer(primary,fit:lk.VideoViewFit.cover)',
  'lk.VideoTrackRenderer(local,fit:lk.VideoViewFit.cover)',
  'for(final p in room.remoteParticipants.values)',
  'final local=_katilimciVideosu(room?.localParticipant)',
  'Ngelx509FloatingCallBridge.hide()',
  'if(widget.goruntulu||_privateVoiceCameraOn507||_voiceGroupVideoOn494)',
  "tooltip:'Gerçek görüntülü küçük pencere (Android PiP)'",
  'onPressed:()=>unawaited(_enterPip520())',
  'bitir({bool',
  '_aramaEkraniniKucult()',
):
    assert k in call,'Missing Flutter PiP / preserved media '+k
for k in (
  "MethodChannel('com.nnentx.ngelx_app/call_pip_520')",
  'static final ValueNotifier<bool> active',
  'if(call.method==',
  "active.value=call.arguments as bool",
  "invokeMethod<bool>('enter')",
  'if(started)active.value=true',
):
    assert k in bridge,'Missing Flutter bridge '+k
for k in (
  'import android.app.PictureInPictureParams',
  'import android.content.res.Configuration',
  'import android.util.Rational',
  'private val pipChannel520',
  '"enter" -> {',
  '!CallAudioService.active',
  'enterPictureInPictureMode(params)',
  'override fun onPictureInPictureModeChanged(',
  'super.onPictureInPictureModeChanged(isInPictureInPictureMode,newConfig)',
  'pipMethodChannel520?.invokeMethod("pipMode520",isInPictureInPictureMode)',
):
    assert k in native,'Missing Android PiP requirement '+k
assert 'android:supportsPictureInPicture="true"' in manifest
assert 'android:resizeableActivity="true"' in manifest
for unsafe in ('lk.Room(', 'DevelopmentTokenSource', 'setCameraEnabled(', 'FirebaseFirestore.instance', 'deleteRoom('):
    assert unsafe not in bridge,'PiP bridge never creates call/media/session state: '+unsafe
print('Build520 SOURCE PASS: explicit native PiP, call stays in same Flutter LiveKit room')
print('Build520 SOURCE PASS: actual LiveKit VideoTrackRenderer drives PiP, with no fake native video placeholder')
print('Build520 LIMIT: OS-controlled PiP is not free-drag TYPE_APPLICATION_OVERLAY; real two-phone QA pending')
