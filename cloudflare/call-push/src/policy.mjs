export const CHUNK=4;
const list=x=>Array.isArray(x)?x:[];
export const fresh=(date,now)=>Number.isFinite(date)&&now-date>=-30000&&now-date<=60000;
export function eventFor(uid, chat, room, now){
 if(!chat||!list(chat.members).includes(uid)||!list(chat.members).includes(chat.callStartedBy)||chat.callRoomName!==room||chat.members.length>60)return null;
 const incoming=chat.callStatus==='ringing';
 if(incoming&&(uid!==chat.callStartedBy||!fresh(chat.callCreatedAt,now)))return null;
 if(!incoming&&(!['active','ended','rejected','missed'].includes(chat.callStatus)||!fresh(chat.callStatus==='active'?chat.callAnsweredAt:chat.callEndedAt,now)))return null;
 return {kind:incoming?'incoming_call':'call_end',roomName:room,video:String(chat.callVideo===true),
  expiresAt:String(incoming?Math.min(now+60000,chat.callCreatedAt+60000):now+60000),
  title:String(chat.callTitle??chat.groupName??'NgelX araması').slice(0,100),
  recipients:[...new Set(chat.members)].filter(x=>typeof x==='string'&&x&&x!==chat.callStartedBy&&!x.includes('/'))};
}
export function eligible(sender,peer,uid){return !!sender&&!!peer&&!sender.deleted&&!sender.deactivated&&!peer.deleted&&!peer.deactivated&&peer.notificationsEnabled!==false&&!list(sender.blocked).includes(uid)&&!list(peer.blocked).includes(sender.uid);}
export function validBody(v){return v&&Object.keys(v).every(k=>['chatId','roomName','offset'].includes(k))&&typeof v.chatId==='string'&&/^[A-Za-z0-9_-]{1,150}$/.test(v.chatId)&&typeof v.roomName==='string'&&/^[A-Za-z0-9_-]{1,200}$/.test(v.roomName)&&Number.isInteger(v.offset??0)&&(v.offset??0)>=0&&(v.offset??0)<60&&(v.offset??0)%CHUNK===0;}
