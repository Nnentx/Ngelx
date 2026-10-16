"""Group call visuals and remote audio toggles cannot act on another user's mic."""
import unittest
from apply_build465_call_participants import transform, VOICE_OLD

VIDEO="""  Widget _katilimciKutusu(lk.Participant p,{bool yerel=false}){
    return Container(
       child:Stack(fit:StackFit.expand,children:[
         Positioned(
           left:10,right:10,bottom:10,
           child:Text("participant"),
         ),
       ]),
    );
  }
"""
VOICE="""  Widget _grupSesliKatilimci(lk.Participant p,{bool yerel=false}){
    return Container(
      decoration:BoxDecoration(
"""+VOICE_OLD+"""
      ),
      child:Stack(children:[
        _katilimciAvatar(p,yerel:yerel,radius:43),
            Positioned(right:-2,bottom:2,child:CircleAvatar(radius:10)),
      ]),
    );
  }
"""
class CallParticipantTests(unittest.TestCase):
    def fixture(self):
        return VIDEO+VOICE+"  Widget _grupAramaAlani(){return Container();}\n"
    def test_reversible_local_audio_and_unclipped_squares(self):
        result=transform(self.fixture())
        self.assertIn("await publication.unsubscribe()",result)
        self.assertIn("await publication.subscribe()",result)
        self.assertIn("person is! lk.RemoteParticipant",result)
        self.assertIn("Sesi yeniden aç (benim için)",result)
        self.assertIn("Sustur (benim için)",result)
        self.assertIn("fit:BoxFit.contain",result)
        self.assertIn("borderRadius:BorderRadius.circular(20)",result)
        self.assertEqual(result.count("_ngelx465RemoteAudioMenu(p)"),2)
        self.assertNotIn("callParticipants",result)
        self.assertEqual(result,transform(result))
    def test_drift_fails_closed(self):
        with self.assertRaises(RuntimeError):
            transform(self.fixture().replace(VOICE_OLD,"decoration:BoxDecoration()"))

if __name__=="__main__":unittest.main()
