import { AwsClient } from 'aws4fetch';
import {
  captionMediaCandidates,
  captionTranscriptionAttempts,
  detectTranslationSource,
  normalizeLanguageCode,
} from './content_tools.js';

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
  stories: 50 * 1024 * 1024,
  'profile-intros': 35 * 1024 * 1024,
  music: 15 * 1024 * 1024,
  'chat-files': 30 * 1024 * 1024,
  'chat-audio': 15 * 1024 * 1024,
  gifs: 12 * 1024 * 1024,
  default: 10 * 1024 * 1024,
};

let jwksCache = null;
let jwksExpiresAt = 0;

const MEDIA_PROTOCOL = 'upload-r2-332';

function uploadLog(event, data = {}) {
  console.log(JSON.stringify({service: 'ngelx-r2-media', protocol: MEDIA_PROTOCOL, event, ...data}));
}

function cors() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Authorization, Content-Type, X-NgelX-Filename, X-NgelX-Client, X-NgelX-Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'X-NgelX-Worker': MEDIA_PROTOCOL,
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

function captionError(code, message, status = 502) {
  const error = new Error(message);
  error.code = code;
  error.status = status;
  return error;
}

async function loadCaptionMedia(candidates, requestUrl, env) {
  const requestHost = new URL(requestUrl).hostname;
  for (const mediaUrl of candidates) {
    let target;
    try { target = new URL(mediaUrl); } catch (_) { continue; }
    if (target.protocol !== 'https:') continue;
    const ngelxMediaHost = target.hostname.endsWith('.workers.dev') ||
      target.hostname === 'media.ngelxsocial.com' ||
      target.hostname === 'media2.ngelxsocial.com';
    const allowedHost = ngelxMediaHost ||
      target.hostname.endsWith('.googleapis.com') ||
      target.hostname.endsWith('.firebasestorage.app') ||
      target.hostname.endsWith('.appspot.com');
    if (!allowedHost) continue;

    // NgelX medya alan adları aynı R2 bucket'ını kullanır. /media/ nesnesini
    // binding ile okumak, alan adı geçişlerindeki yanlış 404'leri önler.
    if (target.pathname.startsWith('/media/') && ngelxMediaHost) {
      try {
        const key = decodeURIComponent(target.pathname.slice('/media/'.length));
        if (key && !key.includes('..')) {
          const object = await env.MEDIA.get(key);
          if (object) {
            if (object.size > 24 * 1024 * 1024) throw captionError('media_too_large_for_captioning', 'Altyazı için video şu an en fazla 24 MB olabilir.', 413);
            return {bytes: new Uint8Array(await object.arrayBuffer()), mediaUrl, via: target.hostname === requestHost ? 'r2-local' : 'r2-alias'};
          }
        }
      } catch (e) {
        if (e?.code) throw e;
      }
    }

    try {
      const response = await fetch(target.toString(), {redirect: 'follow'});
      if (!response.ok) continue;
      const announced = Number(response.headers.get('content-length') || 0);
      if (announced > 24 * 1024 * 1024) throw captionError('media_too_large_for_captioning', 'Altyazı için video şu an en fazla 24 MB olabilir.', 413);
      const bytes = new Uint8Array(await response.arrayBuffer());
      if (!bytes.length) continue;
      if (bytes.length > 24 * 1024 * 1024) throw captionError('media_too_large_for_captioning', 'Altyazı için video şu an en fazla 24 MB olabilir.', 413);
      return {bytes, mediaUrl, via: 'https'};
    } catch (e) {
      if (e?.code) throw e;
    }
  }
  throw captionError('media_not_found', 'Videonun kaynak dosyası sunucuda bulunamadı. Yeni yüklenen bir video ile tekrar dene.', 404);
}

async function extractCaptionAudioCandidates(videoBytes, env) {
  const candidates = [];
  if (env.VIDEO_MEDIA) {
    // Some Android uploads contain audio codecs that Whisper cannot decode after
    // a single m4a conversion. Try several server-side audio containers before
    // falling back to the original media bytes.
    for (const format of ['mp3', 'wav', 'm4a']) {
      try {
        const stream = new Response(videoBytes).body;
        if (!stream) continue;
        const audio = await env.VIDEO_MEDIA
          .input(stream)
          .output({mode: 'audio', format})
          .response();
        if (!audio.ok) throw new Error('audio_extract_http_' + audio.status);
        const bytes = new Uint8Array(await audio.arrayBuffer());
        if (!bytes.length) throw new Error('audio_extract_empty');
        candidates.push({bytes, extracted: true, format});
      } catch (e) {
        console.warn(JSON.stringify({
          service:'ngelx-caption',
          event:'audio_extract_retry',
          format,
          message:String(e?.message||e),
        }));
      }
    }
  }
  candidates.push({bytes: videoBytes, extracted: false, format: 'source'});
  return candidates;
}

function bytesToBase64(bytes) {
  let binary = '';
  for (let i = 0; i < bytes.length; i += 0x8000) {
    binary += String.fromCharCode(...bytes.subarray(i, Math.min(i + 0x8000, bytes.length)));
  }
  return btoa(binary);
}

async function transcribeCaptionAudio(bytes, language, env) {
  const attempts = captionTranscriptionAttempts(language);
  let lastResult = null;
  for (const options of attempts) {
    const result = await env.AI.run('@cf/openai/whisper-large-v3-turbo', {
      audio: bytesToBase64(bytes),
      task: 'transcribe',
      condition_on_previous_text: false,
      ...options,
    });
    lastResult = result;
    if (String(result?.text || '').trim()) return result;
  }
  return lastResult;
}

async function transcribeCaptionMedia(videoBytes, language, env) {
  const audioCandidates = await extractCaptionAudioCandidates(videoBytes, env);
  let lastError = null;
  let lastEmpty = null;
  for (const audio of audioCandidates) {
    try {
      const result = await transcribeCaptionAudio(audio.bytes, language, env);
      if (String(result?.text || '').trim()) return {result, audio};
      lastEmpty = {result, audio};
    } catch (e) {
      lastError = e;
      console.warn(JSON.stringify({
        service:'ngelx-caption',
        event:'transcription_retry',
        format:audio.format,
        extracted:audio.extracted,
        message:String(e?.message||e),
      }));
    }
  }
  if (lastEmpty) return lastEmpty;
  if (lastError) throw lastError;
  return {result:null, audio:{extracted:false, format:'source'}};
}


function directR2Ready(env) {
  return Boolean(env.R2_ACCESS_KEY_ID && env.R2_SECRET_ACCESS_KEY && env.R2_ACCOUNT_ID);
}

function directR2Client(env) {
  if (!directR2Ready(env)) return null;
  return new AwsClient({
    service: 's3',
    region: 'auto',
    accessKeyId: env.R2_ACCESS_KEY_ID,
    secretAccessKey: env.R2_SECRET_ACCESS_KEY,
  });
}

async function directR2Read(env, key, rangeHeader = '') {
  const client = directR2Client(env);
  if (!client) return null;
  const endpoint =
    'https://' + env.R2_ACCOUNT_ID + '.r2.cloudflarestorage.com/ngelx-media/' + encodeKeyForUrl(key);
  const headers = {};
  if (rangeHeader) headers.Range = rangeHeader;
  try {
    const response = await client.fetch(endpoint, {method: 'GET', headers});
    return response.ok || response.status === 206 ? response : null;
  } catch (_) {
    return null;
  }
}

async function presignR2Put(env, key, contentType, expiresIn = 900) {
  if (!directR2Ready(env)) throw new Error('R2 direct upload signer is not configured');
  const r2 = new AwsClient({
    service: 's3',
    region: 'auto',
    accessKeyId: env.R2_ACCESS_KEY_ID,
    secretAccessKey: env.R2_SECRET_ACCESS_KEY,
  });
  const endpoint = new URL(
    'https://' + env.R2_ACCOUNT_ID + '.r2.cloudflarestorage.com/ngelx-media/' + encodeKeyForUrl(key),
  );
  endpoint.searchParams.set('X-Amz-Expires', String(expiresIn));
  const signed = await r2.sign(
    new Request(endpoint.toString(), {
      method: 'PUT',
      headers: {'Content-Type': contentType},
    }),
    {aws: {signQuery: true}},
  );
  return signed.url.toString();
}

async function deleteR2Prefix(env, prefix) {
  let cursor;
  let deleted = 0;
  do {
    const listed = await env.MEDIA.list({prefix, cursor, limit: 1000});
    const keys = (listed.objects || []).map((x) => x.key);
    if (keys.length) {
      for (let i = 0; i < keys.length; i += 100) {
        await env.MEDIA.delete(keys.slice(i, i + 100));
      }
      deleted += keys.length;
    }
    cursor = listed.truncated ? listed.cursor : undefined;
  } while (cursor);
  return deleted;
}

async function deleteAccountMedia(env, uid) {
  let deleted = 0;
  for (const kind of ALLOWED_KINDS) {
    deleted += await deleteR2Prefix(env, kind + '/' + uid + '/');
  }
  deleted += await deleteR2Prefix(env, '__ngelx_chunks/' + uid + '/');
  return deleted;
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
        return json({ok: true, service: 'ngelx-r2-media', r2: true, ai: Boolean(env.AI), mediaTransform: Boolean(env.VIDEO_MEDIA), directUpload: directR2Ready(env), protocol: MEDIA_PROTOCOL});
      } catch (e) {
        return json({ok: false, service: 'ngelx-r2-media', r2: false, directUpload: directR2Ready(env), protocol: MEDIA_PROTOCOL, message: String(e?.message || e)}, 503);
      }
    }


    if (request.method === 'POST' && url.pathname === '/internal/account-media-delete') {
      const supplied = request.headers.get('x-ngelx-account-delete-secret') || '';
      if (!env.ACCOUNT_DELETE_SECRET || supplied !== env.ACCOUNT_DELETE_SECRET) {
        return json({error:'forbidden'},403);
      }
      let body;
      try { body = await request.json(); } catch (_) { return json({error:'invalid_json'},400); }
      const uid = String(body?.uid || '').trim();
      if (!/^[A-Za-z0-9:_-]{1,128}$/.test(uid)) return json({error:'invalid_uid'},400);
      try {
        const deleted = await deleteAccountMedia(env, uid);
        uploadLog('account_media_deleted', {uid:uid.slice(0,8), deleted});
        return json({ok:true, deleted});
      } catch (e) {
        uploadLog('account_media_delete_failed', {uid:uid.slice(0,8), message:String(e?.message||e)});
        return json({error:'account_media_delete_failed',message:String(e?.message||e)},503);
      }
    }


    if (request.method === 'POST' && url.pathname === '/ai/translate') {
      try { await verifyFirebaseIdToken(request, env); } catch (e) { return json({error:'unauthorized',message:String(e?.message||e)},401); }
      if(!env.AI)return json({error:'ai_not_configured',message:'Çeviri servisi yapılandırılmamış.'},503);
      let body;try{body=await request.json();}catch(_){return json({error:'invalid_json'},400);}
      const text=String(body?.text||'').trim(),sourceLanguage=detectTranslationSource(body?.text,body?.sourceLanguage),targetLanguage=normalizeLanguageCode(body?.targetLanguage);
      if(!text||text.length>6000||!targetLanguage)return json({error:'invalid_translation_request'},400);
      if(sourceLanguage===targetLanguage)return json({ok:true,translatedText:text,sourceLanguage,targetLanguage});
      try{
        const result=await env.AI.run('@cf/meta/m2m100-1.2b',{text,source_lang:sourceLanguage,target_lang:targetLanguage});
        const translatedText=String(result?.translated_text||result?.translatedText||result?.text||'').trim();
        if(!translatedText)throw new Error('empty_translation');
        return json({ok:true,translatedText,sourceLanguage,targetLanguage});
      }catch(e){return json({error:'translation_failed',message:String(e?.message||e)},502);}
    }

    if (request.method === 'POST' && url.pathname === '/ai/captions') {
      try { await verifyFirebaseIdToken(request, env); } catch (e) { return json({error:'unauthorized',message:String(e?.message||e)},401); }
      if(!env.AI)return json({error:'ai_not_configured',message:'Altyazı servisi yapılandırılmamış.'},503);
      let body;try{body=await request.json();}catch(_){return json({error:'invalid_json'},400);}
      const mediaUrls=captionMediaCandidates(body),language=normalizeLanguageCode(body?.language);
      if(!mediaUrls.length)return json({error:'invalid_media_url',message:'Altyazı üretilecek video bulunamadı.'},400);
      try{
        const loaded=await loadCaptionMedia(mediaUrls,request.url,env);
        const transcription=await transcribeCaptionMedia(loaded.bytes,language,env);
        const result=transcription.result;
        const text=String(result?.text||'').trim(),vtt=String(result?.vtt||'').trim();
        if(!text)throw captionError('no_speech_detected','Bu videoda altyazıya çevrilebilecek konuşma algılanamadı.',422);
        const detectedLanguage=normalizeLanguageCode(result?.transcription_info?.language||result?.language||language);
        return json({
          ok:true,
          text,
          vtt,
          language:detectedLanguage,
          mediaSource:loaded.via,
          audioExtracted:transcription.audio.extracted,
          audioFormat:transcription.audio.format,
        });
      }catch(e){
        const code=e?.code||'caption_failed';
        const message=code==='no_speech_detected'
          ?'Bu videoda altyazıya çevrilebilecek konuşma algılanamadı.'
          :String(e?.message||e);
        return json({error:code,message},Number(e?.status)||502);
      }
    }

    if (request.method === 'GET' && url.pathname.startsWith('/media/')) {
      const key = decodeURIComponent(url.pathname.slice('/media/'.length));
      if (!key || key.includes('..')) return json({error: 'invalid_key'}, 400);

      const rangeHeader = request.headers.get('range') || '';
      const object = await env.MEDIA.get(
        key,
        rangeHeader ? {range: request.headers} : undefined,
      );

      if (object) {
        const headers = new Headers(cors());
        object.writeHttpMetadata(headers);
        headers.set('etag', object.httpEtag);
        headers.set('cache-control', 'public, max-age=31536000, immutable');
        headers.set('accept-ranges', 'bytes');
        headers.set('access-control-expose-headers', 'Content-Length, Content-Range, Accept-Ranges, ETag, Content-Type');
        headers.set('x-ngelx-media-source', 'r2-binding');

        let status = 200;
        if (rangeHeader && object.range && typeof object.range.offset === 'number' && typeof object.range.length === 'number') {
          const start = object.range.offset;
          const length = object.range.length;
          const end = start + length - 1;
          headers.set('content-range', `bytes ${start}-${end}/${object.size}`);
          headers.set('content-length', String(length));
          status = 206;
        } else {
          // R2 normal GET'te de object.range doldurabiliyor. İstemci Range
          // istemediyse 206 dönmek Android image/video decoderlarını bozuyordu.
          headers.delete('content-range');
          headers.set('content-length', String(object.size));
          status = 200;
        }
        return new Response(object.body, {headers, status});
      }

      // Direct-upload ile yazılmış eski nesne binding tarafında görünmüyorsa
      // aynı anahtarı S3 kimliği üzerinden kurtarmayı dene. Bu, hesap/binding
      // geçişlerinde oluşmuş kırık URL'leri yeniden yükleme istemeden açar.
      const rescue = await directR2Read(env, key, rangeHeader);
      if (rescue) {
        const headers = new Headers(cors());
        for (const name of ['content-type','content-length','content-range','etag','last-modified']) {
          const value = rescue.headers.get(name);
          if (value) headers.set(name, value);
        }
        headers.set('cache-control', 'public, max-age=31536000, immutable');
        headers.set('accept-ranges', 'bytes');
        headers.set('access-control-expose-headers', 'Content-Length, Content-Range, Accept-Ranges, ETag, Content-Type');
        headers.set('x-ngelx-media-source', 'r2-signed-rescue');
        return new Response(rescue.body, {headers, status: rescue.status});
      }

      return json({error: 'not_found'}, 404);
    }

    if (request.method === 'GET' && url.pathname === '/upload/presign') {
      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        uploadLog('presign_auth_failed', {message: String(e?.message || e)});
        return json({error: 'unauthorized', stage: 'presign_auth', protocol: MEDIA_PROTOCOL, message: String(e.message || e)}, 401);
      }

      if (!directR2Ready(env)) {
        uploadLog('presign_not_configured');
        return json({error: 'direct_upload_not_configured', stage: 'presign_config', protocol: MEDIA_PROTOCOL}, 503);
      }

      const kind = cleanKind(url.searchParams.get('kind'));
      if (!kind) return json({error: 'invalid_kind', stage: 'presign_validate', protocol: MEDIA_PROTOCOL}, 400);
      const ext = cleanExt(url.searchParams.get('ext'));
      const size = Number(url.searchParams.get('size') || 0);
      const maxBytes = MAX_BYTES[kind] || MAX_BYTES.default;
      if (!Number.isFinite(size) || size <= 0) {
        return json({error: 'invalid_size', stage: 'presign_validate', protocol: MEDIA_PROTOCOL}, 400);
      }
      if (size > maxBytes) {
        return json({error: 'file_too_large', stage: 'presign_validate', protocol: MEDIA_PROTOCOL, maxBytes}, 413);
      }

      const contentType = contentTypeFor(ext, url.searchParams.get('contentType'));
      const key = kind + '/' + claims.sub + '/' + Date.now() + '_' + crypto.randomUUID() + '.' + ext;
      try {
        const uploadUrl = await presignR2Put(env, key, contentType, 900);
        const mediaUrl = url.origin + '/media/' + encodeKeyForUrl(key);
        uploadLog('presign_created', {kind, size, uid: claims.sub.slice(0, 8)});
        return json({
          ok: true,
          protocol: MEDIA_PROTOCOL,
          transport: 'direct-r2-presigned-put',
          method: 'PUT',
          uploadUrl,
          mediaUrl,
          key,
          contentType,
          size,
          expiresIn: 900,
        });
      } catch (e) {
        uploadLog('presign_failed', {kind, size, message: String(e?.message || e)});
        return json({error: 'presign_failed', stage: 'presign_sign', protocol: MEDIA_PROTOCOL, message: String(e?.message || e)}, 503);
      }
    }

    if (request.method === 'GET' && url.pathname === '/upload/ws') {
      if ((request.headers.get('Upgrade') || '').toLowerCase() !== 'websocket') {
        return json({error: 'websocket_required', protocol: MEDIA_PROTOCOL}, 426);
      }

      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        uploadLog('ws_auth_failed', {message: String(e?.message || e)});
        return json({error: 'unauthorized', stage: 'ws_auth', protocol: MEDIA_PROTOCOL, message: String(e.message || e)}, 401);
      }

      const kind = cleanKind(url.searchParams.get('kind'));
      if (!kind) return json({error: 'invalid_kind', stage: 'ws_create', protocol: MEDIA_PROTOCOL}, 400);
      const ext = cleanExt(url.searchParams.get('ext'));
      const size = Number(url.searchParams.get('size') || 0);
      const maxBytes = MAX_BYTES[kind] || MAX_BYTES.default;
      if (!Number.isFinite(size) || size <= 0) {
        return json({error: 'invalid_size', stage: 'ws_create', protocol: MEDIA_PROTOCOL}, 400);
      }
      if (size > maxBytes) {
        return json({error: 'file_too_large', stage: 'ws_create', protocol: MEDIA_PROTOCOL, maxBytes}, 413);
      }

      const uid = claims.sub;
      const key = kind + '/' + uid + '/' + Date.now() + '_' + crypto.randomUUID() + '.' + ext;
      const contentType = contentTypeFor(ext, url.searchParams.get('contentType'));

      let upload;
      try {
        upload = await env.MEDIA.createMultipartUpload(key, {
          httpMetadata: {contentType, cacheControl: 'public, max-age=31536000, immutable'},
          customMetadata: {uid, kind, transport: 'websocket-multipart', protocol: MEDIA_PROTOCOL},
        });
      } catch (e) {
        uploadLog('ws_create_failed', {kind, size, message: String(e?.message || e)});
        return json({error: 'ws_create_failed', stage: 'ws_create', protocol: MEDIA_PROTOCOL, message: String(e?.message || e)}, 503);
      }

      const pair = new WebSocketPair();
      const client = pair[0];
      const server = pair[1];
      server.accept();

      let partNumber = 0;
      let received = 0;
      let finished = false;
      const parts = [];

      const fail = async (stage, error) => {
        if (finished) return;
        finished = true;
        try { await upload.abort(); } catch (_) {}
        const message = String(error?.message || error || 'upload_failed');
        uploadLog('ws_failed', {kind, stage, received, partNumber, message});
        try {
          server.send(JSON.stringify({type: 'error', stage, protocol: MEDIA_PROTOCOL, message}));
        } catch (_) {}
        try { server.close(1011, 'upload failed'); } catch (_) {}
      };

      server.addEventListener('message', async (event) => {
        if (finished) return;
        try {
          if (typeof event.data === 'string') {
            let message;
            try {
              message = JSON.parse(event.data);
            } catch (_) {
              throw new Error('invalid_control_message');
            }
            if (message?.type === 'complete') {
              if (received !== size) throw new Error('size_mismatch expected=' + size + ' received=' + received);
              if (!parts.length) throw new Error('no_parts_received');
              const object = await upload.complete(parts);
              finished = true;
              uploadLog('ws_completed', {kind, size: object.size, parts: parts.length, uid: uid.slice(0, 8)});
              server.send(JSON.stringify({
                type: 'complete',
                ok: true,
                protocol: MEDIA_PROTOCOL,
                key,
                url: url.origin + '/media/' + encodeKeyForUrl(key),
                size: object.size,
              }));
              server.close(1000, 'done');
              return;
            }
            if (message?.type === 'abort') {
              await upload.abort();
              finished = true;
              server.close(1000, 'aborted');
              return;
            }
            throw new Error('unknown_control_message');
          }

          const body = event.data instanceof ArrayBuffer
            ? event.data
            : event.data?.arrayBuffer
                ? await event.data.arrayBuffer()
                : null;
          if (!body) throw new Error('invalid_binary_frame');
          const length = body.byteLength;
          if (length <= 0 || length > 5 * 1024 * 1024) {
            throw new Error('invalid_part_size ' + length);
          }
          if (received + length > size || received + length > maxBytes) {
            throw new Error('received_too_much_data');
          }

          partNumber += 1;
          const part = await upload.uploadPart(partNumber, body);
          parts.push({partNumber: part.partNumber, etag: part.etag});
          received += length;
          uploadLog('ws_part_saved', {kind, partNumber, length, received, uid: uid.slice(0, 8)});
          server.send(JSON.stringify({
            type: 'part',
            ok: true,
            protocol: MEDIA_PROTOCOL,
            partNumber: part.partNumber,
            received,
          }));
        } catch (e) {
          await fail('ws_message', e);
        }
      });

      server.addEventListener('close', async () => {
        if (!finished) {
          try { await upload.abort(); } catch (_) {}
          uploadLog('ws_client_closed', {kind, received, partNumber, uid: uid.slice(0, 8)});
        }
      });

      server.addEventListener('error', async (event) => {
        await fail('ws_socket', event?.error || 'socket_error');
      });

      server.send(JSON.stringify({
        type: 'ready',
        ok: true,
        protocol: MEDIA_PROTOCOL,
        key,
        uploadId: upload.uploadId,
        size,
      }));
      uploadLog('ws_ready', {kind, size, uid: uid.slice(0, 8)});

      return new Response(null, {
        status: 101,
        webSocket: client,
        headers: {'X-NgelX-Worker': MEDIA_PROTOCOL},
      });
    }

    if (request.method === 'POST' && url.pathname === '/upload/multipart/create') {
      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        uploadLog('multipart_create_auth_failed', {message: String(e?.message || e)});
        return json({error: 'unauthorized', stage: 'multipart_create_auth', protocol: MEDIA_PROTOCOL, message: String(e.message || e)}, 401);
      }

      const kind = cleanKind(url.searchParams.get('kind'));
      if (!kind) return json({error: 'invalid_kind', stage: 'multipart_create', protocol: MEDIA_PROTOCOL}, 400);
      const ext = cleanExt(url.searchParams.get('ext'));
      const maxBytes = MAX_BYTES[kind] || MAX_BYTES.default;
      const size = Number(url.searchParams.get('size') || 0);
      if (!Number.isFinite(size) || size <= 0) return json({error: 'invalid_size', stage: 'multipart_create', protocol: MEDIA_PROTOCOL}, 400);
      if (size > maxBytes) return json({error: 'file_too_large', stage: 'multipart_create', protocol: MEDIA_PROTOCOL, maxBytes}, 413);

      const uid = claims.sub;
      const key = kind + '/' + uid + '/' + Date.now() + '_' + crypto.randomUUID() + '.' + ext;
      const contentType = contentTypeFor(ext, url.searchParams.get('contentType'));
      try {
        const upload = await env.MEDIA.createMultipartUpload(key, {
          httpMetadata: {contentType, cacheControl: 'public, max-age=31536000, immutable'},
          customMetadata: {uid, kind, transport: 'multipart', protocol: MEDIA_PROTOCOL},
        });
        uploadLog('multipart_created', {kind, size, uid: uid.slice(0, 8)});
        return json({
          ok: true,
          protocol: MEDIA_PROTOCOL,
          key,
          uploadId: upload.uploadId,
          url: url.origin + '/media/' + encodeKeyForUrl(key),
        }, 201);
      } catch (e) {
        uploadLog('multipart_create_failed', {kind, size, message: String(e?.message || e)});
        return json({error: 'multipart_create_failed', stage: 'multipart_create', protocol: MEDIA_PROTOCOL, message: String(e?.message || e)}, 503);
      }
    }

    if (request.method === 'POST' && url.pathname === '/upload/multipart/part') {
      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        uploadLog('multipart_part_auth_failed', {message: String(e?.message || e)});
        return json({error: 'unauthorized', stage: 'multipart_part_auth', protocol: MEDIA_PROTOCOL, message: String(e.message || e)}, 401);
      }

      const kind = cleanKind(url.searchParams.get('kind'));
      const key = url.searchParams.get('key') || '';
      const uploadId = url.searchParams.get('uploadId') || '';
      const partNumber = Number(url.searchParams.get('partNumber'));
      if (!kind || !key.startsWith(kind + '/' + claims.sub + '/') || !uploadId ||
          !Number.isInteger(partNumber) || partNumber < 1 || partNumber > 10000) {
        return json({error: 'invalid_multipart_part', stage: 'multipart_part', protocol: MEDIA_PROTOCOL}, 400);
      }
      if (!request.body) return json({error: 'empty_part', stage: 'multipart_part', protocol: MEDIA_PROTOCOL}, 400);
      const announced = Number(request.headers.get('content-length') || 0);
      if (announced <= 0 || announced > 5 * 1024 * 1024) {
        return json({error: 'invalid_part_size', stage: 'multipart_part', protocol: MEDIA_PROTOCOL, announced}, 413);
      }

      try {
        const upload = env.MEDIA.resumeMultipartUpload(key, uploadId);
        const part = await upload.uploadPart(partNumber, request.body);
        uploadLog('multipart_part_saved', {kind, partNumber, announced, uid: claims.sub.slice(0, 8)});
        return json({ok: true, protocol: MEDIA_PROTOCOL, partNumber: part.partNumber, etag: part.etag}, 201);
      } catch (e) {
        uploadLog('multipart_part_failed', {kind, partNumber, announced, message: String(e?.message || e)});
        return json({error: 'multipart_part_failed', stage: 'multipart_part', protocol: MEDIA_PROTOCOL, partNumber, message: String(e?.message || e)}, 503);
      }
    }

    if (request.method === 'POST' && url.pathname === '/upload/multipart/complete') {
      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        uploadLog('multipart_complete_auth_failed', {message: String(e?.message || e)});
        return json({error: 'unauthorized', stage: 'multipart_complete_auth', protocol: MEDIA_PROTOCOL, message: String(e.message || e)}, 401);
      }

      const kind = cleanKind(url.searchParams.get('kind'));
      let payload;
      try {
        payload = await request.json();
      } catch (_) {
        return json({error: 'invalid_json', stage: 'multipart_complete', protocol: MEDIA_PROTOCOL}, 400);
      }
      const key = typeof payload?.key === 'string' ? payload.key : '';
      const uploadId = typeof payload?.uploadId === 'string' ? payload.uploadId : '';
      const parts = Array.isArray(payload?.parts) ? payload.parts : [];
      if (!kind || !key.startsWith(kind + '/' + claims.sub + '/') || !uploadId || !parts.length || parts.length > 10000) {
        return json({error: 'invalid_multipart_complete', stage: 'multipart_complete', protocol: MEDIA_PROTOCOL}, 400);
      }
      const normalizedParts = [];
      for (const raw of parts) {
        const partNumber = Number(raw?.partNumber);
        const etag = typeof raw?.etag === 'string' ? raw.etag : '';
        if (!Number.isInteger(partNumber) || partNumber < 1 || !etag) {
          return json({error: 'invalid_part_manifest', stage: 'multipart_complete', protocol: MEDIA_PROTOCOL}, 400);
        }
        normalizedParts.push({partNumber, etag});
      }
      normalizedParts.sort((a, b) => a.partNumber - b.partNumber);

      try {
        const upload = env.MEDIA.resumeMultipartUpload(key, uploadId);
        const object = await upload.complete(normalizedParts);
        uploadLog('multipart_completed', {kind, size: object.size, parts: normalizedParts.length, uid: claims.sub.slice(0, 8)});
        return json({
          ok: true,
          protocol: MEDIA_PROTOCOL,
          key,
          url: url.origin + '/media/' + encodeKeyForUrl(key),
          size: object.size,
        }, 201);
      } catch (e) {
        uploadLog('multipart_complete_failed', {kind, parts: normalizedParts.length, message: String(e?.message || e)});
        return json({error: 'multipart_complete_failed', stage: 'multipart_complete', protocol: MEDIA_PROTOCOL, message: String(e?.message || e)}, 503);
      }
    }

    if (request.method === 'POST' && url.pathname === '/upload/multipart/abort') {
      let claims;
      try {
        claims = await verifyFirebaseIdToken(request, env);
      } catch (e) {
        return json({error: 'unauthorized', stage: 'multipart_abort_auth', protocol: MEDIA_PROTOCOL, message: String(e.message || e)}, 401);
      }
      let payload;
      try {
        payload = await request.json();
      } catch (_) {
        return json({error: 'invalid_json', stage: 'multipart_abort', protocol: MEDIA_PROTOCOL}, 400);
      }
      const kind = cleanKind(url.searchParams.get('kind'));
      const key = typeof payload?.key === 'string' ? payload.key : '';
      const uploadId = typeof payload?.uploadId === 'string' ? payload.uploadId : '';
      if (!kind || !key.startsWith(kind + '/' + claims.sub + '/') || !uploadId) {
        return json({error: 'invalid_multipart_abort', stage: 'multipart_abort', protocol: MEDIA_PROTOCOL}, 400);
      }
      try {
        await env.MEDIA.resumeMultipartUpload(key, uploadId).abort();
      } catch (_) {}
      uploadLog('multipart_aborted', {kind, uid: claims.sub.slice(0, 8)});
      return json({ok: true, protocol: MEDIA_PROTOCOL});
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
      uploadLog('chunk_saved', {kind, index, total, bytes: bytes.byteLength, uid: claims.sub.slice(0, 8)});
      return json({ok: true, protocol: MEDIA_PROTOCOL, index, total}, 201);
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

      uploadLog('chunk_completed', {kind, size, total, uid: claims.sub.slice(0, 8)});
      return json({
        ok: true,
        protocol: MEDIA_PROTOCOL,
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
          const streamKinds = new Set(['videos', 'stories', 'profile-intros', 'music', 'chat-files', 'chat-audio']);

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
