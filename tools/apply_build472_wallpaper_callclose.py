#!/usr/bin/env python3
"""Build472: private wallpaper must NOT recreate a network image on each chat
rebuild. Prevent finishing a call from editing another user's call message.
No data migrations, chat schema changes, or ringtone changes.
"""
from pathlib import Path
MAIN=Path('app/lib/main.dart')
STATE='class _SohbetPageState extends State<SohbetPage>'
END='class NgelXSesliMesaj extends StatefulWidget'
MARKER='// Build472: memoize the private wallpaper decoration'
def once(s,a,b,label):
    n=s.count(a)
    if n!=1:raise RuntimeError(f'Build472 {label}: expected one anchor got {n}')
    return s.replace(a,b,1)
def transform(src):
    if MARKER in src:return src
    start=src.index(STATE);stop=src.index(END,start)
    part=src[start:stop]
    old='''  String _ozelSohbetArkaPlanUrl(Map<String,dynamic> veri){'''
    new='''  // Build472: memoize the private wallpaper decoration and its image
  // provider. Changing text/typing must not reallocate a ResizeImage or
  // decode the same large gallery image over and over.
  String? _wallpaperKey472;
  BoxDecoration? _wallpaperDecoration472;
  BoxDecoration _ngelx472Wallpaper(Color color,String url,double opacity){
    final key=url+'|'+color.value.toString()+'|'+opacity.toString();
    if(_wallpaperKey472==key && _wallpaperDecoration472!=null){
      return _wallpaperDecoration472!;
    }
    _wallpaperKey472=key;
    _wallpaperDecoration472=BoxDecoration(
      color:color,
      image:url.isEmpty?null:DecorationImage(
        image:ResizeImage(NgelXAgImageProvider(url),width:720),
        fit:BoxFit.cover,
        opacity:opacity,
        filterQuality:FilterQuality.low,
      ),
    );
    return _wallpaperDecoration472!;
  }

  String _ozelSohbetArkaPlanUrl(Map<String,dynamic> veri){'''
    part=once(part,old,new,'wallpaper cache')
    part=once(part,
        'return Container(decoration:BoxDecoration(color:arkaPlan,image:arkaPlanUrl.isEmpty?null:DecorationImage(image:ResizeImage(NgelXAgImageProvider(arkaPlanUrl),width:900),fit:BoxFit.cover,opacity:arkaPlanOpaklik,filterQuality:FilterQuality.low)),child:AnimatedPadding(',
        'return Container(decoration:_ngelx472Wallpaper(arkaPlan,arkaPlanUrl,arkaPlanOpaklik),child:AnimatedPadding(',
        'reuse decoration and image cache')
    if '_ngelx470ComposerTick' not in part or 'onChanged:mesajDegisti' not in part:
        raise RuntimeError('Build470 typing controls lost')
    if 'bottomNavigationBar:ColoredBox(' not in part:
        raise RuntimeError('Build468 Android nav-safe composer lost')
    part=once(part,
      "if(mesajId.isNotEmpty){\n            await widget.aramaRef.collection('messages').doc(mesajId).set({",
      "if(mesajId.isNotEmpty && data['callStartedBy']==me){\n            await widget.aramaRef.collection('messages').doc(mesajId).set({",
      'private call message ownership')
    return src[:start]+part+src[stop:]
if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=transform(before)
    if after!=before:MAIN.write_text(after,encoding='utf-8')
    print('Build472: memoized private wallpaper; only call message author updates original history')
