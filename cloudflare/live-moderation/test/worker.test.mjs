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

test('health reveals Build575 deployment capabilities without exposing worker secrets',async()=>{
 const config={...env,GOOGLE_SERVICE_ACCOUNT:'private-gcp-key-json',
  FIREBASE_PROJECT_ID:'ngelx-44eed',LUDO_ADMOB_AD_UNIT:'ca-app-pub-1234567890123456/1234567890',
  LUDO_MODERATOR_UIDS:'  , trusted-reviewer , '};
 const response=await worker.fetch(new Request('https://example.test/health'),config);
 assert.equal(response.status,200);
 const data=await response.json();
 assert.equal(data.ok,true);
 assert.equal(data.ludo575.sourceVersion,575);
 assert.equal(data.ludo575.configured,true);
 assert.equal(data.ludo575.rewardedAdsConfigured,true);
 assert.equal(data.ludo575.moderationAllowlistConfigured,true);
 assert.ok(data.features.includes('ludo575_auto'));
 assert.ok(data.features.includes('ludo575_reports'));
 assert.equal(JSON.stringify(data).includes('private-gcp-key-json'),false);
 assert.equal(JSON.stringify(data).includes('trusted-reviewer'),false);
 assert.equal(JSON.stringify(data).includes('1234567890123456'),false);
});
test('health fails closed on absent Ludo Firebase project or missing optional credentials',async()=>{
 const config={...env,GOOGLE_SERVICE_ACCOUNT:'dummy',FIREBASE_PROJECT_ID:'not-ngelx',
  LUDO_ADMOB_AD_UNIT:'bad-id',LUDO_MODERATOR_UIDS:' ,  '};
 let r=await worker.fetch(new Request('https://example.test/health'),config);
 assert.equal(r.status,200);
 let result=(await r.json()).ludo575;
 assert.equal(result.configured,false);
 assert.equal(result.rewardedAdsConfigured,false);
 assert.equal(result.moderationAllowlistConfigured,false);
 r=await worker.fetch(new Request('https://example.test/health'),{...config,FIREBASE_PROJECT_ID:'ngelx-44eed'});
 result=(await r.json()).ludo575;
 assert.equal(result.configured,true);
 assert.equal(result.rewardedAdsConfigured,false);
 assert.equal(result.moderationAllowlistConfigured,false);
});

test('Build575 Ludo rejects wrong Firebase project and malformed rewarded-ad setup before DB use',async()=>{
 const request=new Request('https://example.test/ludo',{method:'POST',
  headers:{authorization:'Bearer test','content-type':'application/json'},
  body:JSON.stringify({action:'wallet'})});
 const valid={...env,GOOGLE_SERVICE_ACCOUNT:'private-test',FIREBASE_PROJECT_ID:'ngelx-44eed',
  LUDO_ADMOB_AD_UNIT:'ca-app-pub-1234567890123456/1234567890'};
 const wrong={...valid,FIREBASE_PROJECT_ID:'different-project'};
 const game=await worker.fetch(request.clone(),wrong);
 assert.equal(game.status,503);
 assert.deepEqual(await game.json(),{error:'service_not_configured'});
 const callback='https://example.test/ludo/admob/ssv?transaction_id=invalid';
 assert.equal((await worker.fetch(new Request(callback),wrong)).status,503);
 const malformed={...valid,LUDO_ADMOB_AD_UNIT:'bad-id'};
 const ads=await worker.fetch(new Request(callback),malformed);
 assert.equal(ads.status,503);
 assert.deepEqual(await ads.json(),{error:'ads_not_configured'});
 const health=await worker.fetch(new Request('https://example.test/health'),malformed);
 assert.equal((await health.json()).ludo575.rewardedAdsConfigured,false);
});
