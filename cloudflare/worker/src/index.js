const ALLOWED_KINDS = new Set([
  'photos',
  'videos',
  'music',
  'profiles',
  'stories',
  'chats',
  'groups',
  'support',
  'chat-backgrounds',
  'profile-intros',
  'thumbnails',
  'gifs',
  'chat-files',
  'chat-audio',
]);

const MAX_BYTES = {
  videos: 80 * 1024 * 1024,
  'profile-intros': 35 * 1024 * 1024,
  music: 15 * 1024 * 1024,
  'chat-files': 30 * 1024 * 1024,
  'chat-audio': 15 * 1024 * 1024,
  gifs: 12 * 1024 * 1024,
  default: 10 * 1024 * 1024,
};

let jwksCache = null;
let jwksExpiresAt = 0;

function cors() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type, X-NgelX-Filename, X-NgelX-Client',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
  };
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {'content-type': 'application/json; charset=utf-8', ...cors()},
  });
}

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

async function verifyFirebaseIdToken(request, env) {
  const auth = request.headers.get('authorization') || '';
  if (!auth.startsWith('Bearer ')) throw new Error('Missing Firebase token');

  const token = auth.slice(7).trim();
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

  return payload;
}

function cleanExt(raw) {
  const value = (raw || 'bin').toLowerCase().replace(/[^a-z0-9]/g, '');
  return value.slice(0, 8) || 'bin';
}

function cleanKind(raw) {
  return ALLOWED_KINDS.has(raw) ? raw : null;
}

function cleanUploadId(raw) {
  const value = String(raw || '');
  return /^[A-Za-z0-9_-]{8,80}$/.test(value) ? value : null;
}


function encodeKeyForUrl(key) {
  return key.split('/').map(encodeURIComponent).join('/');
}

function contentTypeFor(ext, supplied) {
  if (supplied && supplied !== 'application/octet-stream') return supplied;
  const map = {
    jpg: 'image/jpeg',
    jpeg: 'image/jpeg',
    png: 'image/png',
    webp: 'image/webp',
    gif: 'image/gif',
    heic: 'image/heic',
    heif: 'image/heif',
    mp4: 'video/mp4',
    mov: 'video/quicktime',
    mp3: 'audio/mpeg',
    m4a: 'audio/mp4',
    aac: 'audio/aac',
    wav: 'audio/wav',
    ogg: 'audio/ogg',
  };
  return map[ext] || 'application/octet-stream';
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, {status: 204, headers: cors()});
    }

    const url = new URL(request.url);

    if (request.method === 'GET' && url.pathname === '/health') {
      try {
        await env.MEDIA.head('__ngelx_healthcheck__');
        return json({ok: true, service: 'ngelx-r2-media', r2: true});
      } catch (e) {
        return json({ok: false, service: 'ngelx-r2-media', r2: false, message: String(e?.message || e)}, 503);
      }
    }

    if (request.method === 'GET' && url.pathname.startsWith('/media/')) {
      const key = decodeURIComponent(url.pathname.slice('/media/'.length));
      if (!key || key.includes('..')) return json({error: 'invalid_key'}, 400);
      const object = await env.MEDIA.get(key);
      if (!object) return json({error: 'not_found'}, 404);

      const headers = new Headers(cors());
      object.writeHttpMetadata(headers);
      headers.set('etag', object.httpEtag);
      headers.set('cache-control', 'public, max-age=31536000, immutable');
      return new Response(object.body, {headers});
    }

    if (request.method === 'POST' && url.pathname === '/upload/chunk') {
      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        return json({error: 'unauthorized', message: String(e.message || e)}, 401);
      }

      const kind = cleanKind(url.searchParams.get('kind'));
      const ext = cleanExt(url.searchParams.get('ext'));
      const uploadId = cleanUploadId(url.searchParams.get('uploadId'));
      const index = Number(url.searchParams.get('index'));
      const total = Number(url.searchParams.get('total'));
      if (!kind || !uploadId || !Number.isInteger(index) || !Number.isInteger(total) ||
          index < 0 || total < 1 || total > 64 || index >= total) {
        return json({error: 'invalid_chunk_request'}, 400);
      }

      const announced = Number(request.headers.get('content-length') || 0);
      if (announced <= 0 || announced > 300 * 1024) {
        return json({error: 'invalid_chunk_size'}, 413);
      }
      const bytes = await request.arrayBuffer();
      if (!bytes.byteLength || bytes.byteLength > 300 * 1024) {
        return json({error: 'invalid_chunk_size'}, 413);
      }
      const chunkKey = '__ngelx_chunks/' + claims.sub + '/' + uploadId + '/' + index;
      await env.MEDIA.put(chunkKey, bytes, {
        httpMetadata: {contentType: 'application/octet-stream'},
        customMetadata: {uid: claims.sub, kind, ext, uploadId, index: String(index), total: String(total)},
      });
      return json({ok: true, index, total}, 201);
    }

    if (request.method === 'POST' && url.pathname === '/upload/complete') {
      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        return json({error: 'unauthorized', message: String(e.message || e)}, 401);
      }

      const kind = cleanKind(url.searchParams.get('kind'));
      const ext = cleanExt(url.searchParams.get('ext'));
      const uploadId = cleanUploadId(url.searchParams.get('uploadId'));
      const total = Number(url.searchParams.get('total'));
      if (!kind || !uploadId || !Number.isInteger(total) || total < 1 || total > 64) {
        return json({error: 'invalid_complete_request'}, 400);
      }

      const maxBytes = MAX_BYTES[kind] || MAX_BYTES.default;
      const chunks = [];
      let size = 0;
      for (let i = 0; i < total; i++) {
        const chunkKey = '__ngelx_chunks/' + claims.sub + '/' + uploadId + '/' + i;
        const object = await env.MEDIA.get(chunkKey);
        if (!object) return json({error: 'missing_chunk', index: i}, 409);
        const part = new Uint8Array(await object.arrayBuffer());
        size += part.byteLength;
        if (size > maxBytes) return json({error: 'file_too_large', maxBytes}, 413);
        chunks.push(part);
      }

      const merged = new Uint8Array(size);
      let offset = 0;
      for (const part of chunks) {
        merged.set(part, offset);
        offset += part.byteLength;
      }

      const uid = claims.sub;
      const key = kind + '/' + uid + '/' + Date.now() + '_' + crypto.randomUUID() + '.' + ext;
      const contentType = contentTypeFor(ext, url.searchParams.get('contentType'));
      await env.MEDIA.put(key, merged, {
        httpMetadata: {contentType, cacheControl: 'public, max-age=31536000, immutable'},
        customMetadata: {uid, kind, transport: 'chunked'},
      });

      await Promise.all(Array.from({length: total}, (_, i) =>
        env.MEDIA.delete('__ngelx_chunks/' + uid + '/' + uploadId + '/' + i)
      ));

      return json({
        ok: true,
        key,
        url: url.origin + '/media/' + encodeKeyForUrl(key),
        size,
      }, 201);
    }

    if (request.method === 'POST' && url.pathname === '/upload') {
      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        return json({error: 'unauthorized', message: String(e.message || e)}, 401);
      }

      const kind = cleanKind(url.searchParams.get('kind'));
      if (!kind) return json({error: 'invalid_kind'}, 400);

      const ext = cleanExt(url.searchParams.get('ext'));
      const maxBytes = MAX_BYTES[kind] || MAX_BYTES.default;
      const announced = Number(request.headers.get('content-length') || 0);
      if (announced > maxBytes * 1.5) return json({error: 'file_too_large', maxBytes}, 413);

      const uid = claims.sub;
      const key = kind + '/' + uid + '/' + Date.now() + '_' + crypto.randomUUID() + '.' + ext;

      try {
        let saved;
        let contentType = contentTypeFor(ext, request.headers.get('content-type'));
        const encoding = url.searchParams.get('encoding') || '';

        if (encoding === 'base64') {
          const payload = await request.json();
          const raw = typeof payload?.data === 'string' ? payload.data : '';
          if (!raw) return json({error: 'empty_file'}, 400);
          const binary = atob(raw);
          if (!binary.length) return json({error: 'empty_file'}, 400);
          if (binary.length > maxBytes) return json({error: 'file_too_large', maxBytes}, 413);
          const bytes = new Uint8Array(binary.length);
          for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
          contentType = contentTypeFor(ext, payload?.contentType || null);
          saved = await env.MEDIA.put(key, bytes, {
            httpMetadata: {contentType, cacheControl: 'public, max-age=31536000, immutable'},
            customMetadata: {uid, kind, transport: 'base64'},
          });
        } else {
          if (!request.body) return json({error: 'empty_file'}, 400);
          const streamKinds = new Set(['videos', 'profile-intros', 'music', 'chat-files', 'chat-audio']);

          if (streamKinds.has(kind) && announced > 0) {
            saved = await env.MEDIA.put(key, request.body, {
              httpMetadata: {contentType, cacheControl: 'public, max-age=31536000, immutable'},
              customMetadata: {uid, kind},
            });
          } else {
            const bytes = await request.arrayBuffer();
            if (!bytes.byteLength) return json({error: 'empty_file'}, 400);
            if (bytes.byteLength > maxBytes) return json({error: 'file_too_large', maxBytes}, 413);
            saved = await env.MEDIA.put(key, bytes, {
              httpMetadata: {contentType, cacheControl: 'public, max-age=31536000, immutable'},
              customMetadata: {uid, kind},
            });
          }
        }

        return json({
          ok: true,
          key,
          url: url.origin + '/media/' + encodeKeyForUrl(key),
          size: saved?.size || announced || 0,
        }, 201);
      } catch (e) {
        return json({error: 'upload_failed', message: String(e?.message || e)}, 503);
      }
    }

    if (request.method === 'DELETE' && url.pathname === '/object') {
      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        return json({error: 'unauthorized', message: String(e.message || e)}, 401);
      }

      const key = url.searchParams.get('key') || '';
      if (!key || key.includes('..')) return json({error: 'invalid_key'}, 400);

      const object = await env.MEDIA.head(key);
      if (!object) return json({ok: true, deleted: false});
      if (object.customMetadata?.uid !== claims.sub) return json({error: 'forbidden'}, 403);

      await env.MEDIA.delete(key);
      return json({ok: true, deleted: true});
    }

    return json({error: 'not_found'}, 404);
  },
};
