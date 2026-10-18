#!/usr/bin/env python3
"""Build491 QA: mixed photo/video picker only for chat composer gallery.

Preserve avatar/cover/photo-only editors, file picker, camera permissions,
existing photo upload and video upload flows. Apply after Build480 and all
main.dart source transformations, before flutter analyze.
"""
from pathlib import Path

MAIN=Path("app/lib/main.dart")
NATIVE=Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt")
MARK="// Build491: chat gallery picks photos or videos without changing photo-only editors"

DART=r"""
// Build491: chat gallery picks photos or videos without changing photo-only editors.
bool ngelxSohbetVideoMu(XFile media) {
  final mime=(media.mimeType??'').toLowerCase();
  final ext=media.name.split('.').last.toLowerCase();
  return mime.startsWith('video/') || const {'mp4','mov','m4v','webm'}.contains(ext);
}

Future<XFile?> ngelxSohbetGaleriMedyaSec() async {
  XFile? media;
  if(Platform.isAndroid){
    try {
      // Null is cancellation: never open a second picker after cancel.
      media=await _ngelxAndroidBelgeSec(const <String>['image/*','video/*']);
      if(media==null)return null;
    }on MissingPluginException{
      media=await ImagePicker().pickMedia();
    }on PlatformException{
      media=await ImagePicker().pickMedia();
    }
  }else{
    media=await ImagePicker().pickMedia();
  }
  if(media==null)return null;
  if(ngelxSohbetVideoMu(media)){
    return _ngelxKaliciYerelKopya(
      media,uzanti:_ngelxYerelUzanti(media,varsayilan:'mp4'),
      mimeType:media.mimeType??'video/mp4',
    );
  }
  return _ngelxGaleridenResmiNormalizeEt(media);
}
"""


def once(s,old,new,label):
    n=s.count(old)
    if n!=1:raise RuntimeError(f"Build491 {label}: expected 1, got {n}")
    return s.replace(old,new,1)


def dart_transform(source):
    if MARK in source:return source
    source=once(source,"Future<XFile?> ngelxResimSec({",DART+"\nFuture<XFile?> ngelxResimSec({","photo/video chat picker helper")

    # Older UI generators may insert guards/formatting into this method.
    # Anchor to the existing group photo sender, not to exact whitespace.
    import re
    group_end=source.index("  Future<void> _grupFotografiniGonder(")
    group_start=source.rfind("  Future<void> medyaGonder(ImageSource kaynak)",0,group_end)
    if group_start<0:
        raise RuntimeError("Build491 group gallery method not found")
    group=source[group_start:group_end]
    selection=re.search(r"final\s+x\s*=\s*await\s+ngelxResimSec\([^;]+\);",group,re.S)
    if selection is None:
        raise RuntimeError("Build491 group gallery image chooser changed: "+repr(group[:1600]))
    group=group[:selection.start()]+"""final x=kaynak==ImageSource.gallery
      ?await ngelxSohbetGaleriMedyaSec()
      :await ngelxResimSec(source:kaynak,imageQuality:76,maxWidth:1280);
    if(x==null)return;
    if(kaynak==ImageSource.gallery&&ngelxSohbetVideoMu(x)){
      await grupVideoGonder(secilen:x);
      return;
    }"""+group[selection.end():]
    source=source[:group_start]+group+source[group_end:]

    source=once(source,
      """  Future<void> grupVideoGonder()async{
    final x=await ngelxVideoSec(source:ImageSource.gallery,maxDuration:const Duration(minutes:3));""",
      """  Future<void> grupVideoGonder({XFile? secilen})async{
    final x=secilen??await ngelxVideoSec(source:ImageSource.gallery,maxDuration:const Duration(minutes:3));""",
      "group pre-selected video")

    # Build477 adds picker guards; find the private photo selection semantically
    # instead of requiring exact whitespace/adjacent source statements.
    private_start=source.index("class _SohbetPageState")
    private_end=source.index("  Future<void> videoGonder(",private_start)
    private_picker=source.rfind("  Future<void> medyaGonder(ImageSource kaynak)",private_start,private_end)
    if private_picker<0:raise RuntimeError("Build491 private media sender missing")
    private=source[private_picker:private_end]
    import re
    chosen=re.search(r"final\s+x\s*=\s*await\s+ngelxResimSec\([\s\S]*?\);",private)
    if chosen is None:raise RuntimeError("Build491 private image selection changed")
    private=private[:chosen.start()]+"""final x=kaynak==ImageSource.gallery
        ?await ngelxSohbetGaleriMedyaSec()
        :await ngelxResimSec(
            source:kaynak,imageQuality:82,maxWidth:1440,maxHeight:1440,
          );
      if(x==null)return;
      if(kaynak==ImageSource.gallery&&ngelxSohbetVideoMu(x)){
        await videoGonder(kaynak,secilen:x);
        return;
      }"""+private[chosen.end():]
    source=source[:private_picker]+private+source[private_end:]

    source=once(source,
      """  Future<void> videoGonder(ImageSource kaynak)async{
    final ben=uid;""",
      """  Future<void> videoGonder(ImageSource kaynak,{XFile? secilen})async{
    final ben=uid;""",
      "private optional selected video")

    source=once(source,
      """      final x=await ngelxVideoSec(source:kaynak,maxDuration:const Duration(minutes:5));
      if(x==null)return;""",
      """      final x=secilen??await ngelxVideoSec(source:kaynak,maxDuration:const Duration(minutes:5));
      if(x==null)return;""",
      "private selected media used")
    return source


def native_transform(source):
    if MARK in source:return source
    condition="""        if (pickerRequestedImage &&
            cleanTypes.all { it.startsWith("image/") } &&
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {"""
    expanded="""        // Build491: chat media accepts image AND video from Android Photo Picker.
        // The original image-only avatar / cover callers retain their filter.
        if (cleanTypes.isNotEmpty() &&
            cleanTypes.all { it.startsWith("image/") || it.startsWith("video/") } &&
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {"""
    source=once(source,condition,expanded,"Android photo picker eligibility")
    source=once(source,
      """                    type = "image/*"
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)""",
      """                    type = when {
                        cleanTypes.all { it.startsWith("image/") } -> "image/*"
                        cleanTypes.all { it.startsWith("video/") } -> "video/*"
                        else -> "*/*"
                    }
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)""",
      "photo picker MIME")
    source=once(source,
      """                        putExtra(
                            MediaStore.EXTRA_PICK_IMAGES_LAUNCH_TAB,
                            MediaStore.PICK_IMAGES_TAB_IMAGES,
                        )""",
      """                        if (cleanTypes.all { it.startsWith("image/") }) {
                            putExtra(
                                MediaStore.EXTRA_PICK_IMAGES_LAUNCH_TAB,
                                MediaStore.PICK_IMAGES_TAB_IMAGES,
                            )
                        }""",
      "image-only tab choice")
    source=once(source,
      """pickerRequestedImage = mimeTypes.any { it == "image/*" || it.startsWith("image/") }""",
      """pickerRequestedImage = mimeTypes.isNotEmpty() && mimeTypes.all { it == "image/*" || it.startsWith("image/") }""",
      "prevent video bytes being treated as image")
    return source


def main():
    for path,fn in ((MAIN,dart_transform),(NATIVE,native_transform)):
        a=path.read_text(encoding="utf-8")
        b=fn(a)
        if a!=b:path.write_text(b,encoding="utf-8")
    print("Build491 mixed chat gallery selection: image/photo-only paths preserved")


if __name__=="__main__":main()
