import {test} from 'node:test';
import assert from 'node:assert/strict';
import {derToP1363_575,verifyAdmobSSV575,createAdSession575,applyAdmobReward575,ludoAdmobEndpoint575} from './admob575.mjs';
import {ludoWallet575} from './rewards575.mjs';
import {createLudo565} from '../../cloudflare/live-moderation/src/ludo565.mjs';
const t=1800000000000;
function store(){
 const data=new Map();let seq=0;
 return {
  data,
  get:async id=>data.get(id)??null,
  put:async(id,room,stamp)=>{
   const old=data.get(id);
   if((old?.stamp??undefined)!==stamp)throw Object.assign(Error('conflict'),{status:409});
   data.set(id,{room:structuredClone(room),stamp:String(++seq)});
  },
  putMany:async entries=>{
   if(entries.some(e=>(data.get(e.id)?.stamp??undefined)!==e.stamp))
    throw Object.assign(Error('conflict'),{status:409});
   entries.forEach(e=>data.set(e.id,{room:structuredClone(e.room),stamp:String(++seq)}));
  }
 };
}
const encodeInt=arr=>{
 let a=Array.from(arr);while(a.length>1&&a[0]===0)a.shift();
 if(a[0]&0x80)a.unshift(0);
 return [2,a.length,...a];
};
function signatureToDer(raw){
 const bytes=new Uint8Array(raw);
 const r=encodeInt(bytes.slice(0,32)),s=encodeInt(bytes.slice(32));
 return Uint8Array.from([0x30,r.length+s.length,...r,...s]);
}
async function signed(token,{transaction='0123456789abcdef0123456789',unit='123456789',item='chips',when=t}={}){
 const kp=await crypto.subtle.generateKey({name:'ECDSA',namedCurve:'P-256'},true,['sign','verify']);
 const exported=await crypto.subtle.exportKey('spki',kp.publicKey);
 const key={keys:[{keyId:1,base64:Buffer.from(exported).toString('base64')}]};
 const data='ad_network=5450213213286189855&ad_unit='+unit+'&custom_data='+token
  +'&reward_amount=1&reward_item='+item+'&timestamp='+when+'&transaction_id='+transaction;
 const raw=await crypto.subtle.sign({name:'ECDSA',hash:'SHA-256'},kp.privateKey,new TextEncoder().encode(data));
 const der=signatureToDer(raw),sig=Buffer.from(der).toString('base64url');
 return {url:'https://example.com/ludo/admob/ssv?'+data+'&signature='+sig+'&key_id=1',keys};
}
test('DER ECDSA conversion preserves 64-byte WebCrypto signature',async()=>{
 const source=new Uint8Array(64);source[0]=0x80;source[32]=0x01;source[33]=0x10;
 assert.deepEqual(derToP1363_575(signatureToDer(source)),source);
});
test('real P-256 signature verification accepts only untouched AdMob query',async()=>{
 const id='0123456789abcdef0123456789abcdef';
 const signedCb=await signed(id);
 const a=await verifyAdmobSSV575(signedCb.url,{keys:signedCb.keys,now:()=>t});
 assert.equal(a.token,id);assert.equal(a.adUnit,'123456789');
 await assert.rejects(verifyAdmobSSV575(signedCb.url.replace('reward_amount=1','reward_amount=9'),
  {keys:signedCb.keys,now:()=>t}),/invalid_signature/);
 await assert.rejects(verifyAdmobSSV575(signedCb.url,{keys:signedCb.keys,now:()=>t+3*86400000}),
  /invalid_callback/);
 await assert.rejects(verifyAdmobSSV575(signedCb.url,{keys:{keys:[]},now:()=>t}),
  /ad_keys_unavailable/);
});
test('verified callback adds 30 chips once and consumes ad session atomically',async()=>{
 const db=store();
 const ad=await createAdSession575(db,'alice',t);
 const signature=await signed(ad.token);
 const evt=await verifyAdmobSSV575(signature.url,{keys:signature.keys,now:()=>t});
 const got=await applyAdmobReward575(db,evt,t+30000,'ca-app-pub-1234567890/123456789');
 assert.equal(got.accepted,true);assert.equal(got.duplicate,false);
 assert.equal((await ludoWallet575(db,'alice')).chips,30);
 const repeated=await applyAdmobReward575(db,evt,t+40000,'ca-app-pub-1234567890/123456789');
 assert.equal(repeated.duplicate,true);
 assert.equal((await ludoWallet575(db,'alice')).chips,30);
});
test('never pay an expired or unknown session or wrong ad unit',async()=>{
 const db=store(),ad=await createAdSession575(db,'alice',t);
 const event=await verifyAdmobSSV575((await signed(ad.token)).url,{
  keys:(await signed(ad.token)).keys,now:()=>t
 }).catch(()=>null);
 // Independently construct a trusted/previously cryptographically verified record.
 const trusted={transactionId:'0123456789abcdef0123456789',token:ad.token,adUnit:'123456789',rewardItem:'chips',rewardAmount:1,timestamp:t};
 await assert.rejects(applyAdmobReward575(db,trusted,t+16*60000,'123456789'),/invalid_ad_session/);
 await assert.rejects(applyAdmobReward575(db,trusted,t+1000,'999999999'),/unapproved_ad_unit/);
 assert.equal((await ludoWallet575(db,'alice')).chips,0);
});
test('failed database transaction cannot credit partial rewarded ad',async()=>{
 const db=store(),ad=await createAdSession575(db,'alice',t);
 const rec={transactionId:'0123456789abcdefabcd',token:ad.token,adUnit:'123456789',rewardItem:'chips',rewardAmount:1,timestamp:t};
 const broken={get:db.get.bind(db),putMany:async()=>{throw Object.assign(Error('db down'),{status:503});}};
 await assert.rejects(applyAdmobReward575(broken,rec,t+1000,'123456789'),/db down/);
 assert.equal((await ludoWallet575(db,'alice')).chips,0);
});
test('unconfigured ads cannot be credited, including fake view-complete requests',async()=>{
 const db=store();
 const api=createLudo565({store:db,verify:async()=>({sub:'alice'}),profile:async()=>({}),now:()=>t});
 const request=(action)=>new Request('https://example.com/ludo',{method:'POST',
  headers:{authorization:'Bearer test','content-type':'application/json'},body:JSON.stringify({action})});
 const resp=await api(request('ad_session'));assert.equal(resp.status,503);
 const x=await api(request('ad_complete'));assert.notEqual(x.status,200);
 const cb=ludoAdmobEndpoint575({store:db,env:{},now:()=>t});
 assert.equal((await cb(new Request('https://example.com/ludo/admob/ssv?transaction_id=evil'))).status,503);
 assert.equal((await ludoWallet575(db,'alice')).chips,0);
});
test('endpoint validates signature and only then returns HTTP 200',async()=>{
 const db=store(),ad=await createAdSession575(db,'alice',t);
 const signedCb=await signed(ad.token);
 const handler=ludoAdmobEndpoint575({store:db,env:{LUDO_ADMOB_AD_UNIT:'ca-app-pub-123/123456789'},
  now:()=>t+2500,fetcher:async()=>Response.json(signedCb.keys)});
 const response=await handler(new Request(signedCb.url));
 assert.equal(response.status,200);
 assert.equal((await ludoWallet575(db,'alice')).chips,30);
 const altered=await handler(new Request(signedCb.url.replace('reward_amount=1','reward_amount=2')));
 assert.equal(altered.status,403);
 assert.equal((await ludoWallet575(db,'alice')).chips,30);
});
