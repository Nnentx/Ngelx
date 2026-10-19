import os,re,unittest
from pathlib import Path
from apply_build541_continuity import TRANSFORMS,transform
class Continuity(unittest.TestCase):
 def baseline(self,name):return (Path(os.environ.get('BUILD541_BASELINE','/workspace/scratch/452c482f9e19/ngelx/app/lib'))/name).read_text()
 def test_all_transformations_are_idempotent(self):
  for name,fn in TRANSFORMS.items():
   s=self.baseline(name);out=transform(s,fn);self.assertEqual(transform(out,fn),out)
 def test_minimize_transfers_original_room_and_does_not_hide_card(self):
  old=self.baseline('main.dart');new=TRANSFORMS['main.dart'](old)
  a=new.index('  Future<void> _aramaEkraniniKucult()');b=new.index('  @override Widget build',a);body=new[a:b]
  self.assertNotIn('ngelx448HideCallCard',body)
  for token in ['ngelx448HiddenCallCard.value=null','room:r','ngelxCallSession444.minimize(widget.roomName)','oda=null','Navigator.pop(context,false)']:self.assertIn(token,body)
  self.assertEqual(new.replace('    ngelx448HiddenCallCard.value=null;','    ngelx448HideCallCard(widget.roomName);').replace('const Ngelx445CallOverlay(),const Ngelx541GlobalCallStrip()','const Ngelx445CallOverlay()'),old)
 def test_livestream_gift_write_gate_and_moderation_unchanged(self):
  old=self.baseline('live_broadcast_studio.dart');new=TRANSFORMS['live_broadcast_studio.dart'](old)
  a=old.index('  Future<void> _hediyeGonder');b=old.index('  Future<void> _hediyePaneli',a)
  self.assertIn(old[a:b],new)
  self.assertIn("()=>_hediyeGonder('Gül','🌹',1)",new)
  self.assertIn("String yazi=_goruntu()==null?'Görüntü bekleniyor':'Bağlı'",new)
 def test_audio_media_lifecycle_and_capacity_preserved(self):
  old=self.baseline('audio_live_rooms.dart');new=TRANSFORMS['audio_live_rooms.dart'](old)
  a=old.index('  Widget koltuk(String id)');self.assertEqual(old[:a],new[:a])
  a=old.index('  @override void dispose()',a);self.assertEqual(old[a:],new[new.index('  @override void dispose()',new.index('  Widget koltuk(String id)')):])
  self.assertIn('.clamp(9,ngelxSesliMaksKonusmaci)',new)
  self.assertIn('onTap:bitti?null:yoneticiyim?istekler:sozIste',new)
 def test_call_video_only_uses_subscribed_unmuted_track(self):
  new=TRANSFORMS['build445_inbox_model.dart'](self.baseline('build445_inbox_model.dart'))
  self.assertIn('publication.subscribed&&!publication.muted&&publication.track is lk.VideoTrack',new)
  self.assertIn('detail.uid!=FirebaseAuth.instance.currentUser?.uid',new)
  self.assertIn('if(ngelx446Calls.muted(name))return;',new)
 def test_unknown_input_rejected(self):
  for name in ['main.dart','live_broadcast_studio.dart','build445_inbox_model.dart']:
   with self.assertRaises((RuntimeError,ValueError)):TRANSFORMS[name]('unknown')
if __name__=='__main__':unittest.main()
