import {verifyFirebaseIdToken} from '../call-push/src/auth.mjs';
import {accessToken} from '../call-push/src/google.mjs';
import {createVerificationHandler561} from './handler.generated.mjs';

const project='ngelx-44eed';
const base=`https://firestore.googleapis.com/v1/projects/${project}/databases/(default)/documents`;
async function google(env,url,body){
 const r=await fetch(url,{method:body?'POST':'GET',headers:{Authorization:`Bearer ${await accessToken(env)}`,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(8000)});
 if(!r.ok)throw Error('google-unavailable');return r.json();
}
// Compare-and-swap both counters atomically. Fail closed on contention/errors.
export async function reserveQuota(env,uid,now=Date.now()){
 const day=new Date(now).toISOString().slice(0,10);
 const uidKey=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid))),b=>b.toString(16).padStart(2,'0')).join('');
 const ids=[`global-${day}`,`user-${uidKey}`];
 const docs=await Promise.all(ids.map(async id=>{const r=await fetch(base+'/_verification_free/'+encodeURIComponent(id),{headers:{Authorization:`Bearer ${await accessToken(env)}`},signal:AbortSignal.timeout(8000)});if(r.status===404)return null;if(!r.ok)throw Error('quota-unavailable');return r.json();}));
 const count=Number(docs[0]?.fields?.count?.integerValue??0);
 const last=Number(docs[1]?.fields?.last?.integerValue??0);
 const hour=Math.floor(now/3600000),oldHour=Number(docs[1]?.fields?.hour?.integerValue??-1);
 const userCount=oldHour===hour?Number(docs[1]?.fields?.count?.integerValue??0):0;
 if(count>=95||userCount>=3||now-last<60000)return false;
 const data=[{count:count+1},{count:userCount+1,hour,last:now}];
 const writes=ids.map((id,i)=>({update:{name:`projects/${project}/databases/(default)/documents/_verification_free/${id}`,fields:Object.fromEntries(Object.entries(data[i]).map(([k,v])=>[k,{integerValue:String(v)}]))},currentDocument:docs[i]?{updateTime:docs[i].updateTime}:{exists:false}}));
 try{await google(env,base+':commit',{writes});return true;}catch{return false;}
}
export async function smallBody(request){
 const reader=request.body?.getReader();if(!reader)throw Error('body-required');let total=0;const chunks=[];
 try{while(true){const {done,value}=await reader.read();if(done)break;total+=value.length;if(total>2048)throw Error('body-too-large');chunks.push(value);}}finally{await reader.cancel();}
 const all=new Uint8Array(total);let offset=0;for(const chunk of chunks){all.set(chunk,offset);offset+=chunk.length;}return JSON.parse(new TextDecoder().decode(all));
}
export function createWorker({verify=verifyFirebaseIdToken,quota=reserveQuota,api=google,sendFetch=fetch}={}){
 return {async fetch(request,env){
 const json=(status,body)=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json','Cache-Control':'no-store'}});
 if(new URL(request.url).pathname!=='/verify-email')return json(404,{error:'not-found'});
 if(request.method!=='POST')return json(405,{error:'method-not-allowed'});
 if(env.FIREBASE_PROJECT_ID!==project||env.EMAIL_FROM!=='NgelX <noreply@ngelxsocial.com>'||!env.RESEND_API_KEY||!env.GOOGLE_SERVICE_ACCOUNT)return json(503,{error:'not-configured'});
 if(!/^application\/json(?:;|$)/i.test(request.headers.get('content-type')??''))return json(400,{error:'invalid-request'});
 let body;try{body=await smallBody(request);}catch{return json(400,{error:'invalid-request'});}
 let currentUser;
 const handler=createVerificationHandler561({
  verifyToken:async()=>{const claims=await verify(request,env);const result=await api(env,`https://identitytoolkit.googleapis.com/v1/projects/${project}/accounts:lookup`,{localId:[claims.sub]});currentUser=result.users?.find(u=>u.localId===claims.sub);if(!currentUser||currentUser.disabled||Number(currentUser.validSince??0)>(claims.auth_time??0))throw Error('revoked');return {...claims,uid:claims.sub};},
  rateLimit:uid=>quota(env,uid),
  getUser:async()=>currentUser,
  generateLink:async email=>{const result=await api(env,`https://identitytoolkit.googleapis.com/v1/projects/${project}/accounts:sendOobCode`,{requestType:'VERIFY_EMAIL',email,returnOobLink:true});return result.oobLink;},
  send:async({to,...template})=>{const r=await sendFetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${env.RESEND_API_KEY}`,'Content-Type':'application/json'},body:JSON.stringify({from:env.EMAIL_FROM,to:[to],...template}),signal:AbortSignal.timeout(12000)});if(!r.ok)throw Error('send-failed');},
 });
 const result=await handler({token:/^Bearer (\S+)$/.exec(request.headers.get('authorization')??'')?.[1],body});return json(result.status,result.body);
 }};
}
export default createWorker();
