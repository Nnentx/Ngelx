import os,sys,unittest
from pathlib import Path
from apply_build543_community_pip import TRANSFORMS,transform
class Preserve(unittest.TestCase):
 def test_idempotent_atomic_sources(self):
  root=Path(os.environ.get('BUILD543_BASELINE','/tmp/build543-baseline'))
  for name,fn in TRANSFORMS.items():
   before=(root/name).read_text();after=transform(before,fn)
   self.assertEqual(after,transform(after,fn))
   if name.endswith('main.dart'):
    for term in ['ngelx527ConfirmGroupRemoteTrack','_toggleVoiceGroupVideo494','_togglePrivateVoiceCamera507','onPopInvokedWithResult','_ngelx469ParticipantMenu']:
     self.assertIn(term,after)
   if name.endswith('MainActivity.kt'):
    self.assertIn('onUserLeaveHint()',after);self.assertIn('CallAudioService.active&&!isInPictureInPictureMode',after)
 def test_no_production_deploy_added(self):
  s=Path('tools/apply_build543_community_pip.py').read_text()
  self.assertNotIn('firebase deploy',s)
if __name__=='__main__':unittest.main()
