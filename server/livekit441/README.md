# Production LiveKit token integration — not deployed

The Flutter Play build enforces NGELX_PLAY_RELEASE=true and never falls back to DevelopmentTokenSource. Configure NGELX_LIVEKIT_TOKEN_URL with an HTTPS endpoint after deploying and verifying this core.

Wire verifyFirebaseToken to Firebase Admin verifyIdToken(token, true). Reject disabled, anonymous and revoked sessions. authorizeRoom must read authoritative Firestore records and check call membership/status, blocks, room bans, visibility, trusted speaker/host permissions and current room identity before returning allowed=true. It must not trust participant_attributes or participant_name. Implement a shared UID/IP rate limiter. API key and secret belong only in the hosting secret manager.

Live/audio hosts request a token before writing the room record. The server adapter must create/authorize a short-lived owner reservation atomically before minting that first token; matching user-prefixed room names alone are not sufficient authorization. A server-side reservation expiry and one-active-room lock are required. Public listeners must never gain publish rights from client role strings. Private/friends/following visibility needs server-side relationship checks.

The tested core intentionally requires these adapters and does not include an unsafe allow-all default. Deploying it without verified authorization operations is a release blocker. Test two authenticated accounts, blocked users, ended/stale rooms, reconnects and revoked sessions against the deployed endpoint before enabling production calls.
