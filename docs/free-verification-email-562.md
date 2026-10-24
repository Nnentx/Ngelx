# Free branded verification email — Build562

Cloudflare Worker deployment succeeded on 2026-10-24. The new isolated endpoint
is https://ngelx-verification-email.alihancaglar76.workers.dev/verify-email .
Firebase stays on Spark. No billing or subscription was changed. Workers Free
was verified from owner screenshots 50688/50689 (100,000 requests/day, Upgrade,
$0) for the matching alihancaglar76 account because the existing deployment token
cannot read subscriptions (403).

The sending-only Resend key is restricted to ngelxsocial.com and stored as a
GitHub Actions secret, then as an encrypted Worker secret. The existing Firebase
server identity is also stored as a Worker secret. No secret values are in source.
Actual Auth lookup/link permissions and Firestore quota reads were verified.
Anonymous requests to the configured deployed endpoint return 401.

The approved HTML and CID image were accepted by Resend's official
`delivered@resend.dev` test recipient; the dashboard reports delivered. This is
a provider simulation, not proof of receipt/rendering in a real Gmail inbox.
An authenticated disposable Auth fixture also exercised the actual deployed
Worker: it generated a real Firebase action link, delivered to the official
Resend simulator, rejected recipient override and enforced resend cooldown.
The fixture was removed with UID/email guards. Existing users were unchanged.
Real-device registration/resend, Gmail rendering and button activation remain
acceptance checks after the new APK is installed. The existing Build561 APK still uses Firebase mail.

Build562 preserves the existing source regeneration, package, update signer,
inbox and other Build561 behavior. It embeds the deployed email endpoint and
increments version to 1.0.332 (562). Profile-post comment lag remains open;
this release must not be described as fixing it.

Limits: Resend Free 100/day and 3,000/month; Worker conservatively reserves at
most 95 attempts/day, three/user/hour and a 60-second cooldown. The provider's
quota is shared with any other sends on the account. Firestore counters consume
existing free quotas; unavailable quota storage fails closed. No paid fallback.

## Verified downloadable APK

Build562 Actions run: https://github.com/Nnentx/Ngelx/actions/runs/40120801727
completed successfully. APK: NgelX-1.0.332-Build562.apk, 47,507,827 bytes.
SHA-256: `7b13237e789fd87be25dc6e5ba99f6f562e6230afe426013e0524ac630483c40`.
The downloaded artifact passed ZIP integrity and transport digest checks. Its
compiled ARM64 app contains the actual verification endpoint. APK v2 signer
SHA-256 matches the installed update identity:
`be20b27f0ba1f4decd2941d410b1536de89e48dc894f04f038f9d26b11ecd6aa`.
CI additionally verified the APK signature and exact package/version using
apksigner and aapt. This file was delivered for owner device acceptance; the
website download link and existing installed app were not changed automatically.
