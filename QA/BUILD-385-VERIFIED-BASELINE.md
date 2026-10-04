# NgelX Build 385 — Verified Regression Baseline

Verified on device: 2026-10-04
Base: Build 384
Build: v1.0.162+385
Branch: work/build-385-chat-playstore-package

## Protected baseline

The following behaviors are verified and must not regress in later builds.

### 11 — Send -> auto scroll to newest message
- Private chat: PASS
- Group chat: PASS
- After sending, the conversation returns to the newest message automatically.

### 12 — Private chat typing performance
- Manual device test: PASS / no lag reported.
- Long text input and send flow worked.
- Keep typing state rebuilds isolated from the full chat UI.

### 13 — Group chat typing performance
- Manual device test: PASS / no lag reported.
- Long text input and send flow worked.
- Keep group typing state rebuilds isolated from the full chat UI.

### 14 — Reply mode
- Group reply mode: PASS.
- Visible "YANIT MODU" state.
- Shows who is being replied to.
- Shows text/media preview.
- Reply can be cancelled with X.
- Sent reply keeps the referenced content preview.

### 15 — Registration safety
- Required-field validation: PASS.
- Terms + Privacy consent gate: PASS.
- Registration is blocked until consent is accepted.
- Birth-date / age gate: PASS.
- Under-13 registration is blocked with a clear warning.
- Repeated email/password fields remain part of the protected registration flow.

### 16 — Store/legal readiness
- NgelX About page: PASS.
- Privacy Policy link present.
- Terms of Use link present.
- Account and data deletion link present and opens the public deletion page.
- Child Safety link present.
- Support link present.
- Android target/compile API 36 and narrow media-permission policy are protected by CI.

## Build 384 compatibility lock

Build 384 reaction behavior remains protected by exact-parity CI checks. Do not replace or simplify the verified reaction detail/mutation ranges unless a new device test explicitly approves the change.

## Rule for future builds

Any later build based on 385 must keep items 11, 12, 13, 14, 15 and 16 working. Treat these as regression blockers. If one breaks, the package is not considered ready even if it compiles.
