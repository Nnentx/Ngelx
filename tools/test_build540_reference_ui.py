import os
import re
import unittest
from pathlib import Path
from apply_build540_reference_ui import live_transform, main_transform, model_transform, guest_transform, composer_transform, pk_transform

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

    def test_guest_and_pk_permissions_preserved(self):
        old=self.baseline('build448_live_guests.dart');new=guest_transform(old)
        self.assertEqual(old[:old.index('class Ngelx448GuestControls')],new[:new.index('class Ngelx448GuestControls')])
        self.assertIn("if(host&&compact)",new)
        self.assertIn("_viewerJoinPanel497(context,uid,status is String?status:null)",new)
        self.assertEqual(guest_transform(new),new)
        old=self.baseline('live_pk.dart');new=pk_transform(old)
        for token in ["if(user==null||user.uid!=ownerUid)return;", "if(mv['pkActive']==true)",
                      "'requestExpiresAt'", "'status':'pending'", "'members':<String>[ownerUid,hedefUid]"]:
            self.assertIn(token,new)
        a=old.index('                              final id=ngelxCanliPkBelgeId');b=old.index("                            icon:const Icon(Icons.flash_on_rounded",a)
        x=new.index('                              final id=ngelxCanliPkBelgeId');y=new.index("                            icon:const Icon(Icons.flash_on_rounded",x)
        self.assertEqual(old[a:b],new[x:y])
        self.assertEqual(pk_transform(new),new)

    def test_composer_retains_draft_send_and_muting(self):
        old=self.baseline('build453_widgets.dart');new=composer_transform(old)
        for token in ['widget.controller','widget.focus','widget.send()',"v['commentsEnabled']!=false&&!muted",'onSubmitted:enabled?(_)=>_send():null']:
            self.assertIn(token,new)
        self.assertIn('valueListenable:widget.controller',new)
        self.assertEqual(composer_transform(new),new)

    def test_unknown_input_is_rejected(self):
        for transform in [main_transform,live_transform,model_transform]:
            with self.assertRaises((RuntimeError,ValueError)):
                transform('class Unknown {}')

if __name__=='__main__':unittest.main()
