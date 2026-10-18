#!/usr/bin/env python3
"""Build519 source regression for final Android-generated native picker."""
import importlib.util
from pathlib import Path

spec=importlib.util.spec_from_file_location('b519','tools/apply_build519_unified_photo_picker.py')
assert spec and spec.loader
patch=importlib.util.module_from_spec(spec);spec.loader.exec_module(patch)
native=patch.KOTLIN.read_text(encoding='utf-8')
gradle=patch.GRADLE.read_text(encoding='utf-8')
assert patch.native_transform(native)==native
assert patch.gradle_transform(gradle)==gradle
a=native.index('private fun launchPicker(')
b=native.index('override fun onActivityResult(',a)
picker=native[a:b]
assert picker.count(patch.MARK)==1
for guard in (
    'visualMediaOnly && !multiple',
    'ActivityResultContracts.PickVisualMedia.isPhotoPickerAvailable(this)',
    'PickVisualMediaRequest.Builder()',
    'ActivityResultContracts.PickVisualMedia.ImageOnly',
    'ActivityResultContracts.PickVisualMedia.VideoOnly',
    'ActivityResultContracts.PickVisualMedia.ImageAndVideo',
    'startActivityForResult(visualIntent, REQUEST_PICK)',
    'Intent(Intent.ACTION_PICK,',
    'MediaStore.Images.Media.EXTERNAL_CONTENT_URI',
    'MediaStore.ACTION_PICK_IMAGES',
    'startActivityForResult(build(firstAction), REQUEST_PICK)',
    'startActivityForResult(build(fallbackAction), REQUEST_PICK)',
    'type = "image/*"',
):
    assert guard in picker,'Missing picker behavior '+guard
assert picker.index('startActivityForResult(visualIntent, REQUEST_PICK)') < picker.index('MediaStore.ACTION_PICK_IMAGES')
assert picker.index('MediaStore.ACTION_PICK_IMAGES') < picker.index('startActivityForResult(build(firstAction), REQUEST_PICK)')
assert 'implementation("androidx.activity:activity:1.9.3")' in gradle
for guard in ('if (pendingPickerResult != null)','if (resultCode != Activity.RESULT_OK || data == null)',
              'copyUriToCache(it, requestedImage)','data.clipData?.let','data.data?.let'):
    assert guard in native,'Existing URI copy/cancel behavior lost '+guard
dart=Path('app/lib/main.dart').read_text(encoding='utf-8')
assert 'ngelxSohbetGaleriMedyaSec()' in dart
assert "await _ngelxAndroidBelgeSec(const <String>['image/*']);" in dart
for forbidden in ('READ_MEDIA_IMAGES','READ_EXTERNAL_STORAGE','MANAGE_EXTERNAL_STORAGE'):
    assert forbidden not in picker,'No new broad storage permission'
print('Build519 SOURCE PASS: story images and chat gallery prefer system/Google supported picker')
print('Build519 SOURCE PASS: URI copy, cancel, existing Document fallback and image/video filters')
print('Build519 DEVICE GATE: manufacturer-specific picker fallback can still be Files; two-phone QA required')
