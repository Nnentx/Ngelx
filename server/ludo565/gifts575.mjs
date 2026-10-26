// Build575 virtual Ludo gifts. Coins are play-only; they are never cash.
import {LudoError} from './engine.mjs';

export const ludoGiftCatalog575=Object.freeze({
  flower:Object.freeze({label:'Çiçek',emoji:'🌹',chips:20}),
  heart:Object.freeze({label:'Kalp',emoji:'❤️',chips:40}),
  crown:Object.freeze({label:'Taç',emoji:'👑',chips:100}),
});
const fail=(code,status=400)=>{throw new LudoError(code,status)};
const giftReceipt=(roomId,nonce)=>roomId+':'+nonce;
const hash=async(uid)=>{
  const raw=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid));
  return 'wallet575_'+Array.from(new Uint8Array(raw),b=>b.toString(16).padStart(2,'0')).join('');
};
const baseWallet=()=>({chips:0,gems:0,xp:0,level:1,wins:0,losses:0,streak:0,receipts:{}});

// One Firestore transaction atomically updates sender wallet, recipient collection and room.
// A JSON-only/local mock without putMany MUST fail closed, not split a payment into writes.
export async function sendLudoGift575(store,roomId,uid,request,now){
 if(!store||typeof store.putMany!=='function')fail('gift_store_unavailable',503);
 if(typeof request.requestId!=='string'||!/^[a-zA-Z0-9_-]{8,100}$/.test(request.requestId))fail('invalid_request');
 const gift=ludoGiftCatalog575[request.kind];
 if(!gift||typeof request.to!=='string'||request.to.length<1||request.to.length>128)fail('invalid_gift');
 if(uid===request.to)fail('cannot_gift_self');
 const senderKey=await hash(uid),receiverKey=await hash(request.to);
 for(let retry=0;retry<6;retry++){
  const roomEntry=await store.get(roomId);
  if(!roomEntry)fail('room_not_found',404);
  const room=roomEntry.room;
  if(room.expiresAt<=now)fail('room_expired',410);
  if(room.status!=='playing')fail('not_playing',409);
  const from=room.players.find(p=>p.uid===uid&&!p.left&&!p.bot);
  const to=room.players.find(p=>p.uid===request.to&&!p.left&&!p.bot);
  if(!from||!to)fail('gift_player_unavailable',403);
  const [senderEntry,receiverEntry]=await Promise.all([store.get(senderKey),store.get(receiverKey)]);
  const sender=senderEntry?.room??baseWallet(),receiver=receiverEntry?.room??baseWallet();
  const receipt=giftReceipt(room.id,request.requestId);
  if(sender.giftReceipts?.[receipt]){
   return {sent:false,alreadySent:true,chips:sender.chips,
    gift:request.kind,to:request.to,room};
  }
  if((sender.chips??0)<gift.chips)fail('insufficient_chips',409);
  if((room.giftLast?.[uid]??0)>now-3000)fail('gift_slow_down',429);
  // Per-room control prevents unbounded documents and rapidly repeated gifts.
  if((room.giftCounts?.[uid]??0)>=30)fail('gift_room_limit',429);
  const newReceipts={...(sender.giftReceipts??{})};
  for(const [key,time] of Object.entries(newReceipts))
   if(Number.isFinite(time)&&time<now-48*3600000)delete newReceipts[key];
  newReceipts[receipt]=now;
  const changedSender={...sender,chips:sender.chips-gift.chips,giftReceipts:newReceipts};
  const giftsReceived={...(receiver.giftsReceived??{}),
   [request.kind]:(receiver.giftsReceived?.[request.kind]??0)+1};
  const changedReceiver={...receiver,giftsReceived};
  const event={from:uid,fromName:from.name,to:to.uid,toName:to.name,kind:request.kind,
   label:gift.label,emoji:gift.emoji,at:now};
  const changedRoom={...room,revision:room.revision+1,
   giftLast:{...(room.giftLast??{}),[uid]:now},
   giftCounts:{...(room.giftCounts??{}),[uid]:(room.giftCounts?.[uid]??0)+1},
   gifts:[...(room.gifts??[]),event].slice(-12)};
  try{
   await store.putMany([
    {id:senderKey,room:changedSender,stamp:senderEntry?.stamp},
    {id:receiverKey,room:changedReceiver,stamp:receiverEntry?.stamp},
    {id:roomId,room:changedRoom,stamp:roomEntry.stamp},
   ]);
   return {sent:true,alreadySent:false,chips:changedSender.chips,
    gift:request.kind,to:request.to,room:changedRoom};
  }catch(e){
   if(e.status!==409||retry===5)throw e;
  }
 }
 fail('gift_conflict',409);
}
