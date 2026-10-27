# Build581 — approved Ludo designs, QA staging

## Scope
This branch adds the approved dark blue / violet Ludo landing and mode layout, server-backed "Puanlarım" stats screen, and direct visual invite delivery to private/group conversations without putting raw invite links in the composer.

- Base: `qa/ludo-feedback-20261026` and exact Build580 assembled source artifact `12689108915` from workflow `40401696200`.
- Patch: `tools/apply_build581_designs.py`. Validates both exact input SHA-256 hashes, refuses unknown inputs, and is idempotent.
- Visual components: `tools/build581_visuals.dart`; server-accurate XP level boundary calculation matches `server/ludo565/rewards575.mjs`.
- Direct invitation: original private / group chat sending logic, permissions, blocked-user checks, group offline queue, and notification handling are reused; only the initial composer-draft route is bypassed for a user-picked Ludo target.
- UI acceptance references: #192 for lobby; #193 for statistics. Sender and recipient user profiles/data are not modified.

## Validation
- GitHub Actions: https://github.com/Nnentx/Ngelx/actions/runs/40414751761
- Backend regression job: successful.
- Exact source patch/idempotence: successful.
- Flutter full analysis: passed with existing nonfatal warnings.
- Old and new Flutter widget/regression tests: passed.
- First Build581 QA workflow 40414751761: full success, 36 Flutter tests, verified signer and compiled APK (1.0.351+581, 49,485,816 bytes, SHA-256 ed946c32ddc588bddf398e6bfcbbb0b6d796b549771d14f1edade52bc93d6b59). 
- Follow-up: direct Ludo invite sending now preserves an existing private/group chat draft, reply, mentions, and typing state. The updated code was added to the patch and is under a separate CI rerun: https://github.com/Nnentx/Ngelx/actions/runs/40468098023. Backend, Flutter analysis, and widget tests passed; final APK build had not yet completed when this status was written.
- Current public Build580 and the update feed remain unchanged.

## Deployment policy
This is a **draft PR** #194 and **not published**. No default branch merge, public APK release, production server changes, in-app update manifest change, account data migration, or removal was performed by this branch. Complete two-device invitation and UI acceptance before promotion. The existing in-app update remains Build580.
