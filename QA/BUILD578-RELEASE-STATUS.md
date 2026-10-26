# Build578 — published in-app update, 26 October 2026

Latest user instruction explicitly requested completing the changes and putting the APK in the application's updater. Publication proceeded after exact automated Android and real staging/live API acceptance. Physical-device acceptance has NOT been fabricated or marked complete; the published GitHub asset is a prerelease. Historical Build575–577 acceptance checklists remain historical, not assertions that two phones were tested.

## Shipped behavior
- Larger home pawns (1.26 cells), track pawns (1.18 cells), compact shared-cell stacking. Home base centered on socket; track base at 78% of tile height, with head above upper edge. Visible footprint anchors replace image-center placement; board-edge clipping removed.
- Six power pickups for NEW games: four dice icons and two shields, plus existing four +1 bonuses. Active older rooms retain their saved maps.
- Persistent server Auto is not canceled by client one-legal-piece assistance. Active Auto/bot sync every 500ms, ordinary play every 1s, spectators every 4s; bounded network backoff retained. No new timeout required for each automatic action.
- Progressive level thresholds 200/500/900/1400 total XP, previously stored levels retained, human win/loss XP 90/15, bot 35/5. Abandoned matches pay neither XP nor chips; receipts prevent repeat rewards.

## Verified evidence
- APK CI [40379566732](https://github.com/Nnentx/Ngelx/actions/runs/40379566732), exact app source `389059e2227d94814bae7fc9f1f21cdee19e70ca`: success, **142 backend/Worker tests + 18 Flutter tests**, analysis, six verifier unit tests, same signing certificate, package/ARM64/content/demo-ad checks, separate optional SDK smoke.
- Real Firebase staging [40378761157](https://github.com/Nnentx/Ngelx/actions/runs/40378761157), runtime source `48669221cd5e0e0e46c12e3e0105546fa84f00bd`: success.
- Guarded production acceptance [40379934754](https://github.com/Nnentx/Ngelx/actions/runs/40379934754): success; Worker version `61737c50-c8da-4a95-b7fb-94e08d083d1f`. Both hostnames converge to `ludo575.clientBuild:578`; six-icon map, authenticated 2/4-player/team/Auto and wallet/gift/reward boundaries pass. Temporary QA data/accounts removed. Prior version checkpoint retained; seven deployment-guard regressions pass.
- APK asset publication [40380185351](https://github.com/Nnentx/Ngelx/actions/runs/40380185351): success; exact anonymously downloaded bytes compared to CI artifact and bundled original 3D image verified.

## Public update
- Package `com.nnentx.ngelx_app`, **1.0.348 / Build578**, **49,462,372 bytes**.
- SHA-256 `7d0ad052906a0b4b7ca5a26bc59867baff3521538212e6581bc5c922ab627153`.
- [APK](https://github.com/Nnentx/Ngelx/releases/download/v1.0.348-build578/NgelX-1.0.348-Build578.apk).
- `Nnentx/ngelx-web/android-update.json` updated LAST, commit `d63fb83d4cfd3484273a8b7f7d7c0150de5dd802`; Pages deployment 40381806450 successful. Direct GET `https://ngelxsocial.com/android-update.json` returns HTTP200, build578 and the exact SHA above, without a cache-busting query (also checked with query). Existing Build574 artifact and rollback metadata preserved.
- Exact new feed is `QA/BUILD578-PUBLISHED-UPDATE.json`; previous feed is `QA/BUILD578-PREVIOUS-UPDATE.json`. Reverting feed prevents additional updates; it does not downgrade already installed higher-version APKs.

## Explicit limitations
Two physical Android devices have not been used for end-to-end acceptance. Full-room/table screenshot integration attempts from the prior correction were not completed and are not counted as passes. This revision's geometry is checked mathematically and the production sprite renderer captured at actual small sizes. Actual appearance, sound, install flow and reconnection still need phone feedback. Rewarded ads remain disabled. Moderator operational ownership/allowlist remains unset; normal users cannot access moderation APIs. No global roles or ad credentials were invented.
