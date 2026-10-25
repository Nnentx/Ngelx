import fs from 'node:fs';
import {createSign,randomBytes,createHash} from 'node:crypto';
import {accessToken} from '../cloudflare/call-push/src/google.mjs';
const raw=process.env.FIREBASE_SERVICE_ACCOUNT_NGELX_44EED||process.env.FIREBASE_SERVICE_ACCOUNT;
if(!raw)throw Error('Firebase server identity missing');
let service;try{service=JSON.parse(raw);}catch{service=JSON.parse(Buffer.from(raw,'base64').toString());}
if(service.project_id!=='ngelx-44eed')throw Error('Wrong project');
const env={FIREBASE_PROJECT_ID:service.project_id,GOOGLE_SERVICE_ACCOUNT:JSON.stringify(service)};
const cfg=JSON.parse(fs.readFileSync('app/android/app/google-services.json','utf8'));
const apiKey=cfg.client.find(c=>c.client_info?.android_client_info?.package_name==='com.nnentx.ngelx_app')?.api_key?.[0]?.current_key;
if(!apiKey)throw Error('App authentication configuration missing');
const root=`https://firestore.googleapis.com/v1/projects/${service.project_id}/databases/(default)/documents/`;
const nonce=randomBytes(10).toString('hex'),users=[],rooms=[],probe='_ngelx_ludo565/qa_probe566_'+nonce;
async function firestore(path,options={}){const r=await fetch(root+path,{...options,headers:{authorization:'Bearer '+await accessToken(env),'content-type':'application/json'},signal:AbortSignal.timeout(12000)});if(!r.ok&&r.status!==404)throw Error('Datastore probe HTTP '+r.status);return r;}
async function login(i){
 const uid='qa_ludo566_'+nonce+'_'+i,now=Math.floor(Date.now()/1000),b64=v=>Buffer.from(JSON.stringify(v)).toString('base64url');
 const input=b64({alg:'RS256',typ:'JWT'})+'.'+b64({iss:service.client_email,sub:service.client_email,aud:'https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit',iat:now,exp:now+600,uid});
 const signature=createSign('RSA-SHA256').update(input).sign(service.private_key,'base64url');
 const r=await fetch('https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key='+apiKey,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token:input+'.'+signature,returnSecureToken:true}),signal:AbortSignal.timeout(12000)});
 if(!r.ok)throw Error('Temporary test login HTTP '+r.status);const d=await r.json();users.push({uid,token:d.idToken});return users.at(-1);
}
async function call(user,body){const r=await fetch((process.env.NGELX_GAME_ENDPOINT||'https://oyun.ngelxsocial.com/ludo'),{method:'POST',headers:{authorization:'Bearer '+user.token,'content-type':'application/json'},body:JSON.stringify(body),signal:AbortSignal.timeout(25000)});const d=await r.json();if(!r.ok)throw Error('Ludo '+body.action+' HTTP '+r.status+' code '+String(d.error));return d.room;}
try{
 await firestore(probe+'?currentDocument.exists=false',{method:'PATCH',body:JSON.stringify({fields:{state:{stringValue:'probe'}}})});
 console.log('Dedicated datastore probe passed.');
 const a=await login(0),b=await login(1);console.log('Two isolated test accounts authenticated.');
 const create={action:'create',capacity:2,team:false,mode:'classic',requestId:'smoke566_'+nonce};
 let room=await call(a,create);rooms.push(room.id);
 const retry=await call(a,create);if(retry.id!==room.id)throw Error('Create retry produced a duplicate room');
 console.log('Authenticated room creation and idempotent retry passed.');
 room=await call(b,{action:'join',id:room.id});
 let n=0;const action=async(user,name,data={})=>room=await call(user,{action:name,id:room.id,revision:room.revision,requestId:'smoke566_'+(++n),...data});
 await action(a,'start');
 for(let i=0;i<20;i++){
  const seat=room.turn,user=seat===0?a:b;await action(user,'roll');
  if(room.dice!==null){const index=room.tokens[seat].findIndex(p=>p===-1?room.dice===6:p<56&&p+room.dice<=56);if(index>=0){await action(user,'move',{token:index});console.log('Two-account join, start, roll and token move passed.');break;}}
  if(i===19)throw Error('No movable roll during bounded smoke test');
 }
 await action(a,'leave');
}finally{
 let failures=0;
 for(const path of [probe,...rooms.map(id=>'_ngelx_ludo565/'+id),...users.map(u=>'_livekit_rate_limits/free_'+createHash('sha256').update('ludo565-create:'+u.uid).digest('hex'))])try{await firestore(path,{method:'DELETE'});}catch{failures++;}
 for(const u of users)try{const r=await fetch('https://identitytoolkit.googleapis.com/v1/accounts:delete?key='+apiKey,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({idToken:u.token}),signal:AbortSignal.timeout(12000)});if(!r.ok)failures++;}catch{failures++;}
 if(failures)throw Error('Temporary test cleanup failures: '+failures);
 console.log('Temporary game records and test accounts removed.');
}
