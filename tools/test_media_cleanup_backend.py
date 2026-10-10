import unittest
import media_cleanup_backend
from media_cleanup435 import media_key
from media_cleanup_backend import inventory_fast
class LegacyOrigins(unittest.TestCase):
 def test_only_actual_deployed_worker_aliases_are_allowed(self):
  for host in ['ngelx-media.alihancaglar76.workers.dev','ngelx-upload.alihancaglar76.workers.dev']:
   self.assertEqual(media_key('https://'+host+'/media/stories/alice/old.mp4'),'stories/alice/old.mp4')
  self.assertIsNone(media_key('https://foreign.workers.dev/media/stories/alice/old.mp4'))
 def test_missing_parent_still_scans_nested_references(self):
  class Snap:
   def __init__(self,exists=True):self.exists=exists
  class Ref:
   def __init__(self,path,exists=True,children=()):self.path=path;self.exists=exists;self.children=children
   def get(self):return Snap(self.exists)
   def collections(self):return iter(self.children)
  class Col:
   def __init__(self,docs):self.docs=docs
   def list_documents(self):return iter(self.docs)
  class DB:
   def collections(self):return iter([Col([Ref('chats/missing',False,[Col([Ref('chats/missing/messages/shared')])])])])
  self.assertEqual(set(inventory_fast(DB())),{'chats/missing/messages/shared'})
  with self.assertRaises(RuntimeError):inventory_fast(DB(),max_docs=1)
 def test_nested_read_error_aborts_whole_inventory(self):
  class Ref:
   path='users/private'
   def get(self):raise RuntimeError('Read unavailable')
   def collections(self):return []
  class Col:
   def list_documents(self):return [Ref()]
  class DB:
   def collections(self):return [Col()]
  with self.assertRaises(RuntimeError):inventory_fast(DB())
if __name__=='__main__':unittest.main()
