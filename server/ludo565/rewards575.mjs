// Ludo-only server-authoritative wallet. No client may set or fabricate balances.
// CAS on one wallet document makes both the receipt and credit atomic/idempotent.
const initial=()=>({chips:0,gems:0,xp:0,level:1,wins:0,losses:0,streak:0,receipts:{}});
const key=async(uid)=>{
 const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid));
 return 'wallet575_'+Array.from(new Uint8Array(digest),b=>b.toString(16).padStart(2,'0')).join('');
};
export async function ludoWallet575(store,uid){
 const doc=await store.get(await key(uid));
 const w=doc?.room??initial();
 return {chips:w.chips??0,gems:w.gems??0,xp:w.xp??0,
  level:w.level??1,wins:w.wins??0,losses:w.losses??0,streak:w.streak??0};
}
export async function settleMatch575(store,uid,room,now){
 if(room?.status!=='finished'||!room?.id)return ludoWallet575(store,uid);
 const player=(room.players??[]).find(p=>p.uid===uid&&!p.bot&&!p.left);
 if(!player)return ludoWallet575(store,uid);
 // A machine opponent is not credited. A human is credited only for a validated match result.
 const won=room.winner!==null&&room.winner!==undefined&&
   (room.team?player.seat%2===room.winner:player.seat===room.winner);
 const walletKey=await key(uid);
 for(let retry=0;retry<6;retry++){
  const prev=await store.get(walletKey),w=prev?.room??initial();
  const receipts={...(w.receipts??{})};
  if(receipts[room.id])return ludoWallet575(store,uid);
  // A game room has a 6-hour lifetime. Keep receipts for another 48 hours.
  for(const [id,expiry] of Object.entries(receipts))if(typeof expiry==='number'&&expiry<now-48*3600000)delete receipts[id];
  receipts[room.id]=room.expiresAt??now;
  const chips=won?(room.botGame?35:150):0,xp=won?(room.botGame?35:90):15;
  const totalXp=(w.xp??0)+xp;
  const next={...w,receipts,chips:(w.chips??0)+chips,
   xp:totalXp,level:1+Math.floor(totalXp/200),
   wins:(w.wins??0)+(won?1:0),
   losses:(w.losses??0)+(won?0:1),
   streak:won?(w.streak??0)+1:0};
  try{
   await store.put(walletKey,next,prev?.stamp);
   return {chips:next.chips,gems:next.gems??0,xp:next.xp,level:next.level,
    wins:next.wins,losses:next.losses,streak:next.streak,reward:{chips,xp,win:won,matchId:room.id}};
  }catch(e){
   if(e.status!==409||retry===5)throw e;
  }
 }
 throw Error('wallet_cas_retries_exhausted');
}
