# Build436 / 1.0.211

## Device failures consolidated

- Friend and private follow request failures: 45738, 45741, 45745, 45746. Canonical requests remain authoritative. Stage deployed request rules and validate sender creation, recipient reads, and blocked rejection before deployment. Production exception diagnosis pending CI/device verification.
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
