# Build556 — verified Android candidate

**Final candidate passed:** https://github.com/Nnentx/Ngelx/actions/runs/40002670349

Source commit: `056c96eebd0d44df924a081ae419ab11371ca060`.
APK: `NgelX-1.0.326-Build556.apk`, 47,475,675 bytes.
APK SHA256: `f124af2aa4c6ffe3419bcdf35d2c106d5f8decabab86b223550b14ab75d87ba6`.
Android package: `com.nnentx.ngelx_app`; versionCode `556`, versionName `1.0.326`.
Signer SHA256: `be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa`, matching the existing updater.

The APK was downloaded from artifact `12524215088`; its archive SHA256 was checked against GitHub's digest, then the APK checksum and ZIP/native-library integrity were verified independently. Source artifact `12523028792` matched every changed source hash and all three helper files. Package, version and signer evidence in that source artifact were also verified. No automatic installation on the owner's phone was performed.

## Changes

| Owner feedback | Delivered change |
| --- | --- |
| Inbox action menu overflows navigation | Scrollable full-height sheet with Android safe area. |
| Mute, microphone, speaker and voice calls | Existing audio controls and preference checks preserved; push/admission/lifecycle regressions passed. Audible operation still requires two phones. |
| Rear camera unavailable after enabling voice-call video | Camera-switch action appears with a local track in private/group voice calls. Toggle/flip operations are serialized; chosen direction persists across capture restart and RTC reconnect. |
| Ayaz / `@herkes` mentions | Immediate command suggestion, Turkish case folding, full member suggestions and retry instead of permanently caching failed profile reads. Existing mention permissions remain enforced. |
| Pending friend requests reappear after update | Scoped legacy pending requests supplement canonical requests only when no canonical record exists; canonical cancellation/acceptance takes precedence. |
| Community deletion fails | `/community/delete` deployed on the existing Worker. Founder/current-membership and exact-name confirmation, verified non-anonymous Firebase identity, revoked-token rejection, server-owned receipt/lease, bounded recursive cleanup and same-owner resumption. The root becomes an inaccessible tombstone until descendants and matching invitation records drain; root deletion and completion receipt commit atomically. Foreign users/chats/media/invites are never deletion targets. |
| Comment counter remains zero | Refresh after comment creation/deletion and closing the comments panel. |
| Community notifications | Approved posts, pending posts, membership requests and comments emit existing Activity notifications with community name and small “Topluluk” label; taps open the community. Existing notification/privacy preferences remain authoritative. |
| Share inside NgelX | Picker includes private/group conversations. Atomic sends check current membership, private-community audience, block/privacy and admin-only posting; message expiry is preserved. Stable per-chat message IDs prevent duplicate retries; shared cards open the community. |
| Manual community refresh | Pull-to-refresh fetches current community/approved-post data and renews the live feed; empty feeds remain scrollable. |
| Community create/admin design | Cover/avatar preview, ordered information/privacy sections, live pending badges, aligned admin rows and responsive editable information dialog. |
| Intermittent gray community blocks | Hardened missing author fields and invalid legacy timestamps, plus refresh recovery. The exact intermittent device exception has not been reproduced; resolution must not be claimed from source checks alone. |
| Intro video sound overlay | Floating speaker icon removed; existing playback controls retained. |
| Highlights invisible to visitors / removal | Visitor highlight list uses the existing profile-access gate plus individual story privacy/hidden-audience checks; live queries remove deleted or unhighlighted stories. |
| Chats open at old messages | Opening scroll waits for nonempty data, tolerates slower layout, stops on history interaction and respects explicit message jumps. |

## Validation

- 104 server authentication, moderation, push and deletion tests passed, including real adapter simulations for nested/missing ancestors, interruption, lease contention, scoped invitation deletion and recreated community IDs.
- 12 standalone Dart mention/highlight-policy checks passed.
- The real patch passed cold application, repeated application, exact source hashes and rejection before mutation on unrelated source drift.
- Three new Flutter tests passed: narrow phone/large text, bounded media preview, and immediate Save eligibility after editing a name.
- The inherited Build395–554 regression chain passed; full regenerated Flutter analysis passed.
- Signed ARM64-capable Android APK build, package/version checks, signer check and native-library/ZIP checks passed.
- Existing Worker deployment passed. Live health reported `community_delete556`; anonymous deletion was rejected with HTTP 401. No real community was deleted merely to test the service, and no billing/subscription/secret changes were made.

Local Flutter invocation was blocked by automatic review because it attempted metadata access. Compilation and tests were completed in the established GitHub environment instead.

## Source integrity and integration

The raw repository app is an older baseline assembled by the historical source-generation pipeline. Build556 must be applied **after all existing Build395–554 generation steps**, not directly to the raw checkout.

The first Build556 guard correctly rejected an incomplete local reconstruction. The package was rebased onto the successful Build555 assembled-source artifact `12438123276` (archive SHA256 `9a6c519e7cfed5bc917a8f8a5258291bed32baa095d83a9671f4d1fe11a85a3b`, main source SHA256 `9b73e7676efb548698b4502017323b56f46c5cc0297115ffd66dd2bb8860fec9`). All Build552–554 application behavior is retained. The final CI run verified the corrected exact baseline and package successfully.

`tools/apply_build556_quality.py` applies only the guarded deltas and copies the three Build556 helper files. `tools/test_build556_quality.py` verifies reproduction and drift protection. `.github/workflows/NgelX-BUILD556-QUALITY.yml` retains the earlier generation/signing checks and gates the build on tests and verification of the already-running Worker. Source artifact `12523381061` preserves the exact baseline for diagnostics. Production Firestore rules, retention/cleanup pauses, websites and stored account data are unchanged by this package.

## Physical acceptance still needed

Use two existing accounts/phones to verify actual microphone mute, speaker routing, ringing, front/back video, friend-request state after update, mention delivery, notification delivery, highlight visibility/deletion and initial chat position. Repeat the community-screen navigation that produced the gray blocks and capture its Flutter exception if it recurs. Confirm deletion from the updated app only on an owner-created disposable test community, including a retry after interruption.

Scheduled or subsequently moderator-approved post notifications depend on the existing server-trigger deployment and remain a separate backend follow-up. Neither the successful APK build nor the unauthenticated endpoint probe substitutes for these device checks.
