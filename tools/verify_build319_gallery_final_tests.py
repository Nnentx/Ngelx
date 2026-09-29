#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/lib/main.dart").read_text(encoding="utf-8")
ANDROID=(ROOT/"app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt").read_text(encoding="utf-8")
GROUP=(ROOT/"app/lib/group_quality.dart").read_text(encoding="utf-8")
PUB=(ROOT/"app/pubspec.yaml").read_text(encoding="utf-8")

def req(ok,msg):
    if not ok:
        raise SystemExit("Build 319 verification failed: "+msg)

req("version: 1.0.100+319" in PUB,"pubspec version")
req("defaultValue: '1.0.100'" in MAIN and "defaultValue: '319'" in MAIN,"runtime version")
req("Future<XFile> _ngelxGaleridenResmiNormalizeEt" in MAIN,"gallery normalization helper")
req("return await _ngelxGaleridenResmiNormalizeEt(x);" in MAIN,"single gallery normalization")
req("guvenli.add(await _ngelxGaleridenResmiNormalizeEt(x))" in MAIN,"multi gallery normalization")
req("class _VideoKartiState extends State<VideoKarti> with WidgetsBindingObserver,RouteAware" in MAIN,"video route audio lifecycle")
req("class _GorselYaziKartiState extends State<GorselYaziKarti> with RouteAware" in MAIN,"photo music route lifecycle")
req("lt('Taslağa kaydet','Save draft')" in MAIN,"create draft localization")
req("lt('Yayınlanamadı: ','Could not publish: ')" in MAIN,"create error localization")
req("private fun decodeGalleryBitmap(uri: Uri): Bitmap?" in ANDROID,"Android gallery decoder")
req("contentResolver.loadThumbnail(uri, Size(2160, 2160), null)" in ANDROID,"Android thumbnail fallback")
req("throw IllegalArgumentException(\"Galeriden seçilen fotoğraf çözülemedi.\")" in ANDROID,"raw undecodable image rejection")
req("const ListTile(\n              leading: CircleAvatar" not in GROUP,"dynamic group message info is not const")
print("Build 319 gallery/final-test verification passed.")
