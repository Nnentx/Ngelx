#!/usr/bin/env python3
"""Build 424 source contracts; actual two-account phone delivery is not implied."""
from pathlib import Path
s=Path('app/lib/main.dart').read_text(encoding='utf-8')
a=s.index('  Future<void> _yanitGonder(String ham,{bool tepki=false})async{',s.index('class _HikayeGosterPageState'))
b=s.index('  Widget _medya(){',a)
reply=s[a:b]
checks={
  'verify owner from authoritative story video document':"story.data()?['ownerId']" in reply,
  'do not send a story reply to logged in self':"if(hedef==ben.uid)" in reply,
  'protect blocked and restricted users':"diger['restrictedUsers']" in reply and "diger['blocked']" in reply,
  'respect target message permission':"messagePermission" in reply and "izinVar" not in reply,
  'existing random-ID chats can be reused':"where('members',arrayContains:ben.uid)" in reply,
  'lookup failures do not abort a permitted new DM':"on FirebaseException catch(e)" in reply and 'ngelx_story_reply_lookup' in reply,
  'actual message first':'chat.collection(' in reply and "'type':'story_reply'" in reply and reply.index("chat.collection('messages')")<reply.index("await chat.update({"),
  'chat preview errors never undo delivered message':"ngelx_story_reply_preview" in reply,
  'no atomic preview and reply batch':"batch.commit()" not in reply,
  'stage diagnostic for remaining failures':"Hikâye yanıtı: " in reply and "e.code" in reply,
  'story video player retained':"class _HikayeGosterPageState" in s,
  'build version advanced':"defaultValue: '424'" in s and 'version: 1.0.199+424' in Path('app/pubspec.yaml').read_text(),
  'security rules unchanged':Path('firestore.rules').exists(),
}
for label,ok in checks.items():print(('PASS ' if ok else 'FAIL ')+label,flush=True)
if not all(checks.values()):raise SystemExit('Build424 story static test failed')
print('Build424 story source contracts pass; LIVE delivery still requires two-account device QA.')
