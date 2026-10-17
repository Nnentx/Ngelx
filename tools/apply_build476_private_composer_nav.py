#!/usr/bin/env python3
"""Build476: recover one-tap camera/gallery and a fixed Android nav reservation.
Preserve all chat, media and call handlers and Build474's photo removal fix.
"""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
BEGIN='class _SohbetPageState extends State<SohbetPage>'
END='class NgelXSesliMesaj extends StatefulWidget'
MARKER='// Build476: stable bottom navigation reservation for all IME states'

def transform(source: str) -> str:
    if MARKER in source:return source
    start=source.index(BEGIN);end=source.index(END,start)
    chat=source[start:end]
    old='    bottomNavigationBar:const SizedBox.shrink(),'
    if chat.count(old)!=1 or 'resizeToAvoidBottomInset:true' not in chat:
        raise RuntimeError('Build476: expected Build475 nav layout in private chat')
    chat=chat.replace(old,'''    // Build476: stable bottom navigation reservation for all IME states.
    // Android 15 can report no safe bottom inset with 3-button nav visible.
    // Never switch the bottom reservation to zero during a keystroke.
    bottomNavigationBar:ColoredBox(
      color:Colors.white,
      child:SizedBox(
        height:math.max(54.0,MediaQuery.viewPaddingOf(context).bottom),
      ),
    ),''',1)
    # Select by the executable conditional, not the comments: earlier
    # generated UI patches may rewrite explanatory comments.
    begin=chat.index('if(MediaQuery.sizeOf(context).width>=430)...[')
    stop=chat.index('                    ValueListenableBuilder<TextEditingValue>(',begin)
    icons=chat[begin:stop]
    for term in ('medyaGonder(ImageSource.camera)',
                 'medyaGonder(ImageSource.gallery)',
                 "tooltip:'Kamera'","tooltip:'Galeri'"):
        if term not in icons:
            raise RuntimeError('Build476 missing original camera/gallery '+term)
    branch_prefix='if(MediaQuery.sizeOf(context).width>=430)...['
    icons=icons.replace(branch_prefix,
      '// Build476: camera and gallery remain directly visible at every width',1)
    pos=icons.rfind('                    ],')
    if pos<0 or icons[pos+len('                    ],'):].strip():
        raise RuntimeError('Build476 camera/gallery group close not unique')
    icons=icons[:pos]+icons[pos:].replace('                    ],','',1)
    for width in ('36','33'):
        icons=icons.replace(
          'constraints:const BoxConstraints.tightFor(width:'+width+',height:44)',
          'constraints:const BoxConstraints.tightFor(width:31,height:44)')
    if icons.count('constraints:const BoxConstraints.tightFor(width:31,height:44)')!=2:
        raise RuntimeError('Build476 camera/gallery width constraints drifted')
    chat=chat[:begin]+icons+chat[stop:]
    for term in (
      'height:math.max(54.0,MediaQuery.viewPaddingOf(context).bottom)',
      'minimum:const EdgeInsets.only(bottom:10)',
      "tooltip:'Kamera'","tooltip:'Galeri'",
      'onPressed:sesKaydiDegistir','onPressed:emojiSec',
      'onPressed:gonderiliyor?null:gonder',
      'onTap:_ngelx465StopOpeningBottom',
      "if(veri.containsKey('backgroundUrl'))",
    ):
        if term not in chat:raise RuntimeError('Build476: prior contract missing '+term)
    return source[:start]+chat+source[end:]

if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if after!=before:MAIN.write_text(after,encoding='utf-8')
    print('Build476: stable Android nav reservation and one-tap camera/gallery restored')
