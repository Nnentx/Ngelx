# NgelX Build505 — Android + staging LiveKit acceptance checklist

**Status:** QA plan only; nothing in this file authorizes deployment, Firestore
rules publication, billing, or changing the production download website.
Protected production candidate remains Build484. Full-chain QA APK
versionCode 505 / versionName 1.0.279. Test branch is not production.

## Separate prerequisites (all required)

- [ ] Build505 GitHub Actions completes successfully, and the Android QA
      artifact, signing SHA-256 and versionCode/name are independently checked.
- [ ] Staging Firebase project, staging LiveKit server, server SDK credentials,
      and temporary **HTTPS** guest moderation endpoint are approved and
      configured only in an isolated build. NEVER put LiveKit API secrets in APK.
- [ ] Verify the endpoint is deployed to staging with Firebase ID-token
      verification/revocation, Firestore owner/guest constraints, and room-admin
      API calls; 200/ok for real action, not a mocked unit-test response.
- [ ] Check server logs redact secrets and bearer credentials.
- [ ] Make two Android devices and at least host+guest accounts available;
      use a separate third account for unauthorized-user checks.
- [ ] Observe both devices' actual LiveKit audio/video tracks and Firestore
      state, rather than relying solely on UI button labels.

## Two-device host / guest cases

| # | Action | Required observable result |
|---|---|---|
| 1 | Host sends invitation, guest accepts | Exactly one accepted guest; video/audio tracks share the original stream; no second live room |
| 2 | Guest requests, host accepts with host camera/mic denied | Host can approve without needing local media permissions; guest grants their own permissions |
| 3 | Host mutes accepted guest while guest speaks | LiveKit server mutes audio track; published video continues and other viewers hear silence |
| 4 | Guest tries to republish audio while muted | Room permission forbids new microphone track, including after reconnect/new token |
| 5 | Host unmutes guest | Microphone does **not** activate automatically; guest must explicitly enable it |
| 6 | Guest enables microphone after permission restored | Audio resumes only after guest action; video and original room remain connected |
| 7 | Host kicks connected guest | Server removes participant; guest request becomes rejected; existing video/audio cease |
| 8 | Guest tries to reuse existing pre-kick JWT | Explicitly test whether the previously issued 5-minute token still allows joining; **security blocker if it does** unless separate effective mitigation exists |
| 9 | Guest obtains new token after kick | Server denies speaker publish authorization; rejected guest cannot publish |
| 10 | Guest leaves voluntarily | Only their tracks end; other guests and host remain live |
| 11 | Unauthorized account calls moderation endpoint | Non-host, other-room owner, self-target, malformed liveId and roomName retargeting are denied, zero remote-admin changes |
| 12 | Host requests two quick/conflicting actions | Final Firestore policy and RTC track state are consistent; no accidentally unmuted guest |
| 13 | LiveKit API succeeds but Firestore transaction fails | Endpoint returns failure; operator can identify and reconcile partial state; no false UI success |
| 14 | Firestore request races with ending the live stream | No action on ended room or wrong/expired owner session |
| 15 | Endpoint unset, non-HTTPS, offline or returns 401/403/409/503 | Client fails closed; no direct-Firestore fallback; no fake success |
| 16 | Guest retries reconnect after permission rejection | Camera stays stable, mic off until allowed and explicitly enabled |
| 17 | 10 simultaneous accepted guests | 10 tiles render, speaker and host role scopes correct, no overflow/phantom video, measured performance |
| 18 | Android 13–15 small display with gesture/3-button navigation | Host controls, compact join sheet, keyboard and SafeArea do not overlap or clip |

## Evidence and release gate

Capture Android version, device models, staging room ID, action timestamp,
server LiveKit track state, Firestore snapshot, and pass/fail for each case.
Redact UIDs/tokens/participant names in shared logs. Failed/untested cases
remain **open** in Issue #110.

**No production merge or deployment** without explicit owner approval after
real-device and staging results. Build505 default APK has no moderation URL;
its buttons are intentionally disabled. A deployed staging function and an
opt-in staging-configured build are prerequisites to running server-action
cases. Never imply that passing source, Node and Flutter CI alone proves
real media moderation.
