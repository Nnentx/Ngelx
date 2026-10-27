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
- Final follow-up review: direct Ludo invitation now preserves existing private/group chat draft text, saved drafts, reply metadata, mention selections and typing state.
- **Final QA workflow [40468098023](https://github.com/Nnentx/Ngelx/actions/runs/40468098023): SUCCESS.** All backend tests and **36 Flutter regression/widget tests** passed; whole-app analysis completed with nonfatal historical warnings. Same signing certificate confirmed by apksigner.
- **Final signed ARM64 APK**: `com.nnentx.ngelx_app`, version `1.0.351`, build `581`, size **49,486,060 bytes**. SHA-256: `9be239b0fd0adf00b5315d217ac892cf38bde44573f6027c9ea4dd6308be89de`. GitHub archive SHA-256: `25aa9708a018f00eb65a93670fc43cb4c3211a2781401ddfe151fadc0a8fd2c7`. APK ZIP/CRC/ARM64 assets and downloaded bytes verified after CI.
- APK artifact: https://github.com/Nnentx/Ngelx/actions/runs/40468098023/artifacts/12717857043
- **Important**: Static regression/Flutter tests do not substitute for two physical devices and screenshot-level matching against the user-approved 3D design mockups. Direct invitation flow requires two-device in-app check before general release.
- The current public Build580 and the in-app updater/feed remain unchanged.

## Deployment policy
This is a **draft PR** #194 and **not published**. No default branch merge, public APK release, production server changes, in-app update manifest change, account data migration, or removal was performed by this branch. Complete two-device invitation and UI acceptance before promotion. The existing in-app update remains Build580.
