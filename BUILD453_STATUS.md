# Build 453 device fixes — 2026-10-14

Candidate: 1.0.228 / 453, commit a556df09ea156e51e2838d4e84cbe859b29360c3.
Build run: https://github.com/Nnentx/Ngelx/actions/runs/38521285091

## Implemented
- Preserve existing app architecture, navigation, theme and call/live media ownership.
- Stable live composer focus and draft, no automatic unfocus on keyboard send.
- Role-specific approved live controls and compact readable comment cards; retain pinned-comment moderation.
- Bounded overlapping hearts rise, fade and are removed; rapid taps remain responsive.
- Host guest selection/invite/accept/reject/remove, viewer request/cancel/accept; refresh connection token and verify acceptance before publishing, including reconnect.
- Private and group photos keep their natural aspect ratio with larger previews and display-sized decoding.
- Larger inbox avatars, readable unread/read hierarchy and group sender previews.
- Cache live/inbox profile sources; remove unused archive listener; aggregate comment count instead of rereading all comments.
- Dispatch committed private/group calls directly; retry device registration without blocking incoming listeners, including resume, account changes and transient failures.
- Avoid replacing an already ringing notification; show actionable notice when notification/ringer settings prevent sound.
- Free Worker reports missing/dead device registrations, cleans only confirmed unregistered tokens, and does not mark unsuccessful delivery as successful.

## Verified
- Initial Build 453 APK pipeline passed.
- Updated Worker: 23 tests passed; free deployment succeeded (run 38521044812).
- Deployed authenticated probe passed after update, sent zero notifications, and cleaned its synthetic fixture.
- Final APK pipeline: widget/behavior/authorization checks passed; remaining signing/build checks in progress.
- Previous group-call diagnostic: 7 recipients, 2 with registered devices, 5 without. This is not a live ringtone test.

## Still requires verification or access
- Firestore composite collection index: posts, status ASC, createdAt DESC. Service-account creation was denied; current Firebase browser redirects to Google sign-in with 502 Connection refused. No IAM or billing changes made.
- Real two-phone ringtone tests: foreground/background/screen locked, private/group, answer/reject/end cleanup.
- Real host/guest audio/video, rejection/removal stops tracks, viewer leaving does not stop host.
- Keyboard behavior and overall frame/navigation latency on real phone; improvements do not prove all performance issues are resolved.
- New release should only publish bytes from the exact successful candidate, with SHA-256 and original signing-certificate checks.
- Official APK website remains Build 452 until final release and website write access are verified.
