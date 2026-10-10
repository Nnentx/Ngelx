import datetime as dt,unittest
from live_history_cleanup import eligible,urls
class LiveCleanup(unittest.TestCase):
 def test_active_and_missing_end_protected(self):
  now=dt.datetime.now(dt.timezone.utc)
  for v in [{'active':True,'status':'ended','ownerId':'u'},{'active':False,'ownerId':'u'},{'active':False,'status':'ended'}]:self.assertFalse(eligible(v,now))
 def test_unsaved_and_saved_boundary(self):
  now=dt.datetime.now(dt.timezone.utc);v={'active':False,'status':'ended','ownerId':'u','endedAt':now-dt.timedelta(days=29)}
  self.assertTrue(eligible(v,now));v['saved']=True;self.assertFalse(eligible(v,now));v['endedAt']=now-dt.timedelta(days=30);self.assertTrue(eligible(v,now))
 def test_media_and_retry(self):
  now=dt.datetime.now(dt.timezone.utc)
  self.assertTrue(eligible({'active':False,'status':'ended','ownerId':'u','saved':True,'deleting':True},now))
  self.assertEqual(urls({'recordingUrl':'https://x/media/videos/u/1','mediaUrl':'https://x/media/videos/u/1'}),{'https://x/media/videos/u/1'})
if __name__=='__main__':unittest.main()
