# Build590 — audio-room reference redesign

Version 1.0.360+590. Public APK: https://github.com/Nnentx/Ngelx/releases/tag/v1.0.360-build590

The supplied video showed the old scrolling information card, action-button wrap, oversized microphone footer and separate blue chat panel. The actual room page now uses a black full-screen composition with a compact host/follow/audience header, three compact functional controls, nine circular microphone positions, transparent comments and a fixed composer/action row.

Implemented:
- All nine positions appear together at normal phone height. Additional legacy speakers scroll inside the stage.
- Host stays first. Speaking/mute indicators, host/moderator labels and user-profile/management actions use existing room and participant data.
- Follow operations, audience list, microphone control, hand requests, reactions, invitations, room minimize/leave and moderator controls are wired to existing behavior.
- Music playback and the audio-PK peer controller remain mounted while their compact controls open dialogs.
- Chat retains message actions, mention suggestions, history scrolling and latest-message navigation.
- Compact phones and enlarged text adapt their stage proportions. Keyboard constraints preserve the composer. System bars use a dark background with light icons.

Validation:
- Exact application QA: https://github.com/Nnentx/Ngelx/actions/runs/41414031341
- Tested application source: 6a7342f992964cd597f76470151a1e80c7115599.
- 230 Node tests, Firestore permission tests, Flutter analysis and 30 Flutter tests passed.
- Complete screen captures cover 393x852 with eight speakers plus one empty seat, host-only room, 360x640 with text scale 1.6, and 320x568. Keyboard, follow/close/request/menu/send actions and all-row visibility are checked.
- Reference normalized from 694px to 393px: first profile center x=84±5, center y=198..218, photo diameter 60..70. These are asserted against the real stage widget.
- Additional settled visual acceptance: https://github.com/Nnentx/Ngelx/actions/runs/41414886813, operations source 6d279c13f5e06a7b5dd6cdf2ec611a7b7160f6ba. Its five tests also require painted composer pixels. Application patch is byte-compared with the exact APK source.
- All four final screenshots inspected. QA portrait fixtures are synthetic; actual rooms use existing user profile photos. Fixtures are outside packaged assets.
- APK publication and anonymous byte comparison: https://github.com/Nnentx/Ngelx/actions/runs/41415953933

APK: NgelX-1.0.360-Build590.apk, 50873066 bytes.
SHA256: ef49dab0566743bac94c483c2f6f3500c4e2e1314a8a0ad06b4a6a79e8f96e0d.
Certificate SHA256: be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa.
Assembled source ZIP SHA256: d2165f1dcca2d32430986a46d1ef4d558b774bf5026875918781563189bd7bed.
Review: https://github.com/Nnentx/Ngelx/pull/202

Site and in-app manifest were updated on Nnentx/ngelx-web. Pages deployment passed: https://github.com/Nnentx/ngelx-web/actions/runs/41416086066
Live canonical/cache-busted updater, website links and public APK bytes: passed https://github.com/Nnentx/ngelx-web/actions/runs/41416410261

No server code or Firestore rules changed. Existing accepted Build589 backend remains the compatible baseline. Physical Android audio/appearance/performance acceptance is still outstanding. The screenshots validate the production rendering components with synthetic room data rather than a live phone/RTC session.

Post-release feature-branch changes are acceptance documentation, screenshot-capture checks and workflow trigger restrictions. The shipped application patch remains byte-identical to source 6a7342f992964cd597f76470151a1e80c7115599.
