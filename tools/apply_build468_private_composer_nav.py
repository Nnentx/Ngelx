#!/usr/bin/env python3
"""Build468: keep private composer above Android three-button/gesture navigation.

The prior Build465 change removed bottomNavigationBar's device reservation and
Build467 only changed control widths. Those were not sufficient on Android 15
with three-button navigation: composer may draw underneath system buttons.
This scoped patch reserves a bottom slot while the keyboard is closed and
lets Scaffold lift the composer with the keyboard when it opens.
No message/attachment/voice/call handlers or server paths are altered.
"""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
BEGIN='class _SohbetPageState extends State<SohbetPage>'
END='class NgelXSesliMesaj extends StatefulWidget'
MARKER='// Build468: explicit Android nav-safe composer slot'

def replace_exact(s,old,new,why):
    n=s.count(old)
    if n!=1:
        raise RuntimeError(f'Build468 {why}: expected one anchor, got {n}')
    return s.replace(old,new,1)

def transform(s):
    if MARKER in s:return s
    a=s.index(BEGIN)
    b=s.index(END,a)
    region=s[a:b]
    region=replace_exact(region,
      """    // Build465: the composer already has SafeArea(top:false) at the bottom.
    bottomNavigationBar:const SizedBox.shrink(),""",
      """    // Build468: explicit Android nav-safe composer slot.
    // A zero-height bar did not reserve Android 3-button navigation on
    // the reported MIUI handset. The composer draws ABOVE this slot.
    // Keyboard insets belong to Scaffold; don't reserve this while typing.
    bottomNavigationBar:ColoredBox(
      color:Colors.white,
      child:SizedBox(
        height:MediaQuery.viewInsetsOf(context).bottom>0
          ?0
          :ngelxAltSistemRezervi(context),
      ),
    ),""",'bottom slot')
    region=replace_exact(region,
      ':SafeArea(top:false,minimum:const EdgeInsets.only(bottom:7),child:Container(',
      ':SafeArea(top:false,bottom:false,child:Container(', 'no duplicate safe area')
    region=replace_exact(region,
      """          : Row(
              crossAxisAlignment:CrossAxisAlignment.end,
              children:[""",
      """          : Row(
              // Center fixed 44dp controls against the message TextField.
              crossAxisAlignment:CrossAxisAlignment.center,
              children:[""",'composer row alignment')
    region=replace_exact(region,
      'contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:10),',
      'contentPadding:const EdgeInsets.symmetric(horizontal:12,vertical:12),',
      'input height')
    # Keep the existing composer on Scaffold's resizeToAvoidBottomInset route.
    if region.count('resizeToAvoidBottomInset:true')!=1:
        raise RuntimeError('Build468: Scaffold keyboard resizing was changed')
    for handler in ('medyaGonder(ImageSource.camera)','medyaGonder(ImageSource.gallery)',
                    'onPressed:sesKaydiDegistir','onPressed:emojiSec','onPressed:gonderiliyor?null:gonder'):
        if handler not in region:raise RuntimeError('Build468: missing handler '+handler)
    return s[:a]+region+s[b:]

def main():
    current=MAIN.read_text(encoding='utf-8')
    changed=transform(current)
    if changed!=current:MAIN.write_text(changed,encoding='utf-8')
    print('Build468: private composer safely above device navbar; keyboard resize retained')

if __name__=='__main__':
    main()
