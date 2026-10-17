#!/usr/bin/env python3
"""Build477: safe full-screen Android gallery and no duplicate photo picker."""
from pathlib import Path
MAIN=Path('app/lib/main.dart')
NATIVE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt')
MARKER='// Build477: native gallery cancellation must never open another picker'
NATIVE_MARKER='// Build477: use full-screen Android DocumentsUI for image selections'

def replace_one(s,old,new,label):
    n=s.count(old)
    if n!=1: raise RuntimeError(f'Build477 {label}: expected 1 anchor, got {n}')
    return s.replace(old,new,1)

def patch_main(s):
    if MARKER in s:return s
    s=replace_one(s,
      """  if(source==ImageSource.gallery&&Platform.isAndroid){
    try{
      final x=await _ngelxAndroidBelgeSec(const <String>['image/*']);
      if(x!=null)return await _ngelxGaleridenResmiNormalizeEt(x);
    }catch(_){}
    yenidenKodla=false;
  }
  final x=await ImagePicker().pickImage(""",
      """  // Build477: native gallery cancellation must never open another picker.
  // Android document picker errors are not a reason to open a second
  // picker; only an unavailable native channel may use legacy fallback.
  if(source==ImageSource.gallery&&Platform.isAndroid){
    try{
      final x=await _ngelxAndroidBelgeSec(const <String>['image/*']);
      if(x==null)return null;
      return await _ngelxGaleridenResmiNormalizeEt(x);
    }on MissingPluginException{
      yenidenKodla=false;
    }
  }
  final x=await ImagePicker().pickImage(""",
      'do not reopen after cancel/error')
    start=s.index('class _SohbetPageState extends State<SohbetPage>')
    stop=s.index('class NgelXSesliMesaj extends StatefulWidget',start)
    chat=s[start:stop]
    chat=replace_one(chat,
      """  Future<void> medyaGonder(ImageSource kaynak) async {
    final ben=uid;
    if(ben==null||ekIslemiSuruyor)return;
    try{""",
      """  // Build477: don't launch another picker while one is still open.
  bool _ngelx477PhotoPickerActive=false;
  Future<void> medyaGonder(ImageSource kaynak) async {
    final ben=uid;
    if(ben==null||ekIslemiSuruyor||_ngelx477PhotoPickerActive)return;
    _ngelx477PhotoPickerActive=true;
    try{""",
      'private gallery duplicate tap guard')
    chat=replace_one(chat,
      """    }finally{
      _ekIslemBitir();
    }
  }

  Future<void> videoGonder(""",
      """    }finally{
      _ngelx477PhotoPickerActive=false;
      _ekIslemBitir();
    }
  }

  Future<void> videoGonder(""",
      'always release on cancel/error')
    for term in ("tooltip:'Galeri'","tooltip:'Kamera'",
      'height:math.max(54.0,MediaQuery.viewPaddingOf(context).bottom)',
      'if(!_ngelx474MessagesOpened)',
      'onChanged:mesajDegisti'):
        if term not in chat:raise RuntimeError('Build477 preserved chat contract missing '+term)
    return s[:start]+chat+s[stop:]

def patch_native(s):
    if NATIVE_MARKER in s:return s
    s=replace_one(s,
      """        try {
            startActivityForResult(build(Intent.ACTION_GET_CONTENT), REQUEST_PICK)""",
      """        // Build477: use full-screen Android DocumentsUI for image selections.
        // GET_CONTENT opens a half-screen OS photo picker on the reported phone.
        val firstAction = if (pickerRequestedImage) Intent.ACTION_OPEN_DOCUMENT
            else Intent.ACTION_GET_CONTENT
        val fallbackAction = if (pickerRequestedImage) Intent.ACTION_GET_CONTENT
            else Intent.ACTION_OPEN_DOCUMENT
        try {
            startActivityForResult(build(firstAction), REQUEST_PICK)""",
      'prefer full-screen native document picker for images')
    s=replace_one(s,
      'startActivityForResult(build(Intent.ACTION_OPEN_DOCUMENT), REQUEST_PICK)',
      'startActivityForResult(build(fallbackAction), REQUEST_PICK)',
      'preserve fallback only if full-screen DocumentsUI unavailable')
    return s

if __name__=='__main__':
    before=MAIN.read_text(encoding='utf-8')
    after=patch_main(before)
    if before!=after:MAIN.write_text(after,encoding='utf-8')
    before=NATIVE.read_text(encoding='utf-8')
    after=patch_native(before)
    if before!=after:NATIVE.write_text(after,encoding='utf-8')
    print('Build477: full-screen image document chooser and single-flight private photo picker')
