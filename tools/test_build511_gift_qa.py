#!/usr/bin/env python3
"""Build511 source-level regression and gift security preflight."""
import importlib.util
from pathlib import Path

def load(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    assert spec and spec.loader
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

source=Path("app/lib/live_broadcast_studio.dart").read_text(encoding="utf-8")
rules=Path("firestore.rules").read_text(encoding="utf-8")
view=source[source.index("class _CanliYayinPageState"):source.index("class _CanliOzetSatiri")]
patch=load("tools/apply_build511_gift_quantity_animation.py","build511_ui")
security=load("tools/apply_build511_gift_rules.py","build511_rules")
assert patch.transform(source)==source, "UI patch must be idempotent"
assert security.transform(rules)==rules, "Firestore rules patch must be idempotent"

for key in (
    patch.MARK,"_watchGifts511();","_giftScreen511()",
    "AnimatedSwitcher(","IgnorePointer(ignoring:true",
    "_giftTimer511?.cancel();","_gifts511?.cancel();",
    "snapshots(includeMetadataChanges:true)",
    "if(snap.metadata.isFromCache)return;",
    "if(change.type==DocumentChangeType.removed)continue;",
    "if(d.metadata.hasPendingWrites)continue;",
    "Timer(Duration(milliseconds:pts>=25?3400:1750)",
    "'giftCount': hediyeAdedi511,",
    "sonHediyeAdedi511=hediyeAdedi511;",
    "'quantity': adet,","'points': puan*adet,",
    "hediyeGonderiliyor||adet<1||adet>10",
    "await giftDoc.set({",
    "int amount511=1;",
    "StatefulBuilder(builder:(c,setGiftAmount)",
    "SingleChildScrollView(child:Padding(",
    "QA sanal hediye · gerçek para/coin ödemesi yok",
    "Hediye adedi","Ayıcık","Elmas","Kalp",
    "_newCommentChip510()","_yorumYonet(d.id,y)",
    "_guestRail488()","_kalpDegistir()",
):
    assert key in view,f"missing gift/comment QA contract: {key}"
start=view.index("  Future<void> _hediyeGonder(")
end=view.index("  Future<void> _hediyePaneli()",start)
send=view[start:end]
assert "collection('comments').add(" not in send
assert "final giftDoc=" in send
assert "bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)" in send
assert send.index("if(!stagingEnabled)") < send.index("await giftDoc.set({"), "QA gift writing must be gated"
assert view.count("child:Center(child:_giftScreen511())")==1
assert ("yama['giftCount']=gifts.docs.fold<int>(" in view or
        "yama['giftCount']=hediyeAdedi511;" in view), "Gift count must come from real Firestore records"
assert source.count(patch.MARK)==1
for marker in (
    security.MARK,
    "function validVirtualGift511()",
    "qty >= 1 && qty <= 10",
    "name == 'Gül'",
    "name == 'Ayıcık'",
    "points == qty * 100",
    "get('createdAt', null) == request.time",
    "resource.data.get('kind', '') != 'gift'",
    "validVirtualGift511()",
):
    assert marker in rules,f"missing Firestore security: {marker}"
print("Build511 source PASS: gift event counts/animations, quantity picker and legacy call/live comment contracts")
print("Build511 security PRECHECK PASS: virtual gift events guarded, immutable and bounded")
print("Build511 remaining: Firebase emulator suite, Flutter build and real Android device tests")
