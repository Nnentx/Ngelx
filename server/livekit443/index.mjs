import {initializeApp, getApps} from 'firebase-admin/app';
import {getAuth} from 'firebase-admin/auth';
import {FieldValue, getFirestore} from 'firebase-admin/firestore';
import {RoomServiceClient, TrackSource, TrackType} from 'livekit-server-sdk';
import {createGuestModeration} from './live-moderation.mjs';
import {createGuestModerationStorage} from './live-moderation-adapters.mjs';
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

export {incomingCall448} from '../calls448/index.mjs';

// Build499: candidate for LIVE server-side guest moderation, NOT DEPLOYED.
// Only verified Firebase host identity may operate the room-admin LiveKit API.
// The application does not call this endpoint until separately reviewed.
export const livekitGuestModeration = onRequest({
  region:'europe-west1',memory:'256MiB',timeoutSeconds:20,
  minInstances:0,maxInstances:3,cors:false,secrets:[apiKey,apiSecret],
}, async(req,res)=>{
  res.set('Cache-Control','no-store');
  if(req.method!=='POST'){res.status(405).json({error:'method_not_allowed'});return;}
  if(!req.is('application/json') || (req.rawBody?.length??0)>2048){
    res.status(400).json({error:'invalid_request'});return;
  }
  try{
    if(!req.ip || !await limiter('guest-moderation-ip:'+req.ip,90)){
      res.status(429).json({error:'rate_limited'});return;
    }
    const url=serverUrl.value();
    if(!url?.startsWith('wss://'))throw Error('livekit_url_not_configured');
    const storage=createGuestModerationStorage({db,FieldValue});
    const moderate=createGuestModeration({
      verifyFirebaseToken:token=>getAuth().verifyIdToken(token,true),
      ...storage, rateLimit:uid=>limiter('guest-moderation-uid:'+uid,20),
      roomService:new RoomServiceClient(url.replace(/^wss:/,'https:'),
        apiKey.value(),apiSecret.value()),
      cameraSource:TrackSource.CAMERA,microphoneSource:TrackSource.MICROPHONE,
      audioTrackType:TrackType.AUDIO,
    });
    const result=await moderate({
      method:req.method,authorization:req.get('authorization'),body:req.body,
    });
    res.set(result.headers).status(result.status).json(result.body);
  }catch{
    res.status(503).json({error:'temporarily_unavailable'});
  }
});

// Build543 prepared endpoint only; production deployment remains a separate action.
export {communityDelete543} from '../community543/index.mjs';

// Build561: optional branded verification email; existing exports preserved.
export {verificationEmail561} from '../verification561/index.mjs';
