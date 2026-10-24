# Free verification email adapter

Candidate prepared locally; NOT deployed or connected to an APK.
Uses Cloudflare Workers Free + Resend Free; Firebase remains Spark.
Do not upgrade plans or enable paid overages. Resend Free currently permits
100 messages/day and 3,000/month shared with all other account sends.
Adapter reserves at most 95 attempts/day globally and 3/user/hour, with a
60-second cooldown. Quota reservations are atomic Firestore CAS writes;
errors/contention fail closed. These writes consume existing Spark quotas.
If Firestore quota is exhausted sending stops; no automatic paid fallback.

The Worker uses the existing server-side Google service-account pattern to
look up the actual Firebase account, check revocation using auth_time, and
request a fresh VERIFY_EMAIL action link. Never accept recipients or links
from the client. Keep service-account and Resend keys in Worker secrets.
No secrets belong in Flutter, the repo, or screenshots.

Build: node cloudflare/verification-email/prepare.mjs
Test: node --test cloudflare/verification-email/worker.test.mjs
Deploy only this new Worker after verifying the Cloudflare account is Free.
Configure RESEND_API_KEY (sending-only, ngelxsocial.com) and
GOOGLE_SERVICE_ACCOUNT (existing project service identity with Auth lookup,
OOB link and Firestore counter access). Do not copy or modify existing Workers.
Live API permissions, limits, actual delivery and signing CPU budget must be
verified before activation. Configure NGELX_VERIFICATION_EMAIL_URL with the
real deployed /verify-email endpoint only after successful live checks.
Rebuild the candidate APK; the existing installed APK still uses Firebase mail.

Generated modules derive from the approved existing template and handler.
Regenerate rather than manually editing them. No public image host is needed.
