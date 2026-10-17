#!/usr/bin/env python3
"""Build475: stable private composer during Android keyboard transitions.

Do not change Firestore security, conversations, media/call controls or
the Build474 background-removal semantics.
"""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
BEGIN='class _SohbetPageState extends State<SohbetPage>'
END='class NgelXSesliMesaj extends StatefulWidget'
MARK='// Build475: prevent a second composer resize during Android IME animation'

def once(src,old,new,name):
    n=src.count(old)
    if n!=1:
        raise RuntimeError(f'Build475 {name}: expected exactly one anchor, found {n}')
    return src.replace(old,new,1)

def transform(src):
    if MARK in src:
        return src
    start=src.index(BEGIN)
    stop=src.index(END,start)
    body=src[start:stop]

    body=once(body,
        """  Widget _engelDurumuDinle({required Widget Function(bool benEngelledim,bool oBeniEngelledi) builder}){""",
        """  // Build475: reuse Firestore snapshot sources between keyboard/layout
  // rebuilds rather than constructing fresh streams for each header/control.
  Stream<DocumentSnapshot<Map<String,dynamic>>>? _ngelx475SelfBlockStream;
  String? _ngelx475SelfBlockUid;
  late final Stream<DocumentSnapshot<Map<String,dynamic>>> _ngelx475PeerBlockStream=
      FirebaseFirestore.instance.collection('users').doc(widget.digerUid).snapshots();

  Widget _engelDurumuDinle({required Widget Function(bool benEngelledim,bool oBeniEngelledi) builder}){""",
        'reuse peer/self block streams')
    body=once(body,
        """    final users=FirebaseFirestore.instance.collection('users');
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:users.doc(ben).snapshots(),
      builder:(_,benSnap)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        stream:users.doc(widget.digerUid).snapshots(),""",
        """    final users=FirebaseFirestore.instance.collection('users');
    if(_ngelx475SelfBlockUid!=ben){
      _ngelx475SelfBlockUid=ben;
      _ngelx475SelfBlockStream=users.doc(ben).snapshots();
    }
    return StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
      stream:_ngelx475SelfBlockStream,
      builder:(_,benSnap)=>StreamBuilder<DocumentSnapshot<Map<String,dynamic>>>(
        stream:_ngelx475PeerBlockStream,""",
        'stable block widget subscriptions')

    # Build468 and Build474 own this property. Preserve the body below it
    # and require their essential guards instead of assuming a comment layout.
    slot_start=body.index('    bottomNavigationBar:ColoredBox(')
    slot_stop=body.index('    body:StreamBuilder',slot_start)
    previous_slot=body[slot_start:slot_stop]
    if ('MediaQuery.viewInsetsOf(context).bottom>0' not in previous_slot
        or 'ngelxAltSistemRezervi(context,minimum:82)' not in previous_slot):
        raise RuntimeError('Build475 unexpected private keyboard reservation')
    body=(body[:slot_start]
        + """    // Build475: prevent a second composer resize during Android IME animation.
    // Android adjustResize + Scaffold already avoid the keyboard. The old
    // 82dp-to-zero bottom bar made the input move twice, and too late.
    bottomNavigationBar:const SizedBox.shrink(),
"""
        + body[slot_stop:])

    body=once(body,
        """:SafeArea(top:false,bottom:false,child:Container(
        decoration:const BoxDecoration(color:Colors.white,border:Border(top:BorderSide(color:ngelxPrivateBlueBorder))),""",
        """:SafeArea(
        top:false,
        minimum:const EdgeInsets.only(bottom:10),
        child:Container(
        decoration:const BoxDecoration(color:Colors.white,border:Border(top:BorderSide(color:ngelxPrivateBlueBorder))),""",
        'single navigation safe area')

    body=once(body,
        """        padding:const EdgeInsets.fromLTRB(4,7,4,8),
        child:sesKaydediliyor""",
        """        padding:const EdgeInsets.fromLTRB(5,6,5,6),
        child:sesKaydediliyor""",
        'reduce unnecessary composer height')

    body=once(body,
        """                      child:AnimatedSize(
                        duration:const Duration(milliseconds:160),
                        curve:Curves.easeOut,
                        alignment:Alignment.bottomCenter,
                        child:TextField(""",
        """                      child:TextField(""",
        'remove animated TextField')
    body=once(body,
        """                          onChanged:mesajDegisti,
                          keyboardType:TextInputType.multiline,""",
        """                          onChanged:mesajDegisti,
                          // Build475: opening IME ends the 2s startup
                          // auto-scroll loop; it must not fight keyboard resize.
                          onTap:_ngelx465StopOpeningBottom,
                          keyboardType:TextInputType.multiline,""",
        'stop startup scrolling on focus')
    body=once(body,
        """                          minLines:1,maxLines:6,scrollPadding:const EdgeInsets.only(bottom:24),""",
        """                          minLines:1,maxLines:4,scrollPadding:EdgeInsets.zero,""",
        'bounded input and no auto-reveal extra scrolling')
    body=once(body,
        """                        ),
                      ),
                    ),

                    ValueListenableBuilder<TextEditingValue>(""",
        """                        ),
                    ),

                    ValueListenableBuilder<TextEditingValue>(""",
        'unwrap AnimatedSize')

    if 'resizeToAvoidBottomInset:true' not in body:
        raise RuntimeError('Build475: Scaffold must keep keyboard inset')
    for keep in (
        "if(veri.containsKey('backgroundUrl'))",
        '_ngelx472Wallpaper(arkaPlan,arkaPlanUrl,arkaPlanOpaklik)',
        'if(MediaQuery.sizeOf(context).width>=430)...[',
        'onPressed:sesKaydiDegistir',
        'medyaGonder(ImageSource.camera)',
        'medyaGonder(ImageSource.gallery)',
        'onPressed:gonderiliyor?null:gonder',
        '_engelDurumuDinle(builder:',
        'if(!_ngelx474MessagesOpened)',
    ):
        if keep not in body:
            raise RuntimeError('Build475: preserving prior behavior requires '+keep)
    return src[:start]+body+src[stop:]

if __name__=='__main__':
    old=MAIN.read_text(encoding='utf-8')
    new=transform(old)
    if new!=old: MAIN.write_text(new,encoding='utf-8')
    print('Build475: keyboard and composer layout stabilized; call/media behaviors preserved')
