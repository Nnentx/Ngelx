#!/usr/bin/env python3
"""Build474: fix removed private wallpaper, repeated scroll and narrow composer.
The existing message, media, voice, call and security paths stay unchanged.
"""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
BEGIN='class _SohbetPageState extends State<SohbetPage>'
END='class NgelXSesliMesaj extends StatefulWidget'
MARKER='// Build474: a cleared shared background must override legacy per-user URLs'

def once(s,old,new,reason):
    n=s.count(old)
    if n!=1: raise RuntimeError(f'Build474 {reason}: expected one anchor, got {n}')
    return s.replace(old,new,1)

def transform(source):
    if MARKER in source:return source
    a=source.index(BEGIN);b=source.index(END,a)
    part=source[a:b]
    part=once(part,
        """  String _ozelSohbetArkaPlanUrl(Map<String,dynamic> veri){
    final ortak=(veri['backgroundUrl']??'').toString().trim();
    if(ortak.isNotEmpty)return ortak;
""",
        """  // Build474: a cleared shared background must override legacy per-user URLs.
  // Only chats without the shared field may fall back to old per-user fields.
  String _ozelSohbetArkaPlanUrl(Map<String,dynamic> veri){
    if(veri.containsKey('backgroundUrl')){
      return (veri['backgroundUrl']??'').toString().trim();
    }
""",'shared background overrides legacy')
    part=once(part,
        """  final List<QueryDocumentSnapshot<Map<String,dynamic>>> _mesajOnbellek=<QueryDocumentSnapshot<Map<String,dynamic>>>[];""",
        """  // Build474: ignore typing/read updates for list auto-scroll.
  String? _ngelx474LastMessageId;
  bool _ngelx474MessagesOpened=false;
  final List<QueryDocumentSnapshot<Map<String,dynamic>>> _mesajOnbellek=<QueryDocumentSnapshot<Map<String,dynamic>>>[];""",
        'message scroll state')
    part=once(part,
        "          if(s.hasData){sonaGit();_ngelx465ScheduleBottomOnOpen();}",
        """          // Build474: only scroll on initial load or a new tail message.
          // Chat metadata updates must not move the message list.
          if(s.hasData){
            final tailId=docs.isEmpty?'':docs.last.id;
            if(!_ngelx474MessagesOpened){
              _ngelx474MessagesOpened=true;
              _ngelx474LastMessageId=tailId;
              sonaGit();
              _ngelx465ScheduleBottomOnOpen();
            }else if(_ngelx474LastMessageId!=tailId){
              _ngelx474LastMessageId=tailId;
              sonaGit();
            }
          }""",
        'scroll only on new messages')
    part=once(part,
        '          :ngelxAltSistemRezervi(context),',
        '          :ngelxAltSistemRezervi(context,minimum:82), // Build474: keep composer above Android navigation',
        'bottom safe area')
    part=once(part,
        """                    // Build465: one-tap camera and gallery, as on group chat.
                    IconButton(""",
        """                    // Build474: camera and gallery stay under Ekle on narrow screens.
                    if(MediaQuery.sizeOf(context).width>=430)...[
                    // Build465: one-tap camera and gallery on wider screens.
                    IconButton(""",
        'compact composer')
    i=part.index('// Build474: camera and gallery')
    j=part.index('                    ValueListenableBuilder<TextEditingValue>(',i)
    chunk=part[i:j]
    if 'medyaGonder(ImageSource.camera)' not in chunk or 'medyaGonder(ImageSource.gallery)' not in chunk:
        raise RuntimeError('Build474 media handlers drifted')
    if not chunk.endswith('                    ),\n'):
        raise RuntimeError('Build474 gallery widget terminator drifted')
    part=part[:j]+'                    ],\n'+part[j:]
    if any(s not in part for s in ('onChanged:mesajDegisti','onPressed:sesKaydiDegistir','onPressed:emojiSec','onPressed:gonderiliyor?null:gonder')):
        raise RuntimeError('Build474 must preserve private composer functions')
    if 'bottomNavigationBar:ColoredBox(' not in part or 'memoize the private wallpaper decoration' not in part:
        raise RuntimeError('Build474 requires previous Build468 and Build472 fixes')
    combined=source[:a]+part+source[b:]
    # The remove action belongs to the separate chat-info class, not the chat list.
    return once(combined,
        """      await ref.set({'backgroundUrl':'','backgroundVersion':FieldValue.increment(1),'backgroundUpdatedBy':me,'backgroundUpdatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      await sistemOlayi('sohbet arka planını kaldırdı','remove');""",
        """      await ref.set({'backgroundUrl':'','backgroundVersion':FieldValue.increment(1),'backgroundUpdatedBy':me,'backgroundUpdatedAt':FieldValue.serverTimestamp()},SetOptions(merge:true));
      await FirebaseFirestore.instance.waitForPendingWrites().timeout(const Duration(seconds:8));
      await sistemOlayi('sohbet arka planını kaldırdı','remove');""",
        'acknowledged background removal')

if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if after!=before:MAIN.write_text(after,encoding='utf-8')
    print('Build474: private wallpaper removal, scroll and Android composer patched')
