#!/usr/bin/env python3
"""Build469 narrow performance: avoid per-keystroke token-list allocation and false profile loading.
No chat data migrations, cache identity changes, or Firestore privilege changes.
"""
from pathlib import Path
MAIN=Path('app/lib/main.dart')
STATE='class _SohbetPageState extends State<SohbetPage>'
END='class NgelXSesliMesaj extends StatefulWidget'
INBOX='class _MesajPageState extends State<MesajPage>'
INBOXEND='class ArsivSohbetlerPage'
TAG='// Build469: do not split the entire draft on every keypress'

def one(s,old,new,what):
    if s.count(old)!=1:
        raise RuntimeError(f'Build469 {what} drift: {s.count(old)}')
    return s.replace(old,new,1)
def transform(s):
    if TAG in s:return s
    a=s.index(STATE);b=s.index(END,a)
    r=s[a:b]
    r=one(r,
      "  void mesajDegisti(String deger){\n    PrivateDraftStore.schedule(widget.chatId,deger);\n    mentionZamanlayici?.cancel();\n    final sonParca=deger.split(RegExp(r'\\s+')).last;",
      """  // Build469: do not split the entire draft on every keypress.
  static final RegExp _wordBreak469=RegExp(r'\\s');
  late final DocumentReference<Map<String,dynamic>> _typingRef469=
      FirebaseFirestore.instance.collection('chats').doc(widget.chatId);
  void mesajDegisti(String deger){
    PrivateDraftStore.schedule(widget.chatId,deger);
    mentionZamanlayici?.cancel();
    final lastSpace=deger.lastIndexOf(_wordBreak469);
    final sonParca=deger.substring(lastSpace+1);""",
      'typing allocation')
    r=one(r,"mentionZamanlayici=Timer(const Duration(milliseconds:220),(){",
        "mentionZamanlayici=Timer(const Duration(milliseconds:350),(){",'mention search debounce')
    r=one(r,
       "    final ref=FirebaseFirestore.instance.collection('chats').doc(widget.chatId);\n    yaziyorZamanlayici?.cancel();",
       "    final ref=_typingRef469;\n    yaziyorZamanlayici?.cancel();",
       'reuse typing document')
    if 'onChanged:mesajDegisti' not in r:raise RuntimeError('chat composer action changed')
    s=s[:a]+r+s[b:]
    a=s.index(INBOX);b=s.index(INBOXEND,a)
    r=s[a:b]
    r=one(r,
        "ngelx455ProfileName(p, fallback:'Kişi bilgisi yükleniyor…')",
        "ngelx455ProfileName(p, fallback:'Kullanıcı')",
        'resolved inbox document cannot remain loading')
    # Actual loading and retry states remain visible and per-UID scoped.
    for expected in ["title:Text('Kişi bilgisi yükleniyor…')",
                     "_ngelx465ProfileRetryTimers",
                     "_profiles453.putIfAbsent"]:
        if expected not in r:raise RuntimeError('inbox retry/identity contract changed: '+expected)
    return s[:a]+r+s[b:]
if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if after!=before:MAIN.write_text(after,encoding='utf-8')
    print('Build469: cheap typing mention lookup; honest loaded profile fallback')
