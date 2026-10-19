import os
import re
import unittest
from pathlib import Path
from apply_build540_reference_ui import live_transform, main_transform, model_transform

class Build540Tests(unittest.TestCase):
    def baseline(self, filename):
        return (Path(os.environ.get('BUILD540_BASELINE', '/tmp/build540-baseline')) / filename).read_text()

    def method(self, source, signature):
        start=source.index(signature)
        match=re.search(r'\n  (?:@override|(?:Future|void|bool|Widget|String|int|lk\.)[^\n]*\()', source[start+len(signature):])
        self.assertIsNotNone(match, signature)
        return source[start:start+len(signature)+match.start()]

    def test_call_connection_and_hangup_bodies_preserved(self):
        old=self.baseline('main.dart');new=main_transform(old)
        a=old.index('class _NgelXAramaPageState');b=old.index('class GrupBilgiPage',a)
        x=new.index('class _NgelXAramaPageState');y=new.index('class GrupBilgiPage',x)
        for signature in ['  Future<void> _aramaEkraniniKucult()',
                          '  Future<void> baglan(', '  Future<void> bitir(']:
            self.assertEqual(self.method(old[a:b],signature), self.method(new[x:y],signature))
        self.assertIn('_controlsTimer540?.cancel();',new)
        self.assertIn('MediaQuery.accessibleNavigationOf(context)',new)
        self.assertEqual(main_transform(new),new)

    def test_comments_and_guest_roles_retained(self):
        old=self.baseline('live_broadcast_studio.dart');new=live_transform(old)
        for signature in ['  Widget _guestControl453(bool host)',
                          '  Future<void> _yorumGonder(', '  Future<void> _hostGuestAction489(']:
            self.assertEqual(self.method(old,signature),self.method(new,signature))
        for token in ['_commentScroll510','_commentHistory514','_newCommentChip510',
                      '_yorumYonet(d.id,y)','_guestControl453(false)',
                      '_guestControl453(true)','_yorumGirisAlani()','_guestRail488()']:
            self.assertIn(token,new)
        self.assertIn('maxHeight:keyboard?76:148',new)
        self.assertEqual(live_transform(new),new)

    def test_minimize_remains_reversible_and_scoped(self):
        old=self.baseline('build445_inbox_model.dart');new=model_transform(old)
        for token in ['ngelx445ReturnCall(name)','ngelx448HideCallCard(name)',
                      'ngelx445EndBackground(name)','FirebaseAuth.instance.currentUser?.uid!=detail.uid',
                      'if(ngelx446Calls.muted(name))return;']:
            self.assertIn(token,new)
        self.assertIn('ngelx540SnapMini',new)
        self.assertIn('MediaQuery.viewInsetsOf(context).bottom',new)
        self.assertEqual(model_transform(new),new)

    def test_unknown_input_is_rejected(self):
        for transform in [main_transform,live_transform,model_transform]:
            with self.assertRaises((RuntimeError,ValueError)):
                transform('class Unknown {}')

if __name__=='__main__':unittest.main()
