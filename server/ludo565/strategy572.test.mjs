import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act} from './engine.mjs';
import {chooseBotToken572,scoreBotMove572} from './strategy572.mjs';
const now=1800000000000;
function started(){
 let r=createRoom({uid:'a',name:'A',capacity:2,id:'123456'},now);
 r=act(r,'b',{action:'join',name:'B'},now);
 r=act(r,'a',{action:'start',revision:r.revision,requestId:'start572'},now);
 return r;
}
test('hard bot prefers capturing an exposed enemy instead of merely advancing',()=>{
 const r=started();r.turn=0;r.dice=3;r.tokens[0]=[2,12,-1,-1];
 r.tokens[2]=[-1,-1,-1,-1];r.tokens[2][0]=44; // global enemy cell (26+44)%52=18
 r.tokens[0][1]=15; // move to 18 captures enemy
 assert.equal(chooseBotToken572(r,0,'hard'),1);
});
test('hard bot values exact finish over mere progress',()=>{
 const r=started();r.turn=0;r.dice=3;r.tokens[0]=[53,48,-1,-1];
 assert.equal(chooseBotToken572(r,0,'hard'),0);
});
test('difficulty uses the same legal moves and never fabricates a die',()=>{
 const r=started();r.turn=0;r.dice=6;r.tokens[0]=[-1,2,55,56];
 for(const level of ['easy','medium','hard']) for(let i=1;i<=6;i++)
  assert.ok([0,1].includes(chooseBotToken572(r,0,level,()=>i)));
 assert.equal(r.dice,6);
});
test('hard bot avoids threatened landing when another route is safe',()=>{
 const r=started();r.turn=0;r.dice=1;r.tokens[0]=[7,11,-1,-1];
 r.tokens[2][0]=39; // enemy on global cell 13; threatens cell 14; next 8 is safe
 assert.equal(chooseBotToken572(r,0,'hard'),0);
});
