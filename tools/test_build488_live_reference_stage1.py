#!/usr/bin/env python3
"""Build488 scoped source checks; no LiveKit or Firebase behavior changes."""
from pathlib import Path
import importlib.util

spec=importlib.util.spec_from_file_location("live488","tools/apply_build488_live_reference_stage1.py")
assert spec is not None and spec.loader is not None
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    s=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
    assert mod.transform(s)==s, "Stage1 patch must be idempotent"
    section=s[s.index("class _CanliYayinPageState"):]
    assert section.count(mod.MARKER)==1
    for token in (
        "takipte?'Takiptesin':_ngelx438Ui(\"Takip et\")",
        "stream:FirebaseFirestore.instance.collection('live_streams').doc(widget.belgeId).snapshots(),",
        "likeCount", "Icons.favorite_rounded",
        ".collection('reactions').snapshots()", "liveLikes??storedLikes",
        "Widget _guestRail488()", "Icons.add_rounded",
        "guest_requests", "d.data()['status']=='accepted'",
        ".take(10).toList()",
        "MediaQuery.sizeOf(context).height*.37",
        "onDoubleTap:()=>unawaited(_kalpDegistir())",
        "child:_guestRail488()",
        "_guestControl453(true)","_guestControl453(false)",
        "NgelXCanliPkKatmani(", "_yorumPaneli()",
        "widget.oda", "_kalpDegistir()",
    ):
        assert token in section, token
    print("Build488 B1: video room, small +, up to 10 guests, compact follow and heart UI retained")


if __name__=="__main__":main()
