# Build455 consolidated follow-up

Target: v1.0.230 / Build455. Base: verified Build454 plus device QA through 47219.mp4.

Implemented candidate source, not yet accepted on physical devices:
- Resolve blank/brand profile name fields; fix inbox nickname lookup to the other member; subscribe private-chat header name/photo to current profile.
- Close old account's locally owned call/audio sessions on auth change; validate notification answer from server and recheck account.
- Bound video initialization waits; show synchronization rather than a premature empty inbox.
- Community-wide white visual foundations for fonts, fields, buttons, chips and dialogs; larger metadata and action labels; creation preview includes selected cover/avatar.
- Separate comment blocks with avatar, clear name/date, profile opening, owner/admin deletion confirmation, threaded replies and reply counts.
- Comment and post reactions with valid emoji selection and real per-user reaction records; real like/comment counts.
- Compact colorful upload status and success notifications; retain real percentage/MB stages.
- Post sharing includes the actual media URL and post identity instead of only the community identity.
- Additive bounded comment/reaction security rules; verify live production baseline before changing only these blocks.

Validation pending: Flutter identity tests, existing layout/behavior regressions, Firestore security tests, release APK signing/version verification and production rules read-back. Build workflow `.github/workflows/NgelX-BUILD455-CONSOLIDATED.yml` is active.

Physical-device acceptance remains mandatory for ringing, two-way group audio/participant joining, feed play/pause and perceived performance. No claim these are fully fixed yet. View and share counts now use one real event document per authenticated account. Views require at least two seconds with at least half the post viewport visible and the route foreground/current. Shares record only platform-confirmed success; counts are labeled unique viewers/sharers. Cancelled or unconfirmed shares do not increment.

Source replay: run existing Build454 chain and patch first, then `python3 tools/apply_build455.py` and `python3 tools/apply_build455_rules.py`. Durable code is the new widget part, replay scripts, workflow and tests in this branch; generated scratch worktree is not the source of truth.
