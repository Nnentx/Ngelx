#!/usr/bin/env python3
"""Build507 QA: private voice camera is local opt-in with truthful track state."""
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location("build507","tools/apply_build507_private_voice_camera.py")
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

src=Path("app/lib/main.dart").read_text(encoding="utf-8")
assert mod.transform(src)==src,"patch idempotence"
body=src[src.index("class _NgelXAramaPageState"):src.index("class GrupBilgiPage")]
assert body.count(mod.MARK)==1

method=body[body.index("  Future<void> _togglePrivateVoiceCamera507()async{"):body.index("  Future<void> kameraDegistir()async{")]
for term in (
    "if(grupAramasi||widget.goruntulu||bitiyor||kucultuluyor||",
    "_privateVoiceCameraBusy507||local==null)return",
    "final turnOn=!_privateVoiceCameraOn507",
    "final permission=await Permission.camera.request()",
    "if(!permission.isGranted)",
    "await local.setCameraEnabled(turnOn,",
    "final published=local.videoTrackPublications.any(",
    "if(turnOn&&(!local.isCameraEnabled()||!published))",
    "if(!turnOn&&local.isCameraEnabled())",
    "setState(()=>_privateVoiceCameraOn507=turnOn)",
    "setState(()=>_privateVoiceCameraBusy507=false)",
):
    assert term in method,term
for must_not in ("widget.aramaRef.set(", "runTransaction(", "new lk.Room(", "remoteParticipants.values.first.setCameraEnabled"):
    assert must_not not in method,must_not

assert "if(!grupAramasi&&!widget.goruntulu)_aramaKontrol(" in body
assert "_privateVoiceCameraOn507?'Görüntüyü kapat':'Görüntüyü aç'" in body
assert "_togglePrivateVoiceCamera507,_privateVoiceCameraOn507" in body
assert "else if(widget.goruntulu||_privateVoiceCameraOn507||_uzakVideo!=null)_videoAlani()" in body
assert "(widget.goruntulu?'Görüntülü arama • ':'Sesli arama • ')+_aramaSureYazi()" in body
assert "cameraWanted:(widget.goruntulu&&kamera)||(!grupAramasi&&_privateVoiceCameraOn507)" in body
assert "if(widget.goruntulu||(!grupAramasi&&_privateVoiceCameraOn507))" in body
assert "arkaPlan.room.localParticipant?.isCameraEnabled()==true" in body
assert "if(grupAramasi&&!widget.goruntulu)_aramaKontrol(" in body
assert "Future<void> _toggleVoiceGroupVideo494()" in body
assert "if(track!=null)" in body   # Build506 group preview preserved
assert "mikrofonDegistir" in body and "hoparlorDegistir" in body
assert "onTap:()=>bitir()" in body and "grupAramasinaKisiDavetEt" in body
print("Build507 PASS: one-to-one voice call camera on/off does not restart call or alter microphone")
print("Build507 PASS: video tile driven by actual published tracks; remote mic/camera never toggled")
print("Build507 PASS: minimize/reconnect state restored only after explicit local camera choice")
