# NgelX authenticated free call push

This Worker sends FCM data notifications after an app has committed its call record. It uses the existing Firebase project and requires no Cloud Functions or Cloud Build deployment. It has no R2, AI, media, paid-plan upgrade or custom-domain binding.

## Security and free-tier bounds

- Firebase ID-token signature, project, expiry and anonymous-provider checks; Authentication user lookup also rejects disabled users and revoked sessions.
- The persisted chat record determines caller, room, current status and recipients. Client-supplied tokens, recipients and titles are rejected.
- Both block directions, account state and notification preferences are enforced.
- Four recipients per request, two most recently registered devices per recipient; at most 60 chat members.
- Each authenticated account gets at most 24 requests per minute. A stored compare-and-set counter fails closed on concurrent updates.
- Server-only leases suppress concurrent/replayed dispatches. Lease documents are reused per chat/recipient/event rather than growing per call. Transient retries occur after 15 seconds; FCM is an external service, so delivery is not an exactly-once guarantee.
- The request has a bounded external-call budget compatible with the Workers Free 50-subrequest limit. Network waiting is excluded from CPU time, but the real Free CPU limit must still be measured with authenticated requests after deployment.
- The Google service account is an encrypted Worker secret; it is never included in the APK or repository.

## Status

18 unit tests pass, including real RSA signature verification and tampered token rejection. Firebase data read/write, Authentication lookup and FCM validate-only access have passed the deployment preflight. No test message was delivered to a person.

Deployment is blocked: the existing Cloudflare token cannot read account subscriptions. The preflight deliberately refuses deployment when it cannot confirm Workers Free. No paid plan or billing account was activated. Required next access: a read-only verification of the account's Workers plan, or a Cloudflare token that can read subscriptions (Billing Read).

`tools/apply_build452.py` integrates outgoing ringing and cancellation events into the existing Android call observer. The app requires a confirmed deployed HTTPS URL via `NGELX_CALL_PUSH_URL`; the default is empty and performs no push requests. Build451 APK does not include this integration. A new APK must be built after deployment and tested on two devices, including background, screen-off, cancellation, group calls and notification permissions. Android force-stop restrictions remain a platform constraint.

Firestore indexes remain a separate permission issue. This Worker does not change security rules, create indexes, or weaken the approved-post query.
