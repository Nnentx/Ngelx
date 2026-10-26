import {test} from 'node:test';
import assert from 'node:assert/strict';
import {act,createRoom,LudoError} from './engine.mjs';
import {createLudo565} from '../../cloudflare/live-moderation/src/ludo565.mjs';

const start=(room,uid='a')=>act(room,uid,{action:'start',revision:room.revision,requestId:'start580_test'},1000,()=>6);
test('four-seat free-for-all starts with two or three, retaining capacity and occupied seats',()=>{
 for(const count of [2,3]){
  let r=createRoom({id:'580580',uid:'a',name:'A',capacity:4},0);
  for(let i=1;i<count;i++)r=act(r,String(i),{action:'join',name:'Other'},500);
  r=start(r);assert.equal(r.status,'playing');assert.equal(r.players.length,count);assert.equal(r.capacity,4);
 }
});
test('early start still requires host, two players, and complete teams/random matches',()=>{
 let r=createRoom({id:'580580',uid:'a',name:'A',capacity:4},0);
 assert.throws(()=>start(r),/waiting_for_players/);
 r=act(r,'b',{action:'join'},500);assert.throws(()=>start(r,'b'),/host_only/);
 assert.throws(()=>start({...r,team:true}),/waiting_for_players/);
 assert.throws(()=>start({...r,matchmaking:true}),/waiting_for_players/);
});
function fixture(){
 let time=1800000000000;const data=new Map();
 const check=(id,stamp)=>{if(data.get(id)?.stamp!==stamp)throw new LudoError('state_changed',409);};
 const put=(id,room)=>data.set(id,{room:structuredClone(room),stamp:String(Number(data.get(id)?.stamp??0)+1)});
 const store={get:async id=>data.has(id)?structuredClone(data.get(id)):null,
  put:async(id,room,stamp)=>{check(id,stamp);put(id,room);},
  putMany:async changes=>{for(const x of changes)check(x.id,x.stamp);for(const x of changes)put(x.id,x.room);}};
 const api=createLudo565({store,verify:async r=>({sub:r.headers.get('x-user')}),
  profile:async uid=>({displayName:uid==='a'?'Alihan':uid,photoUrl:'https://example.test/'+uid+'.jpg'}),
  now:()=>time,uuid:()=>'580580',roll:()=>6});
 const send=async(body,user='a')=>{
  const response=await api(new Request('https://example.test/ludo',{method:'POST',headers:{authorization:'Bearer valid','content-type':'application/json','x-user':user},body:JSON.stringify(body)}));
  return {status:response.status,...await response.json()};
 };
 return {data,send,advance:ms=>time+=ms};
}
async function invite(f){
 const created=await f.send({action:'create',capacity:4,mode:'classic'});assert.equal(created.status,201);
 return f.send({action:'invite_create',id:'580580',requestId:'invitation580_test0001'});
}
test('invitation has server two-minute deadline, sender artwork, idempotent create and bounded public status',async()=>{
 const f=fixture(),i=(await invite(f)).room;
 assert.equal(i.expiresAt-i.createdAt,120000);assert.equal(i.name,'Alihan');assert.match(i.photo,/a.jpg$/);
 assert.equal((await f.send({action:'invite_create',id:'580580',requestId:'invitation580_test0001'})).room.inviteToken,i.inviteToken);
 const status=await f.send({action:'invite_status',inviteToken:i.inviteToken},'b');
 assert.equal(status.room.status,'pending');assert.equal(status.room.players,undefined);assert.equal(status.room.chips,undefined);
 assert.equal((await f.send({action:'invite_create',id:'580580',requestId:'invitation580_test0002'},'b')).status,403);
});
test('expiry at precisely 00:00 rejects joining without modifying the game',async()=>{
 const f=fixture(),i=(await invite(f)).room,room=f.data.get('580580');
 f.advance(120000);
 assert.equal((await f.send({action:'invite_status',inviteToken:i.inviteToken},'b')).room.status,'expired');
 const join=await f.send({action:'invite_join',inviteToken:i.inviteToken},'b');
 assert.equal(join.status,410);assert.equal(join.error,'invite_expired');assert.deepEqual(f.data.get('580580'),room);
});
test('accepted invitation joins once, updates sender status, supports retry and blocks a second recipient',async()=>{
 const f=fixture(),i=(await invite(f)).room;
 f.advance(119999);
 const joined=await f.send({action:'invite_join',inviteToken:i.inviteToken},'b');
 assert.equal(joined.status,200);assert.equal(joined.room.players.length,2);
 assert.equal((await f.send({action:'invite_status',inviteToken:i.inviteToken})).room.status,'joined');
 f.advance(1000);
 const retry=await f.send({action:'invite_join',inviteToken:i.inviteToken},'b');
 assert.equal(retry.status,200);assert.equal(retry.room.players.length,2);
 assert.equal((await f.send({action:'invite_join',inviteToken:i.inviteToken},'c')).status,410);
});
test('simultaneous recipients cannot both consume one invitation',async()=>{
 const f=fixture(),i=(await invite(f)).room;
 const results=await Promise.all(['b','c'].map(u=>f.send({action:'invite_join',inviteToken:i.inviteToken},u)));
 assert.equal(results.filter(r=>r.status===200).length,1);
 assert.equal(f.data.get('580580').room.players.length,2);
});
test('both players see the other verified level; malformed invite capabilities are rejected',async()=>{
 const f=fixture(),i=(await invite(f)).room;
 const joined=await f.send({action:'invite_join',inviteToken:i.inviteToken},'b');
 assert.ok(joined.room.players.every(p=>Number.isInteger(p.level)&&p.level>=1));
 assert.equal((await f.send({action:'invite_status',inviteToken:'../../other'})).status,400);
});
