"""Build474: regression contracts for background removal, scroll and composer."""
import unittest
from pathlib import Path
from apply_build474_private_chat_stability import transform, MARKER, BEGIN, END

class PrivateChat474Tests(unittest.TestCase):
 def test_generated_source_stable_and_all_media_paths_present(self):
  s=Path('app/lib/main.dart').read_text(encoding='utf-8')
  self.assertIn(MARKER,s)
  self.assertEqual(transform(s),s)
  a=s.index(BEGIN);b=s.index(END,a);p=s[a:b]
  for term in (
   "if(veri.containsKey('backgroundUrl'))",
   "return (veri['backgroundUrl']??'').toString().trim();",
   "final eski=(veri['backgroundUrl_'+id]??'').toString().trim();",
   'if(!_ngelx474MessagesOpened)',
   'else if(_ngelx474LastMessageId!=tailId)',
   'ngelxAltSistemRezervi(context,minimum:82)',
   'if(MediaQuery.sizeOf(context).width>=430)...[',
   'medyaGonder(ImageSource.camera)',
   'medyaGonder(ImageSource.gallery)',
   "Navigator.pop(sheetContext,'camera')",
   "Navigator.pop(sheetContext,'gallery')",
   'onChanged:mesajDegisti',
   'onPressed:sesKaydiDegistir',
   'onPressed:emojiSec',
   'onPressed:gonderiliyor?null:gonder',
   '_ngelx472Wallpaper(arkaPlan,arkaPlanUrl,arkaPlanOpaklik)',
   'bottomNavigationBar:ColoredBox('):
   self.assertIn(term,p)
  self.assertNotIn('if(s.hasData){sonaGit();_ngelx465ScheduleBottomOnOpen();}',p)
 def test_cleared_background_precedes_old_fallback_and_write_is_confirmed(self):
  s=Path('app/lib/main.dart').read_text(encoding='utf-8')
  a=s.index('  String _ozelSohbetArkaPlanUrl(')
  b=s.index('  Future<',a)
  p=s[a:b]
  self.assertLess(p.index("if(veri.containsKey('backgroundUrl'))"),p.index('for(final id in'))
  a=s.index("if(secim=='removeImage')")
  b=s.index("final kaynak=secim==",a)
  remove=s[a:b]
  self.assertLess(remove.index("await FirebaseFirestore.instance.waitForPendingWrites()"),remove.index("await sistemOlayi('sohbet arka planını kaldırdı','remove')"))
  self.assertIn("'backgroundUrl':''",remove)

if __name__=='__main__':unittest.main()
