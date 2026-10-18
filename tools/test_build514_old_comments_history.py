#!/usr/bin/env python3
"""Build514 source QA: >100 live events readable with bounded read-only pages."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('build514','tools/apply_build514_old_comments_history.py')
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)

src=Path('app/lib/live_broadcast_studio.dart').read_text(encoding='utf-8')
assert patch.transform(src)==src, 'Build514 source transform must be idempotent'
live=src[src.index('class _CanliYayinPageState'):src.index('class _CanliOzetSatiri')]
archive=live[live.index(patch.MARK):live.index('  Widget _commentSection490(){',live.index(patch.MARK))]
for required in (
    "orderBy('createdAt',descending:true).limit(50).get()",
    "startAfterDocument(last!).limit(50).get()",
    "events.addAll(page.docs.where((d)=>!known.contains(d.id)))",
    "if(page.docs.isNotEmpty)last=page.docs.last;",
    "hasMore=page.docs.length==50;",
    "if(loading||!hasMore||last==null)return;",
    "if(!c.mounted)return;",
    "if(c.mounted)refresh(()=>loading=false);",
    "onPressed:loading?null:loadOlder",
    "Daha eski yorumları getir",
    "Arşiv salt okunurdur",
    "kind=='join'",
    "if(kind=='gift')",
    "createdAt",
    "ListView.builder(",
):
    assert required in archive,'Build514 missing archive paging/display safety: '+required
for forbidden in (
    ".set(", ".update(", ".delete(", ".runTransaction(", "SetOptions(",
    "setCameraEnabled", "setMicrophoneEnabled", "closeRoom", ".add(",
):
    assert forbidden not in archive,'Read-only archive must not change app/server: '+forbidden
for preserved in (
    "if(!_commentsHidden490)_newCommentChip510(),",
    "onPressed:_commentHistory514",
    "label:const Text('Eski yorumlar'",
    "_commentScroll510",
    "_giftHistory512()",
    "_giftScreen511()",
    "_showNextGift513()",
    "_guestRail488()",
    "_yorumYonet(d.id,y)",
    "bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)",
):
    assert preserved in live, 'Build514 lost existing live feature: '+preserved
assert src.count(patch.MARK)==1
assert live.count('onPressed:_commentHistory514')==1
assert "return StreamBuilder" in live and "_comments448" in live
assert ".limit(100).snapshots()" in live, 'Real-time live comment stream must remain bounded and separate'
print('Build514 SOURCE PASS: comments beyond last 100 reachable via 50-event cursor pages')
print('Build514 SOURCE PASS: existing live feed and unread chip preserved; archive is read-only')
print('Build514 LIMIT: Flutter QA, pagination on long live broadcasts, multi-Android QA still needed')
