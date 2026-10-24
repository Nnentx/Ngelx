# Build558 — chat position, media albums and call duration

Based on the exact signed Build557 assembled application (`main.dart` SHA256 `a395e960a803202addf32d9573fb133016696bc94c34af74c6d2bbd91b17ba79`). The raw historical Flutter sources are intentionally unchanged. Run the new applicator after the complete Build557 generator chain. Source hashes are checked before mutation; repeat application is supported and partial/drifted states are rejected.

Implemented:
- The green global call strip displays elapsed minutes/seconds alongside the call name. Its local ticker uses the retained connected-call start and is disposed with the strip. No periodic network request was added.
- Group chat follows a new tail message, instead of treating reaction/deletion snapshots as new messages. Both chat lists retain stable row keys and compensate for changed message heights using the first fully visible existing row, including a photo whose own reaction height changes. Message search and deliberate user scrolling retain priority.
- The group long-press menu now starts with the same horizontal reaction/reply/copy/reminder/More structure as private chat. Existing sender/admin checks and additional operations remain under More. Opening the first menu no longer waits for a server read.
- Group header loading can use the existing cache and has a bounded retry state; membership gates remain in place.
- Inbox notes occupy a real hit-testable area above the avatar. Tapping shows the entire note; the owner can edit or delete it. No overlap with the avatar ring.
- Community notification names use Turkish uppercase and blue; group names use green. Older group-added text can recover an embedded group name. Missing community titles are resolved once per community per page, through existing access rules. Unread backgrounds are darker.
- Gallery selection accepts multiple photos and videos. Existing normalization, upload functions, private message-request checks, group membership/post restrictions, size limit and private disappearing-message expiry are retained. Album uploads are sequential; more than 100 selected items is rejected explicitly rather than silently truncated. An album is one photo/video-compatible message with `albumItems558` and `mediaUrls`, preserving a valid single-item fallback for older clients (a photo when available, otherwise a video).
- Album previews stack photos; tapping opens a grid, then the existing full-screen photo/video viewers. Single/full-album download buttons report failures and stop saving when their viewer is removed. Revocation uses the existing live message-source wrapper. Album URLs join local cache eviction and the existing tombstone cleanup manifest.
- Profile badge rendering uses account IDs, never display names. Alperen's approved final appearance is a smooth circular blue check with **no crown and no KURUCU text**. The other three checks retain the normal style.

## Account identity still needed

The four actual Firebase UID values were not available in sources or prior context. Release-time `NGELX_FOUNDER_UID` and `NGELX_VERIFIED_UIDS` (three comma-separated IDs) must be provisioned from the real accounts. Defaults award no badges. Extra allowlist IDs are rejected. No production user verification flags were changed or guessed from names.

## Rules compatibility

The paired rules update extends the existing sender/admin tombstone operation to clear both album fields and requires the cleanup manifest to match the old message URLs plus its stored album URL list. It also brings the retained modern rules into agreement with the existing Build435 deletion client. No rules were deployed. The complete generated rule delta passed local emulator sender/admin, outsider, forged-manifest and uncleared-album cases. Production deployment is still pending. Automatic retention and cleanup remain paused; this change does not run them.

## Validation

Passed locally:
- Exact verified Build557 baseline hash match.
- Cold/repeat source patch reproduction and rejection of unrelated source drift before mutation.
- Rules patch idempotence and confinement to the existing chat-message block.
- Python compilation and JavaScript/YAML syntax checks.
- Flutter 3.47.8 / Dart 3.13.7: full application analysis passed with `--no-fatal-infos --no-fatal-warnings` and zero errors. Existing warning/info lint debt remains.
- Fourteen Flutter tests passed across Build551 photo/call regression, Build556/557 community regression and the six new Build558 cases: call time boundaries, exact UID allowlist behavior, malformed album records, real visible-row position after a tall earlier photo shrinks, reaction height changes on the visible photo itself, and narrow-phone group menu actions.
- Local demo-project Firestore emulator tests passed: sender and admin can delete the exact album; outsiders, other members, forged manifests and uncleared album fields are rejected. No production database was used.

The initial local Flutter invocation was automatically rejected after an Azure metadata detector request. Read-only inspection of Flutter's `base/bot_detector.dart` established that the standard `CI=true` environment short-circuits that detector. Validation then completed in CI mode without requesting the metadata endpoint; the denied request itself was not retried. Archive extraction used `TAR_OPTIONS=--no-same-owner` because the container cannot adopt archive owner IDs.

Signed candidate build passed: https://github.com/Nnentx/Ngelx/actions/runs/40040789796 for source commit `9792a4d1d8f5fc7960e538df53f5e0db975460a9`. Downloaded source hashes match the committed Build558 manifest and helper exactly. Both downloaded ZIP digests match GitHub artifact metadata, ZIP integrity and included APK checksum passed. Package is `com.nnentx.ngelx_app`, version `1.0.328`, code `558`; existing signer SHA256 is `be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa`. The ARM64 Flutter app/runtime are present; third-party dependencies also bundle other ABI slices. APK SHA256: `1a52aae2c4460b3ffd227a3a636ad632afa1242578d68b059cafa4197abbf255` (47,505,419 bytes).

No physical-device acceptance claim, production deployment or publication. The four real account UIDs remain unprovisioned.

Remaining device acceptance: reaction and deletion while viewing a tall photo, navigating away/back during a long call, mixed albums, revoked media, interrupted upload/download, group cache/retry recovery, note hit targets, and actual account ID provisioning. General intermittent startup slowness still requires device profiling; these changes remove identified unnecessary menu reads/scroll work without claiming every performance issue is resolved.

## Alperen account provisioning

User supplied `https://ngelxsocial.com/?profile=PFBjMyxkGTW4MIZRevxalZ4Ax0h1`. The founder UID default is now bound to this exact account. Other three IDs remain unprovisioned. This source update is newer than the APK linked above; the installed Build558 APK does not gain the badge automatically. No user database flags were changed.

Yılmaz supplied account: `https://ngelxsocial.com/?profile=ImCp8w8HDGMyu8LuQQtQhPdpA9A2`. Verified UID defaults now contain this exact account; Ahsen and Rızgar remain pending. Explicit lists may contain up to three known non-founder IDs; more IDs fail closed, and unknown accounts still get no badge.

Rızgar Umut supplied account: `https://ngelxsocial.com/?profile=ckqq26wzJEg7FsGSSCzq1U2BnLo1`. Added to the exact verified UID defaults. Only Ahsen Can remains pending.

Ahsen Can supplied account: `https://ngelxsocial.com/?profile=ppIxuCf4QjMEALdoCtaAlR3tjzF3`. All four exact account defaults are now provisioned in source. The previously delivered APK predates these defaults.

## Newly reported device feedback — pending implementation

- Following list: last rows overlap Android bottom navigation; respect bottom system inset and keep the final row fully reachable (50536.jpg).
- Verification email: replace generic project-ID branding with NgelX, Turkish subject/body, branded layout, prominent accessible verification button, expiry/error/retry explanations and a fallback link. Use a recognizable sender display name; explain automated replies are not monitored. Current screenshot shows a Firebase default English template in Spam; changing appearance alone must not be claimed to fix spam delivery. Sender configuration and delivery require separate checks. Do not open or record the uploaded one-time verification URL.
- In-app verification screen: clearly distinguish pending/verified/error states, provide resend with cooldown, wrong-address correction and an understandable expired-link flow. These are proposed refinements, not completed changes.
- User requirement: username and full name must not change again before three months have elapsed. Enforce each field's last-change timestamp on the server, not only the client; show the next eligible date before save. Define calendar-month boundaries consistently. Normal editing must not reset the clock without changing the field. Initial profile completion remains distinct from later changes.
- Suggestions for review: display the pending new name and next eligible date before confirmation; provide a controlled support path for genuine spelling mistakes/account recovery. No automatic exceptions or server policy changes have been deployed.

## Additional photo feedback — pending implementation

- 50542.jpg: after sending a photo or album finishes and its final height settles, the new message can remain partially outside the viewport until the sender scrolls. Keep the sender's just-sent media fully visible after final layout when the user is following the latest messages. Do not pull users away from older messages they are reading, or reintroduce reaction/delete jumps.
- 50543.jpg: opened album grid's final row overlaps Android system navigation. Apply the bottom system safe inset and enough scroll padding so the last photo is fully visible and tappable. Check full-screen photo viewer controls too. These reports are recorded, not yet fixed.

## Mention feedback — pending implementation

- 50544.jpg: typing Rizgar in the group composer does not offer a mention. User requests @ to open user suggestions and @herkes/everyone support. In group context, list current group members; filter by both display name and username, including Turkish case/diacritic variants (Rizgar/Rızgar). Clarify broader cross-app discovery if later requested rather than exposing unrelated private accounts.
- Suggestions for review: show avatar, display name and unique username; selection inserts a UID-bound mention; distinguish duplicate names, style mention text and open the correct profile on tap. Show empty/loading states and keep suggestions above the keyboard/system inset. Mention notifications should follow membership and existing notification rules.
- Proposed @herkes guard: group admins only with a short cooldown to avoid notification spam. This restriction is a suggestion, not a user-approved policy or an implemented feature.
