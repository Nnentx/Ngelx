import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act,legal,turnWindow583,autoStep583} from './engine.mjs';
const time=1800000000000;
function started(count=3){
 let r=createRoom({uid:'a',name:'A',id:'583583',capacity:4},time);
 for(const uid of ['b','c','d'].slice(0,count-1))r=act(r,uid,{action:'join'},time);
 return act(r,'a',{action:'start',revision:r.revision,requestId:'start583'},time);
}
test('all three/four seats can roll every face, including six, without blocking a move',()=>{
 for(const count of [3,4])for(let seat=0;seat<count;seat++)for(let face=1;face<=6;face++){
  let r=started(count);r.turn=seat;
  const uid=r.players.find(p=>p.seat===seat).uid;
  r=act(r,uid,{action:'roll',revision:r.revision,requestId:'roll5830'},time+1,()=>face);
  assert.equal(r.lastRoll.value,face);assert.equal(r.lastRoll.seat,seat);
  assert.equal(r.deadline,time+1+turnWindow583);
  if(face===6){
   assert.deepEqual(legal(r,seat),[0,1,2,3]);
   r=act(r,uid,{action:'move',token:0,revision:r.revision,requestId:'move5830'},time+2);
   assert.equal(r.tokens[seat][0],0);assert.equal(r.turn,seat);
  }else assert.equal(r.dice,null);
 }
});
test('three players flooding sync cannot accelerate Auto; cancel restores fifteen seconds',()=>{
 let r=started();
 r=act(r,'a',{action:'auto',enabled:true,revision:r.revision,requestId:'auto5830'},time);
 const revision=r.revision;
 for(let ms=0;ms<autoStep583;ms+=50)for(const uid of ['a','b','c']){
  r=act(r,uid,{action:'sync'},time+ms,()=>6);
  assert.equal(r.revision,revision);assert.equal(r.dice,null);
 }
 r=act(r,'b',{action:'sync'},time+autoStep583,()=>6);
 assert.equal(r.dice,6);const rolled=r.revision;
 for(const uid of ['a','b','c'])r=act(r,uid,{action:'sync'},time+autoStep583+1,()=>6);
 assert.equal(r.revision,rolled);assert.equal(r.tokens[0][0],-1);
 r=act(r,'a',{action:'auto',enabled:false,revision:r.revision,requestId:'stop5830'},time+autoStep583+2);
 assert.equal(r.deadline,time+autoStep583+2+15000);
 const cancelled=r.revision;
 r=act(r,'c',{action:'sync'},time+autoStep583*3,()=>6);
 assert.equal(r.revision,cancelled);assert.equal(r.tokens[0][0],-1);
});
test('timeout starts at fifteen seconds and cannot chain automatic moves immediately',()=>{
 let r=started();const revision=r.revision;
 r=act(r,'b',{action:'sync'},time+14999,()=>6);assert.equal(r.revision,revision);
 r=act(r,'b',{action:'sync'},time+15000,()=>6);assert.equal(r.dice,6);
 r=act(r,'c',{action:'sync'},time+15001,()=>6);assert.equal(r.tokens[0][0],-1);
 r=act(r,'c',{action:'sync'},time+15000+autoStep583,()=>6);assert.equal(r.tokens[0][0],0);
});
test('departure accepts an old revision without relaxing move validation or membership',()=>{
 let r=started();const original=r.revision;
 r=act(r,'b',{action:'auto',enabled:true,revision:r.revision,requestId:'auto_other583'},time+1);
 assert.throws(()=>act(r,'a',{action:'roll',revision:original,requestId:'stale_roll583'},time+2),/state_changed/);
 r=act(r,'a',{action:'leave',revision:original,requestId:'leave58300'},time+2);
 assert.equal(r.players.find(p=>p.uid==='a').left,true);
 assert.equal(r.status,'playing');assert.notEqual(r.turn,0);
 assert.throws(()=>act(r,'outsider',{action:'leave',revision:r.revision,requestId:'outsider583'},time+3),/not_a_player/);
});
