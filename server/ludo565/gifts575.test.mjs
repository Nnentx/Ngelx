import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act} from './engine.mjs';
import {sendLudoGift575} from './gifts575.mjs';
import {claimDaily575,ludoWallet575} from './rewards575.mjs';
import {createLudo565,ludoStore565} from '../../cloudflare/live-moderation/src/ludo565.mjs';

const t=1800000000000;
function mock(){
 const db=new Map();let next=0;
 return {
  async get(id){return db.get(id)??null;},
  async put(id,room,stamp){const prev=db.get(id);if((prev?.stamp??undefined)!==stamp)throw Object.assign(Error('state_changed'),{status:409});db.set(id,{room:structuredClone(room),stamp:String(++next)});},
  async putMany(updates){
   if(updates.some(({id,stamp})=>(db.get(id)?.stamp??undefined)!==stamp))
    throw Object.assign(Error('state_changed'),{status:409});
   updates.forEach(({id,room})=>db.set(id,{room:structuredClone(room),stamp:String(++next)}));
  },
  db,
 };
}
async function room(store){
 let r=createRoom({uid:'a',name:'Ali',id:'777777'},t);
 r=act(r,'b',{action:'join',name:'Bora'},t);
 r=act(r,'a',{action:'start',revision:r.revision,requestId:'start575-gift'},t);
 await store.put(r.id,r);
 return r;
}
test('gift costs sender chips and atomically adds collectible to recipient',async()=>{
 const db=mock(),r=await room(db);
 await claimDaily575(db,'a',t);
 const sent=await sendLudoGift575(db,r.id,'a',{to:'b',kind:'flower',requestId:'gift-abc123'},t+5000);
 assert.equal(sent.sent,true);
 assert.equal(sent.chips,30);
 assert.equal(sent.room.gifts[0].emoji,'🌹');
 const recipient=Array.from(db.db).filter(([key,v])=>key.startsWith('wallet575_')&&v.room.giftsReceived?.flower===1);
 assert.equal(recipient.length,1);
 assert.equal((await ludoWallet575(db,'a')).chips,30);
});
test('replaying a gift request cannot charge twice',async()=>{
 const db=mock(),r=await room(db);
 await claimDaily575(db,'a',t);
 const args={to:'b',kind:'flower',requestId:'gift-replay01'};
 await sendLudoGift575(db,r.id,'a',args,t+5000);
 const repeat=await sendLudoGift575(db,r.id,'a',args,t+5001);
 assert.equal(repeat.alreadySent,true);assert.equal(repeat.chips,30);
 assert.equal((await db.get(r.id)).room.gifts.length,1);
});
test('no gift if coins insufficient, player is outsider, self or kind is invalid',async()=>{
 const db=mock(),r=await room(db);
 const valid={to:'b',kind:'heart',requestId:'gift-rejected'};
 await assert.rejects(sendLudoGift575(db,r.id,'a',valid,t+4000),/insufficient_chips/);
 await claimDaily575(db,'a',t);
 await assert.rejects(sendLudoGift575(db,r.id,'x',valid,t+4000),/gift_player_unavailable/);
 await assert.rejects(sendLudoGift575(db,r.id,'a',{...valid,to:'a'},t+4000),/cannot_gift_self/);
 await assert.rejects(sendLudoGift575(db,r.id,'a',{...valid,kind:'constructor'},t+4000),/invalid_gift/);
 assert.equal((await ludoWallet575(db,'a')).chips,50);
});
test('requires atomic store for transfer, fails closed with no payment',async()=>{
 const db=mock(),r=await room(db);await claimDaily575(db,'a',t);
 const nonAtomic={get:db.get.bind(db),put:db.put.bind(db)};
 await assert.rejects(sendLudoGift575(nonAtomic,r.id,'a',{to:'b',kind:'flower',requestId:'gift-no-store'},t+4000),/gift_store_unavailable/);
 assert.equal((await ludoWallet575(db,'a')).chips,50);
});
test('recipient room limits and 3-second cooldown are server enforced',async()=>{
 const db=mock(),r=await room(db);await claimDaily575(db,'a',t);
 await sendLudoGift575(db,r.id,'a',{to:'b',kind:'flower',requestId:'gift-first001'},t+4000);
 await assert.rejects(sendLudoGift575(db,r.id,'a',{to:'b',kind:'flower',requestId:'gift-second01'},t+4001),/gift_slow_down/);
 assert.equal((await db.get(r.id)).room.gifts.length,1);
});
test('Firestore atomic gift commit carries three compare-and-swap preconditions',async()=>{
 const calls=[];
 const store=ludoStore565({FIREBASE_PROJECT_ID:'ngelx-44eed'},
  {authorize:async()=>'token',fetcher:async(url,opt)=>{calls.push({url,opt});return Response.json({ok:true});}});
 await store.putMany([
  {id:'alice',room:{chips:80},stamp:'2026-10-26T09:30:00Z'},
  {id:'bob',room:{giftsReceived:{flower:1}}},
  {id:'777777',room:{gifts:[]},stamp:'2026-10-26T09:30:01Z'},
 ]);
 const sent=calls[0];
 assert.equal(sent.opt.method,'POST');
 assert.ok(sent.url.endsWith('/documents:commit'));
 const body=JSON.parse(sent.opt.body);
 assert.equal(body.writes.length,3);
 assert.deepEqual(body.writes.map(w=>Boolean(w.currentDocument.exists===false)),[false,true,false]);
 assert.equal(body.writes[1].update.fields.state.stringValue,JSON.stringify({giftsReceived:{flower:1}}));
});
test('authenticated gift endpoint debits coins and shows recipient profile items',async()=>{
 const store=mock();let r=await room(store);await claimDaily575(store,'a',t);
 const handle=createLudo565({store,verify:async req=>({sub:req.headers.get('x-user')}),
  profile:async uid=>({displayName:uid}),now:()=>t+7000,roll:()=>6});
 const send=async(uid,b)=>{
  const result=await handle(new Request('https://example.test/ludo',
   {method:'POST',headers:{authorization:'Bearer valid','content-type':'application/json','x-user':uid},
    body:JSON.stringify(b)}));
  return {status:result.status,body:await result.json()};
 };
 const a=await send('a',{action:'gift',id:r.id,to:'b',kind:'flower',requestId:'gift-http001'});
 assert.equal(a.status,200);
 assert.equal(a.body.room.chips,30);
 assert.equal(a.body.room.gifts[0].kind,'flower');
 const b=await send('b',{action:'wallet'});
 assert.equal(b.status,200);
 assert.equal(b.body.room.receivedGifts?.flower??0,1);
 const bad=await send('outsider',{action:'gift',id:r.id,to:'b',kind:'flower',requestId:'gift-http002'});
 assert.equal(bad.status,403);
});
