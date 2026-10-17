"""Build477: gallery cancellation, no double chooser, safe native full screen."""
import unittest
from pathlib import Path
from apply_build477_gallery_document_picker import patch_main,patch_native,MARKER,NATIVE_MARKER
class Gallery477Tests(unittest.TestCase):
 def test_android_cancellation_and_native_error_do_not_reopen(self):
  s=Path('app/lib/main.dart').read_text(encoding='utf-8')
  self.assertIn(MARKER,s)
  self.assertEqual(patch_main(s),s)
  p=s[s.index(MARKER):s.index('Future<XFile?> ngelxVideoSec',s.index(MARKER))]
  self.assertIn('if(x==null)return null;',p)
  self.assertIn('}on MissingPluginException{',p)
  self.assertNotIn('}catch(_){}',p)
  self.assertIn('ImagePicker().pickImage(',p)
 def test_private_chat_single_flight_including_cancel(self):
  s=Path('app/lib/main.dart').read_text(encoding='utf-8')
  part=s[s.index('class _SohbetPageState extends State<SohbetPage>'):s.index('class NgelXSesliMesaj extends StatefulWidget')]
  p=part[part.index('Future<void> medyaGonder('):part.index('Future<void> videoGonder(')]
  self.assertIn('if(ben==null||ekIslemiSuruyor||_ngelx477PhotoPickerActive)return',p)
  self.assertIn('_ngelx477PhotoPickerActive=true;',p)
  self.assertIn('}finally{\\n      _ngelx477PhotoPickerActive=false;',p)
  for keep in ("tooltip:'Kamera'","tooltip:'Galeri'",
      'height:math.max(54.0,MediaQuery.viewPaddingOf(context).bottom)',
      'onChanged:mesajDegisti',
      "if(veri.containsKey('backgroundUrl'))"):
   self.assertIn(keep,part)
 def test_image_document_first_and_other_media_unchanged(self):
  s=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt').read_text(encoding='utf-8')
  self.assertIn(NATIVE_MARKER,s)
  self.assertEqual(patch_native(s),s)
  self.assertIn('if (pickerRequestedImage) Intent.ACTION_OPEN_DOCUMENT',s)
  self.assertIn('else Intent.ACTION_GET_CONTENT',s)
  self.assertIn('startActivityForResult(build(firstAction), REQUEST_PICK)',s)
  self.assertIn('startActivityForResult(build(fallbackAction), REQUEST_PICK)',s)
  self.assertIn('if (pendingPickerResult != null)',s)
  self.assertIn('copyUriToCache(it, requestedImage)',s)
if __name__=='__main__':unittest.main()
