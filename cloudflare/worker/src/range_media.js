/**
 * Read-only Cloudflare R2 media streaming with HTTP byte-range semantics.
 * No changes to uploads, authorization, object keys, R2 writes or deletes.
 * Not deployed by the Build460 APK workflow.
 */
export async function serveMediaRequest(request, url, media, {cors, json, contentTypeFor}) {
  let key;
  try { key = decodeURIComponent(url.pathname.slice('/media/'.length)); }
  catch { return json({error:'invalid_key'},400); }
  if (!key || key.includes('..')) return json({error:'invalid_key'}, 400);

  const head = request.method === 'HEAD';
  const wantsRange = !head && !!request.headers.get('range');
  const object = head
    ? await media.head(key)
    : wantsRange
      ? await media.get(key, {range:request.headers})
      : await media.get(key);
  if (!object) return json({error:'not_found'},404);

  const headers = new Headers(cors());
  object.writeHttpMetadata(headers);
  headers.set('etag',object.httpEtag);
  headers.set('cache-control','public, max-age=31536000, immutable');
  headers.set('accept-ranges','bytes');
  const ext=(key.split('/').pop()?.split('.').pop() || '').toLowerCase();
  headers.set('content-type',contentTypeFor(ext,headers.get('content-type')));

  if (head) {
    headers.set('content-length',String(object.size));
    return new Response(null,{status:200,headers});
  }
  if (wantsRange) {
    const r=object.range;
    if(r && Number.isSafeInteger(r.offset) && Number.isSafeInteger(r.length)
       && r.offset >= 0 && r.length > 0 && r.offset+r.length<=object.size) {
      headers.set('content-range','bytes '+r.offset+'-'+(r.offset+r.length-1)+'/'+object.size);
      headers.set('content-length',String(r.length));
      return new Response(object.body,{status:206,headers});
    }
    headers.set('content-range','bytes */'+object.size);
    return new Response(null,{status:416,headers});
  }
  headers.set('content-length',String(object.size));
  return new Response(object.body,{status:200,headers});
}
