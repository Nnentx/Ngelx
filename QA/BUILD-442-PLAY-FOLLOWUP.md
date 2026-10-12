# Build442 — 46455 video and Play follow-up

User device acceptance: Build441 login and remaining functional checks reported working. The 46455 English video still shows Turkish UI labels. This is not a complete all-language acceptance.

Implemented: 32 new rows in all 12 supported languages; Create card/tab/tool helpers, profile layout/preview helpers, settings switch descriptions, sensitive-content options and the interpolated pending-message count use the locale lookup. User names, biography text, content tags, route IDs and database enum values remain data, not translated UI.

Validation: Build441 token-aware checks; Build442 complete-language rows and display/data-boundary checks; 11 production token-core tests passed locally. Flutter analysis, device tests and APK/AAB depend on CI. The remaining literal inventory is preserved as an artifact; full app translation completion is not claimed.

## Added user requirement, 12 October 2026

Profile privacy must offer an allow-screen-recording preference. When the profile owner disallows recording, viewing that profile on Android must apply FLAG_SECURE before profile content is displayed. Android's flag also blocks screenshots and unsecured display mirroring; the setting must describe both capture types. Loading/error states must fail closed. Protection must remain while opening profile media/preview and during app backgrounding, and be released when the protected route and its child views leave. Nested protected profiles need reference-counted ownership. Account changes and async navigation must not remove another route's protection. Owner opt-out and visitor capture tests are required. This is recorded, not yet implemented or device-verified.

## Actual external release blockers

Production LiveKit endpoint is not deployed; Firebase Admin authorization/reservation/rate-limit adapters and LiveKit production secrets are required. Existing token-core tests do not prove production calls.

Web repository ngelx-web was located separately. Published policy behavior, cleanup schedule and support contact must match production. Console forms must be based on actual deployment and age/ad choices; no invented declarations. High-resolution branding and clean real-device demo screenshots still need validation. Personal test recordings are not store screenshots.
