# Build580 Ludo feedback — local review candidate

Base: `e7f3fc049ee83d3808d674ef768a42ab5f9c949e` on `feat/build575-ludo-auto-premium-rewards`. Application input is the exact Build579 assembled source from CI `40386052388`, artifact `12681277811`. The historical checked-in `app/` baseline is not replaced in the commit; `tools/apply_build580_ludo.py` applies bounded changes to that verified input.

## Implemented in the candidate

- Queue Auto toggles during mutations, retain the latest desired state, retry revision conflicts for this idempotent toggle, and keep manual moves unreplayed. Enlarge the Auto button and show “Kapat” when enabled.
- Validate wallet/reward/catalog responses independently of room identity. This addresses the actual Puanlarım/daily/chest FormatException.
- Enforce mute at the audio-effect player, cancel timers and in-flight loading playback, and prevent late preference restoration from overriding a user press.
- Permit the host to start a four-seat free-for-all with two or three players. Complete four-player teams and automatic matchmaking rules remain required.
- Larger waiting panel, avatars, names and readable spaced room code; responsive equal-width player slots. The copied code contains no added whitespace.
- Correct pawn base-center anchoring from bitmap-bottom anchoring. Increase movement timing from 160 to 190ms per cell while retaining immediate input dispatch.
- Reuse sprite repaint boundaries during movement, suppress unchanged poll rebuilds, and remove a redundant wallet-read on sync.
- Show all players' server-derived levels, not only the requester's level.
- Add four-second full-screen winner animation with animated confetti and large name, then reveal existing results.
- New invitation capability: authenticated server creation, two-minute server deadline, status view and atomic room join/acceptance. Expired invitation cannot be joined. A duplicate acceptance by the same recipient does not join twice. The original room code paths remain supported.
- Messenger-reference invitation layout: large sender image with branded fallback, light card, game title and broad Join button, status and countdown. New invites are created when the user sends, not when they open the picker. Existing chat send/permission flows remain in place.
- White recipient picker, Turkish-aware person/group search, profile and group photos, cached profile results, SafeArea and scroll padding above system navigation.
- Existing Build579 painter-loop freeze and reconnect/error classification fixes are retained.

## Kamuflaj scope limitation

The current source contains only `control`, `double`, and `shield` powers; no separate camouflage power exists. This candidate adds a pickup receipt for these powers and a visible shield badge when shield protection is active. It does not invent a new camouflage mechanic. If the reported item refers to something else, its identity still needs clarification.

## Verification

- **149 backend/Worker tests passed**, including expiry at precisely two minutes, simultaneous invitation acceptance, retry idempotency, early starts and opponent levels.
- Dart parser/formatter accepted changed source and test files. The exact-source patch was applied successfully and rerun to verify repeat application guards.
- Complete Flutter analysis, widget tests, screenshots, Android compilation and physical-phone acceptance are **pending**. Local pub.dev access was blocked, so Flutter packages could not be resolved.
- A QA-only Actions workflow is prepared to restore the verified source, analyze and test the complete app, produce previews and build/sign a review APK with the original signing fingerprint. No successful CI or APK build is claimed.

## Publication state

Changes are committed locally on `qa/ludo-feedback-20261026`. Automated approval review rejected the GitHub push because publishing code/workflows to the public repository was not sufficiently authorized by the implementation request. No connector workaround was attempted. GitHub upload, PR creation and CI execution await explicit user approval.

No main-branch merge, production Firebase write, Worker deployment, public APK release or updater switch was performed. Backend changes must be tested and deployed before the new invitation protocol can be used by an installed client.
