const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Authorization, Content-Type, Content-Length',
  'Access-Control-Allow-Methods': 'GET, HEAD, PUT, DELETE, OPTIONS',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...corsHeaders, 'content-type': 'application/json; charset=utf-8' },
  });
}

function cleanKey(raw) {
  if (!raw) return null;
  let key;
  try { key = decodeURIComponent(raw); } catch (_) { return null; }
  key = key.replace(/^\/+/, '');
  if (!key || key.length > 512 || key.includes('..') || key.includes('\\')) return null;
  return key;
}

async function firebaseUser(request, env) {
  const auth = request.headers.get('authorization') || '';
  if (!auth.startsWith('Bearer ')) return null;
  const token = auth.slice(7).trim();
  if (!token || !env.FIREBASE_WEB_API_KEY) return null;
  const response = await fetch(
    'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=' + encodeURIComponent(env.FIREBASE_WEB_API_KEY),
    {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ idToken: token }),
    },
  );
  if (!response.ok) return null;
  const data = await response.json();
  const user = data?.users?.[0];
  return user?.localId ? { uid: user.localId } : null;
}

function ownedPath(key, uid) {
  const roots = [
    `videos/${uid}/`, `photos/${uid}/`, `music/${uid}/`,
    `profiles/${uid}/`, `stories/${uid}/`, `profile-intros/${uid}/`,
    `thumbnails/${uid}/`, `groups/${uid}/`, `chats/${uid}/`,
    `chat-backgrounds/${uid}/`, `support/${uid}/`,
  ];
  return roots.some((root) => key.startsWith(root));
}

function publicUrl(request, env, key) {
  const encoded = key.split('/').map(encodeURIComponent).join('/');
  const base = (env.PUBLIC_BASE_URL || '').replace(/\/+$/, '');
  if (base) return base + '/' + encoded;
  const u = new URL(request.url);
  return u.origin + '/media/' + encoded;
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    const u = new URL(request.url);

    if ((request.method === 'GET' || request.method === 'HEAD') && u.pathname.startsWith('/media/')) {
      const key = cleanKey(u.pathname.slice('/media/'.length));
      if (!key) return json({ error: 'bad_path' }, 400);

      if (request.method === 'HEAD') {
        const object = await env.MEDIA.head(key);
        if (!object) return json({ error: 'not_found' }, 404);
        const headers = new Headers(corsHeaders);
        object.writeHttpMetadata(headers);
        headers.set('etag', object.httpEtag);
        headers.set('cache-control', 'public, max-age=31536000, immutable');
        headers.set('accept-ranges', 'bytes');
        headers.set('content-length', String(object.size));
        return new Response(null, { status: 200, headers });
      }

      const object = await env.MEDIA.get(key, { range: request.headers });
      if (!object) return json({ error: 'not_found' }, 404);
      const headers = new Headers(corsHeaders);
      object.writeHttpMetadata(headers);
      headers.set('etag', object.httpEtag);
      headers.set('cache-control', 'public, max-age=31536000, immutable');
      headers.set('accept-ranges', 'bytes');

      let status = 200;
      if (object.range && request.headers.has('range')) {
        const start = object.range.offset;
        const end = start + object.range.length - 1;
        headers.set('content-range', `bytes ${start}-${end}/${object.size}`);
        headers.set('content-length', String(object.range.length));
        status = 206;
      } else {
        headers.set('content-length', String(object.size));
      }
      return new Response(object.body, { status, headers });
    }

    if (u.pathname !== '/upload' && u.pathname !== '/object') {
      return json({ ok: true, service: 'ngelx-media-r2' });
    }

    const user = await firebaseUser(request, env);
    if (!user) return json({ error: 'unauthorized' }, 401);

    const key = cleanKey(u.searchParams.get('path'));
    if (!key || !ownedPath(key, user.uid)) return json({ error: 'forbidden_path' }, 403);

    if (request.method === 'PUT' && u.pathname === '/upload') {
      const max = Number(env.MAX_OBJECT_BYTES || 52428800);
      const length = Number(request.headers.get('content-length') || 0);
      if (!length) return json({ error: 'content_length_required' }, 411);
      if (length > max) return json({ error: 'file_too_large', maxBytes: max }, 413);

      const contentType = request.headers.get('content-type') || 'application/octet-stream';
      const allowed =
        contentType.startsWith('image/') ||
        contentType.startsWith('video/') ||
        contentType.startsWith('audio/') ||
        contentType === 'application/octet-stream';
      if (!allowed) return json({ error: 'unsupported_type' }, 415);

      await env.MEDIA.put(key, request.body, {
        httpMetadata: {
          contentType,
          cacheControl: 'public, max-age=31536000, immutable',
        },
        customMetadata: { ownerUid: user.uid },
      });
      return json({ ok: true, url: publicUrl(request, env, key), path: key });
    }

    if (request.method === 'DELETE' && u.pathname === '/object') {
      await env.MEDIA.delete(key);
      return json({ ok: true });
    }

    return json({ error: 'method_not_allowed' }, 405);
  },
};
