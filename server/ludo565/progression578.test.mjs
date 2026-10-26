import {test} from 'node:test';
import assert from 'node:assert/strict';
import {level578} from './rewards575.mjs';
import {createRoom,act,powerTiles570} from './engine.mjs';
test('progressive level thresholds require 200, then 300, then 400 additional XP',()=>{
 for(const [xp,level] of [[0,1],[199,1],[200,2],[499,2],[500,3],[899,3],[900,4],[1400,5]])assert.equal(level578(xp),level);
});
test('Power pickups remain six total with four collectible dice and two shields',()=>{
 assert.equal(powerTiles570.size,6);
 assert.equal([...powerTiles570.values()].filter(k=>k!=='shield').length,4);
 assert.equal(new Set(powerTiles570.keys()).size,6);
});
test('both persistent Auto seats advance every sync without waiting for another timeout',()=>{
 const t=1800000000000;
 let r=createRoom({uid:'a',name:'A',id:'578578'},t);
 r=act(r,'b',{action:'join'},t);r=act(r,'a',{action:'start',revision:r.revision,requestId:'start578'},t);
 for(const uid of ['a','b'])r=act(r,uid,{action:'auto',enabled:true,revision:r.revision,requestId:'auto578_'+uid},t);
 for(let i=0;i<20;i++){
  const previous=r.revision;r=act(r,'a',{action:'sync'},t+500+i*200,()=>6);
  assert.ok(r.revision>previous);assert.equal(r.autoSeats[0],true);assert.equal(r.autoSeats[2],true);
 }
});
