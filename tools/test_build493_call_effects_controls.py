#!/usr/bin/env python3
"""Build493 source regression for video-only tap overlay and effects menu."""
from pathlib import Path
import importlib.util
spec=importlib.util.spec_from_file_location("b493","tools/apply_build493_call_effects_controls.py")
assert spec and spec.loader
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
s=Path("app/lib/main.dart").read_text(encoding="utf-8")
assert m.transform(s)==s
body=s[s.index("class _NgelXAramaPageState"):s.index("class GrupBilgiPage")]
for k in (
  "bool _videoCallControlsVisible493=true",
  "onTap:_toggleVideoCallControls493",
  "Görüntülü arama efektleri",
  "CheckedPopupMenuItem(value:'retouch'",
  "CheckedPopupMenuItem(value:'blur'",
  "const PopupMenuItem(value:'effects'",
  "_videoEffectMenu493()",
  "if(_videoCallControlsVisible493)Positioned(",
  "if(_videoCallControlsVisible493)Padding(",
  "(!widget.goruntulu||_videoCallControlsVisible493)",
  "onTap:()=>bitir()",
  "if(!widget.goruntulu)_aramaKontrol(",
  "_aramaEkraniniKucult",
):
  assert k in body,k
assert body.count("onTap:_toggleVideoCallControls493")>=2
print("Build493 video-only effects menu and tap-to-hide overlay state PASS")
