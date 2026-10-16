"""Fail-closed synthetic tests for Messenger reply and group sender rhythm."""
import unittest
from apply_build465_message_rhythm import transform,TAG
GROUP="""  Widget mesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,){
      padding:const EdgeInsets.only(left:2,bottom:5,right:6,top:2),
      CircleAvatar(radius:10,backgroundColor:ngelxGroupGreenSoft,
      const SizedBox(width:6),
              Flexible(child:Text(isim,
          if(yanit.isNotEmpty&&yanitGonderen.isNotEmpty)Padding(
            padding:EdgeInsets.only(left:ben?0:8,right:ben?8:0,bottom:3),
            child:Row(mainAxisSize:MainAxisSize.min,children:[
              Icon(Icons.reply_rounded,size:14,color:ben?ngelxPremiumMuted:ngelxGroupGreen),
              const SizedBox(width:4),
              Text(
                ben?(yanitGonderen=='Sen'?'Kendine yanıt verdin':yanitGonderen+'’a yanıt verdin'):yanitGonderen+'’a yanıt verdi',
                style:TextStyle(color:ben?ngelxPremiumMuted:ngelxGroupGreen,fontSize:10.8,fontWeight:FontWeight.w700),
              ),
            ]),
          ),
          GestureDetector(
              onDoubleTap:()=>grupKalpBirak(d),
          ),
          if(yanit.isNotEmpty)Container(
            border:Border.all(color:const Color(0xFFE5E7EB)),
            child:Row(children:[
              Container(width:3,height:30,decoration:BoxDecoration(color:const Color(0xFF9CA3AF),borderRadius:BorderRadius.circular(4))),
              Text(yanit,maxLines:1,overflow:TextOverflow.ellipsis,
            ]),
          ),
  }
class TamEkranMedyaPage{}
"""
PRIVATE="""  Widget ozelMesajKarti(QueryDocumentSnapshot<Map<String,dynamic>> d,){
    child:Container(
      margin:const EdgeInsets.symmetric(horizontal:4,vertical:5),
      child:Column(children:[
              Container(
                width:double.infinity,
                margin:const EdgeInsets.only(bottom:8),
                padding:const EdgeInsets.symmetric(horizontal:9,vertical:7),
                decoration:BoxDecoration(
                  color:Colors.white.withValues(alpha:.96),
                  borderRadius:BorderRadius.circular(12),
                  border:const Border(left:BorderSide(color:ngelxPrivateBlue,width:3)),
                ),
              ),
      ]),
    );
  }
class NgelXSesliMesaj{}
"""

class MessageRhythmTests(unittest.TestCase):
    def fixture(self):return GROUP+PRIVATE
    def test_quote_and_sender_are_compact_without_changing_reactions(self):
        actual=transform(self.fixture())
        self.assertIn(TAG,actual)
        self.assertIn("radius:12,backgroundColor",actual)
        self.assertIn("bottom:2,right:4,top:1",actual)
        self.assertIn("Text(yanit,maxLines:2",actual)
        self.assertNotIn("Kendine yanıt verdin",actual)
        self.assertIn("onDoubleTap:()=>grupKalpBirak(d)",actual)
        self.assertIn("width:math.min(264.0",actual)
        self.assertIn("Color(0xFFF3F5FA)",actual)
        self.assertEqual(actual,transform(actual))
    def test_fails_if_group_profile_layout_changed(self):
        with self.assertRaises(RuntimeError):
            transform(self.fixture().replace("radius:10,backgroundColor","radius:20,backgroundColor"))
if __name__=="__main__":unittest.main()
