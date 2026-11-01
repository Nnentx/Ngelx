# Build588 live rooms and gifts

Based on the exact published Build587 assembled source (SHA256 47b2c9291e6a3aed3eae9da030ee34b380998bdfc8ac4b47a02cb139195ad715).

Implemented for review:
- Profile photo for camera-off preparation and live broadcast; guest/PK tiles keep their existing profile-photo fallback.
- Black audio-room stage, round avatar seats, speaking ring, names and moderator/host roles. Nine seats for new rooms; legacy participants remain visible.
- Matching multi-particle heart/teddy/other gift flows, bounded particle count, reduced-motion support.
- Cat and tiger catalog entries, transparent generated images, local animal sounds, synthetic space effect, gift-sound switch. All sounds serialized by the existing confirmed-event queue.
- Timed comment mute for live moderators, moderator RTC guest controls, target protection and adapter revalidation. Audio-room participant rules restrict moderator role escalation and host targeting.
- Server transaction for PK ending, results, persistent WIN streaks, exactly-once settlement. Win increments, loss resets, draw and early cancellation preserve streak. Active sessions display current WIN. Reject stale sessions to protect a later match.

Validation:
- Targeted PK/moderation server tests passed locally; broader regression result recorded in the conversation.
- Dart parser/formatter completed for changed Dart files.
- Flutter setup was stopped by automatic approval review because a local Flutter process attempted access to cloud-instance metadata. It was not retried. Full analyzer, widget tests and signed APK build are delegated to the isolated GitHub QA workflow.

Not yet production verified:
- This branch has not deployed the Worker or Firestore rules. PK finishing and new role/catalog permissions require those deployments before release.
- Gift characters currently use animated 2D cutouts (translation/scale/glow), not rigged walking or lip-synced 3D models. Existing lion/galaxy art is retained.
- Audio-room PK retains its existing invitation/audio-link implementation; persistent scored WIN settlement in this branch applies to video live PK.
- End-to-end two-device, reconnection, audio mixing, device performance and TikTok-reference visual acceptance remain required. No in-app update feed is changed by this review workflow.
