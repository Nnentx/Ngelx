#!/usr/bin/env python3
"""Build524 generated Flutter source regression, after preceding QA patches."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('build524','tools/apply_build524_comment_send_reliability.py')
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec);spec.loader.exec_module(patch)
src=Path('app/lib/live_broadcast_studio.dart').read_text(encoding='utf-8')
assert patch.transform(src)==src
assert src.count(patch.MARK)==1
start=src.index('class _CanliYayinPageState')
end=src.index('class _CanliOzetSatiri',start)
live=src[start:end]
send=live[live.index(patch.MARK):live.index('  @override\n  void dispose()',live.index(patch.MARK))]
for guard in (
    '_sendingComment524','_pendingCommentSignature524',
    '_pendingCommentId524',
    "final signature='${widget.belgeId}|${user.uid}|$metin';",
    "if(_sendingComment524)return;",
    '.get(const GetOptions(source:Source.server))',
    "v['active']!=true",
    "v['commentsEnabled']==false",
    "v['mutedUsers']",
    "v['slowModeSeconds']",
    'FirebaseFirestore.instance.runTransaction<bool>',
    'final existing=await tx.get(event)',
    'if(existing.exists)',
    "saved['kind']!='comment'",
    "saved['userId']!=user.uid",
    "saved['text']!=metin",
    "throw StateError('live_comment_retry_mismatch')",
    'tx.set(event,<String,dynamic>{',
    'sonYorumZamani=DateTime.now()',
    'if(yorum.text.trim()==metin)yorum.clear()',
    'Yorum doğrulanamadı. Metin korundu',
    'if(mounted)setState(()=>_sendingComment524=false)',
):
    assert guard in live,'Build524 missing required behavior: '+guard
# Some generated layouts route Enter and button through distinct wrappers.
# Both must converge on _yorumGonder(), whose synchronous guard protects
# repeated taps even when the UI does not expose a disabled visual state.
assert live.count('Future<void> _yorumGonder() async')==1
assert send.index('if(_sendingComment524)return;')<send.index('await ref.get(')
assert send.index('tx.set(event,')<send.index('if(yorum.text.trim()==metin)yorum.clear()')
assert "ref.collection('comments').add(" not in send
assert send.count('tx.set(event,')==1
for preserved in (
    'Build514: cursor-paged read-only comment history',
    'Build513: sequential confirmed gift animation queue',
    "bool.fromEnvironment('NGELX_VIRTUAL_GIFT_STAGING',defaultValue:false)",
    '_giftHistory512()', '_commentScroll510',
    '_guestRail488()', '_yorumYonet(d.id,y)'
):
    assert preserved in live,'Build524 lost inherited feature '+preserved
print('Build524 SOURCE PASS: busy control and text field not cleared before commit')
print('Build524 SOURCE PASS: server-verified moderation, stable retry ID and no changed-new-draft erasure')
print('Build524 LIMIT: Firestore emulator and actual Android devices must still pass')
