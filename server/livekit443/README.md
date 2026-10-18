# Production adapter candidate — not deployed

`index.mjs` wires revoked-token-aware Firebase Admin auth, shared Firestore UID/IP limits, current chat membership/status, audience/block/ban checks, trusted audio speakers, listener-only live viewers, and an atomic initial-host reservation with a single server-owned owner lock. It does not use client roles, participant names, metadata or API credentials.

The token-core tests and adapter/policy tests can run without production secrets:

    node --test server/livekit441/token-endpoint.test.mjs server/livekit443/*.test.mjs

Deploy the `server` directory as a separate Firebase Functions codebase with Node 22 after installing its dependencies. Configure `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` through Firebase Secret Manager; `LIVEKIT_SERVER_URL` must be the real `wss://` LiveKit endpoint. No credentials are committed. `livekitToken` uses the Firebase project application's default server identity. The API must be callable by the Android HTTP client; the handler independently requires a verified non-anonymous Firebase identity. Preserve existing function codebases rather than replacing the root Firebase configuration.

Use Firestore TTL on `expiresAt` for `_livekit_rate_limits`; owner locks remain bounded and reusable after expiration. Existing client rules deny these server-only collections. Review current room owner immutability and moderator role rules before production rollout. Tests here use a serial transaction harness; run Firebase emulator integration and deployed two-account authorization tests before calling this production-ready.

Required rollout checks: legitimate private/group calls; both-direction blocks; nonmember/removed-member denial; audio audience/speaker changes; banned listeners; duplicate, ended and stale rooms; simultaneous host starts; abandoned reservation expiry; revoked/disabled accounts; rate-limit datastore failures; and actual media transport/reconnect. Pair old APKs only with the existing test path during transition.

Reservations authorize a first token for 2 minutes; tokens expire after 5 minutes. Active media transport is not terminated by this module when a user is later banned or a database room ends. LiveKit server moderation/webhook/cleanup operations and reconnect behavior must be integrated and verified before public production media. A prefix alone does not grant a host token: current account checks, existing active profile pointers and the atomic owner lock are required.

Only after deployed verification, build the Play AAB with `NGELX_PLAY_RELEASE=true` and the real HTTPS `NGELX_LIVEKIT_TOKEN_URL`. Existing APK/AAB defaults remain unchanged by this candidate. Production hosting/project access and real LiveKit secrets are still needed; no endpoint is claimed deployed.

## Build498 QA: reconnect-token microphone moderation (not deployed)

For an **accepted live guest** whose UID appears in the live room's
`guestAudioMutedUids`, the token policy now issues
`canPublishSources: ['camera']`. This denies *new microphone publications*
while retaining camera/video, using only the trusted Firestore room state.
Malformed server permission output fails closed. No caller-controlled
publication-source field is honored.

**Limitations:** This only applies when the token service is actually
deployed and the guest obtains a new token. Previously published microphone
tracks must still be forcibly muted server-side using a room-admin operation;
existing client-only mute controls are insufficient for authoritative live
moderation. The candidate makes no claim that production token services or
room-admin actions are already deployed. Run real device and real LiveKit
server tests before release.

## Build499 QA: server-only guest mute / unmute / kick candidate

The separate `livekitGuestModeration` HTTPS function validates a **revocation-
aware Firebase identity**, refuses anonymous callers, checks that the caller
is the fresh room's actual Firestore owner, and verifies the target is the
**accepted guest in this same live session**. The room's LiveKit name is
read from server Firestore, never selected by the requester. Shared IP/UID
rate limits and strict request validation apply.

A server `roomAdmin` SDK call reduces a connected guest's publishing sources
to camera only for `mute`; any remaining audio tracks are muted. `unmute`
restores future microphone publication permission **without forcing the
remote microphone to switch itself on**. `kick` disconnects the guest if
present. A server-only Firestore transaction then records the mute state or
rejects an expelled guest, rechecking ownership, active heartbeat and accepted
membership. Offline guests still have their server-side state changed.
Remote actions and Firestore commits are not globally atomic; failures
return an error and need operational retry/reconciliation before release.

**Not deployed**. Current Flutter Build489 moderation buttons still update
Firestore directly and do not call this endpoint. Do not claim immediate
server-enforced moderation works end to end until the Flutter caller is
migrated, production SDK/function configuration is approved, emulator rules
and LiveKit SDK are exercised, and two physical Android devices verify all
accepted/rejected/rejoined guest cases. Build484/main/download site untouched.

## Build501 permission-preservation review

LiveKit's `RoomServiceClient.updateParticipant` **replaces** participant
permission values. A moderation call therefore explicitly preserves
`canSubscribe:true`, `canPublish:true` and `canPublishData:true`
while modifying `canPublishSources`. Otherwise a camera-only mute
could unexpectedly remove all publishing or subscription permissions.
Server tests assert the full permission record on mute and unmute.
This is still a QA-only change requiring live server verification.
