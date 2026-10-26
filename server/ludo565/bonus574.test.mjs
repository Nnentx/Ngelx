import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act} from './engine.mjs';
const NOW=1800000000000;
function start(mode='power'){
 let room=createRoom({uid:'a',name:'Player',id:'654321',mode,capacity:2},NOW);
 room=act(room,'b',{action:'join',name:'Opponent'},NOW);
 room=act(room,'a',{action:'start',revision:room.revision,requestId:'begin574'},NOW);
 return room;
}
test('+1 bonus moves to a new unoccupied safe-eligible tile after pickup',()=>{
 let r=start();
 const origin=4;
 assert.ok(r.bonusTiles.includes(origin));
 const count=r.bonusTiles.length;
 r.turn=0;r.dice=1;r.tokens[0][0]=3;
 const revision=r.revision;
 const move={action:'move',token:0,revision,requestId:'bonus574'};
 const next=act(r,'a',move,NOW);
 assert.equal(next.bonusPickup.cell,origin);
 assert.equal(next.bonusTiles.includes(origin),false);
 assert.equal(next.bonusTiles.length,count);
 assert.equal(new Set(next.bonusTiles).size,count);
 assert.equal(next.dice,null,'Collecting +1 grants another dice roll');
 assert.equal(next.turn,0,'The current player keeps the turn after +1');
 assert.notDeepEqual(next.bonusTiles,r.bonusTiles);
 const duplicate=act(next,'a',move,NOW);
 assert.deepEqual(duplicate.bonusTiles,next.bonusTiles,'Same request cannot collect +1 twice');
});
test('each +1 spot can be collected and relocated',()=>{
 for(const origin of [4,17,30,43]){
  let r=start();r.turn=0;r.dice=1;r.tokens[0][0]=origin-1;
  let next=act(r,'a',{action:'move',token:0,revision:r.revision,requestId:'bonus574_'+origin},NOW);
  assert.equal(next.bonusTiles.includes(origin),false,origin+' must disappear');
  assert.equal(next.bonusTiles.length,4);
 }
});
test('classic games never collect Power +1 bonuses',()=>{
 let r=start('classic');r.turn=0;r.dice=1;r.tokens[0][0]=3;
 const next=act(r,'a',{action:'move',token:0,revision:r.revision,requestId:'classic574'},NOW);
 assert.equal(next.turn,2);
 assert.deepEqual(next.bonusTiles,[4,17,30,43]);
});
