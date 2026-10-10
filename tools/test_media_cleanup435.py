import datetime as dt,unittest
from media_cleanup435 import media_key,key_owner,collect_keys,object_safe,orphan_ready,reference_keys,inventory,remove_media
UTC=dt.timezone.utc
class Snap:
 def __init__(self,v):self.v=v
 def to_dict(self):return self.v
class CleanupSafety435(unittest.TestCase):
 def setUp(self):
  self.now=dt.datetime(2026,10,10,tzinfo=UTC);self.key='chats/alice/a.mp4';self.url='https://media.ngelxsocial.com/media/'+self.key
  self.head={'Metadata':{'uid':'alice'},'ETag':'v1','LastModified':self.now-dt.timedelta(days=8)}
  self.q={'etag':'v1','firstSeenAt':self.now-dt.timedelta(days=2)}
 def test_url_origin_paths_and_encoded_traversal(self):
  self.assertEqual(media_key(self.url),self.key)
  for url in ['http://media.ngelxsocial.com/media/'+self.key,'https://evil.test/media/'+self.key,'https://media.ngelxsocial.com/media/chats/alice/%2e%2e/a.mp4']:
   self.assertIsNone(media_key(url))
  self.assertIsNone(key_owner('_chunks/alice/file'))
 def test_shared_nested_reply_and_profile_media_are_retained(self):
  refs=reference_keys({'users/alice':Snap({'introVideoUrl':self.url}),'chats/c/messages/new':Snap({'reply':{'media':[self.url]}})})
  self.assertIn(self.key,refs)
  self.assertFalse(orphan_ready(self.key,self.head,refs,self.now,self.q))
 def test_hidden_for_is_not_global_deletion(self):
  refs=reference_keys({'chats/c/messages/m':Snap({'hiddenFor':['alice'],'mediaUrl':self.url})})
  self.assertIn(self.key,refs)
 def test_tombstone_manifest_and_jobs_do_not_count_as_active_reference(self):
  refs=reference_keys({'chats/c/messages/m':Snap({'deletedForEveryone':True,'cleanupMediaUrls':[self.url]}),'_media_cleanup435/j':Snap({'urls':[self.url]})})
  self.assertNotIn(self.key,refs)
 def test_all_reference_shapes_collected(self):
  self.assertEqual(collect_keys({'x':[self.url,{'url':self.url}]}),{self.key})
  self.assertIn(self.key,collect_keys('Bak: '+self.url))
  self.assertIn(self.key,collect_keys(self.key))
  self.assertIn(self.key,collect_keys(self.url.replace('media.ngelxsocial.com','legacy.workers.dev')))
 def test_orphan_requires_seven_days_and_second_scan_after_day(self):
  self.assertTrue(orphan_ready(self.key,self.head,set(),self.now,self.q))
  self.assertFalse(orphan_ready(self.key,self.head,set(),self.now,{}))
  self.assertFalse(orphan_ready(self.key,{**self.head,'LastModified':self.now},set(),self.now,self.q))
  self.assertFalse(orphan_ready(self.key,self.head,set(),self.now,{**self.q,'firstSeenAt':self.now}))
 def test_unknown_owner_changed_etag_and_future_stamp_block_deletion(self):
  self.assertFalse(object_safe(self.key,{**self.head,'Metadata':{}}))
  self.assertFalse(object_safe(self.key,{**self.head,'Metadata':{'uid':'bob'}}))
  self.assertFalse(orphan_ready(self.key,{**self.head,'ETag':'v2'},set(),self.now,self.q))
  self.assertFalse(orphan_ready(self.key,{**self.head,'LastModified':self.now+dt.timedelta(days=1)},set(),self.now,self.q))
 def test_inventory_error_aborts_instead_of_empty_references(self):
  class DB:
   def collections(self):raise RuntimeError('Firestore offline')
  with self.assertRaises(RuntimeError):inventory(DB())
 def test_source_exclusion_does_not_remove_other_users_references(self):
  refs=reference_keys({'videos/expired':Snap({'mediaUrl':self.url}),'videos/saved':Snap({'saved':True,'mediaUrl':self.url})},exclude=['videos/expired'])
  self.assertIn(self.key,refs)
 def test_failed_delete_keeps_retryable_intent_and_retry_succeeds(self):
  deleted=[]
  def fail(k):raise OSError('R2 unavailable')
  with self.assertRaises(OSError):remove_media(self.key,'alice',lambda k:self.head,lambda:set(),fail)
  self.assertEqual(remove_media(self.key,'alice',lambda k:self.head,lambda:set(),deleted.append),'deleted')
  self.assertEqual(deleted,[self.key])
 def test_reference_added_during_verification_prevents_delete(self):
  scans=iter([set(),{self.key}]);deleted=[]
  self.assertEqual(remove_media(self.key,'alice',lambda k:self.head,lambda:next(scans),deleted.append),'shared')
  self.assertFalse(deleted)
 def test_restored_source_changed_object_and_wrong_owner_preserved(self):
  deleted=[]
  self.assertEqual(remove_media(self.key,'alice',lambda k:self.head,lambda:set(),deleted.append,lambda:False),'blocked')
  heads=iter([self.head,{**self.head,'ETag':'changed'}])
  self.assertEqual(remove_media(self.key,'alice',lambda k:next(heads),lambda:set(),deleted.append),'blocked')
  self.assertEqual(remove_media(self.key,'bob',lambda k:self.head,lambda:set(),deleted.append),'blocked')
  self.assertFalse(deleted)
 def test_already_deleted_object_is_successfully_idempotent(self):
  self.assertEqual(remove_media(self.key,'alice',lambda k:None,lambda:set(),lambda k:self.fail('delete should not run')),'missing')
if __name__=='__main__':unittest.main()
