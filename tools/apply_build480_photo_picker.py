#!/usr/bin/env python3
"""Build480: gallery icon should open the Android PHOTO picker, not Files/Drive.

Android 13+ uses MediaStore.ACTION_PICK_IMAGES; older/unavailable devices retain
the existing DocumentsUI fallback. No broad media permissions are added.
"""
from pathlib import Path

NATIVE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt')
MARK='// Build480: image-only selection uses Android Photo Picker instead of Files'

def transform(s):
    if MARK in s:return s
    old="""import android.provider.OpenableColumns"""
    new="""import android.provider.MediaStore
import android.provider.OpenableColumns"""
    if s.count(old)!=1:raise RuntimeError('Build480 Android import changed')
    s=s.replace(old,new,1)
    anchor="""        // Build477: use full-screen Android DocumentsUI for image selections."""
    code="""        // Build480: image-only selection uses Android Photo Picker instead of Files.
        // ACTION_OPEN_DOCUMENT was showing "Son", Google Drive and general files.
        // Android's own Photo Picker shows the camera roll and albums without
        // requesting unrestricted device photo/storage permissions.
        if (pickerRequestedImage &&
            cleanTypes.all { it.startsWith("image/") } &&
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            val maxImages = if (multiple) minOf(20, MediaStore.getPickImagesMaxLimit()) else 1
            if (!multiple || maxImages >= 2) {
                val photos = Intent(MediaStore.ACTION_PICK_IMAGES).apply {
                    type = "image/*"
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    if (multiple) putExtra(MediaStore.EXTRA_PICK_IMAGES_MAX, maxImages)
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.VANILLA_ICE_CREAM) {
                        putExtra(
                            MediaStore.EXTRA_PICK_IMAGES_LAUNCH_TAB,
                            MediaStore.PICK_IMAGES_TAB_IMAGES,
                        )
                    }
                }
                try {
                    startActivityForResult(photos, REQUEST_PICK)
                    return // An OS cancel is handled by onActivityResult; do not open Files.
                } catch (_: ActivityNotFoundException) {
                    // Some OEMs lack the system Photo Picker. Keep our former fallback.
                }
            }
        }

"""
    if s.count(anchor)!=1:raise RuntimeError('Build480 expected previous gallery fallback')
    s=s.replace(anchor,code+anchor,1)
    required=(
      'startActivityForResult(build(firstAction), REQUEST_PICK)',
      'startActivityForResult(build(fallbackAction), REQUEST_PICK)',
      'if (pendingPickerResult != null)',
      'if (resultCode != Activity.RESULT_OK || data == null)',
      'data.clipData?.let',
      'data.data?.let',
      'copyUriToCache(it, requestedImage)',
      'pickerAllowMultiple = call.method == "pickDocuments"',
    )
    for v in required:
        if v not in s:raise RuntimeError('Build480 must preserve '+v)
    return s

if __name__=='__main__':
    a=NATIVE.read_text(encoding='utf-8')
    b=transform(a)
    if a!=b:NATIVE.write_text(b,encoding='utf-8')
    print('Build480: Android Photo Picker for images, documents fallback for other media')
