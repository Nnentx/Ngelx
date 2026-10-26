// Ludo-only moderator inbox. Server caller MUST verify Firebase identity and a
// deployment-owned moderator UID allowlist before invoking these functions.
import {LudoError} from './engine.mjs';
const fail=(code,status=400)=>{throw new LudoError(code,status);};
export const moderationDay575=now=>new Date(now).toISOString().slice(0,10);
export const moderationQueueKey575=day=>'moderation_queue575_'+day;
const validId=id=>typeof id==='string'&&/^report575_[a-f0-9]{64}$/.test(id);
const validDay=(day,now)=>typeof day==='string'&&/^\d{4}-\d{2}-\d{2}$/.test(day)
 &&Date.parse(day+'T00:00:00Z')<=now
 &&Date.parse(day+'T00:00:00Z')>=now-15*86400000;
export async function ludoModeratorQueue575(store,day,now){
 if(!validDay(day,now))fail('invalid_review_day');
 const current=await store.get(moderationQueueKey575(day));
 const list=current?.room?.items??[];
 if(!Array.isArray(list))fail('invalid_review_queue',503);
 // Queue only retains IDs/summaries; details and actions are held in separate docs.
 const items=await Promise.all(list.slice(-150).map(async id=>{
  if(!validId(id))return null;
  const entry=await store.get(id);
  return entry?{id,...entry.room}:null;
 }));
 return {day,reports:items.filter(Boolean),total:list.length};
}
export async function ludoModeratorResolve575(store,id,moderatorUid,decision,now){
 if(!validId(id))fail('invalid_report_id');
 if(!['reviewed','dismissed','actioned'].includes(decision))fail('invalid_decision');
 for(let attempt=0;attempt<6;attempt++){
  const entry=await store.get(id);
  if(!entry)fail('report_not_found',404);
  if(entry.room.status!=='pending'){
   return {changed:false,status:entry.room.status};
  }
  const updated={...entry.room,status:decision,moderator:moderatorUid,resolvedAt:now};
  try{
   await store.put(id,updated,entry.stamp);
   return {changed:true,status:decision};
  }catch(e){if(e.status!==409||attempt===5)throw e;}
 }
 fail('state_changed',409);
}
