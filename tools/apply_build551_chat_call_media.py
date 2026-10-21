from pathlib import Path

TAG='// Build551 chat reaction, compact voice cards and photo latency'
def once(s,a,b):
    if s.count(a)!=1:
        raise RuntimeError(f'Build551 expected one anchor, found {s.count(a)}: {a[:100]}')
    return s.replace(a,b,1)

def main_source(s):
    if TAG in s:return s
    s=once(s,"part 'build548_widgets.dart';", "part 'build548_widgets.dart';\npart 'build551_widgets.dart';")
    s=once(s,"import 'build548_policy.dart';", "import 'build548_policy.dart';\nimport 'build551_media.dart';")
    a=s.index('  Widget _grupMedyaTepkiAlani(')
    b=s.index('// Build465 Messenger quote',a)
    s=s[:a]+'''  Widget _grupMedyaTepkiAlani(Widget media,DocumentReference<Map<String,dynamic>> ref,Map<String,int> counts,int total){
    if(total<=0)return media;
    return Ngelx551MediaReaction(media:media,badge:_grupMedyaTepkiBalonu(ref,counts,total));
  }

'''+s[b:]
    a=s.index('  Widget _grupAramaAlani(){')
    b=s.index('  Widget _videoAlani(){',a)
    body=s[a:b]
    start=body.index('child:LayoutBuilder(builder:(_,constraints)=>GridView.builder(')
    end=body.index('      )))),',start)+len('      )))),')
    body=body[:start]+'''child:Ngelx551CallGrid(
        count:katilimcilar.length,columns:sutun,voice:!widget.goruntulu,
        itemBuilder:(_,i)=>_katilimciKutusu(katilimcilar[i].p,yerel:katilimcilar[i].yerel),
      ))),'''+body[end:]
    s=s[:a]+body+s[b:]
    s=once(s,'Future<Uint8List> _ngelxFotografiJpegHazirla(Uint8List hamBytes) async {',
      'Future<Uint8List> _ngelxFotografiJpegHazirla(Uint8List hamBytes,{bool chat=false}) async {')
    s=once(s,'      var decoded=img.decodeImage(hamBytes);',
      '      if(chat)return ngelx551ChatJpeg(hamBytes);\n      var decoded=img.decodeImage(hamBytes);')
    # Unsupported formats still use the existing native PNG conversion fallback.
    s=once(s,'        var decoded=img.decodePng(png);',
      '        if(chat)return ngelx551ChatJpeg(png);\n        var decoded=img.decodePng(png);')
    s=once(s,'yuklenecekBytes=await _ngelxFotografiJpegHazirla(bytes);',
      'yuklenecekBytes=await _ngelxFotografiJpegHazirla(bytes,chat:ngelx551ChatPhotoKind(kind));')
    # Photos already undergo a full remote download and pixel decode. Do that
    # once, instead of a redundant range GET followed by the full download.
    s=once(s,'''    final okunabilir=await _ngelxMedyaYayininiDogrula(url);
    return _ngelxFotoKind(kind)
      ?await _ngelxFotografYayininiDogrula(okunabilir)
      :okunabilir;''', '''    if(_ngelxFotoKind(kind))return _ngelxFotografYayininiDogrula(url);
    return _ngelxMedyaYayininiDogrula(url);''')
    a=s.index('  Future<bool> payloadGonder(')
    b=s.index('  Future<void> gonder()',a)
    body=s[a:b]
    body=once(body,"        final profil=await FirebaseFirestore.instance.collection('users').doc(ben).get();\n        final ad=(profil.data()?['displayName']??profil.data()?['username']??'Bir kullanıcı').toString();\n",'')
    s=s[:a]+body+s[b:]
    return s+'\n'+TAG+'\n'

def apply(root=Path('app/lib')):
    p=root/'main.dart';p.write_text(main_source(p.read_text()))
    for name in ['widgets','media']:
        (root/f'build551_{name}.dart').write_text(Path(f'tools/build551_{name}.dart').read_text())
if __name__=='__main__':apply()
