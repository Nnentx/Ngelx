#!/usr/bin/env python3
"""Build 426 tests for tappable story cards and a nonwrapping header."""
from pathlib import Path
main=Path('app/lib/main.dart').read_text(encoding='utf-8')
viewer=Path('app/lib/story_v66.dart').read_text(encoding='utf-8')
owner=main[main.index('class _SohbetPageState'):main.index('class HikayeGosterPage')]
a=viewer.index('  Future<void> _yanitGonder(')
b=viewer.index('  Widget _medya(){',a)
reply=viewer[a:b]
checks={
  'story DM bubble has tap action':': storyReply\n          ? ()=>_hikayeYanitKartiAc(v)' in owner,
  'story card navigation verifies actual live story':'!ngelxHikayeAktif(v)' in owner and "v['ownerId']" in owner and 'gercekSahip!=kayitliSahip' in owner,
  'story tap links exact requested story ID':"initialStoryId:id" in owner and "ownerUid:gercekSahip" in owner,
  'expired/deleted story gets explanation':'Bu hikâye silinmiş veya süresi dolmuş.' in owner,
  'long story usernames are single line':'Text(widget.kullanici,maxLines:1,softWrap:false,overflow:TextOverflow.ellipsis' in viewer,
  'actions moved away from author name':'Row(mainAxisAlignment:MainAxisAlignment.end,children:[' in viewer,
  'story reply remains in correct current DM':"chat.collection('messages').doc().set({" in reply and "'storyId':storyId" in reply,
  'story reply loads already authenticated story':'final seciliHikaye=belge;' in reply and "seciliHikaye.data()['ownerId']" in reply,
  'story owner and expiration remain protected':'!ngelxHikayeAktif(seciliHikaye.data())' in reply and 'hedef!=widget.ownerUid.trim()' in reply,
  'optional preview does not delay success':'unawaited(chat.update({' in reply and 'await chat.update({' not in reply,
  'blocking/privacy guards remain active':"diger['blocked']" in reply and "messagePermission" in reply and "diger['restrictedUsers']" in reply,
  'story reaction and original gestures kept':"onTap:gonderiliyor?null:()=>_yanitGonder(e,tepki:true)" in viewer and 'onLongPressStart:(_)=>_duraklat()' in viewer,
  'version bumped to 426':"defaultValue: '426'" in main and 'version: 1.0.201+426' in Path('app/pubspec.yaml').read_text(encoding='utf-8'),
}
for name,ok in checks.items():print(('PASS ' if ok else 'FAIL ')+name,flush=True)
if not all(checks.values()):raise SystemExit('Build426 story UX/performance regression checks failed')
print('Build426 source checks PASS; live phone navigation/reply timing still requires device QA')
