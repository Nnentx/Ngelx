"""Build468 regression for Android private-chat composer system-navbar overlap."""
import unittest
from apply_build468_private_composer_nav import transform

BODY="""class _SohbetPageState extends State<SohbetPage> {
  Scaffold(
    resizeToAvoidBottomInset:true,
    // Build465: the composer already has SafeArea(top:false) at the bottom.
    bottomNavigationBar:const SizedBox.shrink(),
    _engelDurumuDinle(builder:(_,__)=>something
        :SafeArea(top:false,minimum:const EdgeInsets.only(bottom:7),child:Container(
          : Row(
              crossAxisAlignment:CrossAxisAlignment.end,
              children:[
                medyaGonder(ImageSource.camera),
                medyaGonder(ImageSource.gallery),
                onPressed:sesKaydiDegistir,
                onPressed:emojiSec,
                onPressed:gonderiliyor?null:gonder,
                contentPadding:const EdgeInsets.symmetric(horizontal:10,vertical:10),
              ],
          ),
        )),
  );
}
class NgelXSesliMesaj extends StatefulWidget {}
"""

class PrivateComposerNavTests(unittest.TestCase):
    def test_android_navigation_slot_is_not_zero_or_doubled(self):
        s=transform(BODY)
        self.assertIn('bottomNavigationBar:ColoredBox(',s)
        self.assertIn('ngelxAltSistemRezervi(context)',s)
        self.assertIn('MediaQuery.viewInsetsOf(context).bottom>0',s)
        self.assertIn('SafeArea(top:false,bottom:false,child:Container(',s)
        self.assertIn('crossAxisAlignment:CrossAxisAlignment.center',s)
        self.assertNotIn('bottomNavigationBar:const SizedBox.shrink()',s)
        self.assertEqual(transform(s),s)
        for unchanged in ('resizeToAvoidBottomInset:true',
                          'medyaGonder(ImageSource.camera)',
                          'medyaGonder(ImageSource.gallery)',
                          'onPressed:sesKaydiDegistir',
                          'onPressed:emojiSec',
                          'onPressed:gonderiliyor?null:gonder'):
            self.assertIn(unchanged,s)

    def test_source_drift_fails_closed(self):
        with self.assertRaises(RuntimeError):
            transform(BODY.replace('bottomNavigationBar:const SizedBox.shrink()',
                                   'bottomNavigationBar:const SizedBox(height:90)'))

if __name__=='__main__':
    unittest.main()
