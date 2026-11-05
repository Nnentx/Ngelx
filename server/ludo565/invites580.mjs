import {act,LudoError} from './engine.mjs';
import {startFull592} from './dice592.mjs';

// A capability in the chat message exposes only the invitation presentation.
// Joining is authenticated, expiry checked by server time and committed with the room.
export async function invitation580({body:b,uid,store,now,roll,profile}){
 if(b.action==='invite_create'){
  if(!/^(?:[0-9]{6}|[A-F0-9]{16})$/.test(b.id??'')||
     !/^[a-zA-Z0-9_-]{16,100}$/.test(b.requestId??''))throw new LudoError('invalid_request');
  const source=await store.get(b.id),room=source?.room;
  if(!room||room.expiresAt<=now)throw new LudoError('room_expired',410);
  const player=room.players.find(p=>p.uid===uid&&!p.left);
  if(!player)throw new LudoError('not_a_player',403);
  if(room.status!=='waiting')throw new LudoError('not_available',409);
  const hash=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid+':'+b.id+':'+b.requestId));
  const token=Array.from(new Uint8Array(hash),x=>x.toString(16).padStart(2,'0')).join('');
  const id='invite580_'+token;
  const old=await store.get(id);
  if(old)return view(old.room,now,room,uid);
  const invite={token,roomId:room.id,from:uid,name:player.name,photo:player.photo??'',
   mode:room.mode,createdAt:now,expiresAt:Math.min(now+120000,room.expiresAt),status:'pending',revision:0};
  try{await store.put(id,invite);}catch(e){if(e.status!==409)throw e;return view((await store.get(id)).room,now);}
  return view(invite,now,room,uid);
 }
 if(!/^[a-f0-9]{64}$/.test(b.inviteToken??''))throw new LudoError('invalid_invite');
 const key='invite580_'+b.inviteToken;
 for(let attempt=0;attempt<4;attempt++){
  const entry=await store.get(key);
  if(!entry)throw new LudoError('invite_expired',410);
  const i=entry.room;
  if(b.action==='invite_status'){
   const room=await store.get(i.roomId);
   return view(i,now,room?.room,uid);
  }
  if(b.action!=='invite_join')throw new LudoError('invalid_request');
  const source=await store.get(i.roomId);
  if(!source||source.room.expiresAt<=now)throw new LudoError('room_expired',410);
  const existing=source.room.players.find(p=>p.uid===uid&&!p.left);
  if(existing)return {joinedRoom:source.room};
  if(i.expiresAt<=now)throw new LudoError('invite_expired',410);
  if(source.room.status!=='waiting'||source.room.players.filter(p=>!p.left).length>=source.room.capacity)throw new LudoError('room_full',409);
  if(!['pending','joined'].includes(i.status))throw new LudoError('invite_used',409);
  if(source.room.capacity===4){source.room.diceMode592='balanced';}
  const p=await profile(uid);
  const joined=startFull592(act(source.room,uid,{action:'join',name:p?.displayName??p?.username??'Oyuncu',photo:p?.photoUrl??''},now,roll),now);
  const joinedBy=[...new Set([...(i.joinedBy??(i.acceptedBy?[i.acceptedBy]:[])),uid])];
  try{
   await store.putMany([{id:i.roomId,room:joined,stamp:source.stamp},
    {id:key,room:{...i,status:joined.status==='waiting'?'pending':'joined',acceptedBy:i.acceptedBy??uid,joinedBy,joinedAt:now,revision:i.revision+1},stamp:entry.stamp}]);
   return {joinedRoom:joined};
  }catch(e){if(e.status!==409||attempt===3)throw e;}
 }
 throw new LudoError('state_changed',409);
}
function view(i,now,room,uid){
 const joined=room?.players?.filter(p=>!p.left).length??0;
 const capacity=room?.capacity??2;
 const available=room?.status==='waiting'&&joined<capacity&&room.expiresAt>now&&i.expiresAt>now;
 const full=joined>=capacity&&['waiting','playing'].includes(room?.status);
 return {inviteToken:i.token,id:i.roomId,name:i.name,photo:i.photo,mode:i.mode,
  createdAt:i.createdAt,expiresAt:i.expiresAt,serverNow:now,capacity,joined,
  remaining:Math.max(0,capacity-joined),viewerJoined:room?.players?.some(p=>p.uid===uid&&!p.left)??false,
  status:available?'pending':full?'joined':'expired'};
}
