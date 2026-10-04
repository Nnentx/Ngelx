# NgelX Build 386 — Open QA Items

Source baseline: Build 385 verified baseline
Branch: work/build-385-chat-playstore-package
Started: 2026-10-04

## 17 — Account switching / login
Status: TEST PENDING

- Sign out from the current account.
- Sign in with a different existing NgelX account.
- Verify login completes without a stuck screen.
- Verify wrong password / invalid login gives a clear user-facing error.

## 18 — Password reset
Status: PARTIAL PASS + BRANDING/LOCALIZATION FIX REQUIRED

Verified:
- "Şifremi unuttum" opens the password reset screen.
- Reset request succeeds.
- User sees a confirmation message.
- Firebase reset email is delivered.
- Reset link opens successfully.
- New password is accepted and saved successfully by the reset page.

Build 386 fixes required:
- Password reset email currently exposes the Firebase project name "ngelx-44eed".
- Replace user-facing project branding with "NgelX".
- Turkish users should receive a Turkish NgelX-branded subject and email body instead of the current English/Firebase-default presentation.
- Keep the secure reset link flow working after branding/localization changes.

Final functional check still pending:
- Sign in to NgelX with the new password successfully.
