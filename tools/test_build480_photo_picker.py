"""Build480: gallery goes to photos/albums, Files remains only fallback."""
from pathlib import Path
import unittest
from apply_build480_photo_picker import transform,MARK

NATIVE=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt')
MAIN=Path('app/lib/main.dart')

class Build480PickerTests(unittest.TestCase):
    def test_android_photo_picker_precedes_document_fallback(self):
        s=NATIVE.read_text(encoding='utf-8')
        self.assertEqual(transform(s),s)
        p=s[s.index('private fun launchPicker('):s.index('override fun onActivityResult(',s.index('private fun launchPicker('))]
        for k in (
            MARK,
            'Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU',
            'cleanTypes.all { it.startsWith("image/") }',
            'Intent(MediaStore.ACTION_PICK_IMAGES)',
            'type = "image/*"',
            'putExtra(MediaStore.EXTRA_PICK_IMAGES_MAX, maxImages)',
            'MediaStore.EXTRA_PICK_IMAGES_LAUNCH_TAB',
            'MediaStore.PICK_IMAGES_TAB_IMAGES',
            'return // An OS cancel is handled by onActivityResult',
            'startActivityForResult(build(firstAction), REQUEST_PICK)',
            'startActivityForResult(build(fallbackAction), REQUEST_PICK)',
        ):
            self.assertIn(k,p)
        self.assertLess(p.index('startActivityForResult(photos, REQUEST_PICK)'),
                        p.index('startActivityForResult(build(firstAction), REQUEST_PICK)'))
        self.assertEqual(p.count('Intent(MediaStore.ACTION_PICK_IMAGES)'),1)
        self.assertEqual(p.count('return // An OS cancel is handled by onActivityResult'),1)
    def test_result_and_cancel_paths_do_not_auto_send_or_reopen(self):
        s=NATIVE.read_text(encoding='utf-8')
        self.assertIn('if (pendingPickerResult != null)',s)
        self.assertIn('if (resultCode != Activity.RESULT_OK || data == null)',s)
        self.assertIn('result.success(null)',s)
        self.assertIn('data.clipData?.let',s)
        self.assertIn('data.data?.let',s)
        self.assertIn('copyUriToCache(it, requestedImage)',s)
        d=MAIN.read_text(encoding='utf-8')
        for k in (
            'if(x==null)return null;',
            '_ngelx477PhotoPickerActive',
            '_ngelx479PickerRouteGuard',
            "tooltip:'Galeri'",
            "tooltip:'Kamera'",
            'if(yaziSaatiDisarida&&saat.isNotEmpty)',
            'height:math.max(54.0,MediaQuery.viewPaddingOf(context).bottom)',
        ):
            self.assertIn(k,d)

if __name__=='__main__':unittest.main()
