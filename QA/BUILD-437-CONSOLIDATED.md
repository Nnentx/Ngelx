# Build437 / 1.0.212 — approved follow-up package

Sources: 45862.mp4 and 45863.mp4, plus the current Build436 source and QA record.
Preserve the Build395–436 generation chain and all user-passed messaging, stories,
privacy, nickname, wallpaper, request acceptance and profile behaviors. Do not
claim that all 46 device checks passed.

## Changes

- Retire private/group read-receipt and typing switches. Ignore legacy false flags.
  Receipt writes require a foreground current route and newest visible messages;
  use the observed message timestamp instead of claiming future messages were seen.
  Inbox clearing unread counts no longer suppresses receipt writes. Group typing
  refreshes its heartbeat during continuous input. Duplicate group receipt writes
  are serialized and failures do not escape into the UI.
- Private/group quick-send emoji uses the shared chat field. The selected emoji
  and resets propagate to every member, subject to existing block permissions.
- Search returns a message ID through the info route to the existing chat.
  Fetch a bounded context around old results; locate variable-height lazy rows
  and mark the selected group row. Preserve the existing media and delete renderer.
  Deleted, hidden and expired targets cannot be reintroduced by search.
- Network chat/media video initializes with a 15-second timeout per known origin,
  bounded buffering and a fresh-controller retry. Full-screen media opens playback
  automatically; compact chat videos still load on demand.
- New profile links use /?profile=UID because the deployed /u/UID returns 404.
  Android routing supports the new link and old links. Web source gains an explicit
  profile opening button and a static-host fallback. Web deployment is separate.
- Media/link listing covers the latest 48 hours, independent of original messages.
  Original chat messages become unavailable at 14 days in live and cached views.
- Managed image cache uses 7-day staleness and 200 entries. Downloaded attachment
  copies are trimmed at 7 days or 256 MB. Camera originals and upload drafts are
  never removed by generic temporary-directory deletion.
- Bounded server retention pages and transaction rechecks: 14-day messages,
  30-day read notifications/search history, 90-day resolved social request history.
  Pending requests, user/profile documents, drafts, saved and archived content
  are protected. Stale interaction notification rows require a verified deleted
  or missing content parent. Empty old chat previews and unread counters are cleared.
- Media-bearing expired messages first produce the existing durable cleanup
  manifest. Source records wait for completed ownership/reference checks before
  physical deletion. The approved orphan age becomes 48 hours, with a second
  reference/ETag check after a 24-hour confirmation interval. Read-budget or quota
  failures retain jobs instead of authorizing deletion from an incomplete scan.

## Validation

Local Build395–436 source preservation chain passed. Flutter analysis: zero errors;
existing warning/info diagnostics remain. 33 Flutter behavior tests passed, including
receipt visibility, shared emoji and 48-hour/14-day boundary tests. 36 Python cleanup
tests passed. Release CI additionally tests canonical and exact deployed Firestore
permissions, shared emoji across accounts, request creation/block protection,
manifest deletion, signed APK and cleanup credentials. CI outcome is recorded after
completion; a source patch alone is not an APK or device pass.

## Remaining evidence and limitations

- Friend/private-follow creation, recipient notifications and private/group everyone
  delete need two-account phone retest. Build436 implementations remain preserved;
  Firestore resource-exhausted/quota failures cannot be cured by UI changes alone.
- Voice recording playback must be confirmed on the phone; it is not marked passed.
- Automatic retention needs its first successful server run. Daily scheduler must
  be installed on the default branch; a scheduler file on a feature branch alone
  does not activate GitHub schedules. It refuses an unvalidated release revision.
- No blanket deletion of unidentified 24-hour failed-upload files: the current
  uploader does not supply a reliable incomplete-upload ownership/state registry.
  Camera originals/drafts cannot safely be treated as abandoned temporary uploads.
- The 46-item checklist remains the authoritative device-test list. Existing passed
  tests stay passed; no untested item is promoted merely because CI passed.
