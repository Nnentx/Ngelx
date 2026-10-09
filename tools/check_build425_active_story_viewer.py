#!/usr/bin/env python3
"""Build 425: protect the actual series story viewer against reply regression."""
from pathlib import Path

main=Path('app/lib/main.dart').read_text(encoding='utf-8')
active=Path('app/lib/story_v66.dart').read_text(encoding='utf-8')
a=active.index('  Future<void> _yanitGonder(String ham,{bool tepki=false})async{')
b=active.index('\n  Widget _medya(){',a)
reply=active[a:b]
checks={
  'real story series viewer is patched':'class NgelXHikayeSeriPage' in active,
  'source of former error removed':"Hikâye yanıtı gönderilemedi." not in reply,
  'active story owner verified':"story.data()?['ownerId']" in reply and 'widget.ownerUid' in reply,
  'story currently shown attached to message':"'storyId':storyId" in reply and "'storyUrl':url" in reply,
  'existing private chat looked up':"where('members',arrayContains:ben.uid)" in reply,
  'story replies are direct chat messages':'await chat.collection('+"'messages'"+').doc().set({' in reply,
  'story messages are created before chat preview':'asama='+"'mesaj-gonderimi'"+'' in reply and reply.index('await chat.collection(')<reply.index('await chat.update({'),
  'nonessential preview can fail without rejecting delivery':'ngelx_story_reply_preview' in reply,
  'no reply+video counter atomic batch':'batch.commit(' not in reply and 'replyCount' not in reply,
  'error stage and Firebase error code visible':'e.code' in reply and "Hikâye yanıtı: " in reply,
  'blocked and restricted users still protected':"diger['blocked']" in reply and "diger['restrictedUsers']" in reply,
  'recipient message preferences honored':"messagePermission" in reply,
  'old working visual viewer retained':'Widget _medya()' in active and 'Widget _ilerleme()' in active,
  'new version 425':"defaultValue: '425'" in main and 'version: 1.0.200+425' in Path('app/pubspec.yaml').read_text(encoding='utf-8'),
}
for label,ok in checks.items():
    print(('PASS ' if ok else 'FAIL ')+label,flush=True)
if not all(checks.values()):raise SystemExit('Build425 active carousel regression')
print('Build425 active story viewer source checks passed. LIVE delivery still unverified.')
