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
Status: FUNCTIONAL PASS + BRANDING/LOCALIZATION FIX REQUIRED

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

Final functional check:
- Sign in to NgelX with the new password successfully: PASS.


## 19 — Follow / unfollow state refresh
Status: FAIL / FIX REQUIRED

Observed on device:
- User taps to unfollow from another user's profile.
- Snackbar confirms: "Takipten çıktın."
- Profile action button remains stuck on "Takip ediyorsun" instead of immediately switching back to the follow state.

Expected:
- After a successful follow/unfollow mutation, the profile UI must update immediately without leaving/reopening the page.
- Follower/following counters must refresh consistently with the action.
- Reopening the profile must show the same final state as the backend.

Build 386 requirement:
- Fix stale local/profile relationship state after follow/unfollow.
- Keep backend relationship mutation and UI state synchronized.
