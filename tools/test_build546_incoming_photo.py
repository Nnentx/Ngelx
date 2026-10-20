import unittest
from pathlib import Path
from apply_build546_incoming_photo import transform
class Photo546(unittest.TestCase):
 def test_native_lookup_never_blocks_ring_or_changes_actions(self):
  old=Path('app/android/app/src/main/kotlin/com/nnentx/ngelx_app/IncomingCallActivity470.kt').read_text();new=transform(old)
  self.assertEqual(transform(new),new)
  for name in ['respond("answer")','respond("reject")','IncomingCallService.cancel(this, room)','timer.postDelayed(check, 700)']:
   self.assertEqual(old.count(name),new.count(name))
  for guard in ['photoExecutor546.execute','currentUser?.uid!=uid','isStillRinging470(room)','instanceFollowRedirects=false','readBounded546','groupPhotoUrl','callStartedBy','photoUrl']:
   self.assertIn(guard,new)
  self.assertNotIn('readNBytes',new)
if __name__=='__main__':unittest.main()
