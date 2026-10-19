# Build540 live and group-call UI implementation plan (review only)

Baseline: Build539 commit 99bf63e0c2328864340c118a290f37bd18e780e1. Preserve working auth, messaging, camera/RTC, Firebase config, package com.nnentx.ngelx_app, signing identity, and version upgrade path. Never deploy or merge automatically.

## Reference behavior
User-provided TikTok-style live and Messenger-style group-call videos are visual/interaction references, not permission to copy trademarks/assets.

### Live host
- Keep full-screen video; compact translucent controls overlaid with safe-area padding.
- Anchor latest 3-4 comments directly above compact input bar; show join/leave as deduplicated transient system events; allow scrolling older comments.
- Keep host-only guest management and request accept/deny; viewer can request guest access, never directly add a guest.
- Separate current viewers from total unique joins; count from server-backed presence, reconcile disconnect/rejoin, avoid treating displayed zero as proof of a bug.
- Place reconnect/error messages outside comment hit targets; only show video unavailable when stream truly fails.
- Keep existing virtual QA gifts labeled as such; no real payment/coin changes.

### Group voice/video call
- Minimize without ending call; in-app draggable mini-window with restore action and persistent call state.
- Android picture-in-picture only where supported, respecting permissions and lifecycle.
- Group participant grid, microphone/camera/speaker controls, invite, and explicit hangup.
- Compact overlay controls auto-hide and restore on tap; back navigation must not terminate an active call unexpectedly.
- Protect RTC tracks and state across route transitions and background/foreground transitions.

## Implementation gates
1. Inventory actual Flutter widget and RTC lifecycle code in generated Build539 source (workflow applies Build395..Build536 generators).
2. Extract role-specific live controls without changing existing connection services.
3. Add layout/widget tests for comment anchor, safe-area, guest roles, and navigation.
4. Add call state tests for minimize/restore, hangup, PiP lifecycle, participant changes.
5. Build review-only signed APK using pinned existing signing certificate; verify versionCode increment and install-over compatibility.
6. Real two-account device test: host/viewer counters, guest request, chat overlay, group call audio/video, app background and resume.

No implementation or phone-runtime acceptance is claimed by this specification.
