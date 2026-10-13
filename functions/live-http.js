import {createServer} from 'node:http';
export function createLiveHttpServer(backend) {
const server = createServer(async (req,res) => {
  const path = new URL(req.url,'http://localhost').pathname;
  res.setHeader('Cache-Control','no-store');
  const response = {
    status(code) { res.statusCode=code; return this; },
    json(body) { res.setHeader('Content-Type','application/json'); res.end(JSON.stringify(body)); },
    sendStatus(code) { res.statusCode=code; res.end(); },
  };
  if (path === '/health' && req.method === 'GET') return response.json({ok:true});
  const webhook = path === '/webhook';
  if (!webhook && !/^\/live\/[a-z-]+$/.test(path)) return response.sendStatus(404);
  if (req.method !== 'POST') return response.sendStatus(405);
  try {
    const chunks=[]; let size=0;
    for await (const chunk of req) {
      size+=chunk.length;
      if (size>16384) return response.sendStatus(413);
      chunks.push(chunk);
    }
    req.rawBody=Buffer.concat(chunks); req.path=path;
    if (!webhook) {
      if (!String(req.headers['content-type']||'').startsWith('application/json')) return response.sendStatus(415);
      try { req.body=JSON.parse(req.rawBody.toString()); } catch (_) { return response.sendStatus(400); }
      if (!req.body || Array.isArray(req.body) || typeof req.body!=='object') return response.sendStatus(400);
    }
    await (webhook?backend.webhook:backend.live)(req,response);
  } catch (_) { if (!res.writableEnded) response.sendStatus(500); }
});
server.requestTimeout=30000;
server.headersTimeout=15000;
return server;
}
