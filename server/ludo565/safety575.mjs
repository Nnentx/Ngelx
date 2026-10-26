// In-room safety actions. Ludo-only blocks and reporting do not change global NgelX relationships.
import {LudoError} from './engine.mjs';

const fail=(reason,status=400)=>{throw new LudoError(reason,status);};
const sha=async s=>{
 const h=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(s));
 return Array.from(new Uint8Array(h),b=>b.toString(16).padStart(2,'0')).join('');
};
const walletKey=async uid=>'wallet575_'+await sha(uid);
function verifyParticipants(room,uid,to,now){
 if(!room||room.expiresAt<=now)fail('room_expired',410);
 if(room.status==='closed')fail('room_closed',409);
 if(typeof to!=='string'||to.length<1||to.length>128||to===uid)fail('invalid_target');
 if(!room.players.some(p=>p.uid===uid&&!p.bot)||!room.players.some(p=>p.uid===to&&!p.bot))fail('player_unavailable',403);
}
export async function ludoBlock575(store,roomId,uid,to,blocked,now){
 if(typeof blocked!=='boolean')fail('invalid_settings');
 const match=await store.get(roomId);if(!match)fail('room_not_found',404);
 verifyParticipants(match.room,uid,to,now);
 const key=await walletKey(uid);
 for(let tries=0;tries<6;tries++){
  const entry=await store.get(key),wallet=entry?.room??{chips:0,xp:0,level:1};
  const blockedUsers=[...new Set(wallet.blockedUsers??[])].filter(x=>x!==to);
  if(blocked){
   if(blockedUsers.length>=100)fail('too_many_blocks',409);
   blockedUsers.push(to);
  }
  try{
   await store.put(key,{...wallet,blockedUsers},entry?.stamp);
   return {blocked,blockedUsers};
  }catch(e){if(e.status!==409||tries===5)throw e;}
 }
 fail('state_changed',409);
}
export async function ludoReport575(store,roomId,uid,to,reason,now){
 const match=await store.get(roomId);if(!match)fail('room_not_found',404);
 verifyParticipants(match.room,uid,to,now);
 if(!['spam','harassment','cheating','other'].includes(reason))fail('invalid_report_reason');
 const id='report575_'+await sha(roomId+':'+uid+':'+to);
 const existing=await store.get(id);
 if(existing)return {submitted:false,alreadyReported:true};
 // Once per room/target/reporter. Only server can review stored reports.
 try{
  await store.put(id,{roomId,reporter:uid,reported:to,reason,at:now,status:'pending'});
  return {submitted:true,alreadyReported:false};
 }catch(e){
  if(e.status===409)return {submitted:false,alreadyReported:true};
  throw e;
 }
}
