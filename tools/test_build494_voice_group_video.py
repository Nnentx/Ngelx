#!/usr/bin/env python3
"""Build494 scoped source guards: same group voice room video toggle."""
from pathlib import Path
import importlib.util
s=importlib.util.spec_from_file_location("b494","tools/apply_build494_voice_group_video.py")
assert s and s.loader
mod=importlib.util.module_from_spec(s);s.loader.exec_module(mod)
src=Path("app/lib/main.dart").read_text(encoding="utf-8")
assert mod.transform(src)==src
body=src[src.index("class _NgelXAramaPageState"):src.index("class GrupBilgiPage")]
for term in (
   mod.MARK,
   "_toggleVoiceGroupVideo494()async",
   "if(!grupAramasi||widget.goruntulu||bitiyor",
   "final permission=await Permission.camera.request()",
   "Sesli görüşme devam ediyor",
   "Görüntüyü aç","Görüntüyü kapat",
   "lk.VideoTrackRenderer(track,fit:lk.VideoViewFit.cover)",
   "Future<void> _aramaEkraniniKucult",
):
  assert term in body,term
assert body.count("if(grupAramasi&&!widget.goruntulu)_aramaKontrol(")==1
assert body.count("_toggleVoiceGroupVideo494,_voiceGroupVideoOn494)")==1
print("Build494 voice group same-room camera toggle and safe permission handling PASS")
