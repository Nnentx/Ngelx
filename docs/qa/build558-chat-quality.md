# Build558 — chat position, media albums and call duration

Based on the exact signed Build557 assembled application (`main.dart` SHA256 `a395e960a803202addf32d9573fb133016696bc94c34af74c6d2bbd91b17ba79`). The raw historical Flutter sources are intentionally unchanged. Run the new applicator after the complete Build557 generator chain. Source hashes are checked before mutation; repeat application is supported and partial/drifted states are rejected.

Implemented:
- The green global call strip displays elapsed minutes/seconds alongside the call name. Its local ticker uses the retained connected-call start and is disposed with the strip. No periodic network request was added.
- Group chat follows a new tail message, instead of treating reaction/deletion snapshots as new messages. Both chat lists retain stable row keys and compensate for changed message heights using a visible unchanged row. Message search and deliberate user scrolling retain priority.
- The group long-press menu now starts with the same horizontal reaction/reply/copy/reminder/More structure as private chat. Existing sender/admin checks and additional operations remain under More. Opening the first menu no longer waits for a server read.
- Group header loading can use the existing cache and has a bounded retry state; membership gates remain in place.
- Inbox notes occupy a real hit-testable area above the avatar. Tapping shows the entire note; the owner can edit or delete it. No overlap with the avatar ring.
- Community notification names use Turkish uppercase and blue; group names use green. Older group-added text can recover an embedded group name. Missing community titles are resolved once per community per page, through existing access rules. Unread backgrounds are darker.
- Gallery selection accepts multiple photos and videos. Existing normalization, upload functions, private message-request checks, group membership/post restrictions, size limit and private disappearing-message expiry are retained. Album uploads are sequential; more than 100 selected items is rejected explicitly rather than silently truncated. An album is one photo-compatible message with `albumItems558` and `mediaUrls`, preserving older clients' first-item fallback.
- Album previews stack photos; tapping opens a grid, then the existing full-screen photo/video viewers. Single/full-album download buttons report failures and stop saving when their viewer is removed. Revocation uses the existing live message-source wrapper. Album URLs join local cache eviction and the existing tombstone cleanup manifest.
- Profile badge rendering uses account IDs, never display names. Alperen's approved final appearance is a smooth circular blue check with **no crown and no KURUCU text**. The other three checks retain the normal style.

## Account identity still needed

The four actual Firebase UID values were not available in sources or prior context. Release-time `NGELX_FOUNDER_UID` and `NGELX_VERIFIED_UIDS` (three comma-separated IDs) must be provisioned from the real accounts. Defaults award no badges. Extra allowlist IDs are rejected. No production user verification flags were changed or guessed from names.

## Rules compatibility

The paired rules update extends the existing sender/admin tombstone operation to clear both album fields and requires the cleanup manifest to match the old message URLs plus its stored album URL list. It also brings the retained modern rules into agreement with the existing Build435 deletion client. No rules were deployed. Review the complete generated rule delta and run the emulator tests before installing a candidate with album deletion enabled. Automatic retention and cleanup remain paused; this change does not run them.

## Validation

Passed locally:
- Exact verified Build557 baseline hash match.
- Cold/repeat source patch reproduction and rejection of unrelated source drift before mutation.
- Rules patch idempotence and confinement to the existing chat-message block.
- Python compilation and JavaScript syntax check.
- Tree-sitter Dart syntax parsing of all changed files and the added widget test.

Prepared but **not run**:
- `tools/build558_widget_test.dart`: call time boundaries, exact UID allowlist behavior, malformed album records and narrow-phone menu actions.
- `tools/build558_rules_test.mjs`: local emulator sender/admin deletion, outsider denial, forged manifests and uncleared-album denial.
- Full Flutter analysis, APK compilation, signature/package identity checks and two-phone testing.

Local Flutter startup/dependency validation was automatically rejected after it attempted a request to the cloud metadata credential boundary (`169.254.169.254`). It was not retried or bypassed. The manual-only Build558 workflow is prepared for authorized validation; it has not been dispatched. There is no Build558 APK or claim of physical-device acceptance.

Remaining device acceptance: reaction and deletion while viewing a tall photo, navigating away/back during a long call, mixed albums, revoked media, interrupted upload/download, group cache/retry recovery, note hit targets, and actual account ID provisioning. General intermittent startup slowness still requires device profiling; these changes remove identified unnecessary menu reads/scroll work without claiming every performance issue is resolved.
