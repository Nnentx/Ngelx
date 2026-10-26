import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createLudo565} from '../../cloudflare/live-moderation/src/ludo565.mjs';

test('authenticated wallet data matches daily + chest rewards and no public credits',async()=>{
 const documents=new Map();
 const store={
  get:async id=>documents.get(id)??null,
  put:async(id,room,stamp)=>{
   const previous=documents.get(id);
   if((previous?.stamp??undefined)!==stamp)throw Object.assign(Error('conflict'),{status:409});
   documents.set(id,{room:structuredClone(room),stamp:String(Number(previous?.stamp??0)+1)});
  }
 };
 let clock=1800000000000;
 const api=createLudo565({store,verify:async req=>({sub:req.headers.get('x-user')}),
  profile:async uid=>({displayName:uid}),now:()=>clock,uuid:()=>'577577'});
 const send=async(uid,action)=>{
  const req=new Request('https://example.test/ludo',{method:'POST',
   headers:{authorization:'Bearer auth','content-type':'application/json','x-user':uid},
   body:JSON.stringify({action})});
  const res=await api(req);assert.equal(res.status,200);
  return (await res.json()).room;
 };
 let a=await send('ali','wallet');
 assert.equal(a.chips,0);assert.equal(a.level,1);
 const gift=await send('ali','daily_reward');
 assert.equal(gift.claimed,true);assert.equal(gift.chipReward,50);
 const chest=await send('ali','chest_reward');
 assert.equal(chest.claimed,true);assert.equal(chest.chipReward,25);
 a=await send('ali','wallet');
 assert.equal(a.chips,75);
 const b=await send('other','wallet');
 assert.equal(b.chips,0);
 const again=await send('ali','chest_reward');
 assert.equal(again.claimed,false);
 assert.equal((await send('ali','wallet')).chips,75);
});
