# Build589 — published status

Build589 (1.0.359) is published. The live Worker, immutable APK, NgelXSocial website links and in-app updater are updated.

Implemented:
- PK reads historical reaction totals and projected gift points at the server start and deadline. Last-second gifts count; later gifts cannot change the result.
- Historical reads are shared across transaction retries. Concurrent finish requests still update WIN exactly once.
- Early 409/not_finished responses retry after one second without a failure notification.
- Gift playback rechecks mute/disposal state after loading and volume setup.
- Actual circular audio-room seats are isolated for rendering and interaction tests.

Verified:
- 230 Node tests; Firestore emulator permission boundaries; actual private historical Firestore fixtures. Fixtures were removed.
- Flutter analysis and widget/interaction tests passed.
- Rendered nine actual seats at 360x640 and 393x852 with text scale 1.6; screenshots inspected. Empty-seat taps fire once and large text does not overflow.
- Exact application QA: https://github.com/Nnentx/Ngelx/actions/runs/41403709092
- Tested source: d0bb555c2679405ea03c8ad8d0c414d7fc6d109f.
- Review PR: https://github.com/Nnentx/Ngelx/pull/201

Published and verified:
- Signed arm64 APK matches the existing certificate be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa.
- 25 Flutter tests passed. APK size: 50871498 bytes. SHA256: ac12bcad83e4d25d671eadbb5e3b523e9f94764e960f00dd25a051d97dab4c27.
- Accepted backend: https://github.com/Nnentx/Ngelx/actions/runs/41405178995 (operations source 67dd885d5e0b3ea0735e84de0b8af3febecae8df).
- Real two-account PK: stale room counters ignored, last-second gift determines winner, late gift excluded, concurrent finish increments WIN once. Temporary accounts/documents removed.
- APK/source release: https://github.com/Nnentx/Ngelx/releases/tag/v1.0.359-build589
- Publication: https://github.com/Nnentx/Ngelx/actions/runs/41405309049
- Website, canonical/cache-busted manifest and anonymous APK bytes: https://github.com/Nnentx/ngelx-web/actions/runs/41405375067
- Pages deployment: https://github.com/Nnentx/ngelx-web/actions/runs/41405374825
- Saved APK: libfile_36595aa570208191a86b52b4ba78edd2, NgelX-1.0.359-Build589.apk.
- Assembled source ZIP SHA256: 7882a966375a5b88a0a3e729623971212e63167e1d6183b90ca9e4e473201f91.

The first backend acceptance attempt stopped at a noninteractive unzip overwrite prompt. Its guarded rollback restored the exact prior Worker; the configuration step was moved before deployment and corrected. The accepted follow-up run above passed all checks. No production Firestore rule changes were made.

Boundaries: no Firestore permission/rule changes in this build. Gift snapshot reads project points through the existing single-field kind index; snapshots above 20,000 gift documents fail closed. Composite-index administration was denied before any index was created. Physical Android visual/audio/performance validation remains outstanding. Existing animated 2D gift artwork and the separate audio-room PK audio-link flow are retained from Build588.
