# NgelX authenticated free call push

This Worker sends FCM data notifications after an app has committed its call record. It uses the existing Firebase project and requires no Cloud Functions or Cloud Build deployment. It has no R2, AI, media, paid-plan upgrade or custom-domain binding.

## Security and free-tier bounds

- Firebase ID-token signature, project, expiry and anonymous-provider checks; Authentication user lookup also rejects disabled users and revoked sessions.
- The persisted chat record determines caller, room, current status and recipients. Client-supplied tokens, recipients and titles are rejected.
- Both block directions, account state and notification preferences are enforced.
- Four recipients per request, two most recently registered devices per recipient; at most 60 chat members.
- Each authenticated account gets at most 40 requests per minute. A stored compare-and-set counter fails closed on concurrent updates.
- Server-only leases suppress concurrent/replayed dispatches. Lease documents are reused per chat/recipient/event rather than growing per call. Transient retries occur after 15 seconds; FCM is an external service, so delivery is not an exactly-once guarantee.
- The request has a bounded external-call budget compatible with the Workers Free 50-subrequest limit. Network waiting is excluded from CPU time, but the real Free CPU limit must still be measured with authenticated requests after deployment.
- The Google service account is an encrypted Worker secret; it is never included in the APK or repository.

## Status

21 unit tests pass, including real RSA signature verification and tampered token rejection. Firebase data read/write, Authentication lookup and FCM validate-only access have passed the deployment preflight. No test message was delivered to a person.

The owner supplied dashboard evidence on 2026-10-14 Europe/Istanbul (47117.jpg): Workers Free, $0, Current plan. The preflight matches the API account's workers.dev subdomain to alihancaglar76 (47115.jpg) before accepting this evidence when subscriptions returns 403. Any available contradictory paid subscription still aborts deployment. The deprecated usage_model field is not treated as a subscription check (Cloudflare Wrangler deprecations documentation). No billing or subscription mutation is performed. Deployment succeeded in GitHub Actions run 38469173387. The deployed endpoint https://ngelx-call-push.alihancaglar76.workers.dev/health returns HTTP 200 with version 452. POST /call with a valid-shaped unauthenticated request returns HTTP 401. Encrypted Google service-account secret installation succeeded. Authenticated device delivery and Free CPU consumption remain unverified.

`tools/apply_build452.py` integrates outgoing ringing and cancellation events into the existing Android call observer. The app requires a confirmed deployed HTTPS URL via `NGELX_CALL_PUSH_URL`; the default is empty and performs no push requests. Build451 APK does not include this integration. The Build452 app workflow now builds version 1.0.227 / 452 with the verified deployed URL and the existing signing certificate. APK generation succeeded in run 38469429163: version 1.0.227 / 452, install-compatible existing certificate verified. Flutter analysis, behavior tests and Firestore emulator checks passed. APK SHA-256: 9f59102d9d08d2518483470f11e76ecdcf63ca6d38becccfb60731e46b3ab127. The artifact is ready; it must still be tested on two devices, including background, screen-off, cancellation, group calls and notification permissions. Android force-stop restrictions remain a platform constraint.

A separate additive-only index workflow (run 38469889603) confirmed HTTP 403 on index administration. The existing Firebase deployment service account needs roles/datastore.indexAdmin, or the project owner must create the exact composite index in Firebase: collection ID posts; query scope COLLECTION; status ASCENDING; createdAt DESCENDING. tools/ensure_community_index452.mjs is idempotent, creates only this missing index, checks READY, and never changes rules, billing, or other indexes. The call-push Worker does not weaken the approved-post query.


Application verification completed successfully after replacing the unavailable HTTP client with the existing Dio client and bounding group cancellation dispatch: https://github.com/Nnentx/Ngelx/actions/runs/38464121891 . No new APK with a live Worker endpoint has been produced.
