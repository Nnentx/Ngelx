#!/usr/bin/env python3
"""Build521 regression: same virtual gift attempt never creates two events."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('build521','tools/apply_build521_idempotent_gifts.py')
assert spec and spec.loader
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
src=Path('app/lib/live_broadcast_studio.dart').read_text(encoding='utf-8')
assert m.transform(src)==src,'Build521 idempotency script should be idempotent'
assert src.count(m.MARK)==1
a=src.index('class _CanliYayinPageState')
b=src.index('class _CanliOzetSatiri',a)
live=src[a:b]
start=live.index('  Future<void> _hediyeGonder(')
end=live.index('  Future<void> _giftHistory512()',start)
send=live[start:end]
for token in (
    '_pendingGiftId521;',
    '_pendingGiftSignature521;',
    "final signature='${widget.belgeId}|${user.uid}|$ad|$adet';",
    '_pendingGiftSignature521==signature?_pendingGiftId521:null;',
    'reusable==null?gifts.doc():gifts.doc(reusable)',
    '_pendingGiftId521=giftDoc.id;',
    'FirebaseFirestore.instance.runTransaction<bool>',
    'final current=await tx.get(giftDoc);',
    "saved['kind']!='gift'",
    "saved['uid']!=user.uid",
    "saved['giftName']!=ad",
    "saved['quantity']!=adet",
    "saved['points']!=puan*adet",
    "throw StateError('virtual_gift_event_mismatch');",
    'tx.set(giftDoc,{',
    '},maxAttempts:4);',
    '_pendingGiftId521=null;',
    '_pendingGiftSignature521=null;',
    'alreadyCommitted',
    'daha önce kaydedilmiş; tekrar sayılmadı',
    "bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)",
    '_giftQueue513',
    '_giftHistory512()',
    '_newCommentChip510()',
    '_guestRail488()',
):
    assert token in live,'Build521 missing immutable event/retry or protected feature: '+token
assert send.index('if(!stagingEnabled)')<send.index('FirebaseFirestore.instance.runTransaction<bool>')
assert "collection('comments').add(" not in send
assert 'await giftDoc.set({' not in send
assert send.count('tx.set(giftDoc,{')==1
assert "'createdAt': FieldValue.serverTimestamp()" in send
assert "'quantity': adet" in send
assert "'points': puan*adet" in send
print('Build521 SOURCE PASS: transaction-based unique gift event and sender/payload-verified retry')
print('Build521 SOURCE PASS: same attempt retains document id after uncertain network error')
print('Build521 SOURCE PASS: a confirmed success clears pending key; existing staging default-off preserved')
print('Build521 LIMIT: emulator tests and cross-device gift event replay require QA acceptance')
