import {test} from 'node:test';
import assert from 'node:assert/strict';
import {balancedRoll592,publicRoom592} from './dice592.mjs';
import {LudoError} from './engine.mjs';
import {createLudo565} from '../../cloudflare/live-moderation/src/ludo565.mjs';
function fixture(){
 const data=new Map();let clock=1800000000000,reads=[];
 const check=(id,stamp)=>{if(data.get(id)?.stamp!==stamp)throw new LudoError('state_changed',409);};
 const put=(id,room)=>data.set(id,{room:structuredClone(room),stamp:String(Number(data.get(id)?.stamp??0)+1)});
 const store={get:async id=>{reads.push(id);return data.has(id)?structuredClone(data.get(id)):null;},
  put:async(id,room,stamp)=>{check(id,stamp);put(id,room);},
  putMany:async changes=>{for(const x of changes)check(x.id,x.stamp);for(const x of changes)put(x.id,x.room);}};
 const api=createLudo565({store,verify:async r=>({sub:r.headers.get('x-user')}),profile:async uid=>({displayName:uid}),now:()=>clock,uuid:()=>'592592'});
 const send=async(body,user='a')=>{
  const r=await api(new Request('https://test/ludo',{method:'POST',headers:{authorization:'Bearer valid','content-type':'application/json','x-user':user},body:JSON.stringify(body)}));
  return {status:r.status,...await r.json()};
 };
 return {data,send,advance:ms=>clock+=ms,resetReads:()=>reads=[],get reads(){return reads;}};
}
test('all four seats and bots get each face once per six accepted rolls; bags are private',()=>{
 const r={};
 for(let cycle=0;cycle<200;cycle++)for(let seat=0;seat<4;seat++){
  const faces=Array.from({length:6},()=>balancedRoll592(r,seat));
  assert.deepEqual([...faces].sort(),[1,2,3,4,5,6]);
 }
 assert.equal(publicRoom592(r).diceBags592,undefined);
});
test('one group invite admits the third and fourth concurrently, then auto-starts exactly once',async()=>{
 const f=fixture();await f.send({action:'create',capacity:4,mode:'classic'});
 const invite=(await f.send({action:'invite_create',id:'592592',requestId:'group_invite592_001'})).room;
 assert.equal((await f.send({action:'invite_join',inviteToken:invite.inviteToken},'b')).status,200);
 const early=await f.send({action:'start',id:'592592',revision:f.data.get('592592').room.revision,requestId:'early_start592'},'a');
 assert.equal(early.status,409);assert.equal(early.error,'waiting_for_players');
 const pending=(await f.send({action:'invite_status',inviteToken:invite.inviteToken},'c')).room;
 assert.equal(pending.status,'pending');assert.equal(pending.remaining,2);
 const joined=await Promise.all(['c','d'].map(u=>f.send({action:'invite_join',inviteToken:invite.inviteToken},u)));
 assert.ok(joined.every(x=>x.status===200));
 const r=f.data.get('592592').room;
 assert.equal(r.status,'playing');assert.equal(r.players.length,4);assert.equal(r.autoStarted592,true);
 assert.equal(new Set(r.players.map(p=>p.seat)).size,4);
 assert.equal((await f.send({action:'invite_status',inviteToken:invite.inviteToken},'e')).room.status,'joined');
 assert.equal((await f.send({action:'invite_join',inviteToken:invite.inviteToken},'e')).status,409);
 f.advance(120001);
 assert.equal((await f.send({action:'invite_join',inviteToken:invite.inviteToken},'d')).room.players.length,4);
});
test('four code joins start automatically; fast mutation avoids opponent wallet and presence reads',async()=>{
 const f=fixture();await f.send({action:'create',capacity:4,mode:'classic'});
 for(const uid of ['b','c','d'])assert.equal((await f.send({action:'join',id:'592592'},uid)).status,200);
 const before=f.data.get('592592').room;assert.equal(before.status,'playing');
 f.resetReads();
 const rolled=await f.send({action:'roll',id:'592592',revision:before.revision,requestId:'roll592_fast',fast592:true});
 assert.equal(rolled.status,200);assert.equal(rolled.room.diceBags592,undefined);
 assert.equal(f.reads.filter(x=>x.startsWith('wallet575_')).length,1);
 assert.equal(f.reads.filter(x=>x.startsWith('view570_')).length,0);
 assert.ok(f.data.get('592592').room.diceBags592);
 const watched=await f.send({action:'watch',id:'592592'},'watcher');
 assert.equal(watched.room.diceBags592,undefined);
});
test('legacy single-consumed four-seat invite can still fill remaining places',async()=>{
 const f=fixture();await f.send({action:'create',capacity:4,mode:'classic'});
 const i=(await f.send({action:'invite_create',id:'592592',requestId:'legacy_invite592_01'})).room;
 await f.send({action:'invite_join',inviteToken:i.inviteToken},'b');
 const entry=f.data.get('invite580_'+i.inviteToken);entry.room.status='joined';entry.room.acceptedBy='b';delete entry.room.joinedBy;
 assert.equal((await f.send({action:'invite_status',inviteToken:i.inviteToken},'c')).room.status,'pending');
 assert.equal((await f.send({action:'invite_join',inviteToken:i.inviteToken},'c')).status,200);
});
