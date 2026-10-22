# Free live moderation backend

Runs the existing host-only moderation core on Cloudflare Workers, without
Firebase Functions or Secret Manager. The adapter uses Web Crypto, LiveKit
RoomService HTTPS calls, Firebase ID-token verification with revocation lookup,
and Firestore REST transactions. Current media still uses the existing LiveKit
project; this worker is a control service, not a video relay.

Free Workers has usage limits. The rollout never enables billing or changes the
account plan. Deployment is gated on a verified matching Cloudflare account,
an unpaid Workers subscription, and existing project credentials. Unknown plan
status pauses deployment. No secret values enter logs or artifacts.

Required Worker secrets: GOOGLE_SERVICE_ACCOUNT (existing Firebase deployment
identity), LIVEKIT_API_KEY, LIVEKIT_API_SECRET, LIVEKIT_SERVER_URL. LiveKit
credentials must belong to the project already used by this app. Do not put them
in Android code, documents, screenshots, or chat messages. The existing GitHub
Actions secrets feed the deployment; only presence is reported by preflight.

Only after deployed authorization and real-room validation should the APK define
NGELX_LIVEKIT_GUEST_MODERATION_URL to the Worker's /moderate URL. Until then
Build554 stays unchanged; no completed moderation feature is claimed. A Worker
alone does not make all existing media hosting or future traffic free/unlimited.

Tests:

    node --test cloudflare/live-moderation/test/*.test.mjs server/livekit443/*.test.mjs
