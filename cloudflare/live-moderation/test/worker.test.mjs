import {test} from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/index.mjs';
import {adminToken,roomService} from '../src/room-service.mjs';
const env={LIVEKIT_API_KEY:'test-key',LIVEKIT_API_SECRET:'test-secret-only',LIVEKIT_SERVER_URL:'wss://test.livekit.cloud'};
test('admin JWT is HMAC signed, room-scoped and expires after two minutes',async()=>{
 const token=await adminToken(env,'room',1800000000000),[head,body,sig]=token.split('.');
 const claims=JSON.parse(Buffer.from(body,'base64url'));assert.equal(claims.iss,'test-key');
 assert.deepEqual(claims.video,{roomAdmin:true,room:'room'});assert.equal(claims.exp-claims.iat,120);
 const key=await crypto.subtle.importKey('raw',new TextEncoder().encode(env.LIVEKIT_API_SECRET),{name:'HMAC',hash:'SHA-256'},false,['verify']);
 assert.equal(await crypto.subtle.verify('HMAC',key,Buffer.from(sig,'base64url'),new TextEncoder().encode(head+'.'+body)),true);
 assert.equal(JSON.stringify(claims).includes(env.LIVEKIT_API_SECRET),false);
});
test('room API preserves participant publishing permissions and normalizes audio enums',async()=>{
 const calls=[];
 const service=roomService(env,async(url,options)=>{
  calls.push([url.toString(),JSON.parse(options.body),options.headers]);
  return Response.json({participants:[{identity:'guest',tracks:[{sid:'mic',type:'AUDIO'}]}]});
 });
 assert.equal((await service.listParticipants('room'))[0].tracks[0].type,0);
 await service.updateParticipant('room','guest',{permission:{canSubscribe:true,canPublishSources:[1]}});
 await service.mutePublishedTrack('room','guest','mic',true);await service.removeParticipant('room','guest');
 assert.equal(calls[1][1].permission.canSubscribe,true);assert.deepEqual(calls[2][1],{room:'room',identity:'guest',trackSid:'mic',muted:true});
 assert.ok(calls.every(([url])=>url.startsWith('https://test.livekit.cloud/twirp/livekit.RoomService/')));
});
test('room API rejects plaintext endpoints and reports upstream failures',async()=>{
 assert.throws(()=>roomService({...env,LIVEKIT_SERVER_URL:'http://test.livekit.cloud'}));
 await assert.rejects(roomService(env,async()=>new Response('',{status:403})).removeParticipant('room','guest'));
});
test('worker denies anonymous callers, invalid methods and oversize streamed JSON',async()=>{
 assert.equal((await worker.fetch(new Request('https://example.test/moderate',{method:'POST'}),{})).status,401);
 assert.equal((await worker.fetch(new Request('https://example.test/moderate'),{})).status,405);
 assert.equal((await worker.fetch(new Request('https://example.test/moderate',{method:'POST',headers:{authorization:'Bearer test','content-type':'application/json'},body:'x'.repeat(2049)}),{})).status,400);
});
test('unconfigured worker never claims working moderation',async()=>{
 const response=await worker.fetch(new Request('https://example.test/health'),{});
 assert.equal(response.status,503);assert.equal((await response.json()).ok,false);
});
