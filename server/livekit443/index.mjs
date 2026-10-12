import {initializeApp, getApps} from 'firebase-admin/app';
import {getAuth} from 'firebase-admin/auth';
import {getFirestore} from 'firebase-admin/firestore';
import {onRequest} from 'firebase-functions/v2/https';
import {defineSecret, defineString} from 'firebase-functions/params';
import {createTokenEndpoint} from '../livekit441/token-endpoint.mjs';
import {createFirestoreRoomAuthorizer, createFirestoreRateLimiter} from './firestore-adapters.mjs';

const apiKey = defineSecret('LIVEKIT_API_KEY');
const apiSecret = defineSecret('LIVEKIT_API_SECRET');
const serverUrl = defineString('LIVEKIT_SERVER_URL');
if (!getApps().length) initializeApp();
const db = getFirestore();
const authorizeRoom = createFirestoreRoomAuthorizer({db});
const limiter = createFirestoreRateLimiter({db});

export const livekitToken = onRequest({region:'europe-west1',memory:'256MiB',timeoutSeconds:15,
  minInstances:0,maxInstances:3,cors:false,secrets:[apiKey,apiSecret]}, async (req,res) => {
  res.set('Cache-Control','no-store');
  if (req.method !== 'POST') { res.status(405).json({error:'method_not_allowed'}); return; }
  if (!req.is('application/json') || (req.rawBody?.length??0)>4096) {
    res.status(400).json({error:'invalid_request'}); return;
  }
  try {
    // req.ip is supplied by the Firebase runtime; never read a body-provided IP.
    if (!req.ip || !await limiter('ip:'+req.ip,120)) {
      res.status(429).json({error:'rate_limited'}); return;
    }
    const handle = createTokenEndpoint({
      verifyFirebaseToken:(token)=>getAuth().verifyIdToken(token,true), authorizeRoom,
      rateLimit:uid=>limiter('uid:'+uid,30),
      apiKey:apiKey.value(),apiSecret:apiSecret.value(),serverUrl:serverUrl.value(),
    });
    const result = await handle({method:req.method,authorization:req.get('authorization'),body:req.body});
    res.set(result.headers).status(result.status).json(result.body);
  } catch {
    // Never disclose credentials, identity tokens or database diagnostics.
    res.status(503).json({error:'temporarily_unavailable'});
  }
});
