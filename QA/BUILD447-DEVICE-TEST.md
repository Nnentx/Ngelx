# Build 447: approved inbox preserved, story and call follow-up

Based on work/build-445-inbox-model (1491bbd). The candidate source pipeline remains intact and tools/build447.patch applies only after Build446 preparation. No production deployment occurs from this candidate workflow.

Changes: member-add selection no longer requires the admin pending-list query; canonical requests still await approval. Story deletion atomically queues the existing authenticated resumable media cleanup and deletes the owned story; rules are required for this transaction. Story keyboard pauses playback, keeps the media repaint isolated and uses direct canonical DM lookup before legacy chat scanning. Minimized call card width increases from 112 to 156 logical pixels and drag position updates do not rebuild card contents. Android ongoing microphone foreground service and a serialized room lifecycle retain audio, hide the camera on app/call minimization, restore only a previously enabled camera and retain manual mute. Group voice/video use square cards, dense three-column scrollable grids, admin-only three-dot mute/remove menus and an animated green ring driven by LiveKit speaking events.

Rules must be validated and deployed through the existing authenticated rules workflow before installing a candidate that uses atomic cleanup or moderation. Client-side call mute/remove is applied by room document listeners; enforcement against modified clients requires LiveKit server moderation and is not claimed here.

Required phone tests:
- Normal member requests one or more additions; founder/admin receives and approves; non-admin cannot approve or alter existing pending target.
- Owner deletes image/video story during media-server outage; disappears on both phones and cleanup remains queued. Another user cannot delete or forge cleanup URLs.
- Story reply keyboard, three repeated replies/reactions and scrolling DM cards remain responsive and messages arrive once.
- Drag larger mini card continuously in private and group calls without resets; rotation/small screen keeps card within usable bounds.
- Switch to GitHub/ChatGPT and screen lock for 30 seconds during private/group audio; peer continues hearing audio; resume requires no restart. Repeat with manually muted mic and Bluetooth.
- Camera previously on: minimize app or call view, peer receives no camera frames; return restores it. Camera previously off must stay off.
- Admin/founder sees three-dot options; member sees no menu. Mute disables target microphone including mini controls. Remove ends only target's call and retains group membership.
- 12 and 15 users: voice and video cards remain reachable by vertical scrolling; controls remain fixed. Green ring follows actual speaking, not merely an enabled mic.
- Approved inbox matches 46740/46741 exactly.
