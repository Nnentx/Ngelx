"""Build476 private Android bottom-nav and attachment regression tests."""
import unittest
from pathlib import Path
from apply_build476_private_composer_nav import BEGIN,END,MARKER,transform

class Build476ComposerTests(unittest.TestCase):
 def test_real_generated_chat_has_safe_nav_and_both_direct_attachments(self):
  src=Path('app/lib/main.dart').read_text(encoding='utf-8')
  self.assertIn(MARKER,src)
  self.assertEqual(transform(src),src)
  p=src[src.index(BEGIN):src.index(END,src.index(BEGIN))]
  for term in (
   'resizeToAvoidBottomInset:true',
   'height:math.max(54.0,MediaQuery.viewPaddingOf(context).bottom)',
   'bottomNavigationBar:ColoredBox(',
   "tooltip:'Kamera'","tooltip:'Galeri'",
   'onPressed:ekIslemiSuruyor?null:()=>medyaGonder(ImageSource.camera)',
   'onPressed:ekIslemiSuruyor?null:()=>medyaGonder(ImageSource.gallery)',
   'onPressed:sesKaydiDegistir','onPressed:emojiSec',
   'onPressed:gonderiliyor?null:gonder',
   'onTap:_ngelx465StopOpeningBottom',
   "if(veri.containsKey('backgroundUrl'))",
  ):self.assertIn(term,p)
  self.assertNotIn('if(MediaQuery.sizeOf(context).width>=430)...[',p)
  self.assertNotIn('height:MediaQuery.viewInsetsOf(context).bottom>0',p)
  self.assertNotIn('bottomNavigationBar:const SizedBox.shrink()',p)
  self.assertEqual(p.count('constraints:const BoxConstraints.tightFor(width:31,height:44)'),2)
  for width in (34,36):
   self.assertIn(f'constraints:const BoxConstraints.tightFor(width:{width},height:44)',p)
  self.assertIn('suffixIconConstraints:const BoxConstraints(minWidth:36,minHeight:40)',p)
  self.assertEqual(p.count("tooltip:'Kamera'"),1)
  self.assertEqual(p.count("tooltip:'Galeri'"),1)
 def test_scoped_and_idempotent(self):
  src=Path('app/lib/main.dart').read_text(encoding='utf-8')
  self.assertEqual(src.count(MARKER),1)
  self.assertEqual(transform(src),src)
if __name__=='__main__':unittest.main()
