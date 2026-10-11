# Build438 identifier login — server core, not deployed

Run `node --test server/auth/test/*.test.mjs`.
The 28 dependency-injected tests do not call production Auth or sign anyone in.
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
- Enforce distributed network and hashed identifier rate limits with expiry;
  neither raw passwords nor account identifiers belong in logs.
- Resolve username through a server-owned unique index. Existing usernameLower
  queries alone do not enforce uniqueness. Migration must reject conflicts and
  coordinate registration/rename ownership transactions with server permissions.
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
