import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act} from './engine.mjs';
import {ludoWallet575,settleMatch575,claimDaily575,claimChest575} from './rewards575.mjs';

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
 assert.equal(b.reward,undefined);
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
 assert.equal(second.chips,300);
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
