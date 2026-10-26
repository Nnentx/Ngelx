// AdMob rewarded SSV. Nothing credits a user unless Google's signature verifies.
// Live rollout remains OFF without the publisher's configured ad unit and mobile SDK.
import {LudoError} from './engine.mjs';
const fail=(code,status=400)=>{throw new LudoError(code,status);};
const keyServer='https://www.gstatic.com/admob/reward/verifier-keys.json';
const decoder=new TextDecoder(),encoder=new TextEncoder();
const decode64=(s)=>Uint8Array.from(atob(s.replace(/-/g,'+').replace(/_/g,'/')+'='.repeat((4-s.length%4)%4)),c=>c.charCodeAt(0));
const sha=async s=>{
 const h=await crypto.subtle.digest('SHA-256',encoder.encode(s));
 return Array.from(new Uint8Array(h),n=>n.toString(16).padStart(2,'0')).join('');
};
const walletKey=async uid=>'wallet575_'+await sha(uid);
// WebCrypto requires ECDSA signature in IEEE P1363 r||s form; AdMob supplies DER.
// Accept only canonical DER INTEGERs within the 32-byte P-256 range.
export function derToP1363_575(der){
 const a=der instanceof Uint8Array?der:new Uint8Array(der);
 if(a.length<8||a.length>73||a[0]!==0x30||a[1]!==a.length-2)fail('invalid_signature');
 let i=2;const parts=[];
 for(let n=0;n<2;n++){
  if(a[i++]!==0x02)fail('invalid_signature');
  const len=a[i++];if(len<1||len>33||i+len>a.length)fail('invalid_signature');
  const val=a.slice(i,i+len);i+=len;
  if(val[0]&0x80)fail('invalid_signature');
  if(len===33&&val[0]!==0)fail('invalid_signature');
  if(len>1&&val[0]===0&&!(val[1]&0x80))fail('invalid_signature');
  const raw=val[0]===0?val.slice(1):val;
  if(raw.length>32)fail('invalid_signature');
  const padded=new Uint8Array(32);padded.set(raw,32-raw.length);parts.push(padded);
 }
 if(i!==a.length)fail('invalid_signature');
 const out=new Uint8Array(64);out.set(parts[0]);out.set(parts[1],32);
 return out;
}
export async function verifyAdmobSSV575(url,{fetcher=fetch,now=Date.now,keys}={}){
 const parsed=new URL(url);
 if(parsed.search.length>4096)fail('invalid_callback');
 const query=parsed.search.slice(1);
 const parts=/^(.*)&signature=([A-Za-z0-9_-]+)&key_id=([0-9]{1,15})$/.exec(query);
 if(!parts||parts[1].includes('&signature=')||parts[1].includes('&key_id='))
  fail('invalid_callback');
 const data=parts[1],params=new URLSearchParams(data);
 for(const required of ['transaction_id','timestamp','custom_data','ad_unit','reward_amount','reward_item']){
  if(params.getAll(required).length!==1)fail('invalid_callback');
 }
 const transactionId=params.get('transaction_id'),token=params.get('custom_data'),timestamp=Number(params.get('timestamp'));
 if(!/^[a-fA-F0-9]{12,128}$/.test(transactionId)||!/^[a-f0-9]{32}$/.test(token)
   ||!Number.isSafeInteger(timestamp)||Math.abs(now()-timestamp)>24*3600000)fail('invalid_callback');
 if(!/^[0-9]{1,24}$/.test(params.get('ad_unit')??''))fail('invalid_callback');
 if(!/^[0-9]{1,8}$/.test(params.get('reward_amount')??''))fail('invalid_callback');
 let response=keys;
 if(!response){
  const res=await fetcher(keyServer,{signal:AbortSignal.timeout(5000)});
  if(!res.ok)fail('ad_keys_unavailable',503);
  response=await res.json();
 }
 if(!Array.isArray(response?.keys)||response.keys.length===0)fail('ad_keys_unavailable',503);
 const entry=response.keys.find(k=>String(k.keyId)===parts[3]);
 if(!entry?.base64)fail('unknown_ad_key',503);
 let valid=false;
 try{
  const pub=await crypto.subtle.importKey('spki',decode64(entry.base64),
   {name:'ECDSA',namedCurve:'P-256'},false,['verify']);
  valid=await crypto.subtle.verify({name:'ECDSA',hash:'SHA-256'},pub,
   derToP1363_575(decode64(parts[2])),encoder.encode(data));
 }catch(e){if(e instanceof LudoError)throw e;fail('invalid_signature');}
 if(!valid)fail('invalid_signature',403);
 return {transactionId,token,timestamp,adUnit:params.get('ad_unit'),
  rewardItem:params.get('reward_item'),rewardAmount:Number(params.get('reward_amount'))};
}
export async function createAdSession575(store,uid,now){
 if(typeof store?.putMany!=='function')fail('ad_store_unavailable',503);
 const key=await walletKey(uid),today=new Date(now).toISOString().slice(0,10);
 for(let retry=0;retry<6;retry++){
  const doc=await store.get(key),w=doc?.room??{chips:0,gems:0,xp:0,level:1,wins:0,losses:0,streak:0,receipts:{}};
  if(w.adDay===today&&(w.adCount??0)>=10)fail('ad_daily_limit',429);
  const attempts=w.adSessionDay===today?(w.adSessionCount??0):0;
  if(w.adPendingUntil>now&&/^[a-f0-9]{32}$/.test(w.adPending??'')){
   // Retry the same ad loading without consuming a new session or Firestore write.
   return {token:w.adPending,expiresAt:w.adPendingUntil,chipReward:30,reused:true};
  }
  if(attempts>=20)fail('ad_session_limit',429);
  const token=crypto.randomUUID().replaceAll('-','');
  const expiresAt=now+15*60000;
  const wallet={...w,adSessionDay:today,adSessionCount:attempts+1,
   adPending:token,adPendingUntil:expiresAt};
  try{
   await store.putMany([
    {id:key,room:wallet,stamp:doc?.stamp},
    {id:'ad_session575_'+token,room:{uid,expiresAt,used:false},stamp:undefined},
   ]);
   return {token,expiresAt,chipReward:30,reused:false};
  }catch(e){if(e.status!==409||retry===5)throw e;}
 }
 fail('ad_session_conflict',409);
}
export async function adRewardStatus575(store,uid,token,now){
 if(typeof token!=='string'||!/^[a-f0-9]{32}$/.test(token))fail('invalid_ad_session',400);
 const entry=await store.get('ad_session575_'+token),session=entry?.room;
 if(!session||session.uid!==uid)fail('invalid_ad_session',403);
 if(session.expiresAt+24*3600000<now)fail('ad_session_expired',410);
 return {verified:session.used===true,chipReward:session.used===true?30:0};
}
export async function applyAdmobReward575(store,event,now,adUnit){
 if(!adUnit||event.adUnit!==adUnit.split('/').at(-1)||event.rewardAmount<1||event.rewardItem!=='chips')
  fail('unapproved_ad_unit',403);
 const sessionKey='ad_session575_'+event.token,receiptKey='ad_receipt575_'+event.transactionId;
 for(let tries=0;tries<6;tries++){
  const [sessionRecord,receipt]=await Promise.all([store.get(sessionKey),store.get(receiptKey)]);
  if(receipt)return {accepted:true,duplicate:true};
  const session=sessionRecord?.room;
  if(!session||session.used||session.expiresAt<now||session.expiresAt-15*60000>event.timestamp
   ||!session.uid)fail('invalid_ad_session',403);
  const wKey=await walletKey(session.uid),account=await store.get(wKey);
  const wallet=account?.room??{chips:0,gems:0,xp:0,level:1,wins:0,losses:0,streak:0,receipts:{}};
  const day=new Date(now).toISOString().slice(0,10),count=wallet.adDay===day?(wallet.adCount??0):0;
  if(count>=10)fail('ad_daily_limit',429);
  if(typeof store.putMany!=='function')fail('ad_store_unavailable',503);
  if(wallet.adPending!==event.token)fail('invalid_ad_session',403);
  const newWallet={...wallet,chips:(wallet.chips??0)+30,adDay:day,adCount:count+1,adPending:null,adPendingUntil:0};
  try{
   await store.putMany([
    {id:wKey,room:newWallet,stamp:account?.stamp},
    {id:sessionKey,room:{...session,used:true,transactionId:event.transactionId},stamp:sessionRecord.stamp},
    {id:receiptKey,room:{uid:session.uid,at:now,amount:30},stamp:undefined},
   ]);
   return {accepted:true,duplicate:false};
  }catch(e){if(e.status!==409||tries===5)throw e;}
 }
 fail('state_changed',409);
}
export function ludoAdmobEndpoint575({store,env,fetcher=fetch,now=Date.now}){
 return async request=>{
  if(request.method!=='GET')return Response.json({error:'method_not_allowed'},{status:405});
  if(!env.LUDO_ADMOB_AD_UNIT)return Response.json({error:'ads_not_configured'},{status:503});
  try{
   const callback=await verifyAdmobSSV575(request.url,{fetcher,now});
   const receipt=await applyAdmobReward575(store,callback,now(),env.LUDO_ADMOB_AD_UNIT);
   return Response.json({ok:receipt.accepted});
  }catch(e){return Response.json({error:e instanceof LudoError?e.message:'ad_verification_unavailable'},
   {status:e.status??503});}
 };
}
