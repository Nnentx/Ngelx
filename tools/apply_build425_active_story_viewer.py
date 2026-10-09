#!/usr/bin/env python3
"""Build 425: repair the *active* NgelXHikayeSeriPage story viewer.

The on-device 45490.mp4 captured the error text emitted by
app/lib/story_v66.dart, not by main.dart/HikayeGosterPage.
Run after Build 424, whose safe message-first reply routine is the source.
"""
from pathlib import Path

main=Path('app/lib/main.dart').read_text(encoding='utf-8')
start=main.index('  Future<void> _yanitGonder(String ham,{bool tepki=false})async{',main.index('class _HikayeGosterPageState'))
end=main.index('\n  Widget _medya(){',start)
delivery=main[start:end]
for needle in ("asama='mesaj-gonderimi'","await chat.collection('messages').doc().set({","ngelx_story_reply_preview"):
    if needle not in delivery:raise SystemExit('Build425 expected shared delivery step missing: '+needle)

# The carousel uses the active story document getters rather than the
# single-story viewer's widget parameters. Keep ownerUid from its widget,
# but attach the actual currently open story and its media to the reply.
for old,new in [
    ('widget.storyId','storyId'),
    ('widget.url','url'),
    ('widget.mediaType','mediaType'),
]:
    delivery=delivery.replace(old,new)

p=Path('app/lib/story_v66.dart')
s=p.read_text(encoding='utf-8')
a=s.index('  Future<void> _yanitGonder(String ham,{bool tepki=false})async{')
b=s.index('\n  Widget _medya(){',a)
old=s[a:b]
if "Hikâye yanıtı gönderilemedi." not in old or "batch.set(" not in old:
    raise SystemExit('Build425 active story viewer source drift; not safe to patch')
s=s[:a]+delivery+s[b:]
p.write_text(s,encoding='utf-8')

# This build contains the updated story viewer. Keep the prior version
# usable until the recipient confirms receipt in a real 2-account test.
p=Path('app/lib/main.dart')
s=p.read_text(encoding='utf-8')
for old,new in [
    ("defaultValue: '424'","defaultValue: '425'"),
    ("defaultValue: '1.0.199'","defaultValue: '1.0.200'"),
]:
    if s.count(old)!=1:raise SystemExit('Build425 version source drift: '+old)
    s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
p=Path('app/pubspec.yaml')
s=p.read_text(encoding='utf-8')
if s.count('version: 1.0.199+424')!=1:
    raise SystemExit('Build425 pubspec source drift')
p.write_text(s.replace('version: 1.0.199+424','version: 1.0.200+425',1),encoding='utf-8')
print('Build425: active story_v66 carousel now sends directly to existing DM messages, with chat preview nonblocking.')
