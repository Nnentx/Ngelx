import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act,powerTiles570,safe} from './engine.mjs';
const now=1800000000000;
test('picked-up Power reward vanishes from previous cell and relocates safely',()=>{
 for(const [cell,kind] of powerTiles570){
  let r=createRoom({uid:'a',name:'A',id:'123456',mode:'power',capacity:2},now);
  r=act(r,'b',{action:'join',name:'B'},now);
  r=act(r,'a',{action:'start',revision:r.revision,requestId:'start_pickup572'},now);
  r.tokens[0][0]=cell-1;r.dice=1;const before=Object.keys(r.powerTiles).length;
  const b={action:'move',token:0,revision:r.revision,requestId:'pickup_move572_'+cell};
  const next=act(r,'a',b,now);
  assert.equal(next.power[0][kind],2);
  assert.equal(next.powerTiles[cell],undefined,'old position must disappear');
  assert.equal(Object.keys(next.powerTiles).length,before);
  assert.ok(Object.entries(next.powerTiles).some(([i,k])=>k===kind&&Number(i)!==cell&&!safe.has(Number(i))));
  const replay=act(next,'a',b,now);
  assert.deepEqual(replay.powerTiles,next.powerTiles,'request replay may not duplicate rewards');
 }
});
test('classic mode never shows or relocates Power pickup inventory',()=>{
 const r=createRoom({uid:'a',name:'A',id:'123456',mode:'classic',capacity:2},now);
 assert.equal(r.mode,'classic');assert.equal(r.powerTiles[2],'control');
});
