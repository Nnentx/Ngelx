import unittest
import media_cleanup_backend
from media_cleanup435 import media_key
class LegacyOrigins(unittest.TestCase):
 def test_only_actual_deployed_worker_aliases_are_allowed(self):
  for host in ['ngelx-media.alihancaglar76.workers.dev','ngelx-upload.alihancaglar76.workers.dev']:
   self.assertEqual(media_key('https://'+host+'/media/stories/alice/old.mp4'),'stories/alice/old.mp4')
  self.assertIsNone(media_key('https://foreign.workers.dev/media/stories/alice/old.mp4'))
if __name__=='__main__':unittest.main()
