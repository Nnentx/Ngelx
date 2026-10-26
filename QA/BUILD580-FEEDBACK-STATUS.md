# Build580 Ludo feedback — verified review APK

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

- Tested source commit: `e04d8e99aea63ede3802b282ff4688062245f965`.
- [QA run 40401696200](https://github.com/Nnentx/Ngelx/actions/runs/40401696200): **success**.
- **149 backend/Worker tests and 34 Flutter tests passed**, including expiry at two minutes, simultaneous invitation acceptance, retry idempotency, early starts, opponent levels, queued Auto cancellation, room paint/Back regressions, narrow waiting panels, recipient search, bottom insets and four-second celebration.
- Complete Flutter app analysis passed with the repository's existing non-fatal warning policy. The exact-source patch applied successfully and reran with its guards.
- Four actual Flutter render previews were generated and visually inspected. An Auto-label overflow and unnecessarily stretched invite card were corrected before the final passing run.
- Release ARM64 APK compiled successfully. Original application signing fingerprint was verified by apksigner: `be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa`.
- Downloaded artifact ZIP digest matched GitHub; APK CRC/content scan passed, required ARM64 Flutter library and assets are present, and Google demo ad IDs are absent.
- Actual binary Android manifest: `com.nnentx.ngelx_app`, version `1.0.350`, versionCode `580`.
- APK: `NgelX-1.0.350-Build580-REVIEW.apk`, **49,482,280 bytes**.
- APK SHA-256: `7743cdf5090d52b7472d89e934c4df3e910d1bef0e698c4a59e25d13a78d23e0` (matches CI build output).
- Two physical phones have not been tested. Actual audio muting, animation smoothness and end-to-end multiplayer acceptance remain physical-device checks.

## Publication state

The user explicitly approved uploading to the QA branch and running APK tests. Changes are uploaded to `qa/ludo-feedback-20261026`; [PR #191](https://github.com/Nnentx/Ngelx/pull/191) is a draft review against the existing Build579 development branch.

The review APK is prepared and saved. No main-branch merge, production Firebase write, Worker deployment, public APK release or updater switch was performed. The new invitation protocol, early starts and complete opponent-level responses require the matching backend changes to be deployed before live acceptance. This is a review build, not a production release.
