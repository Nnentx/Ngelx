const encoder = new TextEncoder();

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Authorization, Content-Type, Content-Length',
  'Access-Control-Allow-Methods': 'GET, PUT, DELETE, OPTIONS',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...corsHeaders, 'content-type': 'application/json; charset=utf-8' },
  });
}

function temizAnahtar(raw) {
  if (!raw) return null;
  let key;
  try { key = decodeURIComponent(raw); } catch (_) { return null; }
  key = key.replace(/^\/+/, '');
  if (!key || key.length > 512 || key.includes('..') || key.includes('\\')) return null;
  return key;
}

async function firebaseKullanici(request, env) {
  const h = request.headers.get('authorization') || '';
  if (!h.startsWith('Bearer ')) return null;
  const token = h.slice(7).trim();
  if (!token || !env.FIREBASE_WEB_API_KEY) return null;
  const r = await fetch(
    'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=' + encodeURIComponent(env.FIREBASE_WEB_API_KEY),
    {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ idToken: token }),
    },
  );
  if (!r.ok) return null;
  const data = await r.json();
  const u = data && data.users && data.users[0];
  return u && u.localId ? { uid: u.localId } : null;
}

function kullaniciYoluMu(key, uid) {
  const izinli = [
    `videos/${uid}/`,
    `photos/${uid}/`,
    `music/${uid}/`,
    `profiles/${uid}/`,
    `stories/${uid}/`,
    `profile-intros/${uid}/`,
    `thumbnails/${uid}/`,
    `groups/${uid}/`,
    `chats/${uid}/`,
    `chat-backgrounds/${uid}/`,
    `support/${uid}/`,
  ];
  return izinli.some((p) => key.startsWith(p));
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

    if (request.method === 'GET' && u.pathname.startsWith('/media/')) {
      const key = temizAnahtar(u.pathname.slice('/media/'.length));
      if (!key) return json({ error: 'bad_path' }, 400);
      const obj = await env.MEDIA.get(key, { range: request.headers });
      if (!obj) return json({ error: 'not_found' }, 404);
      const headers = new Headers(corsHeaders);
      obj.writeHttpMetadata(headers);
      headers.set('etag', obj.httpEtag);
      headers.set('cache-control', 'public, max-age=31536000, immutable');
      return new Response(obj.body, { status: 200, headers });
    }

    if (u.pathname !== '/upload' && u.pathname !== '/object') {
      return json({ ok: true, service: 'ngelx-media-r2' });
    }

    const kullanici = await firebaseKullanici(request, env);
    if (!kullanici) return json({ error: 'unauthorized' }, 401);

    const key = temizAnahtar(u.searchParams.get('path'));
    if (!key || !kullaniciYoluMu(key, kullanici.uid)) {
      return json({ error: 'forbidden_path' }, 403);
    }

    if (request.method === 'PUT' && u.pathname === '/upload') {
      const max = Number(env.MAX_OBJECT_BYTES || 52428800);
      const len = Number(request.headers.get('content-length') || 0);
      if (!len) return json({ error: 'content_length_required' }, 411);
      if (len > max) return json({ error: 'file_too_large', maxBytes: max }, 413);

      const contentType = request.headers.get('content-type') || 'application/octet-stream';
      const izinliTur =
        contentType.startsWith('image/') ||
        contentType.startsWith('video/') ||
        contentType.startsWith('audio/') ||
        contentType === 'application/octet-stream';
      if (!izinliTur) return json({ error: 'unsupported_type' }, 415);

      await env.MEDIA.put(key, request.body, {
        httpMetadata: {
          contentType,
          cacheControl: 'public, max-age=31536000, immutable',
        },
        customMetadata: { ownerUid: kullanici.uid },
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
