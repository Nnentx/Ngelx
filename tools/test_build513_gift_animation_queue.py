#!/usr/bin/env python3
"""Build513 regression: sequential confirmed gifts, no lost monetization guards."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('build513','tools/apply_build513_gift_animation_queue.py')
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)

src=Path('app/lib/live_broadcast_studio.dart').read_text(encoding='utf-8')
assert patch.transform(src)==src, 'Build513 must be repeatable/idempotent'
start=src.index('class _CanliYayinPageState')
end=src.index('class _CanliOzetSatiri',start)
live=src[start:end]
for guard in (
    patch.MARK,
    'final List<Map<String,dynamic>> _giftQueue513',
    'Timer? _giftQueueGap513;',
    'bool _giftTransitioning513=false;',
    'void _showNextGift513(){',
    '_giftVisible511!=null || _giftTransitioning513',
    'final next=_giftQueue513.removeAt(0);',
    '_giftQueueGap513?.cancel();',
    'snap.docChanges.reversed',
    'if(d.metadata.hasPendingWrites)continue;',
    'if(!_knownGiftIds511.add(d.id))continue;',
    'if(event==null||event[\'kind\']!=\'gift\')continue;',
    'if(_giftQueue513.length<32)',
    "_giftQueue513[_giftQueue513.length-1]=<String,dynamic>{",
    "'summary':true",
    "'name':'Toplu hediyeler'",
    '_showNextGift513();',
    '_giftTimer511=Timer(',
    '_giftTransitioning513=true;',
    'Duration(milliseconds:340)',
    '_giftQueue513.clear();',
    '_gifts511?.cancel();',
    '_giftTimer511?.cancel();',
    'IgnorePointer(ignoring:true,child:AnimatedSwitcher(',
    'Timer(Duration(milliseconds:pts>=25?3400:1750)',
    '_giftHistory512()',
    '_newCommentChip510()',
    '_yorumYonet(d.id,y)',
    '_guestRail488()',
    "bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)",
):
    # Original duration reference remains in Build511's scripted transform,
    # not in the final transformed widget.
    if 'Timer(Duration(milliseconds:pts>=25?3400:1750)' in guard:
        assert 'Duration(milliseconds:score>=25?3400:1750)' in live
        continue
    assert guard in live,f'Build513 missing important queue/legacy guard: {guard}'
assert src.count(patch.MARK)==1
assert live.count('void _showNextGift513(){')==1
assert live.count('snap.docChanges.reversed')==1
assert 'if(change.type==DocumentChangeType.added)continue;' not in patch.NEW_LOOP
assert 'FirebaseFirestore' not in patch.FIELDS and 'FirebaseFirestore' not in patch.NEW_LOOP
for forbidden in ('.set(','.add(','.update(','.delete(','.runTransaction('):
    assert forbidden not in patch.FIELDS and forbidden not in patch.NEW_LOOP, 'Queue may not write backend'
assert 'NGELX_VIRTUAL_GIFT_STAGING' not in patch.FIELDS and 'NGELX_VIRTUAL_GIFT_STAGING' not in patch.NEW_LOOP
assert 'int sonHediyeAdedi511=0;' in live
assert "'giftCount'" in live
print('Build513 SOURCE PASS: serialized acknowledged animations, oldest-first burst playback')
print('Build513 SOURCE PASS: 32 bounded slots and overflow summary; no Firestore writes')
print('Build513 SOURCE PASS: cleanup, virtual gift default-off guard, comments and camera preserved')
print('Build513 LIMIT: high-load/two-phone Android animations and native LiveKit overlay need real-device QA')
