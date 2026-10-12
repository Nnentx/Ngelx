import {fresh, millis} from '../livekit443/room-policy.mjs';
export function callPushEvent(before, after, now) {
  if (!after || !Array.isArray(after.members) || !after.members.includes(after.callStartedBy) ||
      typeof after.callRoomName !== 'string' || !after.callRoomName || after.members.length>60) return null;
  if(before?.callRoomName===after.callRoomName&&before?.callStatus===after.callStatus)return null;
  const incoming=after.callStatus==='ringing';
  if(incoming&&!fresh(after.callCreatedAt,now,60_000))return null;
  if(!incoming&&!['active','ended','rejected','missed'].includes(after.callStatus))return null;
  return {kind:incoming?'incoming_call':'call_end',roomName:after.callRoomName,
    video:String(after.callVideo===true),title:String(after.callTitle??after.groupName??'NgelX araması').slice(0,100),
    expiresAt:String(incoming?Math.min(now+60_000,millis(after.callCreatedAt)+60_000):now+60_000),
    recipients:[...new Set(after.members)].filter(uid=>uid!==after.callStartedBy&&typeof uid==='string'&&uid&&!uid.includes('/'))};
}
