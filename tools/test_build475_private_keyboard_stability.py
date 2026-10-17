"""Build475: regression checks for the private Android keyboard transition."""
import unittest
from pathlib import Path
from apply_build475_private_keyboard_stability import transform, BEGIN, END, MARK

class Keyboard475Tests(unittest.TestCase):
 def test_generated_chat_after_transform(self):
  src=Path('app/lib/main.dart').read_text(encoding='utf-8')
  self.assertIn(MARK,src)
  self.assertEqual(transform(src),src)
  region=src[src.index(BEGIN):src.index(END,src.index(BEGIN))]
  self.assertIn('resizeToAvoidBottomInset:true',region)
  self.assertIn('bottomNavigationBar:const SizedBox.shrink()',region)
  self.assertIn('minimum:const EdgeInsets.only(bottom:10)',region)
  self.assertIn('onTap:_ngelx465StopOpeningBottom',region)
  self.assertIn('minLines:1,maxLines:4,scrollPadding:EdgeInsets.zero',region)
  self.assertIn('stream:_ngelx475SelfBlockStream',region)
  self.assertIn('stream:_ngelx475PeerBlockStream',region)
  self.assertIn('_ngelx475SelfBlockUid!=ben',region)
  self.assertNotIn('minimum:82',region)
  self.assertNotIn('child:AnimatedSize(',region[region.index('tooltip:\'Sesli mesaj\''):])
  for preserved in ('_ngelx472Wallpaper(arkaPlan,arkaPlanUrl,arkaPlanOpaklik)',
      "if(veri.containsKey('backgroundUrl'))",
      'if(MediaQuery.sizeOf(context).width>=430)...[',
      'onPressed:sesKaydiDegistir',
      'onChanged:mesajDegisti',
      'onPressed:emojiSec',
      'onPressed:gonderiliyor?null:gonder',
      'medyaGonder(ImageSource.camera)',
      'medyaGonder(ImageSource.gallery)'):
   self.assertIn(preserved,region)

if __name__=='__main__':unittest.main()
