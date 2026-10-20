import unittest,os
from pathlib import Path
from apply_build548_device_live_fixes import main_source,studio_source,guest_source
BASE=Path(os.environ.get('BUILD548_BASELINE','app/lib'))
class Device548(unittest.TestCase):
 def test_gallery_is_mixed_only_for_generic_buttons_and_guards_reentry(self):
  s=main_source((BASE/'main.dart').read_text())
  a=s.index('class _YeniYuklePageState');b=s.index('\nclass ',a+15);c=s[a:b]
  self.assertIn('await ngelxSohbetGaleriMedyaSec()',c)
  self.assertIn('onPressed:yukleniyor||_createBusy548?null:genelGaleri548',c)
  self.assertIn('Icons.photo_library_outlined,()=>unawaited(genelGaleri548())',c)
  self.assertIn('Future<void> medyaSec()=>_createMediaAction548(_medyaSec548)',c)
  self.assertIn('Duration(milliseconds:450)',c)
  self.assertIn('await _taslagiYukle();if(mounted)await _kayipMedyaKurtar()',c)
  self.assertIn('ngelxCokluResimSec',c)
 def test_peer_resolution_and_speaker_semantics(self):
  s=main_source((BASE/'main.dart').read_text());a=s.index('class _NgelXAramaPageState');b=s.index('\nclass GrupBilgiPage ',a);c=s[a:b]
  self.assertEqual(c.count('widget.baslik'),1)
  self.assertEqual(c.count('widget.foto'),1)
  self.assertIn('ngelx548PeerUid',c);self.assertIn('_peerSub548?.cancel()',c)
  self.assertIn("label=='Hoparlör'||label=='Ses'?acik:!acik",c)
  self.assertIn('_speakerBusy548||bitiyor',c)
  self.assertIn('isSpeakerOutputPreferred',c)
 def test_guest_never_publishes_without_choice_and_shows_local_track(self):
  old=(BASE/'live_broadcast_studio.dart').read_text();s=studio_source(old)
  self.assertIn('if(accepted&&!_guestConsent548)',s)
  self.assertIn('cameraPreferred:_guestCameraWanted546,onCameraPreference:_chooseGuestMedia548',s)
  self.assertIn('connected548:_guestActive448',s)
  self.assertIn('Expanded(child:_stage548())',s)
  self.assertIn('final ids=_viewerGuestIds489()..sort()',s)
  self.assertIn('mine?',s)
  self.assertNotIn("'Konuk bağlantısı hazır'",s)
  self.assertNotIn('child:_guestRail488()',s)
  self.assertNotIn('right:12,width:120,height:260',s)
  # Connection authorization, immediate mute, host-only server moderation stay.
  for guard in ['await _guestVerify546(uid)','if(!turnOn546)','_hostGuestAction489','_guestAudioPolicySub489','canPublish:permissions?.canPublish==true']:
   self.assertIn(guard,s)
  for part in ['_heartbeatYaz','_izleyicideYayinBitti','_bitisEkrani']:
   self.assertEqual(old.count(part),s.count(part))
 def test_private_prejoin_preview_is_camera_only_and_disposed_before_join(self):
  widgets=Path('tools/build548_widgets.dart').read_text()
  self.assertIn('enableAudio:false',widgets)
  self.assertNotIn('setCameraEnabled',widgets)
  self.assertNotIn('setMicrophoneEnabled',widgets)
  self.assertIn('opening?.dispose()',widgets)
  guest=guest_source((BASE/'build448_live_guests.dart').read_text())
  action=guest[guest.index('final label='):guest.index('@override Widget build')]
  self.assertLess(action.index('await previewKey.currentState?.stop548()'),action.index('onCameraPreference?.call(camera548)'))
  self.assertIn("action!='connect548'",action)
 def test_gifts_retain_retry_idempotency_and_are_explicitly_free(self):
  old=(BASE/'live_broadcast_studio.dart').read_text();s=studio_source(old)
  self.assertNotIn('NGELX_VIRTUAL_GIFT_STAGING',s)
  for marker in ['_pendingGiftSignature521','_pendingGiftId521','virtual_gift_event_mismatch','maxAttempts:4']:
   self.assertEqual(old.count(marker),s.count(marker))
  self.assertIn('Ücretsiz sanal hediyeler',s)
  self.assertIn('ngelx548ValidGift(ad,puan,adet)',s)
  self.assertIn("live.data()?['active']!=true",s)
 def test_transform_is_idempotent_and_photos_have_no_dark_frame(self):
  for file,fn in [('main.dart',main_source),('live_broadcast_studio.dart',studio_source),('build448_live_guests.dart',guest_source)]:
   new=fn((BASE/file).read_text());self.assertEqual(fn(new),new)
  s=main_source((BASE/'main.dart').read_text());a=s.index('class NgelXSohbetFotoOnizleme');b=s.index('class NgelXSohbetVideoOnizleme',a)
  self.assertNotIn('ColoredBox',s[a:b]);self.assertIn('Ngelx548ChatPhoto',s[a:b])
if __name__=='__main__':unittest.main()
