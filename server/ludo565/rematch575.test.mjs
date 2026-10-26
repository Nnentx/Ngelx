import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createLudo565} from '../../cloudflare/live-moderation/src/ludo565.mjs';

test('same former opponents join one rematch room and start automatically',async()=>{
 const records=new Map();
 let counter=100100;
 const db={
  get:async key=>records.get(key)??null,
  put:async(key,room,stamp)=>{
   const old=records.get(key);
   if((old?.stamp??undefined)!==stamp)throw Object.assign(Error('conflict'),{status:409});
   records.set(key,{room:structuredClone(room),stamp:String(Number(old?.stamp??0)+1)});
  }
 };
 const time=1800000000000;
 const handle=createLudo565({store:db,verify:async r=>({sub:r.headers.get('x-user')}),profile:async uid=>({displayName:uid}),
  now:()=>time,roll:()=>6,uuid:()=>String(++counter)});
 const req=(uid,payload)=>new Request('https://example.test/ludo',{method:'POST',headers:{
  authorization:'Bearer authorized','content-type':'application/json','x-user':uid},body:JSON.stringify(payload)});
 let response=await handle(req('alice',{action:'create',capacity:2,mode:'power'}));
 assert.equal(response.status,201);
 let original=(await response.json()).room;
 response=await handle(req('bob',{action:'join',id:original.id}));
 original=(await response.json()).room;
 response=await handle(req('alice',{action:'start',id:original.id,revision:original.revision,requestId:'start_rematch575'}));
 original=(await response.json()).room;
 const rec=records.get(original.id);
 rec.room.status='finished';rec.room.winner=0;
 const first=await handle(req('alice',{action:'rematch',id:original.id}));
 assert.equal(first.status,200);
 const a=(await first.json()).room;
 assert.equal(a.status,'waiting');
 assert.equal(a.mode,'power');
 const second=await handle(req('bob',{action:'rematch',id:original.id}));
 assert.equal(second.status,200);
 const b=(await second.json()).room;
 assert.equal(b.id,a.id);
 assert.equal(b.status,'playing');
 assert.equal(b.players.length,2);
 const repeated=await handle(req('alice',{action:'rematch',id:original.id}));
 assert.equal((await repeated.json()).room.id,a.id);
 const outsider=await handle(req('mallory',{action:'rematch',id:original.id}));
 assert.equal(outsider.status,409);
});
