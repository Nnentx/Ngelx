import datetime as dt
import unittest
from retention_cleanup import expires_unsaved,own_media_key
class RetentionSafety(unittest.TestCase):
    def setUp(self):
        self.now=dt.datetime.now(dt.timezone.utc)
        self.old={'type':'story','expiresAt':self.now-dt.timedelta(days=1)}
    def test_unsaved_expired_story(self):self.assertTrue(expires_unsaved(self.old,self.now))
    def test_saved_highlight_and_explicit_archive_preserved(self):
        for field,value in [('saved',True),('highlighted',True),('archivedAt',self.now)]:
            self.assertFalse(expires_unsaved(dict(self.old,**{field:value}),self.now))
    def test_active_story_preserved(self):
        self.assertFalse(expires_unsaved(dict(self.old,expiresAt=self.now+dt.timedelta(hours=1)),self.now))
    def test_posts_and_bad_timestamps_preserved(self):
        self.assertFalse(expires_unsaved(dict(self.old,type='video'),self.now))
        self.assertFalse(expires_unsaved(dict(self.old,expiresAt='yesterday'),self.now))
    def test_actual_video_and_story_upload_paths(self):
        for kind in ('videos','stories'):
            self.assertEqual(own_media_key('https://media.example/media/'+kind+'/alice/file.mp4','alice'),kind+'/alice/file.mp4')
    def test_cross_user_paths_and_traversal_rejected(self):
        for key in ('stories/bob/file.mp4','stories/alice/../bob/file.mp4','stories/alice/%2e%2e/file','stories/alice//file'):
            self.assertIsNone(own_media_key('https://media.example/media/'+key,'alice'))
if __name__=='__main__':unittest.main()
