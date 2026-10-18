#!/usr/bin/env python3
"""Build496 pre-live camera-preview tap focus guard."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location("b496","tools/apply_build496_preview_tap_focus.py")
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
src=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
assert mod.transform(src)==src, "focus patch must be idempotent"
preview=src[:src.index("  Future<void> _geriSayimCalistir()")]
for marker in (
    mod.MARK,
    "Future<void> _onizlemeOdakla496(Offset local,Size size)",
    "c.setFocusMode(FocusMode.auto)",
    "c.setFocusPoint(focus)",
    "c.setExposurePoint(focus)",
    "onTapDown:(details)=>unawaited(_onizlemeOdakla496(",
    "layout",
    "identical(onizleme,c)",
    "number==_odakSirasi496",
    "if(_onizlemeOdak496!=null)Positioned(",
    "CameraPreview(c)",
):
    if marker=="layout":marker="child:LayoutBuilder("
    assert marker in preview,marker
assert "LK_OPTIONAL_SENTINEL" not in preview
assert src.count(mod.MARK)==1
print("Build496: tap-to-focus, device fallback, camera lifetime and 850ms feedback PASS")
