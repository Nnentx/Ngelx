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
