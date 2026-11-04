# Build592 — published and verified

NgelX 1.0.362 / Build592 is published. The live Ludo backend, NgelXSocial download links and in-app update manifest are updated.

Implemented:
- One shared four-seat invitation admits the third and fourth participants; the fourth join starts classic/team play automatically.
- Four-seat rolls use equal six-face cycles for every seat, including bots. Remaining faces stay server-private.
- Manual pawn input does not wait for background polling; stale polls cannot replace newer moves. Pending-roll taps are queued once and legal moves retry revision-only conflicts with the same receipt. Pawn animations are faster.
- Sixteen illustrated offline gifts, rooster crow, balloon animation, tomato splat, two-second full-screen fire and water pouring/splash effects. Mute, backgrounding and disposal stop sound playback.
- Nefes exact-UID blue badge and the Build590 audio-room layout are preserved.

Verified:
- 234 backend tests and 28 Flutter tests; Flutter analysis; signing certificate matches be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa.
- QA source: 1e00f001567a1dd0d9cb46e965f050f8ab6fc872.
- QA: https://github.com/Nnentx/Ngelx/actions/runs/41806779588
- Seven deployment guard tests; checkpoint and conditional rollback retain the prior production runtime if live acceptance fails.
- Four real temporary accounts joined the same invitation, including concurrent third/fourth joins. Automatic classic/team start, manual two-seat start, accepted pawn moves, 1–6 once in the first six rolls of every seat, private roll state and single gift charge on retry passed live.
- Temporary accounts, rooms, invitation, wallets, presence and rate-limit fixtures were removed.
- Backend/release: https://github.com/Nnentx/Ngelx/actions/runs/41808409559
- Release: https://github.com/Nnentx/Ngelx/releases/tag/v1.0.362-build592
- APK: 52745408 bytes; SHA256 1b3d233945f1a78af5f2ba6d3c92fe995e348915259ef3c246a0fa532fc52482.
- Assembled source ZIP SHA256: c2a95d7b108e3551429bed40fd19d9e2e1bdb720a3661449b20a299bcfd57a60.
- Website source: 8926aafb8f3734abc17a7b2984276cae1f9817ca.
- Pages deployment: https://github.com/Nnentx/ngelx-web/actions/runs/41808663479
- Public website links, canonical and cache-busted updater manifests, and anonymous APK bytes: https://github.com/Nnentx/ngelx-web/actions/runs/41808664044 (success).
- Saved APK: NgelX-1.0.362-Build592.apk, libfile_4aa48d4095c88191a9ae5682e49bc91c.

Boundary: physical Android audio/performance validation was not performed. No database permission rules were changed.
