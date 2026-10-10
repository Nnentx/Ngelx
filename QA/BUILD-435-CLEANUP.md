# Build435 — 36, 44, 45, 46 consolidated cleanup

Version: 1.0.210+435. Preserve all Build395–434 source-generation checks and behavior tests.

- 36: expired unsaved stories are claimed by version-checked transaction into durable Admin jobs; saved/highlighted/archived and concurrently edited stories stay. Unknown media ownership stays queued rather than deleting someone else's object.
- 44: Benden sil adds only this user's hiddenFor entry; all other members keep the message and shared media. Herkesten sil captures all eight original media fields into an immutable tombstone manifest in the same transaction. Per-account local intent is persisted before mutation and retried on chat entry and every 30 seconds. Server deletion retries independently after app closure, preserving forwarded/shared references.
- 45: sender/recipient row observers evict original/tombstone URL images from memory and disk caches; shared-file exports now use URL-specific app temporary directories. No unrelated download is touched. Old manually exported device/gallery files are not controlled by the app.
- 46: complete recursive Firestore inventory protects references in users, posts, chats, replies, nested payloads, text links and raw storage keys. Verified R2 UID must match key owner; recent objects, unknown metadata, changed ETags, read failures and restored content are preserved. Orphan deletion requires age >=7 days and two observations >=24h apart.

Validation: 395–435 preservation chain, 28 Flutter behavior tests, emulator permissions, and signed APK build passed. Latest backend safety suite: 26 tests passed. Flutter analysis has 843 warning/info findings, no fatal build error. APK source b629fca1def34dfde717e16dbaa9e82d6bd9a0d1; SHA256 6fbbbe2088408a55bb9325c98397f668c793ab1ebe8fcc5ae6a7f165ff6152a3.

Scoped production message rules deployed successfully. Live backend fixture validation stopped with Firestore 429 quota exceeded; its private fixture was cleaned up. Live cleanup is NOT verified. Subsequent backend changes enforce a process-wide 10000 read budget, immediate quota deferral, and a private fixture scan instead of repeated full production scans. Push validation does not run production cleanup; manual validation performs one apply pass. Automatic production scheduling remains pending live verification.

Device evidence inherited: 45705 confirms Build434 settings version. 45718 shows last-active labels, purple actors, answered/cancelled request wording and manual refresh. Online green dot / friends / privacy still need device evidence.

Phone test together after installation:
1. Send photo/video/audio/file. Benden sil on recipient: disappears only there; sender still opens it.
2. Herkesten sil on sender: both accounts see deletion, media cannot reappear after refresh/reopen.
3. Delete with connection interrupted, then reconnect/reopen chat: intent resumes, no duplicate/resurrected row.
4. Forward a photo before deleting original: forwarded copy remains usable.
5. Saved/archived/highlighted story stays; expired unsaved story leaves list and cleanup retries safely.
6. Online/friends/hidden activity, request counters (including new incoming message request), and 27/37/38 live-history device checks remain separate from automated code tests.

Scheduled production execution must be confirmed separately; GitHub schedules run only on the default branch. No claim of 46/46 device completion.
