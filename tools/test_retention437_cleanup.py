import datetime as dt,unittest
from retention437_cleanup import action
UTC=dt.timezone.utc
NOW=dt.datetime(2026,10,10,tzinfo=UTC)
def ago(days):return NOW-dt.timedelta(days=days)
class Retention437Tests(unittest.TestCase):
    def test_message_boundary(self):
        p='chats/c/messages/m'
        self.assertIsNone(action(p,{'createdAt':ago(13.999)},NOW))
        self.assertEqual(action(p,{'createdAt':ago(14)},NOW),'delete')
    def test_media_is_queued_not_unchecked_deleted(self):
        v={'createdAt':ago(15),'mediaUrl':'https://media.ngelxsocial.com/media/chats/a/x'};p='chats/c/messages/m'
        self.assertEqual(action(p,v,NOW),'queue-media')
        v.update(deletedForEveryone=True,mediaCleanupState='pending')
        self.assertEqual(action(p,v,NOW),'wait-media')
        v['mediaCleanupState']='shared-retained'
        self.assertEqual(action(p,v,NOW),'delete')
    def test_deleted_media_manifest_still_blocks_purge(self):
        self.assertEqual(action('chats/c/messages/m',{'createdAt':ago(20),'deletedForEveryone':True,'cleanupMediaUrls':['https://file'],'mediaCleanupState':'pending'},NOW),'wait-media')
    def test_pending_requests_survive_even_if_read(self):
        for status in ('pending',None,'processing'):
            self.assertIsNone(action('notifications/n',{'read':True,'type':'friend_request','status':status,'createdAt':ago(200)},NOW))
    def test_social_history_uses_resolution_time(self):
        p='friend_requests/a/outgoing/b'
        self.assertIsNone(action(p,{'status':'accepted','createdAt':ago(200),'updatedAt':ago(1)},NOW))
        self.assertIsNone(action(p,{'status':'accepted','createdAt':ago(200)},NOW))
        self.assertEqual(action(p,{'status':'cancelled','updatedAt':ago(90)},NOW),'delete')
    def test_notifications_start_from_read_time(self):
        p='notifications/n'
        self.assertIsNone(action(p,{'read':False,'createdAt':ago(200)},NOW))
        self.assertIsNone(action(p,{'read':True,'createdAt':ago(200),'readAt':ago(1)},NOW))
        self.assertEqual(action(p,{'read':True,'readAt':ago(30)},NOW),'delete')
    def test_protected_content_is_never_scoped_for_deletion(self):
        for p in ('videos/v','users/u','users/u/drafts/d','users/u/saved/s','chats/c','live_streams/l'):
            self.assertIsNone(action(p,{'createdAt':ago(200)},NOW))
        for flag in ('draft','saved','highlighted','archivedAt'):
            self.assertIsNone(action('chats/c/messages/m',{'createdAt':ago(200),flag:True},NOW))
    def test_deleted_content_notifications_require_parent_recheck(self):
        self.assertEqual(action('notifications/n',{'type':'interaction','sourceId':'p'},NOW),'check-content')
        for v in ({'type':'security','sourceId':'p'},{'type':'interaction','sourceId':'a/b'},{'type':'interaction','sourceId':'p','targetKind':'group'}):
            self.assertIsNone(action('notifications/n',v,NOW))
    def test_orphans_need_two_verified_scans_after_48_hours(self):
        import media_cleanup437 as media
        previous=media.ORPHAN_MIN_HOURS
        try:
            media.ORPHAN_MIN_HOURS=48
            head={'LastModified':ago(2),'ETag':'etag','Metadata':{'uid':'a'}}
            confirmed={'etag':'etag','firstSeenAt':ago(1)}
            self.assertTrue(media.orphan_ready('chats/a/file',head,set(),NOW,confirmed))
            self.assertFalse(media.orphan_ready('chats/a/file',head,{'chats/a/file'},NOW,confirmed))
            self.assertFalse(media.orphan_ready('chats/a/file',head,set(),NOW,{'etag':'changed','firstSeenAt':ago(1)}))
            self.assertFalse(media.orphan_ready('chats/a/file',head,set(),NOW,None))
        finally:media.ORPHAN_MIN_HOURS=previous
    def test_search_history_and_unknown_timestamps(self):
        self.assertEqual(action('users/u/searchHistory/s',{'createdAt':ago(30)},NOW),'delete')
        for stamp in (None,'2020-01-01',dt.datetime(2020,1,1),NOW+dt.timedelta(days=1)):
            self.assertIsNone(action('chats/c/messages/m',{'createdAt':stamp},NOW))
if __name__=='__main__':unittest.main()
