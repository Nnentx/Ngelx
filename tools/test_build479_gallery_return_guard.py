"""Build479: OS gallery dismissal may not pop private chat or reopen actions."""
from pathlib import Path
import unittest
from apply_build479_gallery_return_guard import transform,BEGIN,END,MARK

class GalleryRoute479Tests(unittest.TestCase):
 def test_native_gallery_has_bounded_pop_and_tap_guard(self):
  s=Path('app/lib/main.dart').read_text(encoding='utf-8')
  self.assertIn(MARK,s)
  self.assertEqual(transform(s),s)
  chat=s[s.index(BEGIN):s.index(END,s.index(BEGIN))]
  for k in (
   'Widget build(BuildContext context)=>PopScope(',
   'canPop:!_ngelx479PickerRouteGuard',
   '_ngelx479BeginPicker();',
   '_ngelx479EndPicker();',
   'const Duration(milliseconds:850)',
   'if(_ngelx479PickerRouteGuard||_ngelx477PhotoPickerActive)return;',
   'onPressed:ekIslemiSuruyor||_ngelx479PickerRouteGuard?null:()=>medyaGonder(ImageSource.gallery)',
   'onPressed:ekIslemiSuruyor||_ngelx479PickerRouteGuard?null:()=>medyaGonder(ImageSource.camera)',
   '_ngelx479PickerReturnTimer?.cancel();WidgetsBinding.instance.removeObserver(this)',
   "tooltip:'Galeri'","tooltip:'Kamera'",
   'if(yaziSaatiDisarida&&saat.isNotEmpty)',
   '_ngelx478HistoryPointer()',
   'height:math.max(54.0,MediaQuery.viewPaddingOf(context).bottom)',
   'if(!_ngelx474MessagesOpened)',
  ):self.assertIn(k,chat)
  self.assertEqual(chat.count('canPop:!_ngelx479PickerRouteGuard'),1)
  self.assertEqual(chat.count('_ngelx479BeginPicker();'),1)
  self.assertEqual(chat.count('_ngelx479EndPicker();'),1)
  self.assertEqual(chat.count('onChanged:mesajDegisti'),1)

 def test_unrelated_chat_and_os_picker_are_unchanged(self):
  s=Path('app/lib/main.dart').read_text(encoding='utf-8')
  self.assertEqual(s.count(MARK),1)
  self.assertIn('if(x==null)return null;',s)
  native=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/MainActivity.kt').read_text(encoding='utf-8')
  self.assertIn('if (pickerRequestedImage) Intent.ACTION_OPEN_DOCUMENT',native)
  self.assertIn('if (pendingPickerResult != null)',native)
if __name__=='__main__':unittest.main()
