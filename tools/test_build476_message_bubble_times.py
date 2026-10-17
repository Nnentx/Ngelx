"""Build476 timestamps must leave only normal text bubbles, not media/call."""
from pathlib import Path
import unittest
from apply_build476_message_bubble_times import transform,MARK,BEGIN,END
class MessageBubbleTimes476Tests(unittest.TestCase):
 def test_bubble_clock_outside_and_reactions_unchanged(self):
  s=Path('app/lib/main.dart').read_text(encoding='utf-8')
  self.assertEqual(transform(s),s)
  r=s[s.index(BEGIN):s.index(END,s.index(BEGIN))]
  self.assertIn(MARK,r)
  self.assertIn('final yaziSaatiDisarida=!photo&&!video&&!shared&&!sharedProfile',r)
  self.assertIn('if(saat.isNotEmpty&&!yaziSaatiDisarida)',r)
  self.assertIn('if(yaziSaatiDisarida&&saat.isNotEmpty)',r)
  self.assertIn('crossAxisAlignment:ben?CrossAxisAlignment.end:CrossAxisAlignment.start',r)
  self.assertLess(r.index('child:Container('),r.index('if(yaziSaatiDisarida&&saat.isNotEmpty)'))
  self.assertIn('_ozelMedyaTepkiBalonu(d.reference,sayilar,tepkiler.length)',r)
  self.assertIn('onLongPress:()=>mesajMenusu(d)',r)
  self.assertIn('onDoubleTap:()=>mesajTepkiDegistir(d,quickReaction)',r)
  self.assertIn('if(goruldu)...[',r)
  self.assertIn("Text('Süreli'",r)
  self.assertIn('replyText',r)
if __name__=='__main__': unittest.main()
