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
Status: FUNCTIONAL PASS + APP LOCALIZATION IMPLEMENTED / EXTERNAL FIREBASE BRANDING PENDING

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
Status: IMPLEMENTED / DEVICE QA PENDING

Observed on device:
- User taps to unfollow from another user's profile.
- Snackbar confirms: "Takipten çıktın."
- Profile action button remains stuck on "Takip ediyorsun" instead of immediately switching back to the follow state.
- After leaving the profile and reopening it, the state becomes correct: button shows "Takip et" and the follower count reflects the unfollow.
- This confirms the backend mutation succeeds; the defect is stale in-page/local relationship state refresh.

Expected:
- After a successful follow/unfollow mutation, the profile UI must update immediately without leaving/reopening the page.
- Follower/following counters must refresh consistently with the action.
- Reopening the profile must show the same final state as the backend.

Build 386 requirement:
- Fix stale local/profile relationship state after follow/unfollow.
- Keep backend relationship mutation and UI state synchronized.


## 20 — Profile message button / private chat open
Status: PASS

Verified on device:
- Tapping "Mesaj" from another user's profile opens the correct 1:1 private conversation.
- Existing conversation history loads.
- Custom chat background renders.
- New messages can be sent successfully.
- No blank/stuck transition observed.


## 21 — Friendship request flow
Status: PASS

Verified on device:
- Removing an existing friendship succeeds.
- Friendship count updates to 0 immediately.
- Profile action updates immediately to "Arkadaş ekle".
- Snackbar confirms "Arkadaşlık kaldırıldı."

Verified:
- Tapping "Arkadaş ekle" sends a new friendship request.
- Sender profile immediately changes to "Arkadaşlık isteği bekliyor".

Verified:
- Recipient receives the friendship request in Activity.
- Request card shows active accept and reject controls.

Verified:
- Recipient can accept the request successfully.
- Activity confirms "Arkadaşlık isteği kabul edildi."
- Recipient profile friendship count updates to 1.
- Friends list shows the accepted account.
- Friendship state is consistent after acceptance.


## 23 — Friends discovery model
Status: IMPLEMENTED / DEVICE QA PENDING

Reference: user-provided social friends discovery screen.

Add an NgelX-native friends/discovery model with:
- Top tabs: "Arkadaşlar", "Takip", "Önerilenler", "Ortak noktalar".
- Search field for people/friends.
- Visible total friend count.
- Person rows with avatar, display name and relevant relationship context.
- Mutual-connection count when available (for example "76 ortak arkadaş").
- Three-dot overflow menu on each person row for relationship actions.
- Suggested/discovery emphasis indicator where useful.
- Fast switching between tabs without losing scroll/search state.
- White NgelX visual language; use NgelX typography/colors/components rather than copying another app's branding.
- Keep follow and friendship as separate concepts.
- "Ortak noktalar" can surface shared groups/interests/mutual connections depending on available data.
- Mutual-friends display is now explicitly INCLUDED by the user's latest request and supersedes the earlier exclusion.

Acceptance:
- Lists load without blank states/stuck UI.
- Counts and relationship states refresh immediately after follow/friend actions.
- Search filters the visible list correctly.
- Opening a person row navigates to the correct NgelX profile.


## Build 386 implementation progress

Implemented in code:
- 18: Firebase Auth language code is set from the NgelX app language before password-reset email delivery.
- 18: Added a Turkish, NgelX-branded custom password reset web handler at web/reset-password.html.
- 19: Added optimistic local follow state + follower count delta so follow/unfollow updates immediately without reopening the profile.
- 23: Rebuilt the Friends page with Arkadaşlar / Takip / Önerilenler / Ortak noktalar tabs, search, mutual-friend context and per-person action menus.
- 17 and 22 remain functional QA gates; no defect has been confirmed in those flows yet.

External configuration still required for complete item 18 branding:
- Firebase Authentication email-template sender/project display name must be changed from the raw project id to NgelX.
- Firebase Authentication custom email action handler/template configuration must point password reset actions to the deployed NgelX reset handler.


## 24 — Consolidated device findings after Build 386 manual QA
Status: FIXED IN CODE / CI VALIDATION RUNNING

Consolidated in commit be1972e:
- Private-chat background/theme is now shared at chat level so either participant's change is visible to both sides.
- Message composer hot path no longer starts mention lookup on every keystroke; mention lookup is debounced.
- Account-add bottom sheet now respects safe area and keyboard bottom inset.
- Interaction summary cards (Beğeni / Yorum / Paylaşım / Gönderi) are actionable and open metric detail lists.
- Story owner menu now includes share, highlight/unhighlight and archive actions.
- Story deletion now requires explicit confirmation.
- Follow/unfollow and follower removal wait for pending Firestore writes; follower removal also refreshes the owner document from server to avoid stale count bounce.

Manual QA already passed and must not regress:
- save/remove saved content,
- story start/end/remaining time,
- message send/receive and seen state,
- message requests,
- inbox filters,
- friend request/accept/remove,
- follower request accept and follower removal,
- privacy screen,
- archive/live-history empty states.

CI gate:
- flutter analyze,
- Android release APK build,
- Build 386 source regression markers.
