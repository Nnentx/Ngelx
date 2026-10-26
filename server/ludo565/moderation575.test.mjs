import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act} from './engine.mjs';
import {createLudo565} from '../../cloudflare/live-moderation/src/ludo565.mjs';
import {ludoReport575} from './safety575.mjs';
import {ludoModeratorQueue575,ludoModeratorResolve575,moderationDay575,moderationQueueKey575} from './moderation575.mjs';

const now=1800000000000;
function memory(){
 const db=new Map();let clock=0;
 return {
  db,
  async get(id){return db.get(id)??null;},
  async put(id,room,stamp){
   if((db.get(id)?.stamp??undefined)!==stamp)throw Object.assign(Error('CAS'),{status:409});
   db.set(id,{room:structuredClone(room),stamp:String(++clock)});
  },
  async putMany(changes){
   if(changes.some(x=>(db.get(x.id)?.stamp??undefined)!==x.stamp))
    throw Object.assign(Error('CAS'),{status:409});
   changes.forEach(x=>db.set(x.id,{room:structuredClone(x.room),stamp:String(++clock)}));
  },
 };
}
async function setup(){
 const store=memory();
 let r=createRoom({uid:'alice',name:'Alice',id:'925575'},now);
 r=act(r,'bob',{action:'join',name:'Bob'},now);
 r=act(r,'alice',{action:'start',revision:r.revision,requestId:'mod-start575'},now);
 await store.put(r.id,r);
 return {store,room:r};
}
const api=(store,isModerator=async()=>false)=>createLudo565({
 store,isModerator,verify:async req=>({sub:req.headers.get('x-player')}),
 profile:async uid=>({displayName:uid}),now:()=>now+4000,roll:()=>6,
});
async function call(handler,uid,data){
 const response=await handler(new Request('https://example.test/ludo',{
  method:'POST',headers:{authorization:'Bearer valid','content-type':'application/json','x-player':uid},
  body:JSON.stringify(data),
 }));
 return {status:response.status,body:await response.json()};
}
test('reports are atomically listed in a private daily moderator inbox',async()=>{
 const {store,room}=await setup(),handle=api(store,async uid=>uid==='trusted-mod');
 let res=await call(handle,'alice',{action:'report',id:room.id,to:'bob',reason:'harassment'});
 assert.equal(res.status,200);assert.equal(res.body.room.submitted,true);
 const day=moderationDay575(now+4000);
 const q=await store.get(moderationQueueKey575(day));
 assert.equal(q.room.items.length,1);
 assert.match(q.room.items[0],/^report575_[a-f0-9]{64}$/);
 res=await call(handle,'alice',{action:'report',id:room.id,to:'bob',reason:'spam'});
 assert.equal(res.body.room.alreadyReported,true);
 assert.equal((await store.get(moderationQueueKey575(day))).room.items.length,1);
 res=await call(handle,'trusted-mod',{action:'moderation_queue'});
 assert.equal(res.status,200);
 assert.equal(res.body.room.reports.length,1);
 assert.equal(res.body.room.reports[0].reason,'harassment');
 assert.equal(res.body.room.reports[0].status,'pending');
});
test('unlisted signed-in users cannot view or resolve sensitive reports',async()=>{
 const {store,room}=await setup(),handle=api(store);
 await call(handle,'alice',{action:'report',id:room.id,to:'bob',reason:'spam'});
 const id=(await store.get(moderationQueueKey575(moderationDay575(now+4000)))).room.items[0];
 for(const action of ['moderation_queue','moderation_resolve']){
  const res=await call(handle,'alice',{action,reportId:id,decision:'actioned'});
  assert.equal(res.status,403);
  assert.equal(res.body.error,'moderator_only');
 }
 assert.equal((await store.get(id)).room.status,'pending');
});
test('a trusted moderator can resolve a report once, with stored identity and time',async()=>{
 const {store,room}=await setup(),handle=api(store,async uid=>uid==='trusted-mod');
 await call(handle,'alice',{action:'report',id:room.id,to:'bob',reason:'spam'});
 const id=(await store.get(moderationQueueKey575(moderationDay575(now+4000)))).room.items[0];
 let res=await call(handle,'trusted-mod',{action:'moderation_resolve',reportId:id,decision:'dismissed'});
 assert.equal(res.status,200);assert.equal(res.body.room.changed,true);
 assert.equal((await store.get(id)).room.moderator,'trusted-mod');
 assert.equal((await store.get(id)).room.resolvedAt,now+4000);
 res=await call(handle,'trusted-mod',{action:'moderation_resolve',reportId:id,decision:'actioned'});
 assert.equal(res.body.room.changed,false);assert.equal(res.body.room.status,'dismissed');
 const bad=await call(handle,'trusted-mod',{action:'moderation_resolve',reportId:'nonsense',decision:'actioned'});
 assert.equal(bad.status,400);
});
test('two concurrent separate reports both appear after CAS retry',async()=>{
 const {store,room}=await setup(),handle=api(store,async uid=>uid==='trusted-mod');
 const [a,b]=await Promise.all([
  call(handle,'alice',{action:'report',id:room.id,to:'bob',reason:'harassment'}),
  call(handle,'bob',{action:'report',id:room.id,to:'alice',reason:'cheating'}),
 ]);
 assert.equal(a.status,200);assert.equal(b.status,200);
 const q=await ludoModeratorQueue575(store,moderationDay575(now+4000),now+4000);
 assert.equal(q.reports.length,2);
 assert.deepEqual(new Set(q.reports.map(x=>x.reporter)),new Set(['alice','bob']));
});
test('when moderator index atomic commit fails, no invisible report document exists',async()=>{
 const {store,room}=await setup();
 const unavailable={get:store.get.bind(store),putMany:async()=>{throw Error('upstream_offline');}};
 await assert.rejects(ludoReport575(unavailable,room.id,'alice','bob','spam',now+4000),/upstream_offline/);
 assert.equal([...store.db.keys()].filter(x=>x.startsWith('report575_')).length,0);
});
test('invalid or old moderator queue days cannot access unlimited records',async()=>{
 const {store}=await setup();
 await assert.rejects(ludoModeratorQueue575(store,'2020-01-01',now),/invalid_review_day/);
 await assert.rejects(ludoModeratorQueue575(store,'9999-01-01',now),/invalid_review_day/);
 await assert.rejects(ludoModeratorQueue575(store,'not-a-day',now),/invalid_review_day/);
 await assert.rejects(ludoModeratorResolve575(store,'report575_bad','mod','actioned',now),/invalid_report_id/);
});

test('moderator inbox pagination keeps all older reviews accessible',async()=>{
 const store=memory(),day=moderationDay575(now),ids=[];
 for(let i=0;i<105;i++){
  const id='report575_'+i.toString(16).padStart(64,'0');
  ids.push(id);await store.put(id,{reporter:'u'+i,reported:'target',status:'pending',at:now+i});
 }
 await store.put(moderationQueueKey575(day),{day,items:ids});
 const first=await ludoModeratorQueue575(store,day,now,0);
 const second=await ludoModeratorQueue575(store,day,now,1);
 const third=await ludoModeratorQueue575(store,day,now,2);
 assert.deepEqual([first.reports.length,second.reports.length,third.reports.length],[50,50,5]);
 assert.deepEqual([first.hasMore,second.hasMore,third.hasMore],[true,true,false]);
 assert.equal(new Set([...first.reports,...second.reports,...third.reports].map(x=>x.id)).size,105);
 await assert.rejects(ludoModeratorQueue575(store,day,now,-1),/invalid_review_page/);
 await assert.rejects(ludoModeratorQueue575(store,day,now,'1'),/invalid_review_page/);
});
