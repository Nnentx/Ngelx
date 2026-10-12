# Build443 profile capture privacy follow-up

Implemented for Android owner, visitor and visitor-preview profiles: persisted `allowProfileCapture` opt-in, default protected, native FLAG_SECURE leases per mounted profile, native acknowledgement before rendering, authoritative non-cache/non-pending preferences, conservative protection on loading/error/offline, independent nested leases, delayed final-frame cleanup, and save failure feedback. Descendant media and backgrounded profiles retain the parent lease. The switch describes screenshots and screen recording together. Other platforms are not claimed protected.

48 additional complete translation rows cover the new privacy setting, errors, recovery/blocked-account descriptions, comment counts/options, notification/data descriptions and join-date display. Settings switch helper text now uses the presentation lookup. Join dates no longer hardcode Turkish month names; year is displayed with the selected-language template. User text and persisted enum values remain data. A remaining literal inventory is produced by CI; full localization is NOT complete.

Automated checks: five widget tests exercise native-ack rendering, privacy updates/errors, nested lease cleanup, native failure and stale acknowledgements. CI also runs Flutter analysis, existing behavior/security tests and native APK/AAB builds. Local source integration checks passed. Initial CI identified test platform cleanup and nested descendant recreation; these were corrected before a fresh full build. Final CI/device results must be appended after execution.

Required device acceptance: two accounts, deny/allow screen recording and screenshot on both owner/visitor profiles, nested media, back navigation, background/reopen, offline loading, account change and save failure. APK is a candidate until these checks pass. Do not replace the public Build442 download before the candidate's build and tests pass.

Remaining release work: full localization; production LiveKit auth/room/host-reservation/rate-limit adapters and deployment; verified production retention/deletion; store graphics and device screenshots; truthful Console forms and reviewer account; identity/phone verification and account-specific testing requirements. Browser automation for Play Console was previously rejected by automatic approval review and cannot be bypassed. The developer's phone can complete account verification when Google approves identity.

Server follow-up: Firebase Functions entry point and Firestore auth/room/reservation/rate-limit adapter candidates added. 31 Node tests pass locally. Deployment, Firebase emulator integration and LiveKit moderation/cleanup still remain; production credentials/hosting access are not present.

## Verified delivery, 12 October 2026

Source commit: `51fbceb44b1b5538384c0fdbbeae73ffb6e1f0f1`. Full CI run `38229602376`, job `114745909048`: success. Five capture widget tests, 31 Node authorization/adapter tests, existing Flutter behavior tests and Firestore rules emulator checks passed; Flutter analysis had no blocking errors. Final generated locale catalog: 48 complete rows, 16 additional presentation literals connected; inventory retains 832 unwrapped Turkish literals (plus separate dynamic/helper review).

APK `NgelX-1.0.218-Build-443-CANDIDATE.apk`: 146,412,386 bytes; SHA-256 `8f62f814c765871aa5480d977ff78d4b9543b2fd44cc2d38a1c51dafb8dd5401`. APK v2 signature verified by apksigner; existing certificate `BE:20:B2:7F:0B:A1:F4:DE:CD:29:41:D4:10:B1:53:6D:E8:9E:48:DC:89:4F:04:F0:38:F9:D2:6B:11:EC:D6:AA` retained for installation updates. Artifact `11738522033` ZIP digest `0b4fd74acd55d1a0a3f9fe8398ebe4ad94b872336b44d4f550cbe2d5bac45ab6` and extracted APK checksum matched locally.

Play preparation AAB compiled and all nine arm64 libraries met 16 KB PT_LOAD alignment. This is the debug/test-signed preparation bundle, not a final Play upload package. Production token endpoint configuration, upload signing and Play acceptance are not claimed complete.

APK and its checksum file were delivered as durable download files. Public ngelxsocial.com remains on Build442 until candidate device acceptance. Both phones need Build443 for the new Android capture behavior; no capture protection is claimed for older installed clients. LiveKit server adapter tests use a serial transaction harness; these do not substitute for server emulator, deployed authorization or actual two-phone media checks.
