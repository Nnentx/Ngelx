Build543 continues verified Build542 without replacing it.

Implemented in the Android candidate:
- Group KATIL reads the row's call document immediately and selects the latest server call timestamp, preventing an old room heartbeat from masking a new call. Slight device clock skew is tolerated; ended/stale calls stay hidden.
- The existing LiveKit room renders all twelve participants in Android system PiP over the launcher/other apps. Published video is real; camera-off participants show profile circles. Android controls window size/drag and exposes microphone/speaker/end actions. No second connection, token or camera capture is created.
- Background hangup is self-only for groups, including the initiating caller; it persists the existing Build542 leave record before server retry.
- Community counters fail independently, moderator-only views do not query admin-only membership requests, short legacy community names can be edited, and a deleted management root no longer spins forever.
- A founder-only typed confirmation surface is included for full record deletion.

Production restrictions and remaining prerequisites:
- Read-only diagnosis run 39386926408 found deployed rules fingerprint 0307f035ad68f047, with community456 moderation/comment slow-mode guards absent. The client cannot bypass those deployed rules. No production rules/data/functions were changed.
- Isolated emulator candidates add bounded founder/admin settings compatibility and freeze root/nested writes during server deletion; client deletion and role promotion remain denied.
- server/community543 is a prepared, authenticated, rate-limited recursive record deletion endpoint, not a deployed service. NGELX_COMMUNITY_DELETE_URL defaults to empty; the Android UI explicitly states the service is not enabled and does not claim deletion. Enabling requires a separately authorized backend/rules release. No destructive operation was performed.
- Recursive deletion covers Firestore community records and all nested collections. Unrelated users/chats and arbitrary shared media URLs must never be deleted. A separate ownership-aware media purge integration is required before promising physical deletion of every external uploaded file.
- Native system PiP is constrained by Android/device settings. Two physical devices and permission-disabled cases still need runtime QA; generated previews are design references, not proof of exact OS window styling.
