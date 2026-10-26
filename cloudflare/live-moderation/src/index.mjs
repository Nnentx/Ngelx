import {createLudo565,ludoStore565} from './ludo565.mjs';
import {ludoAdmobEndpoint575} from '../../../server/ludo565/admob575.mjs';
import {communityDeleteStorage,createCommunityDelete556} from './community-delete.mjs';
import {verifyFirebaseIdToken} from '../../call-push/src/auth.mjs';
import {googleIo} from '../../call-push/src/google.mjs';
import {createGuestModeration} from '../../../server/livekit443/live-moderation.mjs';
import {roomService} from './room-service.mjs';
import {storage} from './storage.mjs';
const json=(body,status)=>new Response(JSON.stringify(body),{status,
  headers:{'content-type':'application/json','cache-control':'no-store'}});
export const configured=env=>['LIVEKIT_API_KEY','LIVEKIT_API_SECRET','LIVEKIT_SERVER_URL','GOOGLE_SERVICE_ACCOUNT'].every(k=>typeof env[k]==='string'&&env[k].length>0);
export default {async fetch(request,env){
  const path=new URL(request.url).pathname;
  if(path==='/health'&&request.method==='GET'){
   const coreReady=configured(env);
   const ludoReady=coreReady&&env.FIREBASE_PROJECT_ID==='ngelx-44eed';
   return json({ok:coreReady,service:'ngelx-live-moderation',
    features:['community_delete556','ludo565','ludo568','ludo569',
     'ludo575_auto','ludo575_chips','ludo575_gifts','ludo575_reports'],
    ludo575:{sourceVersion:575,configured:ludoReady,
     rewardedAdsConfigured:ludoReady&&typeof env.LUDO_ADMOB_AD_UNIT==='string'&&
       new RegExp('^ca-app-pub-[0-9]{16}/[0-9]{10}$').test(env.LUDO_ADMOB_AD_UNIT),
     moderationAllowlistConfigured:ludoReady&&typeof env.LUDO_MODERATOR_UIDS==='string'&&
       env.LUDO_MODERATOR_UIDS.split(',').some(x=>x.trim().length>0)}},coreReady?200:503);
  }
  if(path==='/ludo/admob/ssv'){
    if(!configured(env))return json({error:'service_not_configured'},503);
    return ludoAdmobEndpoint575({store:ludoStore565(env),env})(request);
  }
  if(path==='/ludo'){
    if(request.method!=='POST')return json({error:'method_not_allowed'},405);
    if(!/^Bearer [^\s]+$/.test(request.headers.get('authorization')??''))return json({error:'unauthorized'},401);
    if(!configured(env))return json({error:'service_not_configured'},503);
    const identity=googleIo(env),db=storage(env);
    return createLudo565({store:ludoStore565(env),adEnabled:Boolean(env.LUDO_ADMOB_AD_UNIT),
      isModerator:async uid=>typeof env.LUDO_MODERATOR_UIDS==='string'&&
       env.LUDO_MODERATOR_UIDS.split(',').map(x=>x.trim()).filter(Boolean).includes(uid),
      profile:uid=>identity.getUser(uid),limit:(uid,action)=>['create','bot','match'].includes(action)?db.rateLimit('ludo565-create:'+uid,4):Promise.resolve(true),verify:async()=>{const claims=await verifyFirebaseIdToken(request,env);await identity.checkAuth(claims);return claims;}})(request);
  }
  if(path!=='/moderate'&&path!=='/community/delete')return json({error:'not_found'},404);
  if(request.method!=='POST')return json({error:'method_not_allowed'},405);
  if(!/^Bearer [^\s]+$/.test(request.headers.get('authorization')??''))return json({error:'unauthorized'},401);
  if(!request.headers.get('content-type')?.startsWith('application/json'))return json({error:'invalid_request'},400);
  try{
    // Bound streamed input too; Content-Length alone is caller-controlled.
    const reader=request.body?.getReader();if(!reader)return json({error:'invalid_request'},400);
    const chunks=[];let size=0;
    while(true){const {value,done}=await reader.read();if(done)break;size+=value.byteLength;
      if(size>2048){await reader.cancel();return json({error:'invalid_request'},400);}chunks.push(value);}
    const bytes=new Uint8Array(size);let offset=0;for(const c of chunks){bytes.set(c,offset);offset+=c.byteLength;}
    let body;try{body=JSON.parse(new TextDecoder().decode(bytes));}catch{return json({error:'invalid_request'},400);}
    if(!configured(env))return json({error:'service_not_configured'},503);
    const db=storage(env),identity=googleIo(env);
    if(path==='/community/delete'){
      const handler=createCommunityDelete556({store:communityDeleteStorage(env),rateLimit:uid=>db.rateLimit('community-delete556:'+uid,90),verify:async()=>{const claims=await verifyFirebaseIdToken(request,env);await identity.checkAuth(claims);return {...claims,uid:claims.sub};}});
      const result=await handler(request,body);return json(result.body,result.status);
    }
    const ip=request.headers.get('cf-connecting-ip');
    if(!ip||!await db.rateLimit('ip:'+ip,60))return json({error:'rate_limited'},429);
    const handler=createGuestModeration({
      ...db,rateLimit:uid=>db.rateLimit('uid:'+uid,20),
      verifyFirebaseToken:async()=>{
        const claims=await verifyFirebaseIdToken(request,env);
        await identity.checkAuth(claims);
        return {...claims,uid:claims.sub};
      },roomService:roomService(env),cameraSource:1,microphoneSource:2,audioTrackType:0,
    });
    const result=await handler({method:'POST',authorization:request.headers.get('authorization'),body});
    return json(result.body,result.status);
  }catch{return json({error:'temporarily_unavailable'},503);}
}};
