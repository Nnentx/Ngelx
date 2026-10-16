"""Call buttons should fit narrow screens, retain all original callbacks."""
import unittest
from apply_build465_messenger_call_controls import (
    transform,START,END,ROW,LAST,OLD_END,TAG,METHOD_ANCHOR,
)

class CallControlsTests(unittest.TestCase):
    def fixture(self):
        return (START+"\nWidget build()=>Column(children:[\n"
            +"          if(bitisDurumu==null&&hata==null)Padding(\n"
            +"            padding:const EdgeInsets.fromLTRB(14,15,14,7),\n"
            +ROW+"\n"
            +"""              _aramaKontrol(mikrofon?Icons.mic_rounded:Icons.mic_off_rounded,'Mikrofon',mikrofonDegistir,mikrofon),
"""
            +LAST+"\n"+OLD_END
            +"]);\n"+METHOD_ANCHOR+"[]);\n}\n"
            +END+"\n")
    def test_wrap_hangup_single_action(self):
        result=transform(self.fixture())
        self.assertIn(TAG,result)
        self.assertIn("alignment:WrapAlignment.center",result)
        self.assertIn("runSpacing:12",result)
        self.assertEqual(result.count("onTap:()=>bitir()"),1)
        self.assertIn("shape:BoxShape.circle",result)
        self.assertIn("'Mikrofon',mikrofonDegistir,mikrofon",result)
        self.assertIn("'Ses',hoparlorDegistir,hoparlor",result)
        self.assertEqual(result,transform(result))
    def test_unknown_controls_abort(self):
        with self.assertRaises(RuntimeError):
            transform(self.fixture().replace("mainAxisAlignment:MainAxisAlignment.spaceEvenly","mainAxisAlignment:MainAxisAlignment.start"))
if __name__=="__main__":unittest.main()
