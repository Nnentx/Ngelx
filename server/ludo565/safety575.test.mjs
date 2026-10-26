import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act} from './engine.mjs';
import {createLudo565} from '../../cloudflare/live-moderation/src/ludo565.mjs';
import {claimDaily575,ludoWallet575} from './rewards575.mjs';

const time=1800000000000;
function memory(){
 const m=new Map();let n=1;
 return {
  get:async key=>m.get(key)??null,
  put:async(key,room,stamp)=>{
   const prev=m.get(key);
   if((prev?.stamp??undefined)!==stamp)throw Object.assign(Error('state_changed'),{status:409});
   m.set(key,{room:structuredClone(room),stamp:String(n++)});
  },
  putMany:async changes=>{
   if(changes.some(x=>(m.get(x.id)?.stamp??undefined)!==x.stamp))
    throw Object.assign(Error('state_changed'),{status:409});
   for(const x of changes)m.set(x.id,{room:structuredClone(x.room),stamp:String(n++)});
  },
  data:m,
 };
}
function setup(){
 const store=memory();
 let r=createRoom({uid:'alice',name:'Alice',id:'565575'},time);
 r=act(r,'bob',{action:'join',name:'Bob'},time);
 r=act(r,'alice',{action:'start',revision:r.revision,requestId:'start_safety575'},time);
 return {store,room:r};
}
const endpoint=(store)=>createLudo565({store,verify:async req=>({sub:req.headers.get('x-user')}),
 profile:async uid=>({displayName:uid}),now:()=>time+1000,roll:()=>6});
async function post(api,uid,body){
 const response=await api(new Request('https://example.com/ludo',{
  method:'POST',headers:{'content-type':'application/json',authorization:'Bearer valid','x-user':uid},
  body:JSON.stringify(body),
 }));
 return {status:response.status,room:(await response.json()).room,error:response.status>=400?'error':null};
}
test('Ludo block is private, idempotent and reversible without global accounts',async()=>{
 const {store,room}=setup();await store.put(room.id,room);
 const api=endpoint(store);
 let x=await post(api,'alice',{action:'block',id:room.id,to:'bob',blocked:true});
 assert.equal(x.status,200);assert.equal(x.room.blocked,true);
 x=await post(api,'alice',{action:'wallet'});
 assert.deepEqual(x.room.blockedUsers,['bob']);
 x=await post(api,'bob',{action:'wallet'});
 assert.deepEqual(x.room.blockedUsers,[]);
 x=await post(api,'alice',{action:'block',id:room.id,to:'bob',blocked:false});
 assert.equal(x.status,200);assert.deepEqual(x.room.blockedUsers,[]);
});
test('blocked player cannot send paid Ludo gifts and balance remains intact',async()=>{
 const {store,room}=setup();await store.put(room.id,room);
 await claimDaily575(store,'alice',time);
 const api=endpoint(store);
 await post(api,'bob',{action:'block',id:room.id,to:'alice',blocked:true});
 const failed=await post(api,'alice',{action:'gift',id:room.id,to:'bob',kind:'flower',requestId:'safe_gift575'});
 assert.equal(failed.status,403);
 assert.equal((await ludoWallet575(store,'alice')).chips,50);
 assert.equal((await store.get(room.id)).room.gifts,undefined);
});
test('report accepts only a participant, reason and one report per recipient per match',async()=>{
 const {store,room}=setup();await store.put(room.id,room);
 const api=endpoint(store);
 const report={action:'report',id:room.id,to:'bob',reason:'harassment'};
 let x=await post(api,'alice',report);
 assert.equal(x.status,200);assert.equal(x.room.submitted,true);
 x=await post(api,'alice',report);
 assert.equal(x.room.submitted,false);assert.equal(x.room.alreadyReported,true);
 x=await post(api,'outsider',report);
 assert.equal(x.status,403);
 x=await post(api,'alice',{...report,to:'alice'});
 assert.equal(x.status,400);
 x=await post(api,'alice',{...report,reason:'madeup'});
 assert.equal(x.status,400);
 const records=[...store.data.entries()].filter(([key])=>key.startsWith('report575_'));
 assert.equal(records.length,1);
 assert.equal(records[0][1].room.status,'pending');
});
test('no player may block another without having joined their room',async()=>{
 const {store,room}=setup();await store.put(room.id,room);
 const api=endpoint(store);
 const x=await post(api,'outsider',{action:'block',id:room.id,to:'bob',blocked:true});
 assert.equal(x.status,403);
});
