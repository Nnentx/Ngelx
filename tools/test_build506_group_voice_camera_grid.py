#!/usr/bin/env python3
"""Build506 regression: actual tile shows camera for audio-originated calls."""
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location("build506","tools/apply_build506_group_voice_camera_grid.py")
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
src=Path("app/lib/main.dart").read_text(encoding="utf-8")
assert mod.transform(src)==src,"patch idempotence"
start=src.index("class _NgelXAramaPageState")
end=src.index("class GrupBilgiPage",start)
body=src[start:end]
grid=body[body.index("  Widget _katilimciKutusu(lk.Participant p,{bool yerel=false}){"):body.index("  // Build465: only this listener can mute")]
main=body[body.index("  Widget _grupAramaAlani(){"):body.index("  Widget _videoAlani(){")]
assert "itemBuilder:(_,i)=>_katilimciKutusu(katilimcilar[i].p" in main
assert "final ad=_katilimciAdi(p,yerel:yerel),track=_katilimciVideosu(p);" in grid
assert grid.count("if(track!=null)")==2,"show published video AND compact participant avatar"
assert "if(widget.goruntulu&&track!=null)" not in grid
assert "yerel?_efektliVideo(track):lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover)" in grid
assert "else Center(child:Ngelx446SpeakingRing(" in grid,"avatar for audio only"
assert "if(grupAramasi&&!widget.goruntulu)_aramaKontrol(" in body
assert "_toggleVoiceGroupVideo494()" in body
assert "setCameraEnabled(enabled" in body
assert "final permission=await Permission.camera.request()" in body
assert "if(!grupAramasi||widget.goruntulu||bitiyor||oda?.localParticipant==null)return;" in body
assert "grupAramasinaKisiDavetEt" in body
assert "mikrofonDegistir" in body and "hoparlorDegistir" in body
print("Build506 PASS: actual voice group grid renders LiveKit tracks with no initial video-call flag")
