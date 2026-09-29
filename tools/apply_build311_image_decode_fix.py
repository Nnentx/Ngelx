#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / "app/lib/main.dart"
PUB_PATH = ROOT / "app/pubspec.yaml"
ANDROID_PATH = ROOT / "app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt"

main = MAIN_PATH.read_text(encoding="utf-8")
pub = PUB_PATH.read_text(encoding="utf-8")
android = ANDROID_PATH.read_text(encoding="utf-8")

if "version: 1.0.92+311" in pub:
    print("Build 311 already applied.")
    raise SystemExit(0)

def one(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Build 311 patch failed: {label}: expected 1 match, got {count}")
    return text.replace(old, new, 1)

start = main.find("Future<String> ngelxFotografYukle({")
end = main.find("Future<void> ngelxMedyaSil(", start)
if start < 0 or end < 0:
    raise SystemExit("Build 311 patch failed: ngelxFotografYukle block not found")

photo_helper = r'''Future<String> ngelxFotografYukle({
  required XFile dosya,
  required String kind,
  required String legacyPath,
  String? ext,
  void Function(int sent,int total)? onProgress,
}) async {
  final ad=dosya.name.trim();
  final mime=(dosya.mimeType??'').trim().toLowerCase().split(';').first;
  final hamExt=(ext??(ad.contains('.')?ad.split('.').last:'jpg')).toLowerCase();
  var temizExt=_ngelxUzantiTemizle(hamExt);

  if(mime=='image/jpeg'||mime=='image/jpg')temizExt='jpg';
  else if(mime=='image/png')temizExt='png';
  else if(mime=='image/webp')temizExt='webp';
  else if(mime=='image/gif')temizExt='gif';
  else if(mime=='image/heic')temizExt='heic';
  else if(mime=='image/heif')temizExt='heif';
  else if(mime=='image/avif')temizExt='avif';

  final tur=mime.startsWith('image/')?mime:_ngelxContentType(temizExt);
  try{
    final boyut=await dosya.length();
    if(boyut<=0)throw Exception('Seçilen fotoğraf boş görünüyor.');
    return await ngelxMedyaYukleDosya(
      dosya:dosya,
      kind:kind,
      ext:temizExt,
      legacyPath:legacyPath.replaceFirst(RegExp(r'\.[^.]+$'),'.'+temizExt),
      contentType:tur,
      onProgress:onProgress,
    );
  }catch(e){
    throw Exception('Fotoğraf yüklenemedi: '+_ngelxKisaHata(e));
  }
}

'''
main = main[:start] + photo_helper + main[end:]

android = one(
    android,
    "import android.database.Cursor\n",
    "import android.database.Cursor\nimport android.graphics.Bitmap\nimport android.graphics.BitmapFactory\nimport android.graphics.ImageDecoder\nimport android.os.Build\n",
    "Android image imports",
)
android = one(
    android,
    "import java.util.concurrent.Executors\n",
    "import java.util.concurrent.Executors\nimport kotlin.math.max\n",
    "Android math import",
)

copy_start = android.find("    private fun copyUriToCache(uri: Uri): Map<String, Any?> {")
copy_end = android.find("    private fun displayName(uri: Uri): String {", copy_start)
if copy_start < 0 or copy_end < 0:
    raise SystemExit("Build 311 patch failed: copyUriToCache block not found")

copy_block = r'''    private fun copyUriToCache(uri: Uri): Map<String, Any?> {
        val originalName = displayName(uri).ifBlank { "ngelx_${System.currentTimeMillis()}" }
        val mimeType = contentResolver.getType(uri)?.lowercase()

        if (mimeType?.startsWith("image/") == true && mimeType != "image/gif") {
            val normalized = normalizeImageToJpeg(uri)
            if (normalized != null && normalized.length() > 0L) {
                val baseName = originalName.substringBeforeLast('.', originalName)
                    .replace(Regex("[^A-Za-z0-9._-]"), "_")
                    .ifBlank { "ngelx_${System.currentTimeMillis()}" }
                return mapOf(
                    "path" to normalized.absolutePath,
                    "name" to "$baseName.jpg",
                    "mimeType" to "image/jpeg",
                    "size" to normalized.length(),
                )
            }
        }

        val safeName = originalName.replace(Regex("[^A-Za-z0-9._-]"), "_")
            .ifBlank { "ngelx_${System.currentTimeMillis()}" }
        val pickerDir = File(cacheDir, "ngelx_picker").apply { mkdirs() }
        val target = File(pickerDir, "${System.currentTimeMillis()}_$safeName")
        contentResolver.openInputStream(uri).use { input ->
            requireNotNull(input) { "Dosya akışına erişilemedi." }
            FileOutputStream(target).use { output -> input.copyTo(output) }
        }
        return mapOf(
            "path" to target.absolutePath,
            "name" to originalName,
            "mimeType" to mimeType,
            "size" to target.length(),
        )
    }

    private fun normalizeImageToJpeg(uri: Uri): File? {
        return try {
            val bitmap: Bitmap? = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                val source = ImageDecoder.createSource(contentResolver, uri)
                ImageDecoder.decodeBitmap(source) { decoder, info, _ ->
                    decoder.allocator = ImageDecoder.ALLOCATOR_SOFTWARE
                    val width = info.size.width
                    val height = info.size.height
                    val largest = max(width, height)
                    if (largest > 4096) {
                        val ratio = 4096.0 / largest.toDouble()
                        decoder.setTargetSize(
                            max(1, (width * ratio).toInt()),
                            max(1, (height * ratio).toInt()),
                        )
                    }
                }
            } else {
                val bounds = BitmapFactory.Options().apply { inJustDecodeBounds = true }
                contentResolver.openInputStream(uri).use { input ->
                    if (input != null) BitmapFactory.decodeStream(input, null, bounds)
                }
                var sample = 1
                while (
                    bounds.outWidth > 0 &&
                    bounds.outHeight > 0 &&
                    max(bounds.outWidth / sample, bounds.outHeight / sample) > 4096
                ) {
                    sample *= 2
                }
                val options = BitmapFactory.Options().apply { inSampleSize = sample }
                contentResolver.openInputStream(uri).use { input ->
                    if (input == null) null else BitmapFactory.decodeStream(input, null, options)
                }
            }

            if (bitmap == null) return null
            val pickerDir = File(cacheDir, "ngelx_picker").apply { mkdirs() }
            val target = File(pickerDir, "normalized_${System.currentTimeMillis()}.jpg")
            val ok = FileOutputStream(target).use { output ->
                bitmap.compress(Bitmap.CompressFormat.JPEG, 92, output)
            }
            bitmap.recycle()
            if (!ok || target.length() <= 0L) {
                target.delete()
                null
            } else {
                target
            }
        } catch (_: Throwable) {
            null
        }
    }

'''
android = android[:copy_start] + copy_block + android[copy_end:]

main = one(main, "defaultValue: '1.0.91'", "defaultValue: '1.0.92'", "runtime version")
main = one(main, "defaultValue: '310'", "defaultValue: '311'", "runtime build")
pub = one(pub, "version: 1.0.91+310", "version: 1.0.92+311", "pubspec version")

MAIN_PATH.write_text(main, encoding="utf-8")
PUB_PATH.write_text(pub, encoding="utf-8")
ANDROID_PATH.write_text(android, encoding="utf-8")

print("Build 311 image decode fallback fix applied.")
