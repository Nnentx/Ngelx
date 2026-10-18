#!/usr/bin/env python3
"""Build491 scoped tests for chat-only mixed image/video gallery."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("b491","tools/apply_build491_chat_gallery_video.py")
assert spec and spec.loader
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
a=Path("app/lib/main.dart").read_text(encoding="utf-8")
b=Path("app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt").read_text(encoding="utf-8")
assert m.dart_transform(a)==a
assert m.native_transform(b)==b
for value in (
   "ngelxSohbetGaleriMedyaSec()",
   "_ngelxAndroidBelgeSec(const <String>['image/*','video/*'])",
   "bool ngelxSohbetVideoMu(XFile media)",
   "media=await ImagePicker().pickMedia()",
   "if(media==null)return null;",
   "grupVideoGonder(secilen:x)",
   "videoGonder(kaynak,secilen:x)",
   "Future<void> grupVideoGonder({XFile? secilen})",
   "Future<void> videoGonder(ImageSource kaynak,{XFile? secilen})",
   "ng elx-placeholder",
):
    if value=="ng elx-placeholder":value="return _ngelxGaleridenResmiNormalizeEt(media)"
    assert value in a,value
for value in (
   'cleanTypes.all { it.startsWith("image/") || it.startsWith("video/") }',
   'cleanTypes.all { it.startsWith("image/") } -> "image/*"',
   'cleanTypes.all { it.startsWith("video/") } -> "video/*"',
   'else -> "*/*"',
   'pickerRequestedImage = mimeTypes.isNotEmpty() && mimeTypes.all',
   'MediaStore.ACTION_PICK_IMAGES',
):
    assert value in b,value
assert "await _ngelxAndroidBelgeSec(const <String>['image/*']);" in a, "avatar/photo path must remain image only"
print("Build491: chat mixed media, original photo-only editor, group/private video upload routing PASS")
