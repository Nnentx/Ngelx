# Build588 — published status

Build588 (1.0.358) is published. The live Worker, scoped Firestore rule changes, public APK, NgelXSocial download links and in-app manifest are updated.

Implemented:
- Profile photo for camera-off preparation and live broadcast.
- Black audio-room stage with round avatars, speaking rings and moderator/host labels; nine places for new rooms while legacy participants remain visible.
- Multiple matching heart/teddy/other gift particles, bounded rendering and reduced-motion support.
- Cat and tiger catalog entries with transparent generated artwork, local animal/space audio and a sound switch.
- Live moderator timed comment mute and RTC guest controls; peer/host protection and server adapter revalidation.
- Transactional PK result and persistent WIN series: win increments, loss resets, draw/early cancellation preserves. Repeated and concurrent settlement cannot increment twice.

Validation:
- 219 server tests; full Flutter analysis; existing/new widget and interaction tests; signed arm64 APK with the existing app certificate.
- Exact APK/source QA: https://github.com/Nnentx/Ngelx/actions/runs/41358497846
- Accepted Worker and scoped current-production rules: https://github.com/Nnentx/Ngelx/actions/runs/41359532044
- Actual two-account production PK smoke: common winner, single WIN increment, idempotent retry, readable server statistics and forbidden client statistic writes. Temporary records and accounts removed.
- Live website, canonical/cache-busted manifest and anonymous APK bytes: https://github.com/Nnentx/ngelx-web/actions/runs/41360231258
- Public release: https://github.com/Nnentx/Ngelx/releases/tag/v1.0.358-build588

APK SHA256: 852185e6ed679079c07a54444cc2aff76a58056aeee81c6df09849f36c36a730
APK size: 50872938 bytes.
Tested source: f99ff01dc298102ce5e285f93144fb11edaa631d.

Deployment preserved all unrelated current-production rules and website assets. The updater is served from Nnentx/ngelx-web on GitHub Pages. The initial obsolete Firebase Hosting route was corrected without modifying website hosting assets.

Physical Android visual/audio/performance acceptance remains for the user's device. Gift animals use animated 2D cutouts, not rigged 3D walking or mouth animation. Scored WIN settlement applies to video-live PK; the existing separate audio-room PK audio-link flow is retained.
