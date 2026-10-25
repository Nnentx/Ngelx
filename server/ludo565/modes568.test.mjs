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
test('new room codes contain exactly six digits and create retries preserve the game',async()=>{const {call}=fixture();const body={action:'create',capacity:2,mode:'classic',requestId:'same_request_568_123456'};const a=await call(body);assert.match(a.room.id,/^\d{6}$/);assert.equal((await call(body)).room.id,a.room.id);});
test('bots occupy opposite seats and take legal server-controlled turns',async()=>{const {call}=fixture();let {room}=await call({action:'bot',capacity:2,mode:'power',difficulty:'hard'});assert.equal(room.status,'playing');assert.equal(room.players[1].seat,2);assert.equal(room.players[1].bot,true);
 for(let i=0;i<3;i++){room=(await call({action:'roll',id:room.id,revision:room.revision,requestId:'human_roll_'+i})).room;if(i<2)room=(await call({action:'move',token:0,id:room.id,revision:room.revision,requestId:'human_move_'+i})).room;}
 assert.equal(room.turn,2);assert.equal(room.dice,6);
 room=(await call({action:'sync',id:room.id})).room;assert.equal(room.tokens[2][0],0);
 assert.equal((await call({action:'sync',id:room.id},'outsider')).status,403);
});
test('random opponents match by mode and capacity and start without host action',async()=>{const {call}=fixture();const settings={action:'match',capacity:2,mode:'power'};const a=await call(settings),b=await call(settings,'b');assert.equal(a.room.id,b.room.id);assert.equal(b.room.status,'playing');assert.equal(b.room.matchmaking,true);assert.equal(b.room.players.length,2);const c=await call({...settings,mode:'classic'},'c');assert.notEqual(c.room.id,a.room.id);});
test('concurrent random joins cannot overfill or lose a player',async()=>{const {call}=fixture();const settings={action:'match',capacity:4,mode:'classic'};const results=await Promise.all(['a','b','c','d'].map(user=>call(settings,user)));assert.ok(results.every(x=>x.room),JSON.stringify(results));const rooms=new Set(results.map(x=>x.room.id));assert.equal(rooms.size,1);const latest=await call({action:'sync',id:results[0].room.id});assert.equal(latest.room.players.length,4);assert.equal(latest.room.status,'playing');});
test('cancelled and expired searches are not matched with a new player',async()=>{const {call,tick}=fixture();const settings={action:'match',capacity:2,mode:'classic'};const a=await call(settings);await call({action:'leave',id:a.room.id,revision:a.room.revision,requestId:'cancel_search568'});const b=await call(settings,'b');assert.notEqual(a.room.id,b.room.id);tick(90001);const c=await call(settings,'c');assert.notEqual(c.room.id,b.room.id);});

test('matching retries resume the same started room even after queue rotation',async()=>{const {call}=fixture();const a={action:'match',capacity:2,mode:'classic',requestId:'matching_request568_a'};const first=await call(a);await call({...a,requestId:'matching_request568_b'},'b');await call({...a,requestId:'matching_request568_c'},'c');const retry=await call(a);assert.equal(retry.room.id,first.room.id);assert.equal(retry.room.status,'playing');});

for(const mode of ['classic','power'])for(const difficulty of ['easy','medium','hard'])test(`complete ${mode} game against ${difficulty} bot reaches a valid winner`,async()=>{
 let seed=42;const roll=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>16)%6+1;};
 const {call}=fixture({roll});let {room}=await call({action:'bot',capacity:2,mode,difficulty});
 for(let i=0;i<4000&&room.status==='playing';i++){
  let body={action:'sync'};
  if(room.turn===0){if(room.dice===null)body={action:'roll'};else{const options=legal(room,0).sort((a,b)=>room.tokens[0][b]-room.tokens[0][a]);body={action:'move',token:options[0]};}}
  const response=await call({...body,id:room.id,revision:room.revision,requestId:'simulation568_'+i});assert.ok(response.room,JSON.stringify(response));room=response.room;
 }
 assert.equal(room.status,'finished',JSON.stringify({tokens:room.tokens,turn:room.turn,dice:room.dice}));assert.ok([0,2].includes(room.winner));assert.ok(room.tokens[room.winner].every(x=>x===56));
});
