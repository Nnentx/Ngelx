#!/usr/bin/env python3
"""Build479: keep the private chat route during Android DocumentsUI returns.

Avoid synthetic second-back and accidental plus-sheet taps while the picker
finishes. Does not change data, auth, camera/media contents or gallery provider.
"""
from pathlib import Path

MAIN=Path('app/lib/main.dart')
BEGIN='class _SohbetPageState extends State<SohbetPage>'
END='class NgelXSesliMesaj extends StatefulWidget'
MARK='// Build479: protect private chat navigation during gallery return'

def one(s,old,new,why):
    n=s.count(old)
    if n!=1:raise RuntimeError(f'Build479 {why}: expected one anchor; found {n}')
    return s.replace(old,new,1)

def transform(src):
    if MARK in src:return src
    first=src.index(BEGIN)
    last=src.index(END,first)
    p=src[first:last]
    p=one(p,
        '''  // Build477: don't launch another picker while one is still open.
  bool _ngelx477PhotoPickerActive=false;''',
        '''  // Build477: don't launch another picker while one is still open.
  bool _ngelx477PhotoPickerActive=false;
  // Build479: protect private chat navigation during gallery return.
  // Some Android 15 devices deliver another Back after DocumentsUI closes.
  // Block route pop + delayed tap dispatch for one short bounded period.
  bool _ngelx479PickerRouteGuard=false;
  Timer? _ngelx479PickerReturnTimer;
  void _ngelx479BeginPicker(){
    _ngelx479PickerReturnTimer?.cancel();
    if(mounted)setState(()=>_ngelx479PickerRouteGuard=true);
  }
  void _ngelx479EndPicker(){
    _ngelx479PickerReturnTimer?.cancel();
    _ngelx479PickerReturnTimer=Timer(const Duration(milliseconds:850),(){
      if(mounted)setState(()=>_ngelx479PickerRouteGuard=false);
    });
  }''',
        'single picker return guard state')
    p=one(p,
        '''      final x=await ngelxResimSec(
        source:kaynak,
        imageQuality:82,
        maxWidth:1440,
        maxHeight:1440,
      );
      if(x==null)return;''',
        '''      // Build479: hold the current conversation while Android DocumentsUI
      // is in front; release shortly after a deliberate select/cancel.
      _ngelx479BeginPicker();
      XFile? x;
      try{
        x=await ngelxResimSec(
          source:kaynak,
          imageQuality:82,
          maxWidth:1440,
          maxHeight:1440,
        );
      }finally{
        _ngelx479EndPicker();
      }
      if(x==null)return;''',
        'wrap only native gallery interaction')
    p=one(p,
        '''  void dispose(){WidgetsBinding.instance.removeObserver(this);_ngelx478FollowKeyboard=false;''',
        '''  void dispose(){_ngelx479PickerReturnTimer?.cancel();WidgetsBinding.instance.removeObserver(this);_ngelx478FollowKeyboard=false;''',
        'clear picker guard timer')
    p=one(p,
        '''  Widget build(BuildContext context)=>Theme(''',
        '''  Widget build(BuildContext context)=>PopScope(
    canPop:!_ngelx479PickerRouteGuard,
    child:Theme(''',
        'protect chat route while picker visible')
    p=one(p,
        '''    ])));}),
  ));
}

''',
        '''    ])));}),
  )));
}

''',
        'close PopScope around chat scaffold')
    p=one(p,
        '''                      onPressed:ekIslemiSuruyor?null:()async{
                        FocusManager.instance.primaryFocus?.unfocus();''',
        '''                      onPressed:ekIslemiSuruyor?null:()async{
                        // Ignore late OS taps after gallery closes; never
                        // open a sheet from a cancelled photo selection.
                        if(_ngelx479PickerRouteGuard||_ngelx477PhotoPickerActive)return;
                        FocusManager.instance.primaryFocus?.unfocus();''',
        'guard Ekle bottom-sheet ghost click')
    for action in ('camera','gallery'):
        p=one(p,
            f'onPressed:ekIslemiSuruyor?null:()=>medyaGonder(ImageSource.{action})',
            f'onPressed:ekIslemiSuruyor||_ngelx479PickerRouteGuard?null:()=>medyaGonder(ImageSource.{action})',
            'disable repeat native picker while returning '+action)
    for k in (
        'if(yaziSaatiDisarida&&saat.isNotEmpty)',
        'height:math.max(54.0,MediaQuery.viewPaddingOf(context).bottom)',
        '_ngelx478HistoryPointer()',
        'onTap:_ngelx478ComposerFocus',
        'bool _ngelx477PhotoPickerActive=false',
        "tooltip:'Kamera'","tooltip:'Galeri'",
        'onChanged:mesajDegisti',
        "if(veri.containsKey('backgroundUrl'))",
    ):
        if k not in p:raise RuntimeError('Build479 preserving prior fixes requires '+k)
    return src[:first]+p+src[last:]

if __name__=='__main__':
    orig=MAIN.read_text(encoding='utf-8')
    transformed=transform(orig)
    if orig!=transformed:MAIN.write_text(transformed,encoding='utf-8')
    print('Build479: private chat remains on screen during native gallery return')
