"""Build478 keyboard layout stability and clock readability regression tests."""
from pathlib import Path
import unittest
from apply_build478_private_keyboard_follow import transform,MARK,CLOCK,BEGIN,END

class Keyboard478Tests(unittest.TestCase):
 def test_keyboard_only_pins_chat_when_reading_latest_messages(self):
  s=Path('app/lib/main.dart').read_text(encoding='utf-8')
  self.assertEqual(transform(s),s)
  r=s[s.index(BEGIN):s.index(END,s.index(BEGIN))]
  for term in (MARK,
    'Ngelx437MessageJump<SohbetPage>, WidgetsBindingObserver',
    'WidgetsBinding.instance.addObserver(this)',
    'WidgetsBinding.instance.removeObserver(this)',
    'void didChangeMetrics()',
    'onTap:_ngelx478ComposerFocus',
    'onPointerDown:(_)=>_ngelx478HistoryPointer()',
    '_ngelx478FollowKeyboard=p.maxScrollExtent-p.pixels<150',
    'if(!mounted||!_ngelx478FollowKeyboard||jumpActive||!liste.hasClients)return',
    'liste.jumpTo(p.maxScrollExtent)'):
   self.assertIn(term,r)
  self.assertEqual(r.count('WidgetsBinding.instance.addObserver(this)'),1)
  self.assertEqual(r.count('WidgetsBinding.instance.removeObserver(this)'),1)
  self.assertNotIn('onTap:_ngelx465StopOpeningBottom',r)
 def test_outside_text_times_readable_over_photo_without_moving_inside_bubble(self):
  s=Path('app/lib/main.dart').read_text(encoding='utf-8')
  r=s[s.index(BEGIN):s.index(END,s.index(BEGIN))]
  for term in (CLOCK,
    'if(yaziSaatiDisarida&&saat.isNotEmpty)',
    'color:Colors.white.withValues(alpha:.90)',
    'fontWeight:FontWeight.w600',
    '_ozelMedyaTepkiBalonu(d.reference,sayilar,tepkiler.length)',
    'if(saat.isNotEmpty&&!yaziSaatiDisarida)',
    '_ngelx477PhotoPickerActive=false',
    "tooltip:'Galeri'","tooltip:'Kamera'"):
   self.assertIn(term,r)
  self.assertEqual(r.count(CLOCK),1)

if __name__=='__main__':unittest.main()
