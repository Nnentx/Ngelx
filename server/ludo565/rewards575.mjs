// Ludo-only server-authoritative wallet. No client may set or fabricate balances.
// CAS on one wallet document makes both the receipt and credit atomic/idempotent.
const initial=()=>({chips:0,gems:0,xp:0,level:1,wins:0,losses:0,streak:0,receipts:{}});
const key=async(uid)=>{
 const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid));
 return 'wallet575_'+Array.from(new Uint8Array(digest),b=>b.toString(16).padStart(2,'0')).join('');
};
const viewWallet=w=>({chips:w.chips??0,gems:w.gems??0,xp:w.xp??0,
 level:w.level??1,wins:w.wins??0,losses:w.losses??0,streak:w.streak??0,
 receivedGifts:w.giftsReceived??{},blockedUsers:w.blockedUsers??[]});
export async function ludoWallet575(store,uid){
 const doc=await store.get(await key(uid));
 return viewWallet(doc?.room??initial());
}
export async function settleMatch575(store,uid,room,now){
 if(room?.status!=='finished'||!room?.id||(room.expiresAt??Infinity)<=now)return ludoWallet575(store,uid);
 const player=(room.players??[]).find(p=>p.uid===uid&&!p.bot&&!p.left);
 if(!player)return ludoWallet575(store,uid);
 // A machine opponent is not credited. A human is credited only for a validated match result.
 const won=room.winner!==null&&room.winner!==undefined&&
   (room.team?player.seat%2===room.winner:player.seat===room.winner);
 const walletKey=await key(uid);
 for(let retry=0;retry<6;retry++){
  const prev=await store.get(walletKey),w=prev?.room??initial();
  const receipts={...(w.receipts??{})};
  if(receipts[room.id]){
   const priorReward=w.matchRewards?.[room.id];
   return {...viewWallet(w),...(priorReward?{reward:priorReward}:{})};
  }
  // A game room has a 6-hour lifetime. Keep receipts for another 48 hours.
  for(const [id,expiry] of Object.entries(receipts))if(typeof expiry==='number'&&expiry<now-48*3600000)delete receipts[id];
  receipts[room.id]=room.expiresAt??now;
  const matchRewards={...(w.matchRewards??{})};
  for(const id of Object.keys(matchRewards))if(!receipts[id])delete matchRewards[id];
  const nextStreak=won?(w.streak??0)+1:0;
  const streakBonus=won?Math.min(room.botGame?50:100,Math.max(0,nextStreak-1)*(room.botGame?10:20)):0;
  const chips=won?(room.botGame?35:150)+streakBonus:0,xp=won?(room.botGame?35:90):15;
  const totalXp=(w.xp??0)+xp;
  const reward={chips,xp,streakBonus,win:won,matchId:room.id};
  matchRewards[room.id]=reward;
  const next={...w,receipts,matchRewards,chips:(w.chips??0)+chips,
   xp:totalXp,level:1+Math.floor(totalXp/200),
   wins:(w.wins??0)+(won?1:0),
   losses:(w.losses??0)+(won?0:1),
   streak:nextStreak};
  try{
   await store.put(walletKey,next,prev?.stamp);
   return {...viewWallet(next),reward};
  }catch(e){
   if(e.status!==409||retry===5)throw e;
  }
 }
 throw Error('wallet_cas_retries_exhausted');
}

export async function claimDaily575(store,uid,now){
 const walletKey=await key(uid);
 const day=new Date(now).toISOString().slice(0,10);
 const previous=new Date(now-86400000).toISOString().slice(0,10);
 for(let retry=0;retry<6;retry++){
  const entry=await store.get(walletKey),wallet=entry?.room??initial();
  if(wallet.lastDaily===day){
   return {claimed:false,nextAt:Date.parse(day+'T00:00:00.000Z')+86400000, ...await ludoWallet575(store,uid)};
  }
  const streak=wallet.lastDaily===previous?(wallet.dailyStreak??0)+1:1;
  const chips=Math.min(100,40+10*streak);
  const updated={...wallet,lastDaily:day,dailyStreak:streak,
   chips:(wallet.chips??0)+chips};
  try{
   await store.put(walletKey,updated,entry?.stamp);
   return {claimed:true,chipReward:chips,dailyStreak:streak,nextAt:Date.parse(day+'T00:00:00.000Z')+86400000,
    chips:updated.chips,gems:updated.gems??0,xp:updated.xp??0,level:updated.level??1};
  }catch(e){if(e.status!==409||retry===5)throw e;}
 }
 throw Error('daily_cas_retries_exhausted');
}
export async function claimChest575(store,uid,now){
 const walletKey=await key(uid);
 for(let retry=0;retry<6;retry++){
  const entry=await store.get(walletKey),wallet=entry?.room??initial();
  const unlock=(wallet.lastChest??0)+8*3600000;
  if(now<unlock)return {claimed:false,nextAt:unlock,...await ludoWallet575(store,uid)};
  const updated={...wallet,lastChest:now,chips:(wallet.chips??0)+25,xp:(wallet.xp??0)+10};
  updated.level=1+Math.floor(updated.xp/200);
  try{
   await store.put(walletKey,updated,entry?.stamp);
   return {claimed:true,chipReward:25,xpReward:10,nextAt:now+8*3600000,
    chips:updated.chips,gems:updated.gems??0,xp:updated.xp,level:updated.level};
  }catch(e){if(e.status!==409||retry===5)throw e;}
 }
 throw Error('chest_cas_retries_exhausted');
}
