# Build433 — request pages, notifications and live history

User-authorized scope: inbox/request pages and counters, profile notification bell, colored actors; original46 items27,37,38. Preserve working messages, stories, archive and profile search.

## Device confirmations carried forward
User confirmed long story playback, failed video retry, correct story selection, archive, profile search and profile transition speed as complete on 2026-10-10. Do not request these tests again unless a regression occurs.
Build432 video45659 displayed inbox, notifications and requests without prior endless loading.

## Changes
- Follow/friend cards open category-specific title and pending list, no Activity/category tabs. Shared newest-state dedup for list/card counters, accepted newer state suppresses old pending duplicates.
- Friend/follow rows: round photo, name, blue Onayla and gray Sil, manual refresh and pending count. Existing social backend kept.
- Message request count retains shared pending-chat predicate from432.
- Profile bell remains purple inside white circle; opens only Bildirimler list. Inbox Tümü notification actor names are purple, body remains dark.
- Live history excludes active streams and ended unsaved records. Saved records retained30days from end. This is the chosen default retention rule; it can be adjusted centrally.
- Owner-checked deletion marks durable deleting state, awaits verified media cleanup, clears comments/reactions/viewers in batches, deletes root last. Failed cleanup retains retry state. Host end triggers unsaved cleanup after existing summary metrics and disconnect, history/manual refresh retries.

## Validation
Pending Flutter analysis, behavior/rules tests and signed APK. Server live cleanup workflow verifies media ownership, atomically queues unchanged eligible ended records, recursively cleans child records and retains retry jobs. Deployment/production cleanup results pending. Crash-stale active records are conservatively protected. No46/46 claim.

Server run38054945244 succeeded: existing deployed rules changed only live child delete permissions; preview30 eligible ended records, queued30/cleaned30, unverifiable0. No scheduled global sweep is enabled; immediate host end and history refresh handle new owner records. Production records marked active are protected even after a crash.

Final source3137f47d6f84c139cc61db5e6f9ad077368b3c34, CI38055242305 passed: full Build395–433 chain, Flutter analysis with831 existing warnings/info (no fatal errors),23 behavior tests, live host/outsider Firestore emulator tests, signed release APK verified v2. New device tests remain open.

APK145085310bytes SHA256c4c592f4fdda71f497aed04631eaaeffac30b3de43a884b386c6b6e538d44dc0. Artifact ZIP SHA256d3ba0891f891641880cf054db0b45e589b4c68ca7240c9106fc0b56752c3b620. Download hashes verified.
