"""First-open scroll behavior must not restore old middle-of-chat offsets."""
import unittest
from apply_build465_chat_initial_scroll import transform

GROUP="""class _GrupSohbetPageState extends State<GrupSohbetPage>{
  final mesaj=TextEditingController(),liste=ScrollController();
  @override void dispose(){liste.dispose();super.dispose();}
  void render(){
    if(_ilkMesajKaydirma||_enAltta)sonaGit();
    return RefreshIndicator(
      child:ListView.builder(
                    controller:liste,
                    itemBuilder:(_,i)=>Text("a(b)c"), // Dart comment (ignored)
                  ),
    );
  }
}
class TamEkranMedyaPage {}
"""

PRIVATE="""class _SohbetPageState extends State<SohbetPage>{
  final mesaj=TextEditingController(),liste=ScrollController();
  @override
  void dispose(){liste.dispose();super.dispose();}
  void render(){
    if(s.hasData)sonaGit();
    return RefreshIndicator(
      child:ListView.builder(
            key:PageStorageKey<String>('private_chat_'+widget.chatId),
            itemBuilder:(_,i)=>Text("hello"),
          ),
    );
  }
}
class NgelXSesliMesaj {}
"""

class OpeningScrollTests(unittest.TestCase):
    def fixture(self):
        return GROUP+PRIVATE
    def test_latest_message_anchor_and_user_pointer_cancellation(self):
        updated=transform(self.fixture())
        self.assertEqual(updated.count("ScrollController(keepScrollOffset:false)"),2)
        self.assertEqual(updated.count("Timer.periodic("),2)
        self.assertEqual(updated.count("_ngelx465ScheduleBottomOnOpen();"),2)
        self.assertEqual(updated.count("child:Listener(onPointerDown:(_)"),2)
        self.assertEqual(updated.count("_ngelx465StopOpeningBottom();"),2)
        self.assertEqual(updated,transform(updated))
    def test_missing_expected_chat_list_aborts(self):
        with self.assertRaises(RuntimeError):
            transform(self.fixture().replace("controller:liste,","controller:changed,",1))

if __name__=="__main__":
    unittest.main()
