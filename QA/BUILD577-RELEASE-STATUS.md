# Build577 signed review — 26 October 2026

Build576's pawn appearance was rejected by the user. Build577 replaces gameplay's cone-like vector rendering with the original transparent glossy 3D asset at `tools/assets/ludo577_pawns.png`, retaining natural proportions through explicit alpha bounds. The new asset has a rounded pear body, short neck and thin oval rim. Board geometry, existing screens, game sounds and one-time server-side starter chips are retained.

## Final validated APK

- Version **1.0.347 / Build577**, package `com.nnentx.ngelx_app`, ARM64-capable, same existing signing certificate.
- [CI 40373345638](https://github.com/Nnentx/Ngelx/actions/runs/40373345638) **success**, tested app source `c48b08d44c993c0d9d0031c6e290b8520f6d3e6e`.
- **136/136 backend/Worker tests**, Flutter analyze, **17 Flutter tests**, six APK-verifier unit tests and separate optional AdMob SDK smoke passed.
- [NgelX-Build577-Review-APK](https://github.com/Nnentx/Ngelx/actions/runs/40373345638/artifacts/12673767877): **49,461,560 bytes**, SHA-256 `822791be8bf4540f6c7dda0425460c129e98b34556eb75a9caa87ab3be6ca8ae`.
- Downloaded APK digest independently matches CI. ZIP integrity checked. APK entry `assets/flutter_assets/assets/ludo577_pawns.png` is byte-for-byte equal to the selected repository asset: **713,587 bytes**, SHA-256 `9cd7855352a6128a9ddb7ccdfc2a9bb92527a7c5661817a25926f4cb0a341cbb`.
- [Real Flutter sprite captures](https://github.com/Nnentx/Ngelx/actions/runs/40373345638/artifacts/12674150696) at **28/44/80 logical pixels** were inspected. This is actual production SpritePainter output and has real alpha transparency. It is not a full application screenshot or user approval.

## Departure changes and validation limits

Both stages of the delayed one-legal-piece move respect the departure dialog's `_asking` flag. Leave retries are bounded at four, keep one idempotency key and sync after revision conflicts. Controller regressions pass for repeated conflicts and for exhaustion that must retain a genuine error rather than fabricate a successful departure. Already decoded pawn images are reused directly, avoiding redundant async redraws.

New whole-room/table/painter-composition screenshot harness attempts timed out. They were not counted as passes; those additional integration captures were withdrawn in favor of focused production-sprite rendering plus existing widget/geometry checks and departure-controller tests. Do not infer that full in-game layout or the actual leave dialog was verified from CI. Real Android checks remain necessary.

## Publication

This is a signed manual review APK, not the application-wide update. The Build576-era live Worker remains deployed and validated by run 40361587627; no Worker deployment or live update manifest change occurred for this visual correction. `QA/BUILD576-UPDATE-CANDIDATE.json` is historical, not a Build577 release manifest. Two-phone install/game/audio/visual acceptance and moderator operational ownership remain open. Rewarded ads remain disabled.

Generation mode, prompt summary and source/reference roles: `QA/BUILD577-PAWN-REFERENCE.md`. The user has already authorized publication after completion; do not ask for the same publication permission again, and do not fabricate pending acceptance results.
