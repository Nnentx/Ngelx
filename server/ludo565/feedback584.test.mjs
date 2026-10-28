import {test} from 'node:test';
import assert from 'node:assert/strict';
import {act,createRoom,legal,secureRoll} from './engine.mjs';

const now=1800000000000;
function waiting(count,capacity=4){
 let r=createRoom({uid:'a',name:'A',id:'584584',capacity},now);
 for(const uid of ['b','c','d'].slice(0,count-1))r=act(r,uid,{action:'join'},now);
 return r;
}
const start=r=>act(r,'a',{action:'start',revision:r.revision,requestId:'start584'},now);
test('two opponents face each other in two-seat and early-started four-seat rooms',()=>{
 for(const capacity of [2,4]){
  const r=start(waiting(2,capacity));
  assert.deepEqual(r.players.map(p=>p.seat),[0,2]);
  assert.equal(r.capacity,capacity);
  assert.equal(r.turn,0);
 }
});
test('seat relocation preserves waiting Auto preference and player identity',()=>{
 let r=waiting(2);const old=r.players[1].seat;
 r=act(r,'b',{action:'auto',enabled:true,revision:r.revision,requestId:'auto5840'},now);
 r=start(r);
 assert.equal(r.players[1].uid,'b');assert.equal(r.players[1].seat,2);
 assert.equal(r.autoSeats[2],true);assert.equal(r.autoSeats[old],undefined);
 assert.deepEqual(r.tokens[2],[-1,-1,-1,-1]);
 assert.throws(()=>act(r,'a',{action:'start',revision:r.revision,requestId:'start_again584'},now),/waiting_for_players/);
});
test('three/four-player and team starts preserve each assigned color',()=>{
 for(const count of [3,4]){
  const r=waiting(count),before=r.players.map(p=>p.seat);
  assert.deepEqual(start(r).players.map(p=>p.seat),before);
 }
 const r=waiting(4);r.team=true;
 assert.deepEqual(start(r).players.map(p=>p.seat),[0,1,2,3]);
});
test('every player in 2/3/4-player games can roll all six faces and leave home on six',()=>{
 for(const count of [2,3,4])for(const mode of ['classic','power']){
  const original=start({...waiting(count),mode});
  for(const player of original.players)for(let face=1;face<=6;face++){
   const seat=player.seat;
   let r=act({...original,turn:seat},player.uid,{action:'roll',revision:original.revision,requestId:'roll5840'},now+1,()=>face);
   assert.equal(r.lastRoll.value,face);assert.equal(r.lastRoll.seat,seat);
   if(face===6){
    assert.equal(r.dice,6);assert.deepEqual(legal(r,seat),[0,1,2,3]);
    r=act(r,player.uid,{action:'move',token:0,revision:r.revision,requestId:'move5840'},now+2);
    assert.equal(r.tokens[seat][0],0);assert.equal(r.turn,seat);
   }else{assert.equal(r.dice,null);assert.equal(r.openingRolls,1);}
  }
 }
});
test('production secureRoll maps each residue equally and rejects biased uint32 tail',t=>{
 // Test the real sampler with exact crypto input, not a flaky frequency bound.
 let samples=[],calls=0;
 t.mock.method(crypto,'getRandomValues',array=>{calls++;assert.ok(samples.length);array[0]=samples.shift();return array;});
 for(const base of [0,6,4294967286]){
  const counts=[0,0,0,0,0,0];
  for(let i=0;i<6;i++){samples=[base+i];counts[secureRoll()-1]++;}
  assert.deepEqual(counts,[1,1,1,1,1,1]);
 }
 samples=[4294967292,4294967293,4294967294,4294967295,5];
 const before=calls;assert.equal(secureRoll(),6);assert.equal(calls-before,5);
});
