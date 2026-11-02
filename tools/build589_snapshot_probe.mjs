import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createSign,randomBytes,createHash} from 'node:crypto';
import {accessToken} from '../cloudflare/call-push/src/google.mjs';
import {pkStorage588} from '../cloudflare/live-moderation/src/pk588-storage.mjs';
const raw=process.env.FIREBASE_SERVICE_ACCOUNT_NGELX_44EED||process.env.FIREBASE_SERVICE_ACCOUNT;
if(!raw)throw Error('Server identity missing');
let service;try{service=JSON.parse(raw);}catch{service=JSON.parse(Buffer.from(raw,'base64').toString());}
assert.equal(service.project_id,'ngelx-44eed');
const env={FIREBASE_PROJECT_ID:service.project_id,GOOGLE_SERVICE_ACCOUNT:JSON.stringify(service)};
const root=`https://firestore.googleapis.com/v1/projects/${service.project_id}/databases/(default)/documents/`;
const nonce=randomBytes(10).toString('hex'),prefix='qa_pk589_'+nonce;
const paths=[],users=[],a=prefix+'_a',b=prefix+'_b',ra=prefix+'_ra',rb=prefix+'_rb';
const field=v=>v===null?{nullValue:null}:typeof v==='boolean'?{booleanValue:v}:typeof v==='number'?{integerValue:String(v)}:typeof v==='string'?{stringValue:v}:Array.isArray(v)?{arrayValue:{values:v.map(field)}}:{mapValue:{fields:Object.fromEntries(Object.entries(v).map(([k,v])=>[k,field(v)]))}};
async function request(path,options={}){
 const r=await fetch(root+path,{...options,headers:{authorization:'Bearer '+await accessToken(env),'content-type':'application/json'},signal:AbortSignal.timeout(15000)});
 if(!r.ok&&!(options.method==='DELETE'&&r.status===404))throw Error('Probe datastore HTTP '+r.status);
 return options.method==='DELETE'?null:r.json();
}
async function put(path,values){
 if(!paths.includes(path))paths.push(path);
 return request(path,{method:'PATCH',body:JSON.stringify({fields:Object.fromEntries(Object.entries(values).map(([k,v])=>[k,field(v)]))})});
}
const pause=()=>new Promise(resolve=>setTimeout(resolve,120));
let apiKey;
async function login(uid){
 const now=Math.floor(Date.now()/1000),b64=v=>Buffer.from(JSON.stringify(v)).toString('base64url');
 const value=b64({alg:'RS256',typ:'JWT'})+'.'+b64({iss:service.client_email,sub:service.client_email,aud:'https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit',iat:now,exp:now+600,uid});
 const signature=createSign('RSA-SHA256').update(value).sign(service.private_key,'base64url');
 const r=await fetch('https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key='+apiKey,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token:value+'.'+signature,returnSecureToken:true}),signal:AbortSignal.timeout(15000)});
 if(!r.ok)throw Error('Temporary authentication HTTP '+r.status);const token=(await r.json()).idToken;users.push({uid,token});return users.at(-1);
}
try{
 // These inactive private records never appear in live discovery or invitations.
 await put('live_streams/'+ra,{ownerId:a,active:false,visibility:'private',pkActive:true,pkSessionId:prefix,likeCount:0,giftPoints:0});
 await put('live_streams/'+rb,{ownerId:b,active:false,visibility:'private',pkActive:true,pkSessionId:prefix,likeCount:999999,giftPoints:999999});
 await put('live_streams/'+ra+'/reactions/counted',{uid:a,count:5});
 await put('live_streams/'+ra+'/reactions/legacy',{uid:a});
 await put('live_streams/'+rb+'/reactions/counted',{uid:b,count:2});
 await put('live_streams/'+ra+'/comments/before',{kind:'gift',points:10});
 const initial=await put('live_streams/'+rb+'/comments/before',{kind:'gift',points:100});
 const start=Date.parse(initial.updateTime)+1;await pause();
 await put('live_streams/'+ra+'/reactions/counted',{uid:a,count:7});
 await put('live_streams/'+rb+'/reactions/counted',{uid:b,count:12});
 const last=await put('live_streams/'+ra+'/comments/last_second',{kind:'gift',points:150});
 const end=Date.parse(last.updateTime)+1;await pause();
 await put('live_streams/'+rb+'/comments/after_deadline',{kind:'gift',points:100000});
 const store=pkStorage588(env);
 assert.deepEqual(await store.totalsAt(ra,start),{likeCount:6,giftPoints:10});
 assert.deepEqual(await store.totalsAt(rb,start),{likeCount:2,giftPoints:100});
 assert.deepEqual(await store.totalsAt(ra,end),{likeCount:8,giftPoints:160});
 assert.deepEqual(await store.totalsAt(rb,end),{likeCount:12,giftPoints:100});
 console.log('Historical aggregate preflight PASS: start baseline, legacy hearts, last-second gift and late gift exclusion');
 if(process.env.NGELX_PK589_LIVE==='1'){
  const cfg=JSON.parse(fs.readFileSync('app/android/app/google-services.json','utf8'));
  apiKey=cfg.client.find(c=>c.client_info?.android_client_info?.package_name==='com.nnentx.ngelx_app')?.api_key?.[0]?.current_key;
  assert.ok(apiKey);const ua=await login(a),ub=await login(b);
  await put('calls/'+prefix,{type:'live_pk',status:'active',members:[a,b],inviterUid:a,inviteeUid:b,inviterLiveId:ra,inviteeLiveId:rb,
   startedAt:start,clientStartedAt:start-500,endsAt:end,startLikeA:999999,startLikeB:999999,startGiftA:999999,startGiftB:999999});
  paths.push('live_pk_stats588/'+a,'live_pk_stats588/'+b,...[a,b].map(uid=>'_livekit_rate_limits/free_'+createHash('sha256').update('pk588:'+uid).digest('hex')));
  async function finish(user){
   const r=await fetch('https://ngelx-live-moderation.alihancaglar76.workers.dev/pk/finish',{method:'POST',headers:{authorization:'Bearer '+user.token,'content-type':'application/json'},body:JSON.stringify({sessionId:prefix}),signal:AbortSignal.timeout(30000)});
   if(!r.ok)throw Error('Live PK HTTP '+r.status);return r.json();
  }
  const results=await Promise.all([finish(ua),finish(ub)]);
  for(const result of results){assert.equal(result.scoreSource589,'firestore_read_time');assert.equal(result.winnerUid,a);assert.deepEqual(result.finalScoreByUid,{[a]:17,[b]:10});assert.equal(result.streakByUid[a],1);assert.equal(result.streakByUid[b],0);}
  const retry=await finish(ua);assert.equal(retry.streakByUid[a],1);assert.deepEqual(retry.finalScoreByUid,results[0].finalScoreByUid);
  console.log('Live PK PASS: stale room counters ignored, last-second gift decides winner, late gift excluded, concurrent WIN saved once');
 }
}catch(error){
 if(error.details589)console.error('Snapshot API detail:',error.details589);
 throw error;
}finally{
 let failures=0;
 for(const path of [...paths].reverse())try{await request(path,{method:'DELETE'});}catch{failures++;}
 for(const user of users)try{const r=await fetch('https://identitytoolkit.googleapis.com/v1/accounts:delete?key='+apiKey,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({idToken:user.token}),signal:AbortSignal.timeout(15000)});if(!r.ok)failures++;}catch{failures++;}
 if(failures)throw Error('Temporary fixture cleanup failures: '+failures);
 console.log('Private probe documents and temporary accounts removed');
}
