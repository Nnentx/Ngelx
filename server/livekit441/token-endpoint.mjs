/** Production token core. Inject VERIFIED Firebase auth and server-side room authorization.
 * No deployment is enabled by this module. Never expose API secrets to Flutter.
 */
import {createHmac} from 'node:crypto';
const encode=value=>Buffer.from(JSON.stringify(value)).toString('base64url');
export function createTokenEndpoint({verifyFirebaseToken,authorizeRoom,rateLimit,apiKey,apiSecret,serverUrl,now=()=>Date.now()}) {
 if(![verifyFirebaseToken,authorizeRoom,rateLimit].every(x=>typeof x==='function'))throw Error('Authentication, room authorization and rate limiter required');
 if(!apiKey||!apiSecret||!serverUrl?.startsWith('wss://'))throw Error('Production LiveKit configuration required');
 return async function handle({method,authorization,body}) {
  const response=(status,json)=>({status,headers:{'Content-Type':'application/json','Cache-Control':'no-store'},body:json});
  if(method!=='POST')return response(405,{error:'method_not_allowed'});
  const bearer=/^Bearer ([^\s]+)$/.exec(authorization??'');
  if(!bearer)return response(401,{error:'unauthorized'});
  let identity;
  try{identity=await verifyFirebaseToken(bearer[1],true);}catch{return response(401,{error:'unauthorized'});}
  const uid=identity?.uid;
  if(!uid||identity.firebase?.sign_in_provider==='anonymous'||identity.disabled)return response(401,{error:'unauthorized'});
  if(!body||typeof body.room_name!=='string'||body.room_name.length<1||body.room_name.length>160||!/^[\w-]+$/.test(body.room_name))return response(400,{error:'invalid_room'});
  if(body.participant_identity&&body.participant_identity!==uid)return response(403,{error:'identity_mismatch'});
  if(body.room_config||body.agent_name||body.participant_metadata)return response(400,{error:'unsupported_options'});
  if(!await rateLimit(uid))return response(429,{error:'rate_limited'});
  let permission;
  try{permission=await authorizeRoom({uid,roomName:body.room_name});}catch{return response(503,{error:'temporarily_unavailable'});}
  if(!permission?.allowed||!['host','speaker','listener','caller'].includes(permission.role))return response(403,{error:'forbidden'});
  const seconds=Math.floor(now()/1000);
  const header=encode({alg:'HS256',typ:'JWT'});
  // Name, role and publish rights originate exclusively from trusted server records.
  const payload=encode({iss:apiKey,sub:uid,iat:seconds,nbf:seconds-5,exp:seconds+300,
   name:String(permission.displayName??uid).slice(0,80),attributes:{role:permission.role},
   video:{room:body.room_name,roomJoin:true,canSubscribe:true,canPublish:permission.canPublish===true,canPublishData:permission.canPublishData===true}});
  const signature=createHmac('sha256',apiSecret).update(header+'.'+payload).digest('base64url');
  return response(200,{server_url:serverUrl,participant_token:header+'.'+payload+'.'+signature,room_name:body.room_name,participant_name:String(permission.displayName??uid).slice(0,80)});
 };
}
