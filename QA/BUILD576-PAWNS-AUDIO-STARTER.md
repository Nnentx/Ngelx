# Build576 review — rounded pawns, game audio, starter chips

User requested preserving the existing NgelX structure, improving Ludo pawns to the supplied Messenger reference, giving new players 5,000 free chips and adding game audio with persistent mute. Publishing the updater is the final step, after release validation.

Changes:
- Rounded vector pawns with a spherical head, wider body, highlights and contact shadow at any board resolution. Board geometry, stack offsets, navigation and other app screens are retained.
- Original synthesized bundled WAVs for dice, movement steps, captures and match completion, played through existing just_audio. Server state changes drive effects for local, remote, bot and Auto actions. Repeated dice values have separate server roll revisions. Sound preference persists, mute cancels pending steps, lifecycle pause and disposal stop playback. These are original effects, not copied Messenger audio.
- Authenticated new wallet creation grants 5,000 chips in a single create-only Firestore CAS operation. Concurrent requests/reconnects cannot regrant. Existing wallets are preserved without resetting balance or receipts. No client-supplied balance or public credit endpoint.
- Android version 1.0.346 / build 576, retaining the existing signing certificate and APK verification gates.

Validation before CI: 136/136 backend/Worker tests; six APK verifier unit tests; additive patch applied successfully to the downloaded verified Build574 source; frontend structure checks pass. CI must additionally analyze Flutter, run widget tests, build/sign/inspect APK, and bundle Worker.

Release remains gated by the Build575 runbook: live Worker/Firebase and compatibility checks, two real Android phones, update/install and sound quality checks, operational moderation and explicit AdMob enabled/disabled decision. No update manifest or production deployment changed in this commit. Previous release remains available. Physical-device audio audibility and the requested visual quality require user acceptance of the new APK.
