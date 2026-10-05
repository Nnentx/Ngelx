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
- Message Requests: routing/UI logic remains present; the DİLEK fresh-account scenario is still a pending device test, not declared passed.
- Inbox filters and conversation list behavior.
- Friendship request, accept and remove flow.
- Follow request accept and follower removal flow.
- Privacy/settings screen behavior.
- Archive and live-history empty states.
- Message typing debounce/performance fix.
- Shared private-chat background behavior from Build 387.
- Interaction cards remain tappable.
- Follow/follower counts remain Firestore-driven; no local counter delta is reintroduced.

## CI gate

A Build 388 APK is valid only when:
- source regression markers pass,
- `flutter analyze --no-fatal-infos --no-fatal-warnings` completes,
- release APK build succeeds,
- the existing stable NgelX signing certificate check succeeds.

If any frozen marker disappears, the workflow must fail before APK packaging.
