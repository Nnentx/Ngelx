"""Call-screen presentation regressions without changing the LiveKit lifecycle."""
import unittest
from apply_build465_call_status_minimize import (
    transform,START,END,VOICE_OLD,VIDEO_OLD,BODY_OLD,TAG
)

class CallStatusMinimizeTests(unittest.TestCase):
    def fixture(self):
        return (START+"\n"
          "  Future<void> _aramaEkraniniKucult()async{ngelxArkaPlanAramaSakla(roomName:widget.roomName);}\n"
          "  Widget build()=>Container(\n"
          + BODY_OLD+"\n"
          + VOICE_OLD + "\n" + VIDEO_OLD + "\n"
          + "])));\n}\n" + END+"\n")
    def test_wait_for_real_connected_participant(self):
        text=transform(self.fixture())
        self.assertIn(TAG,text)
        self.assertEqual(text.count("aramaBaslangic==null?'Aranıyor…'"),3)
        self.assertIn("if(bitisDurumu==null&&hata==null&&oda!=null)",text)
        self.assertIn("unawaited(_aramaEkraniniKucult())",text)
        self.assertIn("Icons.keyboard_arrow_down_rounded",text)
        self.assertNotIn("onTap:()=>bitir()",text)
        self.assertEqual(text,transform(text))
    def test_no_breakage_if_call_markup_changes(self):
        with self.assertRaises(RuntimeError):
            transform(self.fixture().replace("child:SafeArea(child:Column(children:[","child:SafeArea(child:ListView(children:["))

if __name__=="__main__":unittest.main()
