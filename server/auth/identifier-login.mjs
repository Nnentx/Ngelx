// Server-only orchestration. No HTTP route is enabled by this module.
// Adapters must use Admin Auth for account identity, a private/unique username
// index, App Check, distributed rate limits and Firebase password verification.
export class LoginFailure extends Error {
  constructor(code = 'invalid-credential') {
    super(code);
    this.code = code;
  }
}

export function parseIdentifier(raw) {
  if (typeof raw !== 'string') throw new LoginFailure();
  const value = raw.trim();
  if (!value || value.length > 254) throw new LoginFailure();
  if (value.includes('@')) {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) throw new LoginFailure();
    return {kind: 'email', value: value.toLowerCase()};
  }
  if (value.startsWith('+')) {
    const phone = value.replace(/[ ()-]/g, '');
    if (!/^\+[1-9][0-9]{7,14}$/.test(phone)) throw new LoginFailure();
    return {kind: 'phone', value: phone};
  }
  if (!/^[a-zA-Z0-9._]{3,20}$/.test(value)) throw new LoginFailure();
  return {kind: 'username', value: value.toLowerCase()};
}

export async function loginWithIdentifier(input, context, adapters) {
  // Every adapter is mandatory: missing protection fails closed.
  for (const name of ['verifyAppCheck', 'consumeRateLimit', 'resolveUniqueUid',
    'getAuthUser', 'verifyPassword', 'createCustomToken']) {
    if (typeof adapters?.[name] !== 'function') throw new LoginFailure('unavailable');
  }
  await adapters.verifyAppCheck(context);
  const identifier = parseIdentifier(input?.identifier);
  const password = input?.password;
  if (typeof password !== 'string' || password.length < 6 || password.length > 4096) {
    throw new LoginFailure();
  }
  // Adapter must hash identifier keys and use a trusted network identity.
  await adapters.consumeRateLimit(identifier, context);
  try {
    const uid = await adapters.resolveUniqueUid(identifier);
    if (typeof uid !== 'string' || !uid || uid.length > 128) throw new LoginFailure();
    const user = await adapters.getAuthUser(uid);
    if (!user || user.uid !== uid || user.disabled || !user.email || user.tenantId ||
        user.multiFactor?.enrolledFactors?.length) throw new LoginFailure();
    // Phone claims come from the linked Auth phone provider, never users/{uid}.
    if (identifier.kind === 'phone' && (user.phoneNumber !== identifier.value ||
        !user.providerData?.some(p => p.providerId === 'phone' &&
          p.phoneNumber === identifier.value))) throw new LoginFailure();
    if (identifier.kind === 'email' &&
        user.email.toLowerCase() !== identifier.value) throw new LoginFailure();
    const verified = await adapters.verifyPassword(user.email, password);
    // A stale or reassigned index cannot authenticate a different UID.
    if (verified?.uid !== uid || verified?.mfaPendingCredential) throw new LoginFailure();
    const latest = await adapters.getAuthUser(uid);
    if (!latest || latest.uid !== uid || latest.disabled || latest.email !== user.email || latest.tenantId ||
        latest.multiFactor?.enrolledFactors?.length ||
        (identifier.kind === 'phone' && (latest.phoneNumber !== identifier.value ||
          !latest.providerData?.some(p => p.providerId === 'phone' &&
            p.phoneNumber === identifier.value)))) throw new LoginFailure();
    const customToken = await adapters.createCustomToken(uid);
    // Do not return email, UID, Firebase refresh token or raw provider errors.
    return {customToken};
  } catch {
    throw new LoginFailure();
  }
}
