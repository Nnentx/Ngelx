#!/usr/bin/env python3
"""Build519 QA: prefer AndroidX supported system/backported photo picker.
Only visual media requests: Story image, group chat gallery image/video.
Never requests broad storage permissions or silently opens cloud providers.
Runs AFTER the existing Build480 + Build491 Android transformations.
"""
from pathlib import Path

KOTLIN=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt')
GRADLE=Path('app/android/app/build.gradle.kts')
MARK='// Build519: prefer supported system or backported photo picker'
PATCH=r"""
        // Build519: prefer supported system or backported photo picker.
        // This single-media AndroidX contract selects platform/OEM/GMS picker
        // where available, including some older Android 11/12 phones.
        // A true picker is used before ACTION_GET_CONTENT / DocumentsUI.
        val visualMediaOnly = cleanTypes.isNotEmpty() &&
            cleanTypes.all { it.startsWith("image/") || it.startsWith("video/") }
        if (visualMediaOnly && !multiple) {
            val mediaType = when {
                cleanTypes.all { it.startsWith("image/") } ->
                    ActivityResultContracts.PickVisualMedia.ImageOnly
                cleanTypes.all { it.startsWith("video/") } ->
                    ActivityResultContracts.PickVisualMedia.VideoOnly
                else -> ActivityResultContracts.PickVisualMedia.ImageAndVideo
            }
            if (ActivityResultContracts.PickVisualMedia.isPhotoPickerAvailable(this)) {
                val request = PickVisualMediaRequest.Builder()
                    .setMediaType(mediaType).build()
                val visualIntent = ActivityResultContracts.PickVisualMedia()
                    .createIntent(this, request).apply {
                        addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                    }
                try {
                    startActivityForResult(visualIntent, REQUEST_PICK)
                    return // User cancellation remains cancellation; no second picker.
                } catch (_: ActivityNotFoundException) {
                    // A broken OEM picker is not a user cancellation.
                }
            }
            // Some devices lack every Photo Picker provider. For image-only
            // selections, a gallery-based ACTION_PICK is less confusing than
            // opening a general file browser. Final fallback is unchanged.
            if (cleanTypes.all { it.startsWith("image/") }) {
                val gallery = Intent(Intent.ACTION_PICK,
                    MediaStore.Images.Media.EXTERNAL_CONTENT_URI).apply {
                    type = "image/*"
                    addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                }
                try {
                    startActivityForResult(gallery, REQUEST_PICK)
                    return
                } catch (_: ActivityNotFoundException) {}
            }
        }

"""

def once(s,old,new,label):
    n=s.count(old)
    if n!=1:raise RuntimeError(f'Build519 {label}: anchor count {n}')
    return s.replace(old,new,1)

def native_transform(s):
    if MARK in s:return s
    s=once(s,'import android.app.Activity\n',
      'import android.app.Activity\nimport androidx.activity.result.PickVisualMediaRequest\n'
      'import androidx.activity.result.contract.ActivityResultContracts\n',
      'AndroidX picker imports')
    start=s.index('private fun launchPicker(')
    end=s.index('override fun onActivityResult(',start)
    sec=s[start:end]
    if 'Build491: chat media accepts image AND video from Android Photo Picker.' not in sec:
        raise RuntimeError('Build519 requires Build491 image/video safety first')
    # All previous picker types and URI copying continue unchanged.
    needle='''        // Build491: chat media accepts image AND video from Android Photo Picker.'''
    sec=once(sec,needle,PATCH+needle,'picker before prior Android 13 and DocumentsUI')
    for important in ('MediaStore.ACTION_PICK_IMAGES','startActivityForResult(build(firstAction), REQUEST_PICK)',
                      'startActivityForResult(build(fallbackAction), REQUEST_PICK)',
                      'MediaStore.EXTRA_PICK_IMAGES_MAX'):
        if important not in sec:raise RuntimeError('Build519 must preserve previous fallback '+important)
    return s[:start]+sec+s[end:]

def gradle_transform(s):
    if 'implementation("androidx.activity:activity:1.9.3")' in s:return s
    # Application owns only its media picker contract; this library provides
    # OS/OEM/GMS picker selection and its old-device fallback.
    anchor='flutter {\n    source = "../.."\n}'
    return once(s,anchor,'''dependencies {
    implementation("androidx.activity:activity:1.9.3")
}

'''+anchor,'AndroidX photo picker dependency')

if __name__=='__main__':
    for path,patch in ((KOTLIN,native_transform),(GRADLE,gradle_transform)):
        old=path.read_text(encoding='utf-8')
        new=patch(old)
        if old!=new:path.write_text(new,encoding='utf-8')
    print('Build519 AndroidX/backported photo picker preferred; gallery-only fallback; existing URI copy unchanged')
