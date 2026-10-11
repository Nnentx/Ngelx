# Build438 identifier login — server core, not deployed

Run `node --test server/auth/test/*.test.mjs`.
The 40 dependency-injected tests do not call production Auth or sign anyone in.
`firebase-adapters.mjs` implements the Admin Auth/App Check/private username
lookup interfaces and the bounded Firebase REST password verifier. The REST
endpoint is fixed server-side; redirect following is disabled. The 8-second
deadline covers both request and response parsing, with generic failures.

This module returns only a custom token after Firebase password verification
returns the same UID as the private lookup. It never returns a resolved email.
Passwords retain exact whitespace. Disabled accounts, tenant accounts and MFA
accounts fail closed; those users must continue their existing provider flow.
The existing email login is unchanged.

Before enabling any endpoint, implement and integration-test all adapters:

- Configure Admin Auth, Firestore and allowed App Check app IDs on the server.
- Configure the implemented Firestore transaction limiter with a server secret
  of at least 32 bytes and a trusted deployment remote address. Defaults are 5
  attempts per identifier and 30 per IP in a 60-second window. All attempts count,
  including successful ones. Missing counter storage fails closed. Records use
  domain-separated HMAC keys and contain no raw identifiers or IPs. Expiry is
  enforced by timestamps; TTL cleanup is optional and not enabled here. IPv6
  spelling and IPv4-mapped IPv6 are normalized. No raw X-Forwarded-For is trusted.
  CI also runs a real local Firestore emulator concurrency test with a demo
  project, denied client rules and no production credentials.
- Resolve username through a server-owned unique index. Existing usernameLower
  queries alone do not enforce uniqueness. Migration must reject conflicts and
  coordinate registration/rename ownership transactions with server permissions.
  `username-ownership.mjs` implements existing-profile claim/rename in an Admin
  transaction, protects unindexed legacy owners and retires old names. Its
  migration planner is read-only and never chooses between duplicate owners.
  The claim function is NOT a public endpoint. Before enabling it, freeze direct
  username edits in rules, migrate with server revalidation, and route registration
  through trusted Auth/App Check and the server transaction. Old APK compatibility
  must be coordinated. No accounts have been migrated and no rules changed here.
- Resolve phone using Admin Auth and require a linked phone provider; do not
  query profile recovery phone fields. Phone provider linking needs SMS proof.
- Integration-test the implemented Firebase Auth REST signInWithPassword adapter
  using the project's configured API key; test localId, MFA and timeouts.
- Load current Admin Auth user before and after password verification, then
  mint a Firebase custom token. Do not persist password or provider refresh token.
- Use bounded upstream calls, generic public failures, no response caching,
  body size limits and HTTPS. Handle MFA with the existing supported flow.
- Connect Flutter signInWithCustomToken only after deployed endpoint validation;
  preserve ordinary email login and remembered-account behavior.

No route, billing change, secret installation, migration or deployment is enabled
by these files. The media worker remains unchanged.

Primary references:
- https://firebase.google.com/docs/reference/rest/auth
- https://firebase.google.com/docs/auth/admin/create-custom-tokens
- https://firebase.google.com/docs/auth/admin/manage-users
