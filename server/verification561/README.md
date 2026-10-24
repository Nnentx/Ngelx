# NgelX branded verification email / Build561

The approved white-card, lavender, envelope/shield and purple-blue button concept is implemented as table-based HTML plus a plain-text alternative. The main CTA is real HTML text linked to a freshly generated Firebase action; it is not a screenshot of a button. The illustration is an inline CID attachment, so a separate public image host is unnecessary. Gradients have a solid-purple fallback. Rendering varies by mail client; a real Gmail/Outlook delivery acceptance check remains required. No production email has been sent during development.

`verification-envelope.png` was derived using the built-in image tool from the user's approved reference. Prompt: extract only the purple-blue envelope/checkmark-shield illustration, preserve colors/materials/proportions, white background, remove all typography and card/button elements. The complete reference remains authoritative for the visual direction.

`verificationEmail561` is exported from the existing Functions entry point. Before activation, the existing Firebase project must have the `NGELX_EMAIL_API_KEY` secret and a verified sender configured as `NGELX_EMAIL_FROM=NgelX <address@verified-domain>`. Reuse the configured provider/domain; this change creates no provider account, billing plan or domain. Deploy only the reviewed `verificationEmail561` export. Other Functions and Firestore rules are outside this change.

Set the repository Actions variable `NGELX_VERIFICATION_EMAIL_URL` to the actual deployed HTTPS endpoint, then build the candidate. No endpoint is guessed. If the variable is empty, registration and resend retain the existing native Firebase sender; the branded HTML is **not** active in that case. A configured endpoint failure is reported, rather than silently claiming that a branded message was sent. Recipient, display name and action link are resolved on the server from the verified Firebase user; client-supplied recipient/link fields are rejected.

Verification: `node --test server/verification561/verification.test.mjs` (synthetic one-time codes only). The suite covers actual-recipient selection, HTML escaping, inline-image integrity, wrong action/host rejection, revoked/anonymous/disabled accounts, rate limiting, already-verified accounts, and delivery failures.

Primary API reference: https://resend.com/changelog/embed-images-using-cid and https://firebase.google.com/docs/auth/admin/email-action-links .
