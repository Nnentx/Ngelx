#!/usr/bin/env python3
"""Build506 QA: show published video in the ACTUAL group participant grid.

A real Build505 Android screen recording proved that the Build494 camera
button switches to 'Görüntüyü kapat' but the main group tile remains an
avatar. _grupSesliKatilimci had received optional video rendering; the
active _grupAramaAlani instead uses _katilimciKutusu. That widget gated
both video and avatar overlays on the INITIAL widget.goruntulu flag.
A voice-originated room never flips that flag, even when LiveKit has video.

Do not modify call signaling, permissions, media publishing, or roles.
"""
from pathlib import Path

FILE=Path("app/lib/main.dart")
MARK="// Build506: any published video renders in group grid, even voice-originated"

def transform(src: str) -> str:
    if MARK in src:
        return src
    start=src.index("  Widget _katilimciKutusu(lk.Participant p,{bool yerel=false}){")
    end=src.index("  // Build465: only this listener can mute", start)
    grid=src[start:end]
    before="if(widget.goruntulu&&track!=null)"
    if grid.count(before)!=2:
        raise RuntimeError("Build506 expected exactly two initial-call-type video gates")
    if "final ad=_katilimciAdi(p,yerel:yerel),track=_katilimciVideosu(p);" not in grid:
        raise RuntimeError("Build506 must use an actual published LiveKit track")
    grid=grid.replace(before,"if(track!=null)")
    grid=grid.replace("  Widget _katilimciKutusu(lk.Participant p,{bool yerel=false}){",
       "  "+MARK+"\n  Widget _katilimciKutusu(lk.Participant p,{bool yerel=false}){",1)
    return src[:start]+grid+src[end:]

if __name__=="__main__":
    old=FILE.read_text(encoding="utf-8")
    new=transform(old)
    if new!=old:
        FILE.write_text(new,encoding="utf-8")
    print("Build506 actual group grid shows published video in voice-originated room; audio and controls unchanged")
