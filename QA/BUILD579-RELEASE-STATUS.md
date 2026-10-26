# Build579 — published in-app hotfix, 26 October 2026

## Result
The incoming Ludo invite's Join button no longer enters the inherited non-incrementing board-painter loop before room data arrives. Back navigation is covered both while joining and after room load. The fallback pickup map is constant, and the invitation title stays within its card.

Polling now completes before a mutation takes its revision. Auto/bot sync conflicts recover with at most three attempts. A conflicting manual roll/move is never replayed; the authoritative board is refreshed. Gameplay rejections keep their real message. Established rooms show reconnect after repeated transport failures, and a successful response clears it. Initial joins can show retry after one transport failure. Failure backoff uses transport failure counts rather than arbitrary notifications.

## Evidence
- Exact tested app source: `2208838b2fe50d2b5addb3dd9d07c2bad9ac7d16`.
- [Android CI 40386052388](https://github.com/Nnentx/Ngelx/actions/runs/40386052388): success; **142 backend/Worker tests, 26 Flutter tests, six verifier unit tests**, analysis, package/ARM64/content checks, original signing fingerprint and separate optional ad SDK analysis.
- New regression coverage includes every missing-map board orientation/classic/loading paint, actual invite activation and pending-join Back, joined-room Back, in-flight poll/action revision serialization, Auto sync conflict recovery, transport failure/recovery, gameplay throttling classification, and no manual-move replay after conflict.
- [Release 40386163392](https://github.com/Nnentx/Ngelx/actions/runs/40386163392): success. APK and bundled sprite verified, anonymous public download compared byte-for-byte to CI artifact.
- No server/Cloudflare source changed relative to the Build578 live-accepted source. Existing [live acceptance 40379934754](https://github.com/Nnentx/Ngelx/actions/runs/40379934754) remains applicable; no Worker redeployment occurred. Runtime compatibility marker remains clientBuild578.
- Web feed switched LAST at commit `832d42ff59679fb8159cb415d0ae7339475547e3`. [Pages 40387895854](https://github.com/Nnentx/ngelx-web/actions/runs/40387895854): success. Direct unqueried GET of `https://ngelxsocial.com/android-update.json` returns build579 and the exact APK hash.

## Public package
- Package `com.nnentx.ngelx_app`, **1.0.349 / Build579**, **49,463,948 bytes**.
- SHA-256 `b84cdaa351abb66fe9e732066e5dd8363b4c0d78fb16a6445df03289bfa52de3`.
- [APK](https://github.com/Nnentx/Ngelx/releases/download/v1.0.349-build579/NgelX-1.0.349-Build579.apk).
- Exact current feed: `QA/BUILD579-PUBLISHED-UPDATE.json`; previous578 feed: `QA/BUILD579-PREVIOUS-UPDATE.json`. Earlier artifacts and feed backups retained. Reverting the feed prevents additional updates; it does not downgrade already installed higher versions.

## Limits
Two physical Android devices have not been used for end-to-end acceptance. Automated route/controller tests are not physical-device evidence. The earlier full-room test stalls were the real painter defect, not an environmental issue; see BUILD579-FREEZE.md. Existing pawn layout, sound, wallet, XP and persistent Auto are retained. Rewarded ads remain disabled and moderator privileges remain restricted.
