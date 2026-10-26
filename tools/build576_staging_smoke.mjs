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
const endpoint=process.env.NGELX_GAME_ENDPOINT;
if(!endpoint||!/^https:\/\/ngelx-ludo576-qa-[0-9]+\.alihancaglar76\.workers\.dev\/ludo$/.test(endpoint))throw Error('Isolated QA endpoint required');
const nonce=randomBytes(10).toString('hex'),users=[],rooms=[],probe='_ngelx_ludo565/qa_probe576_'+nonce;
async function firestore(path,options={}){const r=await fetch(root+path,{...options,headers:{authorization:'Bearer '+await accessToken(env),'content-type':'application/json'},signal:AbortSignal.timeout(12000)});if(!r.ok&&r.status!==404)throw Error('Datastore probe HTTP '+r.status);return r;}
async function login(i){
 const uid='qa_ludo576_'+nonce+'_'+i,now=Math.floor(Date.now()/1000),b64=v=>Buffer.from(JSON.stringify(v)).toString('base64url');
 const input=b64({alg:'RS256',typ:'JWT'})+'.'+b64({iss:service.client_email,sub:service.client_email,aud:'https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit',iat:now,exp:now+600,uid});
 const signature=createSign('RSA-SHA256').update(input).sign(service.private_key,'base64url');
 const r=await fetch('https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key='+apiKey,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({token:input+'.'+signature,returnSecureToken:true}),signal:AbortSignal.timeout(12000)});
 if(!r.ok)throw Error('Temporary test login HTTP '+r.status);const d=await r.json();users.push({uid,token:d.idToken});return users.at(-1);
}
async function call(user,body){const r=await fetch(endpoint,{method:'POST',headers:{authorization:'Bearer '+user.token,'content-type':'application/json'},body:JSON.stringify(body),signal:AbortSignal.timeout(25000)});const d=await r.json();if(!r.ok)throw Error('Ludo '+body.action+' HTTP '+r.status+' code '+String(d.error));return d.room;}
try{
 await firestore(probe+'?currentDocument.exists=false',{method:'PATCH',body:JSON.stringify({fields:{state:{stringValue:'probe'}}})});
 console.log('Dedicated datastore probe passed.');
 const a=await login(0),b=await login(1);console.log('Two isolated test accounts authenticated.');
 const wallets=await Promise.all(Array.from({length:5},()=>call(a,{action:'wallet'})));
 if(wallets.some(w=>w.chips!==5000))throw Error('Starter grant missing or duplicated');
 if((await call(b,{action:'wallet'})).chips!==5000)throw Error('Second starter grant missing');
 console.log('Live Firestore create-only CAS: concurrent 5000 starter requests verified.');
 const create={action:'create',capacity:2,team:false,mode:'classic',requestId:'smoke566_'+nonce};
 let room=await call(a,create);rooms.push(room.id);if(!/^[0-9]{6}$/.test(room.id))throw Error('Room code is not six digits');
 const retry=await call(a,create);if(retry.id!==room.id)throw Error('Create retry produced a duplicate room');
 console.log('Authenticated room creation and idempotent retry passed.');
 room=await call(b,{action:'join',id:room.id});
 let n=0;const action=async(user,name,data={})=>room=await call(user,{action:name,id:room.id,revision:room.revision,requestId:'smoke566_'+(++n),...data});
 await action(a,'start');
 const gift={action:'gift',id:room.id,to:b.uid,kind:'flower',requestId:'gift576_'+nonce};
 room=await call(a,gift);if(room.chips!==4980||!room.giftSent)throw Error('Gift charge failed');
 room=await call(a,gift);if(room.chips!==4980||!room.giftAlreadySent)throw Error('Gift retry charged twice');
 const received=await call(b,{action:'wallet'});
 if(received.chips!==5000||received.receivedGifts?.flower!==1)throw Error('Recipient gift CAS failed');
 await call(b,{action:'block',id:room.id,to:a.uid,blocked:true});
 const denied=await fetch(endpoint,{method:'POST',headers:{authorization:'Bearer '+a.token,'content-type':'application/json'},body:JSON.stringify({...gift,requestId:'blocked576_'+nonce}),signal:AbortSignal.timeout(25000)});
 if(denied.status!==403||(await denied.json()).error!=='gift_blocked')throw Error('Blocked gift accepted');
 if((await call(a,{action:'wallet'})).chips!==4980)throw Error('Blocked gift charged coins');
 await call(b,{action:'block',id:room.id,to:a.uid,blocked:false});
 const daily=await call(a,{action:'daily_reward'}),again=await call(a,{action:'daily_reward'});
 if(!daily.claimed||again.claimed||daily.chips!==5030||again.chips!==5030)throw Error('Daily reward duplicate');
 const chest=await call(a,{action:'chest_reward'}),chestAgain=await call(a,{action:'chest_reward'});
 if(!chest.claimed||chestAgain.claimed||chestAgain.chips!==5055)throw Error('Chest reward duplicate');
 console.log('Live atomic gifts, duplicate payment protection, block/unblock, daily and chest verified.');
 room=await call(a,{action:'sync',id:room.id});
 for(let i=0;i<20;i++){
  const seat=room.turn,user=seat===0?a:b;await action(user,'roll');
  if(room.dice!==null){const index=room.tokens[seat].findIndex(p=>p===-1?room.dice===6:p<56&&p+room.dice<=56);if(index>=0){await action(user,'move',{token:index});console.log('Two-account join, start, roll and token move passed.');break;}}
  if(i===19)throw Error('No movable roll during bounded smoke test');
 }
 await action(a,'leave');
 const bot=await call(a,{action:'bot',capacity:2,mode:'power',difficulty:'medium',requestId:'bot_smoke569_'+nonce});rooms.push(bot.id);
 if(!/^[0-9]{6}$/.test(bot.id)||!bot.botGame||bot.status!=='playing'||!bot.players.some(p=>p.bot))throw Error('Bot game did not start');
 if(bot.deadline-Date.now()>11000)throw Error('Turn window is not ten seconds');
 console.log('Six-digit codes, bot creation and ten-second turn window verified live.');
 const c=await login(2),d=await login(3);
 for(const team of [false,true]){
  let four=await call(b,{action:'create',capacity:4,team,mode:'classic',requestId:'four576_'+team+'_'+nonce});rooms.push(four.id);
  for(const user of [a,c,d])four=await call(user,{action:'join',id:four.id});
  four=await call(b,{action:'start',id:four.id,revision:four.revision,requestId:'start_four576_'+team});
  if(four.status!=='playing'||four.players.length!==4||four.team!==team)throw Error('4-player/team room failed');
  four=await call(b,{action:'auto',id:four.id,revision:four.revision,requestId:'auto_on576_'+team,enabled:true});
  if(four.autoSeats?.['0']!==true)throw Error('Auto did not enable');
  four=await call(b,{action:'auto',id:four.id,revision:four.revision,requestId:'auto_off576_'+team,enabled:false});
  if(four.autoSeats?.['0']===true)throw Error('Auto did not disable');
 }
 console.log('Four authenticated accounts: classic, team and explicit Auto on/off verified.');
 const mod=await fetch(endpoint,{method:'POST',headers:{authorization:'Bearer '+a.token,'content-type':'application/json'},body:JSON.stringify({action:'moderation_queue'}),signal:AbortSignal.timeout(25000)});
 if(mod.status!==403)throw Error('Normal player reached moderator queue');
 console.log('Moderator allowlist boundary verified; no production reports created.');
}finally{
 let failures=0;
 for(const path of [probe,...rooms.map(id=>'_ngelx_ludo565/'+id),...users.map(u=>'_ngelx_ludo565/wallet575_'+createHash('sha256').update(u.uid).digest('hex')),...users.map(u=>'_livekit_rate_limits/free_'+createHash('sha256').update('ludo565-create:'+u.uid).digest('hex'))])try{await firestore(path,{method:'DELETE'});}catch{failures++;}
 for(const u of users)try{const r=await fetch('https://identitytoolkit.googleapis.com/v1/accounts:delete?key='+apiKey,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({idToken:u.token}),signal:AbortSignal.timeout(12000)});if(!r.ok)failures++;}catch{failures++;}
 if(failures)throw Error('Temporary test cleanup failures: '+failures);
 console.log('Temporary game records and test accounts removed.');
}
