import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act} from './engine.mjs';
import {ensureStarter575,ludoWallet575,settleMatch575,claimDaily575,claimChest575} from './rewards575.mjs';

const t=1800000000000;
function store(){
 const docs=new Map();
 return {get:async id=>docs.get(id)??null,put:async(id,room,stamp)=>{
  const old=docs.get(id);
  if((old?.stamp??undefined)!==stamp)throw Object.assign(Error('conflict'),{status:409});
  docs.set(id,{room:structuredClone(room),stamp:String((Number(old?.stamp??0))+1)});
 },size:()=>docs.size};
}
function game(){
 let r=createRoom({uid:'human',name:'Ben',id:'575575'},t);
 r=act(r,'other',{action:'join'},t);
 r=act(r,'human',{action:'start',revision:r.revision,requestId:'start575x'},t);
 r.status='finished';r.winner=0;
 return r;
}
test('win credits coins, XP and level only once per match/uid',async()=>{
 const db=store(),r=game();
 const a=await settleMatch575(db,'human',r,t+5000);
 assert.equal(a.chips,150);
 assert.equal(a.xp,90);
 assert.equal(a.wins,1);
 assert.equal(a.reward.chips,150);
 const b=await settleMatch575(db,'human',r,t+6000);
 assert.equal(b.chips,150);
 assert.deepEqual(b.reward,a.reward);
 assert.equal(db.size(),1);
});
test('loser resets win streak and cannot collect win coins',async()=>{
 const db=store();const r=game();
 const loser=await settleMatch575(db,'other',r,t+5000);
 assert.equal(loser.chips,0);
 assert.equal(loser.losses,1);
 assert.equal(loser.xp,15);
});
test('spectator or unfinished game cannot claim money',async()=>{
 const db=store();const r=game();
 const outsider=await settleMatch575(db,'stranger',r,t+5000);
 assert.equal(outsider.chips,0);
 r.status='playing';
 const player=await settleMatch575(db,'human',r,t+5000);
 assert.equal(player.chips,0);
 assert.equal(db.size(),0);
});
test('bot match pays lower real verified server amount',async()=>{
 const db=store();const r=game();r.botGame=true;
 const w=await settleMatch575(db,'human',r,t+5000);
 assert.equal(w.chips,35);assert.equal(w.xp,35);
});
test('a second verified win raises total coins, XP, streak and level',async()=>{
 const db=store();const a=game(),b=game();b.id='575576';
 const first=await settleMatch575(db,'human',a,t+5000);
 const second=await settleMatch575(db,'human',b,t+5000);
 assert.equal(first.level,1);
 assert.equal(second.chips,320);
 assert.equal(second.reward.streakBonus,20);
 assert.equal(second.streak,2);
 assert.equal(second.xp,180);
});

test('daily gift is claimed once per UTC day and streak is repeatable',async()=>{
 const db=store();
 const a=await claimDaily575(db,'human',t);assert.equal(a.claimed,true);assert.equal(a.chipReward,50);
 const b=await claimDaily575(db,'human',t+30000);assert.equal(b.claimed,false);assert.equal(b.chips,50);
 const c=await claimDaily575(db,'human',t+86400000);assert.equal(c.claimed,true);assert.equal(c.dailyStreak,2);assert.equal(c.chips,110);
});
test('treasure chest only credits again after eight hours',async()=>{
 const db=store(),a=await claimChest575(db,'human',t);
 assert.equal(a.claimed,true);assert.equal(a.chips,25);assert.equal(a.xp,10);
 const b=await claimChest575(db,'human',t+7*3600000);assert.equal(b.claimed,false);
 const c=await claimChest575(db,'human',t+8*3600000);
 assert.equal(c.chips,50);assert.equal(c.xp,20);assert.equal(c.claimed,true);
});

test('five-win streak pays capped bonus but cannot be claimed twice',async()=>{
 const db=store();
 for(let i=0;i<10;i++){
  const r=game();r.id='match_streak_'+i;
  const w=await settleMatch575(db,'human',r,t+5000);
  assert.equal(w.streak,i+1);
  assert.ok(w.reward.chips<=250);
  const after=await settleMatch575(db,'human',r,t+5100);
  assert.equal(after.chips,w.chips);
  assert.deepEqual(after.reward,w.reward);
 }
 const final=await ludoWallet575(db,'human');
 assert.equal(final.streak,10);
 assert.equal(final.chips,150+170+190+210+230+250*5);
});

test('network reconnect returns original win payout receipt without paying again',async()=>{
 const db=store(),room=game();
 const first=await settleMatch575(db,'human',room,t+5000);
 const same=await settleMatch575(db,'human',room,t+7000);
 assert.equal(same.reward.matchId,room.id);
 assert.deepEqual(same.reward,first.reward);
 assert.equal(same.chips,150);assert.equal(same.xp,90);
 assert.equal(same.wins,1);assert.equal(db.size(),1);
 // Other players never see this user's reward receipt or its value.
 const outsider=await settleMatch575(db,'spectator',room,t+7000);
 assert.equal(outsider.reward,undefined);
 assert.equal(outsider.chips,0);
});
test('reward receipt remains stable after claiming chest and daily gifts',async()=>{
 const db=store(),room=game();
 const result=await settleMatch575(db,'human',room,t+5000);
 await claimDaily575(db,'human',t+6000);
 await claimChest575(db,'human',t+6000);
 const replay=await settleMatch575(db,'human',room,t+7000);
 assert.deepEqual(replay.reward,result.reward);
 assert.equal(replay.chips,225);
 assert.equal(replay.wins,1);
 assert.equal(replay.xp,100);
});
test('match payout receipt stays on its own room and other room has distinct reward',async()=>{
 const db=store(),a=game(),b=game();
 b.id='575575_next_match';b.winner=1;
 const first=await settleMatch575(db,'human',a,t+5000);
 const second=await settleMatch575(db,'human',b,t+6000);
 assert.equal(second.reward.win,false);assert.equal(second.reward.xp,15);
 assert.equal(second.reward.matchId,b.id);
 const repeat=await settleMatch575(db,'human',a,t+7000);
 assert.deepEqual(repeat.reward,first.reward);
 assert.equal(repeat.chips,150);assert.equal(repeat.losses,1);
});
test('old settled wallet without matchReward metadata remains idempotent and never invents a payout',async()=>{
 const db=store(),r=game();
 await settleMatch575(db,'human',r,t+5000);
 const hash=await crypto.subtle.digest('SHA-256',new TextEncoder().encode('human'));
 const walletId='wallet575_'+Buffer.from(hash).toString('hex');
 const entry=await db.get(walletId),wallet={...entry.room};
 delete wallet.matchRewards; // Records saved by the earlier Build575 reward implementation.
 await db.put(walletId,wallet,entry.stamp);
 const older=await settleMatch575(db,'human',r,t+7000);
 assert.equal(older.reward,undefined);
 assert.equal(older.chips,150);assert.equal(older.wins,1);
 assert.equal(db.size(),1);
});

test('new account starter is persisted once under concurrent requests and reconnects',async()=>{
 const db=store();
 const values=await Promise.all(Array.from({length:5},()=>ensureStarter575(db,'new-player')));
 assert.ok(values.every(w=>w.chips===5000));assert.equal(db.size(),1);
 await claimDaily575(db,'new-player',t);
 assert.equal((await ensureStarter575(db,'new-player')).chips,5050);
 assert.equal((await ludoWallet575(db,'new-player')).chips,5050);
});
test('existing wallets keep their balance, XP, receipts and gifts without reset or grant',async()=>{
 const db=store();await claimDaily575(db,'existing',t);
 const before=await ludoWallet575(db,'existing');
 assert.deepEqual(await ensureStarter575(db,'existing'),before);
 assert.equal(before.chips,50);
});
test('starter storage errors fail closed without returning a fabricated balance',async()=>{
 await assert.rejects(ensureStarter575({get:async()=>null,put:async()=>{throw Error('unavailable');}},'new-player'),/unavailable/);
});
