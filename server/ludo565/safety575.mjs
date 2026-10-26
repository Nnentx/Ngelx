// In-room safety actions. Ludo-only blocks and reporting do not change global NgelX relationships.
import {LudoError} from './engine.mjs';
import {moderationDay575,moderationQueueKey575} from './moderation575.mjs';

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
 if(typeof store.putMany!=='function')fail('report_store_unavailable',503);
 const id='report575_'+await sha(roomId+':'+uid+':'+to);
 const day=moderationDay575(now),queueKey=moderationQueueKey575(day);
 for(let attempt=0;attempt<6;attempt++){
  const [existing,q]=await Promise.all([store.get(id),store.get(queueKey)]);
  if(existing)return {submitted:false,alreadyReported:true};
  const items=q?.room?.items??[];
  if(!Array.isArray(items)||items.length>=500||items.includes(id))
   fail('report_queue_unavailable',503);
  // Firestore commits the record AND its moderator inbox entry together.
  // A half-saved report would otherwise be invisible to human reviewers.
  try{
   await store.putMany([
    {id,room:{roomId,reporter:uid,reported:to,reason,at:now,status:'pending'},stamp:undefined},
    {id:queueKey,room:{day,items:[...items,id]},stamp:q?.stamp},
   ]);
   return {submitted:true,alreadyReported:false};
  }catch(e){if(e.status!==409||attempt===5)throw e;}
 }
 fail('state_changed',409);
}
