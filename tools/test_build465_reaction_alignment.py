"""Badge must follow media, not a stretched message row."""
import unittest
from apply_build465_reaction_alignment import transform

GROUP="""  Widget _grupMedyaTepkiAlani(Widget media,dynamic ref,dynamic counts,int total){
    if(total<=0)return media;
    return Stack(
      clipBehavior:Clip.none,
      children:[
        Padding(padding:const EdgeInsets.only(bottom:12),child:media),
        Positioned(
          right:8,
          bottom:2,
          child:Text('heart'),
        ),
      ],
    );
  }
"""
PRIVATE="""  Widget _ozelMedyaTepkiAlani(Widget media,dynamic ref,dynamic counts,int total){
    const sagDokunmaAlani=42.0,altDokunmaAlani=13.0;
    return Stack(clipBehavior:Clip.none,children:[
      Column(children:[media]),
      if(total>0)Positioned(
        right:sagDokunmaAlani,
        bottom:altDokunmaAlani,
        child:FractionalTranslation(
          translation:const Offset(.5,.5),
          child:Text('heart'),
        ),
      ),
    ]);
  }
"""
class ReactionTests(unittest.TestCase):
    def fixture(self):
        return GROUP+"  Widget mesajKarti(){}\n"+PRIVATE+"  Widget ozelMesajKarti(){}\n"
    def test_group_and_private_badges_shrink_wrap(self):
        result=transform(self.fixture())
        self.assertEqual(result.count("Align(widthFactor:1.0,alignment:Alignment.centerLeft,child:Stack("),2)
        self.assertIn("right:18,",result)
        self.assertIn("right:sagDokunmaAlani+5",result)
        self.assertIn("Offset(.25,.5)",result)
        self.assertEqual(result,transform(result))
    def test_fail_closed_on_unknown_layout(self):
        with self.assertRaises(RuntimeError):
            transform(self.fixture().replace("right:8,","right:45,"))
if __name__=="__main__":unittest.main()
