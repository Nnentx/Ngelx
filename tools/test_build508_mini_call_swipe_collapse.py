#!/usr/bin/env python3
"""Build508 QA: shrinking overlay is reversible and never ends an active call."""
from pathlib import Path
import importlib.util

spec=importlib.util.spec_from_file_location("build508","tools/apply_build508_mini_call_swipe_collapse.py")
assert spec and spec.loader
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
source=Path("app/lib/build445_inbox_model.dart").read_text(encoding="utf-8")
assert mod.transform(source)==source,"Build508 patch is idempotent"

start=source.index("class _Ngelx445CallOverlayState")
end=source.index("class Ngelx445InboxCallBanner",start)
overlay=source[start:end]

for needle in (
    mod.MARK,
    "String? _collapsedRoom508;",
    "_verticalDrag508+=delta.delta.dy;",
    "if(_verticalDrag508>=96&&mounted)",
    "setState(()=>_collapsedRoom508=name)",
    "if(_collapsedRoom508==name){",
    "button:true,label:'Görüşmeye geri dön'",
    "Tooltip(message:'Görüşmeye dön'",
    "onTap:()=>_returnCall508(name)",
    "if(mounted)setState(()=>_collapsedRoom508=null);",
    "ngelx445ReturnCall(roomName)",
    "onPanStart:(_){_verticalDrag508=0;}",
    "onPanEnd:(_){",
    "final room=_ngelxArkaPlanAramaOdalari[name];",
    "FirebaseAuth.instance.currentUser?.uid!=detail.uid",
    "onEnd:()=>ngelx445EndBackground(name)",
    "_ngelx469Preview(room,detail.photo)",
    "if(detail.video||_hasLiveVideo508(room))",
    "if(remote==null&&active.localParticipant!=null)",
    "onMicrophone:()async{",
    "onSpeaker:()async{",
):
    assert needle in overlay,needle
assert overlay.count("_returnCall508(name)")==2,"tap card or collapsed chip"
collapse=overlay[overlay.index("if(_collapsedRoom508==name){"):
                 overlay.index("    final x=(",overlay.index("if(_collapsedRoom508==name){"))]
assert "ngelx445ReturnCall" not in collapse,"return uses method with reset"
assert "ngelx445EndBackground" not in collapse
assert "disconnect()" not in collapse
assert "ng elx446".replace(" ","") not in collapse
assert "SizedBox.shrink()" not in collapse
assert "if(name==null||detail==null||room==null||!ngelxCallSession444.background" in overlay
assert "Stack" not in collapse or "Positioned" in collapse
banner=source[end:source.index("Future<void> ngelx445OpenCallChat",end)]
assert "onTap:()=>ngelx445ReturnCall(name)" in banner,"Inbox return route retained"
assert "Aramaya dönmek için dokun" in banner
print("Build508 PASS: swipe down collapses in-app floating card, not call session")
print("Build508 PASS: one-tap recovery and old inbox return banner preserved")
print("Build508 PASS: floating video reacts to published peer/local LiveKit track")
