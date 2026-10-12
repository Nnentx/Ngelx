# Build445 approved inbox model

Reference: user-approved white inbox concept from 12 October 2026, with five filter tabs and compact horizontal profiles. Use real account data, not mockup contacts/messages.

Implemented: persistent search, purple accents and separators, compact friend/following strip with online privacy checks and available story rings, direct private-chat navigation preserving existing message authorization, conversation-only All filter and unread sum, existing notification/request pages and create/group/archive/mute/pin flows. Minimized calls have draggable in-app controls and an inbox return banner; existing LiveKit room is resumed without a new join. Background call cleanup runs on sign-out/account change.

Validation: candidate workflow adds four filter/count tests and retains all prior tests. Two-device calls and signed-in native visual inspection remain required. This implementation provides an in-app floating call card; OS picture-in-picture outside the app is not implemented.

Pending consolidated QA: capture preference immediate application/default/scope, story deletion failure, private message/story reply typing jank, remaining localization gaps, incoming ringtone validation, duplicate notification investigation. Note balloons render stored unexpired inboxNote values; note creation is not implemented. Follow/follower/other profile lists retain their existing layout.
