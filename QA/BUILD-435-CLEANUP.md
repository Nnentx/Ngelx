# Build435 — 36, 44, 45, 46 consolidated cleanup

Version: 1.0.210+435. Preserve all Build395–434 source-generation checks and behavior tests.

- 36: expired unsaved stories are claimed by version-checked transaction into durable Admin jobs; saved/highlighted/archived and concurrently edited stories stay. Unknown media ownership stays queued rather than deleting someone else's object.
- 44: Benden sil adds only this user's hiddenFor entry; all other members keep the message and shared media. Herkesten sil captures all eight original media fields into an immutable tombstone manifest in the same transaction. Per-account local intent is persisted before mutation and retried on chat entry and every 30 seconds. Server deletion retries independently after app closure, preserving forwarded/shared references.
- 45: sender/recipient row observers evict original/tombstone URL images from memory and disk caches; shared-file exports now use URL-specific app temporary directories. No unrelated download is touched. Old manually exported device/gallery files are not controlled by the app.
- 46: complete recursive Firestore inventory protects references in users, posts, chats, replies, nested payloads, text links and raw storage keys. Verified R2 UID must match key owner; recent objects, unknown metadata, changed ETags, read failures and restored content are preserved. Orphan deletion requires age >=7 days and two observations >=24h apart.

Local: 395–435 preservation chain and 22 Python safety tests passed. Flutter behavior, emulator permissions, signed APK and real server job pending at initial commit.

Device evidence inherited: 45705 confirms Build434 settings version. 45718 shows last-active labels, purple actors, answered/cancelled request wording and manual refresh. Online green dot / friends / privacy still need device evidence.

Phone test together after installation:
1. Send photo/video/audio/file. Benden sil on recipient: disappears only there; sender still opens it.
2. Herkesten sil on sender: both accounts see deletion, media cannot reappear after refresh/reopen.
3. Delete with connection interrupted, then reconnect/reopen chat: intent resumes, no duplicate/resurrected row.
4. Forward a photo before deleting original: forwarded copy remains usable.
5. Saved/archived/highlighted story stays; expired unsaved story leaves list and cleanup retries safely.
6. Online/friends/hidden activity, request counters (including new incoming message request), and 27/37/38 live-history device checks remain separate from automated code tests.

Scheduled production execution must be confirmed separately; GitHub schedules run only on the default branch. No claim of 46/46 device completion.
