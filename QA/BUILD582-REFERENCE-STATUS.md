# Build582 — Ludo reference implementation

Based on exact Build581 assembled source from successful run 40468098023, artifact 12717657392. `tools/apply_build582_reference.py` verifies the input Ludo SHA-256, applies the frontend-only patch, updates to 1.0.352+582 and installs the reference assets. Reapplying is safe.

Changes:
- Uses artwork extracted from the two user-supplied references for Ludo headings, statistic icons and badge faces. No sample user portrait or sample balances are embedded.
- Statistics use four columns and two rows, profile/XP, history summaries, and achievements in the reference palette.
- Refresh requests the authoritative wallet. Profile uses the signed-in user's existing profile. XP uses unchanged server thresholds; sample 165/500 is not substituted for the actual 165/200 boundary.
- History popup filters won/lost summaries. All badges opens real requirements and current earned/locked states.
- Lobby selections use horizontal cards with selection outlines, room creation/join actions, classic/power and player-count controls. Existing room/game/transport/invitation logic remains in place.

Validation completed locally: 149 backend regression tests pass; all 39 selected Flutter regression/widget tests pass; full app analysis exits successfully with 111 existing/nonfatal notices and no errors; patch input guard and second-run idempotence pass; generated source parses and git whitespace validation passes. Phone screenshots were rendered with decoded reference artwork and Material icons and visually inspected. After the final lobby spacing and quick-action label fit adjustment, all five targeted lobby/statistics tests also pass, and the updated phone screenshots were inspected.

Pending: signed Android APK and physical-device comparison. The user explicitly approved uploading the code and reference artwork to public Nnentx/Ngelx and starting the Build582 APK workflow on 27 October 2026. The source branch is being uploaded under that authorization. No APK or in-app update is claimed until its build and verification complete.

The workflow `.github/workflows/NgelX-BUILD582-REFERENCE-QA.yml` is prepared to run existing regression tests plus the new statistics/refresh/filter/badge/phone-render tests and produce the signed review APK once the branch is authorized and uploaded.
