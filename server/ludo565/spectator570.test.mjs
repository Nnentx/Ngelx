import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createLudo565} from '../../cloudflare/live-moderation/src/ludo565.mjs';
import {LudoError,legal} from './engine.mjs';
function fixture({roll=()=>6}={}){
 const records=new Map();let stamp=0,id=583920,clock=1800000000000;
 const store={get:async k=>structuredClone(records.get(k)??null),put:async(k,room,previous)=>{const current=records.get(k);if(current?current.stamp!==previous:previous!==undefined)throw new LudoError('state_changed',409);records.set(k,{room:structuredClone(room),stamp:String(++stamp)});}};
 const handler=createLudo565({store,verify:async r=>({sub:r.headers.get('x-user')}),profile:async uid=>({displayName:uid}),uuid:()=>String(++id),now:()=>clock,roll});
 const call=async(body,user='a')=>{const r=await handler(new Request('https://example.test/ludo',{method:'POST',headers:{authorization:'Bearer valid','content-type':'application/json','x-user':user},body:JSON.stringify(body)}));return {status:r.status,...await r.json()};};
 return {call,records,tick:n=>clock+=n};
}

test('spectators see game without a player seat, count expires and leaves cleanly',async()=>{
 const {call,tick}=fixture();const {room}=await call({action:'create',capacity:2,mode:'power'});
 const view=await call({action:'watch',id:room.id},'viewer');assert.equal(view.room.spectatorCount,1);assert.equal(view.room.players.length,1);assert.equal(view.room.revision,room.revision);
 assert.equal((await call({action:'chat',id:room.id,revision:room.revision,requestId:'viewer_chat_570',text:'hi'},'viewer')).status,403);
 assert.equal((await call({action:'watch',id:room.id},'viewer')).room.spectatorCount,1);
 assert.equal((await call({action:'watch_leave',id:room.id},'viewer')).room.spectatorCount,0);
 await call({action:'watch',id:room.id},'viewer');tick(25001);
 assert.equal((await call({action:'sync',id:room.id})).room.spectatorCount,0);
});
