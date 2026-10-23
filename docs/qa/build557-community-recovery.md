# Build557 — community recovery and post approval notifications

Preserves the signed Build556 candidate and historical source generation. Apply `apply_build557_quality.py` only after Build556; full before/after hashes, cold/repeated application and pre-mutation drift rejection are enforced.

Changes:
- A community image/video record with a missing or invalid media URL no longer constructs a widget requiring a String or starts an invalid player.
- Legacy cover framing accepts numeric strings, rejects non-finite/invalid values and clamps to the supported range in both preview and editor.
- Community membership/role display helpers tolerate malformed lists while retaining only nonempty String IDs. Server rules still decide access.
- Information editing tolerates absent or legacy non-String text values.
- Single and bulk pending-post approval use the same transaction. Only posts actually transitioned from pending produce an approval notification after commit, with the existing community name/Topluluk label, per-recipient preferences and deduplication. A stale repeat approval produces no event. Membership approvals and report handling retain their behavior.
- Updated server counts now invalidate cached count futures instead of retaining an old shares/views value.

Local validation: exact patch cold/repeat/drift regression passed; 104 existing server tests passed. Added Dart malformed-data edge cases and a bounded narrow-phone cover widget test. Full Flutter analysis, tests, signing and Android identity checks are in the existing GitHub workflow. No unrelated worker redeployment is needed; the workflow probes the already-running service.

The exact intermittent gray-screen exception has not been reproduced on a physical phone. These are concrete crash prevention fixes, not evidence that every possible gray screen is resolved. Audio routing/rear camera still need two physical phones. Scheduled-post server-trigger deployment remains outside this client patch.

## Verified candidate

CI: https://github.com/Nnentx/Ngelx/actions/runs/40014721841 . Tested source commit: `4bee5ef3854dc211a6ce6d98103ee2a05075b47d`.

- Historical regression suite, Build556/557 patch reproduction, Dart edge cases, Flutter widget checks and full Flutter analysis passed.
- Android release build, package `com.nnentx.ngelx_app`, versionCode `557`, versionName `1.0.327` and existing update certificate passed.
- APK: `NgelX-1.0.327-Build557.apk`, 47,482,799 bytes. SHA256: `fc5441928ee84cde91e7c7c4f36b5e20860a80b53be81f64856b2c443f112582`.
- APK artifact `12528008764`, ZIP SHA256 `4c8d2b931aa1e9383b3cca503c6e8d8e762fabdfe1536c32482eb0a6cc0a97ea`.
- Source artifact `12528043843`, ZIP SHA256 `68b25efa70347b6ed92331f3ede54908d9fa0fd1ddca55b612a57f15ce020a67`.
- Downloaded archive digests, APK checksum/ZIP integrity, ARM64 native libraries, all changed source hashes and helper bytes were independently verified; included signing and Android badging evidence matches.
- Candidate saved for owner download. No physical-phone acceptance testing or automatic installation was performed.
