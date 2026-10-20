#!/usr/bin/env python3
"""Regression contracts for assembled sources; baseline is the verified541 app."""
import os,unittest
from pathlib import Path
from apply_build542_call_refinements import TRANSFORMS,transform
class Refinements(unittest.TestCase):
 def setUp(self):
  self.root=Path(os.environ.get('BUILD542_BASELINE','/tmp/build541-full/lib'))
  self.before={n:(self.root/n).read_text() for n in TRANSFORMS}
  self.after={n:transform(s,TRANSFORMS[n]) for n,s in self.before.items()}
 def test_atomic_anchors_and_idempotence(self):
  for n,s in self.after.items(): self.assertEqual(transform(s,TRANSFORMS[n]),s)
 def test_media_and_moderation_preserved(self):
  a=self.before['main.dart'];b=self.after['main.dart']
  for anchor in ['lk.VideoTrackRenderer','_ngelx469ParticipantMenu','ngelx446MuteMenu','onPopInvokedWithResult','_stopLocal444','_enterPip520','_requestFloating509','Permission.camera.request()']:
   self.assertIn(anchor,b)
  self.assertEqual(a.count('lk.VideoTrackRenderer'),b.count('lk.VideoTrackRenderer'))
 def test_direct_intent_keeps_transaction_guards(self):
  s=self.after['build534_explicit_group_rejoin.dart']
  self.assertNotIn('showDialog',s)
  self.assertIn("data['callKickedUids']",s)
  self.assertIn("data['callRoomName'] != roomName",s)
  self.assertIn('userConfirmed:approved',s)
 def test_only_new_account_capture_default(self):
  s=self.after['main.dart']
  self.assertIn("'allowProfileCapture': true,",s)
  self.assertIn("profilKayitIzni=v['allowProfileCapture']==true",s)
 def test_no_duplicate_call_banners(self):
  s=self.after['main.dart']
  self.assertNotIn('const Ngelx445InboxCallBanner(),',s)
  self.assertNotIn('Arama devam ediyor • Aramaya dön',s)
  self.assertNotIn("title:const Text('Görüşmeden ayrıl?')",s)
 def test_friends_and_group_join_stay_separate(self):
  s=self.after['build445_inbox_model.dart']
  friends=s[s.index('class Ngelx445FriendsStrip'):s.index('Future<void> ngelx445ReturnCall')]
  self.assertIn("collection('friendships').where('members',arrayContains:widget.uid)",friends)
  self.assertNotIn('KATIL',friends)
  self.assertNotIn("...List<String>.from(data['following']",friends)
  self.assertIn('top:visible?64:0',s)
  self.assertIn('right:0,height:64',s)
 def test_only_selected_sources_change(self):
  self.assertEqual(set(TRANSFORMS),{'main.dart','build445_inbox_model.dart','build534_explicit_group_rejoin.dart','build517_group_leave.dart'})
if __name__=='__main__':unittest.main()
