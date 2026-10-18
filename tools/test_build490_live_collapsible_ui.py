#!/usr/bin/env python3
"""Build490 live two independent overlays: source-level acceptance guards."""
from pathlib import Path
import importlib.util

spec=importlib.util.spec_from_file_location("build490","tools/apply_build490_live_collapsible_ui.py")
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    src=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
    assert mod.transform(src)==src, "Build490 patch should be idempotent"
    view=src[src.index("class _CanliYayinPageState"):]
    for s in (
        mod.MARKER,
        "bool _commentsHidden490=false", "bool _hostDockOpen490=true",
        "_commentSection490()", "_hostDockHandle490()",
        "Offstage(offstage:_commentsHidden490,child:_yorumPaneli())",
        "Yorumlar gizli · Dokun aç",
        "Kontroller · Yukarı çek",
        "onVerticalDragEnd:(details)",
        "speed<0",
        "(!widget.yayinSahibi||_hostDockOpen490)",
        "AnimatedSize(",
        "duration:const Duration(milliseconds:180)",
        "const SizedBox.shrink()",
        "_yorumGirisAlani()",
        "_guestRail488()", "_hostGuestAction489",
        "_guestControl453(false)", "_guestControl453(true)",
        "_yayinMikrofonunuDegistir", "_yayinKamerasiniAcKapat",
        "Yayını bitir", "NgelXCanliPkButonu", "_hearts453",
    ):
        assert s in view, f"Missing Build490 contract: {s}"
    assert view.count(mod.MARKER)==1
    assert view.count("Offstage(offstage:_commentsHidden490,child:_yorumPaneli())")==1
    print("Build490 QA: independent comment/dock collapse, all four states and guest/camera controls retained")


if __name__=="__main__":main()
