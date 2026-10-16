"""Private bottom composer must expose camera/gallery and reserve nav bar once."""
import unittest
from apply_build465_private_composer import (
    transform, ADD_BUTTON, EMOJI_EXTERNAL, EMOJI_SUFFIX, DOUBLE_INSET
)

class PrivateComposerTests(unittest.TestCase):
    def template(self):
        return (
          "class _SohbetPageState {\n"
          "  Widget build(){\n"
          +DOUBLE_INSET+"\n"
          +ADD_BUTTON+"\n"
          +EMOJI_SUFFIX+"\n"
          +EMOJI_EXTERNAL+"\n"
          "  }\n}\nclass NgelXSesliMesaj {}"
        )
    def test_matches_group_composer_without_changing_send(self):
        result=transform(self.template())
        self.assertIn("onPressed:ekIslemiSuruyor?null:()=>medyaGonder(ImageSource.gallery)",result)
        self.assertIn("onPressed:ekIslemiSuruyor?null:()=>medyaGonder(ImageSource.camera)",result)
        self.assertIn("suffixIcon:IconButton(",result)
        self.assertNotIn(DOUBLE_INSET,result)
        self.assertIn("bottomNavigationBar:const SizedBox.shrink()",result)
        self.assertEqual(result,transform(result))
    def test_modified_ui_anchor_refuses_guessing(self):
        with self.assertRaises(RuntimeError):
            transform(self.template().replace("hintText:'Mesaj'","hintText:'Message'"))

if __name__=="__main__":unittest.main()
