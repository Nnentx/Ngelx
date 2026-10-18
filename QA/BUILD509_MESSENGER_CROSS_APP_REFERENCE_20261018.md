# Build509 — Cross-app Messenger-like floating call

**Reference:** 44-second Android screen recording shared by the user on
2026-10-18. Private chat, group call and app-drawer contact names and images
are redacted here; the video is not uploaded to GitHub.

## Observed interaction sequence

| Video | Actual visual state | Required NgelX behavior |
|---|---|---|
| ~0–2s | Full-screen Messenger call, compact call controls, then messenger chat | Call remains connected when the full screen is left |
| ~3–5s | Messenger inbox, floating card showing caller and other participant | Card follows the current, single active call |
| ~6–11s | Android home screen and all-apps drawer with floating call card | **System-wide** overlay on other apps and launcher, not only Flutter Stack |
| ~12–18s | Two-avatar card moved around different parts of screen | Drag, bounded edges, no lost controls or call termination |
| ~19–23s | ChatGPT in foreground; call card remains on top | No navigation to NgelX on passive overlay appearance |
| ~23–25s | Tap compact card; larger controls layer: settings, close, fullscreen, mic/speaker/end | **First tap expands card locally**, does not jump to full-screen call |
| ~25–27s | Fullscreen control returns to ongoing Messenger call | Only explicit fullscreen action resumes NgelX full call screen |
| ~28–33s | Call minimized again; compact panel and green in-app call banner | Shrink/expand cycles preserve audio, room, elapsed time, participants |
| ~34–44s | Call continues; UI and controls adjust without recreating a new call | No duplicate LiveKit session, invitation, mic toggle or reconnect |

## Behavior contract (must pass on physical Android)

- [ ] **All-app availability**: home, app drawer, messaging, browser, video
  app and ChatGPT show a floating NgelX call while there is a valid call.
- [ ] Explicit user consent for Android **Display over other apps**
  (`Settings.canDrawOverlays`, `SYSTEM_ALERT_WINDOW`). Never enable this
  permission automatically; if denied, use in-app call return/notification.
- [ ] Compact avatar/video preview floats freely. Its size, rounded corners,
  contrast and pointer targets are comparable to the reference, with NgelX
  branding rather than copying Messenger artwork.
- [ ] Tap compact preview -> expanded card with **settings, collapse/close,
  fullscreen, microphone, speaker, end-call**. First tap must NOT navigate home
  to NgelX. Touch outside or idle -> compact preview again.
- [ ] Drag compact or expanded card to any screen edge without clipping under
  status bar, camera cutout, navigation, system gesture region or keyboard.
- [ ] Swipe down to minimize further: preserve at least a **small return chip**,
  not a disconnected call and not a permanently invisible card.
- [ ] Fullscreen action -> bring NgelX to foreground and resume exactly the
  same call with the same LiveKit Room and microphone/camera choices.
- [ ] 1:1 and group voice/video, remote and local track publication: video
  preview reflects real LiveKit media when present; otherwise avatar only.
  Never start either participant's camera without an explicit user action.
- [ ] Microphone toggle is **local only**; end-call requires current
  authenticated call context and immediately removes all floating UI.
- [ ] Logout, account switch, call rejected/ended, revocation, process/task
  stopped, display-permission revoked -> remove floating view promptly.
- [ ] Permission denial, device restrictions, Android 13–15 and MIUI/HyperOS
  differences are shown as actionable but not blocking audio call continuation.
- [ ] Feature respects foreground call service, microphone/camera background
  restrictions and OS overlay visibility/security limits.

## Architecture review

Build508 PR #134 only places Flutter `Positioned` within NgelX; it cannot
float above other Android apps. Android PiP is OS-managed and gives limited
control over gestures/expanded controls; choose explicit opt-in
`TYPE_APPLICATION_OVERLAY` for the exact expandable, draggable interaction,
managed by an active-call-only foreground service. The native overlay must
never access media tokens or bypass LiveKit room authorization.

**Important limitation:** Rendering genuine Flutter LiveKit video textures in
an independent native WindowManager overlay needs explicit media/surface
integration and physical device acceptance. Showing avatars in a native
overlay is not proof of video parity. Do not claim feature is complete until
real remote/local video works across app transitions.

**Release gate:** Draft QA branches only. Do not alter main, Build484, the
public download site, production Firebase/LiveKit or users' accounts. Issue
#135 owns this cross-app acceptance; issue #133 is in-app minimization;
issues #129/#131 own optional camera behavior.
