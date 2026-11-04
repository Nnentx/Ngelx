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
const production=endpoint==='https://oyun.ngelxsocial.com/ludo';
if(!endpoint||(!/^https:\/\/ngelx-ludo576-qa-[0-9]+\.alihancaglar76\.workers\.dev\/ludo$/.test(endpoint)&&!(production&&process.env.NGELX_PRODUCTION_SMOKE==='592')))throw Error('Approved test endpoint required');
const invites=[];
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
 const a=await login(0),b=await login(1),c=await login(2),d=await login(3);
 let room=await call(a,{action:'create',capacity:4,mode:'classic',requestId:'create592_'+nonce});rooms.push(room.id);
 const invite=await call(a,{action:'invite_create',id:room.id,requestId:'invite592_'+nonce});invites.push(invite.inviteToken);
 room=await call(b,{action:'invite_join',inviteToken:invite.inviteToken});
 const status=await call(c,{action:'invite_status',inviteToken:invite.inviteToken});
 if(status.status!=='pending'||status.joined!==2||status.remaining!==2)throw Error('Shared invite closed before seats filled');
 await Promise.all([c,d].map(u=>call(u,{action:'invite_join',inviteToken:invite.inviteToken})));
 room=await call(a,{action:'sync',id:room.id,fast592:true});
 if(room.status!=='playing'||room.players.length!==4||new Set(room.players.map(p=>p.seat)).size!==4||!room.autoStarted592)throw Error('Four-seat automatic start failed');
 if((await call(b,{action:'invite_join',inviteToken:invite.inviteToken})).players.length!==4)throw Error('Join retry duplicated a seat');
 console.log('PASS: four authenticated accounts; third/fourth concurrent invitation joins and automatic start.');
 const byUid=new Map(users.map(u=>[u.uid,u])),faces=[[],[],[],[]],seen=new Set();let serial=0,moved=false;
 for(let step=0;step<100&&!faces.every(f=>f.length===6);step++){
  const player=room.players.find(p=>p.seat===room.turn),who=byUid.get(player.uid);
  if(room.dice===null){
   room=await call(who,{action:'roll',id:room.id,revision:room.revision,requestId:'roll592_'+nonce+'_'+(++serial),fast592:true});
   if('diceBags592' in room)throw Error('Private roll bag exposed');
   const last=room.lastRoll;
   if(last&&!seen.has(last.revision)){
    seen.add(last.revision);const bag=faces[last.seat];
    if(bag.length<6){if(bag.includes(last.value))throw Error('Balanced roll repeated within first cycle');bag.push(last.value);}
   }
  }
  if(room.dice!==null){
   const seat=room.turn,user=byUid.get(room.players.find(p=>p.seat===seat).uid);
   const index=room.tokens[seat].findIndex(p=>p===-1?room.dice===6:p<56&&p+room.dice<=56);
   if(index<0)throw Error('Accepted die has no legal move');
   room=await call(user,{action:'move',id:room.id,revision:room.revision,requestId:'move592_'+nonce+'_'+(++serial),token:index,fast592:true});moved=true;
  }
 }
 if(!moved||!faces.every(f=>f.length===6))throw Error('Bounded live move/roll verification incomplete');
 console.log('PASS: all four seats received 1–6 once in their first six rolls; accepted pawn moves and private dice state.');
 const gift={action:'gift',id:room.id,to:b.uid,kind:'rooster',requestId:'gift592_'+nonce};
 const before=await call(a,{action:'wallet'}),sent=await call(a,gift),retry=await call(a,gift);
 if(!sent.giftSent||!retry.giftAlreadySent||sent.chips!==retry.chips||sent.chips>=before.chips)throw Error('Gift receipt/payment idempotency failed');
 if(!sent.gifts.some(g=>g.kind==='rooster'&&g.from===a.uid))throw Error('Gift event missing');
 const watch=await call(b,{action:'watch',id:room.id});if('diceBags592' in watch)throw Error('Spectator exposed dice state');
 console.log('PASS: server-accepted rooster receipt, single charge on retry and safe spectator response.');
 let team=await call(a,{action:'create',capacity:4,team:true,mode:'classic',requestId:'team592_'+nonce});rooms.push(team.id);
 for(const u of [b,c,d])team=await call(u,{action:'join',id:team.id});
 if(team.status!=='playing'||!team.team||!team.autoStarted592)throw Error('Team/code automatic start failed');
 let pair=await call(a,{action:'create',capacity:2,mode:'classic',requestId:'pair592_'+nonce});rooms.push(pair.id);
 pair=await call(b,{action:'join',id:pair.id});if(pair.status!=='waiting')throw Error('Two-seat start changed');
 pair=await call(a,{action:'start',id:pair.id,revision:pair.revision,requestId:'pair_start592_'+nonce});
 if(pair.status!=='playing')throw Error('Manual two-seat start failed');
 console.log('PASS: team code joins auto-start; two-player manual start preserved.');
}finally{
 let failures=0;
 const paths=[probe,...rooms.map(id=>'_ngelx_ludo565/'+id),...rooms.map(id=>'_ngelx_ludo565/view570_'+id),...invites.map(t=>'_ngelx_ludo565/invite580_'+t),...users.map(u=>'_ngelx_ludo565/wallet575_'+createHash('sha256').update(u.uid).digest('hex')),...users.flatMap(u=>['ludo565-create','ludo580-invite'].map(action=>'_livekit_rate_limits/free_'+createHash('sha256').update(action+':'+u.uid).digest('hex')))];
 for(const path of paths)try{await firestore(path,{method:'DELETE'});}catch{failures++;}
 for(const u of users)try{const r=await fetch('https://identitytoolkit.googleapis.com/v1/accounts:delete?key='+apiKey,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({idToken:u.token}),signal:AbortSignal.timeout(12000)});if(!r.ok)failures++;}catch{failures++;}
 if(failures)throw Error('Temporary test cleanup failures: '+failures);
 console.log('Temporary game records, receipts, wallets and test accounts removed.');
}
