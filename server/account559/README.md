# Build559 account services

Prepared, not deployed. The Flutter app has no embedded provider key or administrative credential. No email was sent while developing or testing these modules.

- `profileIdentity559` uses a revoked-token-aware Firebase Auth check, per-user distributed rate limiting and one transaction for names, independent change timestamps and username ownership. Three **calendar months in UTC** are added, clamping month ends while retaining the time of day. Existing accounts without change timestamps can make their first tracked change. Unchanged fields do not reset clocks. Retired handles are not reassigned.
- `verificationEmail559` obtains the recipient from Admin Auth, generates a fresh Firebase verification action, sets `lang=tr` and sends a Turkish HTML/text message with an NgelX wordmark and linked button. It accepts no recipient/action URL from the client. Only the actual `ngelx-44eed.firebaseapp.com` verification action path is accepted. The sender is a verified address configured server-side; `noreply` may still be the underlying local part, with the human-readable sender name NgelX.

Activation prerequisites:

1. Configure `NGELX_EMAIL_API_KEY` as a Functions secret and `NGELX_EMAIL_FROM` as `NgelX <address@verified-domain>`. This prepared adapter uses Resend; no account, domain, paid plan or subscription was created. Verify sender-domain DNS using the chosen provider. Appearance alone cannot guarantee inbox delivery or repair a spam reputation.
2. Audit existing profiles and resolve duplicate/invalid username ownership using the existing `server/auth/username-ownership.mjs` migration planner. Seed the private `login_usernames` index atomically and revalidate conflicts. Set server-owned `app_config/identity559.usernameIndexReady=true` only after the index audit completes. Username changes fail closed before then; display-name changes have a separate clock.
3. Deploy **only** the two account559 Functions exports and the reviewed Build559 user-rule delta alongside the prior reviewed album tombstone rules. Preserve all other existing exports/rules. The rules block direct identity/timestamp edits, private ownership-index access, and profile deletion/recreation that could reset the cooldown. Account erasure must continue through the existing server-owned deletion process. Automatic retention/cleanup remains paused.
4. Set repository build variables `NGELX_PROFILE_IDENTITY_URL` and `NGELX_VERIFICATION_EMAIL_URL` to the verified deployed HTTPS URLs and rebuild the candidate. No URLs are guessed. Without the identity endpoint, identity edits show a clear service-unavailable message; other profile edits still work. Without the custom email endpoint, the app retains Firebase's standard sender with explicit Turkish localization, not the custom HTML template.
5. In Firebase Authentication Templates set public app name/sender name to NgelX and verify Turkish defaults for native fallback, password reset and email-change confirmation. The custom verification service does not rewrite Firebase Console settings. Wrong-address correction reauthenticates with the current password and uses Firebase `verifyBeforeUpdateEmail`; it never overwrites the email without verification.

Validation: `node --test server/account559/policy.test.mjs`; demo Firestore emulator `tools/build559_rules_test.mjs`. Do not use uploaded real one-time verification links for testing.

Primary references: https://firebase.google.com/docs/auth/admin/email-action-links and https://firebase.google.com/docs/auth/flutter/manage-users .
