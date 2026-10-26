import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act} from './engine.mjs';
const now=1800000000000;
function room(){let r=createRoom({uid:'a',name:'A',id:'123456'},now);r=act(r,'b',{action:'join'},now);return act(r,'a',{action:'start',revision:r.revision,requestId:'start569'},now);}
test('roll receives a fresh ten second move window',()=>{let r=room();r=act(r,'a',{action:'roll',revision:r.revision,requestId:'roll5690'},now+9000,()=>6);assert.equal(r.deadline,now+19000);assert.equal(r.dice,6);});
test('timeout enters persistent Auto, which executes its next action on sync',()=>{let r=room();r=act(r,'b',{action:'sync'},now+10000,()=>6);assert.equal(r.dice,6);assert.equal(r.turn,0);assert.equal(r.deadline,now+20000);assert.equal(r.autoSeats[0],true);r=act(r,'b',{action:'sync'},now+10001);assert.deepEqual(r.tokens[0],[0,-1,-1,-1]);assert.equal(r.turn,0);});
test('automatic move captures normally and preserves bonus turn',()=>{let r=room();r.tokens[0]=[10,20,-1,-1];r.tokens[2][0]=37;r.dice=1;r=act(r,'b',{action:'sync'},now+10000);assert.equal(r.tokens[0][0],11);assert.equal(r.tokens[2][0],-1);assert.equal(r.turn,0);assert.equal(r.dice,null);});
test('simultaneous timeout requests cannot move twice after revision check',()=>{let r=room();r.dice=6;const old=r.revision;r=act(r,'a',{action:'sync'},now+10000);assert.throws(()=>act(r,'a',{action:'move',token:1,revision:old,requestId:'stale569'},now+10001),/state_changed/);});
