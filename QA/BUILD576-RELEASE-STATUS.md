# Build576 release status — 26 October 2026

The signed review APK is ready: 1.0.346 / build 576, 48,747,540 bytes, SHA-256 `37c338b83bc290e3b7193e94f1153a0a6db253622695225a47dc4295f80cc96f`. Android review run [40352800633](https://github.com/Nnentx/Ngelx/actions/runs/40352800633) passed analysis, widget tests, original signing certificate, package/ABI/content/demo-ad exclusion verification and separate optional SDK smoke. Runtime code is unchanged from that tested app/Worker source; later commits add acceptance tooling.

## Completed live validation

- Isolated Cloudflare + real Firebase acceptance: [40359911230](https://github.com/Nnentx/Ngelx/actions/runs/40359911230), repeated successfully with Auto-aware acceptance in [40361587536](https://github.com/Nnentx/Ngelx/actions/runs/40361587536).
- Production Worker deployment + authenticated acceptance: [40361587627](https://github.com/Nnentx/Ngelx/actions/runs/40361587627), source `864b5fe7c56d56d254a691a80afb5205f59f1d09`, deployed Worker version `56b7ec38-cea7-4191-8b08-9f5f67df970c`.
- Both `oyun.ngelxsocial.com` and the direct Worker hostname return HTTP 200, core features preserved, `ludo575.configured:true`. Backend retains its compatibility version marker 575; Build576 adds the verified starter grant.
- Concurrent 5,000-chip creation credited once; atomic paid gifts/duplicate retry, received collection, block/unblock, daily/chest idempotency, two-account move, four authenticated accounts, classic/team rooms, Auto on/off and normal-user moderator rejection passed against real Firestore.
- Temporary QA accounts, wallets, room documents, rate-limit records and staging Worker removed.
- Seven deployment-guard tests pass. Two earlier acceptance failures restored the checkpoint successfully: the first caught a stale game-domain response immediately after deployment; the second caught an acceptance harness that tried to roll after Auto had already rolled. Both hostname convergence and consuming an existing die are now required.

## Pending release gates — not assumed complete

- Two real Android phones: in-place update without deleting the app, visual acceptance of pawns, audible dice/steps/capture/end effects, persisted mute, multiplayer/Auto/reconnect and the existing full device checklist.
- Real moderator allowlist/operation ownership remains unset. Moderator API is closed to ordinary users; no moderator permission was invented or granted.
- Rewarded ads remain disabled in both the APK and production release decision; no demo ad IDs were published and no live AdMob setup is claimed.

## Updater preparation

`QA/BUILD576-UPDATE-CANDIDATE.json` records the exact APK metadata for review. Its release URL is a proposed destination, not a published asset. It is not the live updater feed. Do not copy it into the website before device acceptance and publication/download-byte verification.

`Nnentx/ngelx-web/android-update.json` was re-read and remains Build574 (`1.0.344`, blob `a0ed55685e959c3da4c2271122c3fc40debcf351`). No APK was added to the application-wide updater. The user has authorized publication after completion; no additional permission request is needed once the actual release gates are satisfied. Never mark physical-device checks complete from CI/API success.
