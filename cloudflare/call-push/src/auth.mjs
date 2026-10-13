let jwksCache=null,jwksExpiresAt=0;
function decodeBase64Url(value) {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/');
  const padded = normalized.padEnd(Math.ceil(normalized.length / 4) * 4, '=');
  const raw = atob(padded);
  const out = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) out[i] = raw.charCodeAt(i);
  return out;
}

function decodeJwtPart(value) {
  return JSON.parse(new TextDecoder().decode(decodeBase64Url(value)));
}

async function getFirebaseJwks() {
  const now = Date.now();
  if (jwksCache && now < jwksExpiresAt) return jwksCache;

  const response = await fetch(
    'https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com',
    {cf: {cacheTtl: 3600, cacheEverything: true}},
  );
  if (!response.ok) throw new Error('Firebase public keys could not be loaded');

  const body = await response.json();
  const maxAge = Number(
    (response.headers.get('cache-control') || '').match(/max-age=(\d+)/)?.[1] || 3600,
  );
  jwksCache = body.keys || [];
  jwksExpiresAt = now + Math.max(300, maxAge - 60) * 1000;
  return jwksCache;
}

export async function verifyFirebaseIdToken(request, env) {
  const auth = request.headers.get('authorization') || '';
  if (!auth.startsWith('Bearer ')) throw new Error('Missing Firebase token');

  const token = auth.slice(7).trim();
  if(token.length>8192)throw new Error('Invalid token size');
  const parts = token.split('.');
  if (parts.length !== 3) throw new Error('Invalid Firebase token');

  const header = decodeJwtPart(parts[0]);
  const payload = decodeJwtPart(parts[1]);
  if (header.alg !== 'RS256' || !header.kid) throw new Error('Invalid token algorithm');

  const keys = await getFirebaseJwks();
  const jwk = keys.find((x) => x.kid === header.kid);
  if (!jwk) throw new Error('Firebase signing key not found');

  const key = await crypto.subtle.importKey(
    'jwk',
    jwk,
    {name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256'},
    false,
    ['verify'],
  );

  const verified = await crypto.subtle.verify(
    {name: 'RSASSA-PKCS1-v1_5'},
    key,
    decodeBase64Url(parts[2]),
    new TextEncoder().encode(parts[0] + '.' + parts[1]),
  );
  if (!verified) throw new Error('Invalid Firebase signature');

  const now = Math.floor(Date.now() / 1000);
  const projectId = env.FIREBASE_PROJECT_ID;
  if (payload.aud !== projectId) throw new Error('Invalid Firebase audience');
  if (payload.iss !== 'https://securetoken.google.com/' + projectId) throw new Error('Invalid Firebase issuer');
  if (typeof payload.sub !== 'string' || payload.sub.length === 0 || payload.sub.length > 128) {
    throw new Error('Invalid Firebase subject');
  }
  if (typeof payload.exp !== 'number' || payload.exp <= now) throw new Error('Firebase token expired');
  if (typeof payload.iat !== 'number' || payload.iat > now + 300) throw new Error('Invalid Firebase issue time');

  if(payload.firebase?.sign_in_provider==='anonymous')throw new Error('Anonymous user');
  return payload;
}

