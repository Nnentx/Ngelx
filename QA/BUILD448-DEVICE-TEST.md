# Build448 device checks

Keep Build447's approved inbox, group member-add approval and own-story deletion.

1. Install over Build447 on two Android phones; allow NgelX notifications, microphone and camera.
2. Private and group calls: test recipient inside NgelX, in another app, screen locked, and after removing NgelX from recent apps. Expect incoming caller/group title, ringtone, Answer/Reject; answered or ended calls stop ringing. Android force-stop and blocked notification permissions prevent delivery.
3. Background and return: audio continues when leaving NgelX. Hide/minimize the call screen by downward swipe; floating card disappears. Return via call banner; restore only a camera that was previously enabled. Repeatedly switch apps without manually toggling microphone.
4. Group voice/video: founder/admin three-dot menu has readable dark text on white; mute and remove apply only to the ongoing call; removed user remains a group member. Ordinary member cannot moderate. Test 12 and 15 participants and vertical scrolling.
5. Group @mention: choose members with and without usernames; select at a cursor in the middle of text and preserve trailing text. Type continuously, open/close keyboard while voice call is ongoing.
6. Group background: Hafif, Normal, Belirgin, Güçlü update visibility and survive reopening. Only administrators change group background.
7. In an ongoing call, live/audio entry is blocked. Double taps cannot launch two sessions. An ended/failed join releases the session so a later entry works.
8. Live comments: type while video is playing, receive comments and audio activity; verify reduced lag and retained video. Ended live returns with one tap without waiting for network cleanup.
9. Live guest: viewer sends request; host accepts; camera/microphone publish only after mutual consent. Host can invite from viewer menu; viewer may reject. Rejected or ended participation stops publication. Test host and guest disconnect/reconnect and rapid revoke while joining.
10. PK: host selects another active live broadcaster, recipient accepts/rejects; both live owners update only their own live state. Observe 3-minute PK and ending either broadcast.
11. Explore groups: nonmember Katıl creates pending request, never membership. Button says İstek gönderildi; admin accepts and membership opens. Direct old-client self-join fails. Founder/admin requests appear in existing approval UI.
12. Explore ordering: ongoing voice/video group first, then recent messages/call activity; stale ended calls lose priority.

Automated validation: Flutter analysis, call/overlay/session tests, inherited preservation checks, Firestore emulator consent/approval/device-token access tests, server call-push and LiveKit authorization tests. Actual hardware remains necessary for notification delivery, recording indicators, Android microphone background behavior and frame timing.

Deployment: app candidate run 38302110094 passed. Production rules readback SHA256 10b9955aeed10cf4fedfef9ee2cabde9532bf8b3e2fddd2828d1533939b57620. Incoming-call Cloud Function could not deploy because the existing credential cannot enable cloudbuild.googleapis.com (and required Cloud Functions/Artifact Registry APIs). Foreground ringtone/UI are available; terminated-app FCM delivery remains blocked until project owner enables required APIs and deployment permission is available.
