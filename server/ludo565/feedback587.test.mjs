import {test} from 'node:test';
import assert from 'node:assert/strict';
import {act,createRoom,secureRoll,legal} from './engine.mjs';
const time=1800000000000;
function room(count=2,mode='classic'){
 let r=createRoom({uid:'a',name:'A',id:'587587',capacity:count===2?2:4,mode},time);
 for(const uid of ['b','c','d'].slice(0,count-1))r=act(r,uid,{action:'join'},time);
 return act(r,'a',{action:'start',revision:r.revision,requestId:'start587'},time);
}
test('each seat gets exactly one accepted roll and no-move passes immediately',()=>{
 for(const count of [2,3,4])for(const mode of ['classic','power']){
  const original=room(count,mode);
  for(const p of original.players)for(const face of [1,2,3,4,5]){
   let calls=0;
   const body={action:'roll',revision:original.revision,requestId:'single587'};
   const r=act({...original,turn:p.seat,openingRolls:1},p.uid,body,time+1,()=>{calls++;return face;});
   assert.equal(calls,1);assert.notEqual(r.turn,p.seat);assert.equal(r.dice,null);
   assert.equal(r.openingRolls,0);assert.equal(r.lastRoll.value,face);
   assert.deepEqual(act(r,p.uid,body,time+2,()=>{throw Error('duplicate reroll');}),r);
   assert.throws(()=>act(r,p.uid,{...body,revision:r.revision,requestId:'another587'},time+2),/not_your_turn/);
  }
 }
});
test('one roll per turn applies to server Auto and controlled dice too',()=>{
 let r=room();r=act(r,'b',{action:'sync'},time+15000,()=>2);
 assert.equal(r.turn,2);assert.equal(r.lastRoll.value,2);
 r=room(2,'power');r=act(r,'a',{action:'power',kind:'control',number:2,revision:r.revision,requestId:'power587'},time+1);
 assert.equal(r.turn,2);assert.equal(r.power[0].control,0);
});
test('six stays equally possible for every seat and bot; sampler never reads player state',t=>{
 let value=0;
 t.mock.method(crypto,'getRandomValues',array=>{array[0]=value++;return array;});
 for(const count of [2,3,4])for(const player of room(count).players)for(const bot of [false,true]){
  const counts=[0,0,0,0,0,0];
  for(let i=0;i<600;i++){
   const original=room(count);original.turn=player.seat;original.players.find(p=>p.uid===player.uid).bot=bot;
   const r=act(original,player.uid,{action:'roll',revision:original.revision,requestId:'fairroll587'},time+1,secureRoll);
   counts[r.lastRoll.value-1]++;
   if(r.lastRoll.value===6)assert.equal(legal(r,player.seat).length,4);
  }
  assert.deepEqual(counts,[100,100,100,100,100,100]);
 }
});
