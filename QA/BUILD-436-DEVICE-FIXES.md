# Build436 / 1.0.211

## Device failures consolidated

- Friend and private follow request failures: 45738, 45741, 45745, 45746. Canonical requests remain authoritative. Stage deployed request rules and validate sender creation, recipient reads, and blocked rejection before deployment. Canonical and exact production rule emulator validation passed; device retest pending.
- Info friend button: 45761, 45777. Guard blocked pairs and report exceptions instead of false pending/friends status.
- Nickname: 45758–45760. Store nested participant map, edit selected peer, update chat/info headers, persistent system event.
- Solid color with existing wallpaper: 45763–45764. Clear shared and legacy participant wallpaper fields; retain camera/gallery upload.
- Blocked info presence/friend/theme edits: 45775–45778. Hide controls/presence, recheck server before actions; server rule denies shared writes and system events.
- Repeated block: 45779–45780. Idempotent block helper and live unblock info action.
- Delete everyone: 45743, 45800–45801. Preserve null source values in immutable cleanup manifest; distinguish permission/quota/transient errors; permanent failures leave retry queue. Private/group tombstones stay in place. Device verification pending.
- Intro over35 MB: 45755. Compress oversized input without deleting original, validate final size before upload and show readable failure. Valid small and compressed device checks pending.
- Profile/messages/friends activity: friend OR follow OR mutual message history, privacy and both block directions honored.

## Passed and protected

Public direct follow/counter; incoming message request/count/accept; two-way text/photo/reactions; Benden sil; activity privacy off/on; camera/gallery shared wallpaper; profile biography/cover; block communication UI on both sides; privacy unblock and resumed messaging; restrict/unrestrict/resumed messaging. Restriction label issue withdrawn after 45790–45791.

Voice call delivery/accept/timer/resume banner passed. Actual two-device sound not verified. Long stories/retry/correct story, archive, profile search/speed accepted by user; do not reopen.

Backend cleanup live verification remains deferred by Firestore quota429. No automatic production retention enabled in this change.

## Build436 verification

Actions 38081602455, commit f2d204c25e94d3cff7447328d06f32d741b3897d: Build395–435 generation and preservation checks, Flutter analysis and behavior tests, canonical Firestore emulator checks, and the exact production patch emulator checks passed. The exact tested scoped production rules deployed. Signed APK generation passed. 30 Flutter behavior tests and 26 cleanup tests passed. Local APK manifest confirms 1.0.211+436 and com.nnentx.ngelx_app; compiled Build436 guards and Build435 cleanup classes are present. APK SHA256: 42dd5c8f2bf5299ef333266e7665329a7c3a86a6eb2fd0b43f531a49505de8d3. Artifact ZIP hash matched GitHub digest; APK hash matched its build-generated manifest. Signing certificate SHA256: be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa.

The emulator exposed a metadata-only private chat update path that bypassed the first block check. Build436 now gates every private chat update branch before evaluating the existing permissions. Group permissions retain their existing behavior.

## Two-account acceptance order

1. Unblocked: send friend and private-follow requests; confirm one pending record, recipient notification and accept/cancel state.
2. Change the other participant's nickname; both accounts see the changed header and actor-named system event. Remove nickname and verify the original name returns.
3. Choose a solid color while a custom photo is active; both accounts see the color. Camera and gallery wallpaper remain available.
4. Block the peer, switch accounts: shared nickname/background changes and new requests are denied; activity hidden; message/call composer remains closed. Already-blocked account shows unblock action.
5. Unblock via privacy and verify messaging resumes. Restrict/unrestrict remains user-passed.
6. Delete text, photo and video for everyone in private and group chats: sender sees “Bu mesajı sildin”, others see “Bu mesaj silindi” in the original position. Benden sil only hides the caller's view. No false connection-retry message for a permission rejection.
7. Upload a valid small intro and an oversized compressible intro. Confirm preserved original, final size limit, preview and readable failure.
8. Check activity in profile, chat and friends with friend/follow/mutual-chat eligibility, privacy off/on and both block directions.

None of these new device checks is marked passed merely because automated checks passed.
