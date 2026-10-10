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
Pending Flutter analysis, behavior/rules tests and signed APK. Automatic server sweep is not enabled by this APK; offline/stale historical records require history refresh or server cleanup follow-up. No46/46 claim.
