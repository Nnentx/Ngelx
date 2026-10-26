import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createRoom,act} from './engine.mjs';

const t=1800000000000;
function started(){
 let r=createRoom({uid:'human',name:'Sen',id:'575575'},t);
 r=act(r,'other',{action:'join',name:'Rakip'},t);
 return act(r,'human',{action:'start',revision:r.revision,requestId:'build575start'},t);
}
const request=(r,action,extra={},uid='human',when=t+1000)=>
 act(r,uid,{action,...extra,revision:r.revision,requestId:'u575_'+r.revision},when,()=>6);

test('timeout activates persistent Auto for the timed-out seat',()=>{
 let r=started();
 r=act(r,'other',{action:'sync'},t+10000,()=>6);
 assert.equal(r.autoSeats[0],true);
 assert.equal(r.dice,6);
 r=act(r,'other',{action:'sync'},t+10001,()=>6);
 assert.deepEqual(r.tokens[0],[0,-1,-1,-1]);
 assert.equal(r.autoSeats[0],true);
});

test('tapping Auto cancels automatic turns and renews the remaining time',()=>{
 let r=started();
 r=act(r,'other',{action:'sync'},t+10000,()=>6);
 r=request(r,'auto',{enabled:false},'human',t+10001);
 assert.equal(r.autoSeats[0],undefined);
 assert.equal(r.deadline,t+20001);
 const before=r.revision;
 r=act(r,'other',{action:'sync'},t+10002,()=>6);
 assert.equal(r.revision,before);
});

test('manual pawn move disables persistent auto mode',()=>{
 let r=started();r.dice=6;r.autoSeats={0:true};
 r=request(r,'move',{token:0},'human',t+1000);
 assert.equal(r.autoSeats[0],undefined);
});

test('smart Auto captures enemy instead of moving the first legal pawn',()=>{
 let r=started();r.tokens[0]=[1,10,-1,-1];r.tokens[2]=[37,-1,-1,-1];r.dice=1;
 r=act(r,'other',{action:'sync'},t+10000,()=>3);
 assert.equal(r.tokens[0][1],11);
 assert.equal(r.tokens[2][0],-1);
});

test('an off-turn player cannot toggle another player Auto',()=>{
 let r=started();
 r=request(r,'auto',{enabled:true},'other',t+1000);
 assert.equal(r.autoSeats[0],undefined);
 assert.equal(r.autoSeats[2],true);
});

test('timeout with no legal pawn does not fail or freeze the match',()=>{
 let r=started();r.dice=1;r.tokens[0]=[-1,-1,-1,-1];
 r=act(r,'other',{action:'sync'},t+10000,()=>6);
 assert.equal(r.turn,2);
 assert.equal(r.autoSeats[0],true);
 assert.equal(r.status,'playing');
});
