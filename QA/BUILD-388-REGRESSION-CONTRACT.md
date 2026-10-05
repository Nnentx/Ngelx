# NgelX Build 388 — Regression Hardening Contract

Build 388 starts from the tested Build 387 branch. The purpose of this package is to fix the device-test defects without reopening flows that already passed.

## Fix scope from Build 387 device QA

1. Friendship request resend / stale duplicate request notifications
   - A new request generation owns one current notification id.
   - Old notification generations are treated as superseded instead of showing “Bu istek daha önce sonuçlandırılmış”.
   - Activity and inbox activity badges dedupe friend/follow requests by requestKey.

2. Inbox realtime state
   - Chat streams use a consistent 100-chat window.
   - Private message writes update lastMessage, lastMessageClientAt and lastSenderId atomically.
   - Sorting falls back to lastMessageClientAt while server timestamps settle.
   - unread_* values are read as num instead of unsafe int casts.

3. Shared private-chat background
   - Shared background URL/color/opacity remain chat-level values visible to both participants.
   - Every shared background change increments backgroundVersion.
   - Pending writes are awaited for user-visible background changes.
   - Background images are selected smaller and decoded through ResizeImage to reduce keyboard/render pressure.

4. Android bottom safe area
   - Private chat reserves the system navigation area when the keyboard is closed.
   - Sohbet Bilgisi reserves the system navigation area.
   - Etkileşim summary and detail reserve the system navigation area.

5. Story delete confirmation
   - Delete confirmation is forced to a light dialog theme.
   - Title/body/action colors are explicit and readable from the dark story viewer.

6. Story video upload size mismatch
   - Story video validation and upload now use the video transport size path instead of the 10 MB generic story-file fallback.

7. Bottom status messages
   - Social actions touched by this package use colored, floating, rounded feedback instead of the old flat black snackbar.

## Passed-device baseline — MUST NOT REGRESS

The following Build 386/387 flows were already manually verified and are frozen as regression requirements:

- Saved content: save, open and remove from Saved.
- Stories: start/publish time, end/remaining time, archive/highlight menu.
- Private messaging: send/receive and seen state.
- Message Requests: DEVICE VERIFIED on Build 388 with the fresh Umay → Rojin scenario. A first message from a non-friend/non-following account lands in Message Requests with a badge, Accept removes it from requests, preserves the messages, and moves the conversation into the normal Inbox with the request badge cleared.
- Inbox filters and conversation list behavior.
- Inbox realtime unread flow: DEVICE VERIFIED on Build 388. Rojin → Umay message appeared immediately as the latest preview with unread badge = 1 and top Mesajlar = 1; after opening the chat and returning, the row badge cleared and top Mesajlar returned to 0 while the latest preview stayed intact.
- Friendship request, accept and remove flow.
- Follow request accept and follower removal flow.
- Privacy/settings screen behavior.
- Archive and live-history empty states.
- Message typing debounce/performance fix.
- Shared private-chat background behavior from Build 387.
- Interaction cards remain tappable.
- Follow/follower counts remain Firestore-driven; no local counter delta is reintroduced.

## Build 388 device verification added on 2026-10-05

### Rojin → Umay realtime inbox
- Sent “Testr 388” from Rojin to Umay.
- Umay inbox immediately showed “Testr 388” as the latest preview.
- Conversation unread badge = 1 and top Mesajlar counter = 1.
- After opening the chat and returning, both unread indicators cleared to 0.
- Latest preview remained “Testr 388”.

- Fresh sender: Umay Umay.
- Recipient: Rojin Candan.
- Incoming request appeared under Mesaj İstekleri with “Kabul et”.
- Inbox showed Mesaj İstekleri badge = 1 before acceptance.
- After acceptance, Mesaj İstekleri became empty.
- Existing “Slm” and 👍 messages remained visible.
- Umay moved into the normal Gelen Kutusu list.
- Mesaj İstekleri badge cleared.

## Build 388 video QA — 2026-10-05

Source: user device recording 44176.mp4 (~21.7 s), private chat with a photo background.

### New defect observed
- **Chat background jumps/reframes when the keyboard opens or closes.**
  - With the keyboard closed, the wallpaper is framed one way.
  - Opening the keyboard changes the available chat height and the `BoxFit.cover` image is visibly re-cropped/shifted.
  - Closing the keyboard makes the wallpaper jump back again.
  - This is a visual stability regression and remains **OPEN**.
  - Fix goal: keep the wallpaper anchored to a stable full-screen canvas while only the message/composer area resizes for IME, so opening/closing the keyboard does not zoom/reframe the background.

### Verified from the same recording
- Composer stays above the Android system navigation area; no bottom-button overlap was visible.
- Messages remain readable over the photo background.
- Text input and send action worked throughout the recording.
- No obvious message-list disappearance or crash occurred.

### Not proven by this recording
- Two-device / two-account background synchronization cannot be declared passed from this single-side recording alone.
- Keyboard latency is not marked as a failure from this clip; the clear reproducible issue is the wallpaper reframe/jump.

## Build 388 shared chat background device verification — 2026-10-05

### Passed
- Shared private-chat photo background synchronization is DEVICE VERIFIED.
- The background changed on the opposite account too, so the shared chat-level wallpaper sync works across both participants.

### New UX gap
- **Who changed the shared chat background is not shown in the conversation UI.**
  - The backend already stores `backgroundUpdatedBy` / `backgroundUpdatedAt`, but the chat does not surface this to users.
  - Expected behavior: add a lightweight system event such as “Umay sohbet arka planını değiştirdi” (and equivalent for color/reset), with timestamp.
  - This is tracked as an OPEN UX defect; do not break the now-verified two-account synchronization while adding attribution.

## Build 388 chat info bottom safe-area device verification — 2026-10-05

- Sohbet Bilgisi was scrolled to the bottom on device.
- The final action, “Sohbeti sil”, remained fully visible.
- There is clear spacing above the Android system navigation area.
- No text, icon, chevron or action row overlaps the system buttons.
- Result: **DEVICE VERIFIED / PASSED**.

## Build 388 interaction bottom safe-area device verification — 2026-10-05

- Etkileşim screen was scrolled to the bottom on device.
- The final “Gönderi / Toplam etkileşim: 0” row remained fully visible.
- There is clear spacing above the Android system navigation area.
- No card, text, chevron or interaction row overlaps the system buttons.
- Result: **DEVICE VERIFIED / PASSED**.

## Build 388 story delete device verification — 2026-10-05

### Passed
- Story delete confirmation dialog is readable on the dark story viewer.
- Title, body, “Vazgeç” and “Sil” actions are visible.
- Delete action completes and the app shows “Hikâye silindi.”
- Result for the original delete-dialog visibility bug: **DEVICE VERIFIED / PASSED**.

### New defect observed
- In the story options bottom sheet, the first three owner actions show their purple icons but their text labels are not visible.
- “Hikâyeyi sil” remains visible in red.
- Affected actions are the rows for share, highlight and archive.
- This is tracked as an **OPEN UI defect**. Fix must restore readable labels without breaking the now-verified delete dialog.

## Build 388 story video upload device verification — 2026-10-05

### Failed
- A 00:17 video was selected for a story, so the duration is within the intended 30-second story limit.
- Upload failed with: “Hikâye yüklenemedi: Dosya boyutu bu medya türü için sınırı aşıyor.”
- Result: **DEVICE FAILED / OPEN**.
- The Build 388 transport-path change did not fully solve real-device story video uploads.
- Fix direction: inspect actual selected-file size, then compress/transcode oversized short videos before upload instead of immediately rejecting them; keep the 30-second duration cap and server/storage safeguards.

### Additional UI defect observed
- The story upload failure is still shown as the old plain light bottom snackbar.
- It is not using the new colored/modern status feedback style.
- Result: **OPEN UI defect**.

## Build 388 follow-request profile check — 2026-10-05

### Passed
- From Rojin's view of Umay's profile, tapping the follow-request action changes the button to “Takip isteği bekliyor”.
- The pending follow-request state is reflected immediately on the profile.

### Open UI defect
- The success feedback still appears as the old flat dark snackbar: “Takip isteği gönderildi.”
- This profile follow-request path is not yet using the new colored/modern status feedback component.

### Test status
- The intended friendship resend test has **not started yet** in these screenshots.
- “Arkadaş ekle” is still visible and has not been pressed, so no friend request was created in this step.

## CI gate

A Build 388 APK is valid only when:
- source regression markers pass,
- `flutter analyze --no-fatal-infos --no-fatal-warnings` completes,
- release APK build succeeds,
- the existing stable NgelX signing certificate check succeeds.

If any frozen marker disappears, the workflow must fail before APK packaging.
