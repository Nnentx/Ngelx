import {LoginFailure} from './identifier-login.mjs';

// Server configuration only: no client-supplied endpoint or API key.
export function createPasswordVerifier({apiKey, fetchImpl = fetch, timeoutMs = 8000}) {
  if (typeof apiKey !== 'string' || !apiKey || !Number.isFinite(timeoutMs) ||
      timeoutMs < 1 || timeoutMs > 20000) throw new LoginFailure('unavailable');
  const endpoint = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' +
    encodeURIComponent(apiKey);
  return async (email, password) => {
    const controller = new AbortController();
    let timer;
    // Race bounds the whole operation, including body parsing. Abort alone is
    // insufficient when an upstream/adapter does not honor AbortSignal.
    const deadline = new Promise((_, reject) => {
      timer = setTimeout(() => {
        controller.abort();
        reject(new LoginFailure('unavailable'));
      }, timeoutMs);
    });
    try {
      return await Promise.race([deadline, (async () => {
        const response = await fetchImpl(endpoint, {
          method:'POST', redirect:'error', cache:'no-store',
          headers:{'Content-Type':'application/json'},
          body:JSON.stringify({email,password,returnSecureToken:true}),
          signal:controller.signal,
        });
        if (!response.ok) throw new LoginFailure();
        const body = await response.json();
        if (body?.mfaPendingCredential || body?.mfaInfo?.length ||
            typeof body?.localId !== 'string' || !body.localId ||
            body.localId.length > 128 || typeof body.idToken !== 'string' ||
            !body.idToken || body.registered === false) throw new LoginFailure();
        // Refresh token, ID token, resolved email and raw error body never leave
        // this adapter. The core checks UID before it signs a custom token.
        return {uid:body.localId};
      })()]);
    } catch (error) {
      if (error instanceof LoginFailure) throw error;
      throw new LoginFailure('unavailable');
    } finally {
      clearTimeout(timer);
    }
  };
}

export function createAdminIdentityAdapters({auth, db, appCheck,
    allowedAppIds, apiKey, consumeRateLimit, fetchImpl, timeoutMs}) {
  if (!auth || !db || !appCheck || !Array.isArray(allowedAppIds) ||
      !allowedAppIds.length || typeof consumeRateLimit !== 'function') {
    throw new LoginFailure('unavailable');
  }
  const verifyPassword = createPasswordVerifier({apiKey,fetchImpl,timeoutMs});
  return {
    verifyPassword, consumeRateLimit,
    verifyAppCheck:async context => {
      if (typeof context?.appCheckToken !== 'string' || !context.appCheckToken ||
          context.appCheckToken.length > 8192) throw new LoginFailure();
      const result = await appCheck.verifyToken(context.appCheckToken);
      if (!allowedAppIds.includes(result.appId)) throw new LoginFailure();
    },
    resolveUniqueUid:async identifier => {
      if (identifier.kind === 'email') {
        return (await auth.getUserByEmail(identifier.value)).uid;
      }
      if (identifier.kind === 'phone') {
        return (await auth.getUserByPhoneNumber(identifier.value)).uid;
      }
      // Server-owned index is mandatory. No fallback to editable profile phone
      // or a public username query; migration/registration must maintain it.
      const record = await db.collection('login_usernames').doc(identifier.value).get();
      const value = record.data();
      if (!record.exists || value?.status !== 'active' ||
          typeof value.uid !== 'string') throw new LoginFailure();
      const profile = await db.collection('users').doc(value.uid).get();
      if (!profile.exists || profile.data()?.usernameLower !== identifier.value) {
        throw new LoginFailure();
      }
      return value.uid;
    },
    getAuthUser:uid => auth.getUser(uid),
    createCustomToken:uid => auth.createCustomToken(uid),
  };
}
