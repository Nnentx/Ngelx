import {test} from 'node:test';import assert from 'node:assert/strict';import {createHmac} from 'node:crypto';
import {createTokenEndpoint} from './token-endpoint.mjs';
const config={apiKey:'test-key',apiSecret:'test-only-secret',serverUrl:'wss://example.invalid',now:()=>1800000000000,
 verifyFirebaseToken:async (token,revoked)=>{assert.equal(revoked,true);if(token!=='valid')throw Error('bad');return {uid:'alice',firebase:{sign_in_provider:'password'}};},
 authorizeRoom:async ({uid,roomName})=>({allowed:uid==='alice'&&roomName==='allowed',role:'listener',displayName:'Alice',canPublish:false,canPublishData:false}),rateLimit:async()=>true};
const req={method:'POST',authorization:'Bearer valid',body:{room_name:'allowed',participant_identity:'alice',participant_attributes:{role:'host'}}};
test('signed JWT binds verified identity, server role and five-minute TTL',async()=>{const r=await createTokenEndpoint(config)(req);assert.equal(r.status,200);assert.equal(r.headers['Cache-Control'],'no-store');const [h,p,s]=r.body.participant_token.split('.');assert.equal(s,createHmac('sha256',config.apiSecret).update(h+'.'+p).digest('base64url'));const data=JSON.parse(Buffer.from(p,'base64url'));assert.equal(data.sub,'alice');assert.equal(data.attributes.role,'listener');assert.equal(data.video.canPublish,false);assert.equal(data.exp-data.iat,300);});
test('missing authorization rejected',async()=>assert.equal((await createTokenEndpoint(config)({...req,authorization:''})).status,401));
test('invalid and revoked authentication rejected',async()=>assert.equal((await createTokenEndpoint(config)({...req,authorization:'Bearer bad'})).status,401));
test('anonymous auth rejected',async()=>assert.equal((await createTokenEndpoint({...config,verifyFirebaseToken:async()=>({uid:'alice',firebase:{sign_in_provider:'anonymous'}})})(req)).status,401));
test('client identity spoof rejected',async()=>assert.equal((await createTokenEndpoint(config)({...req,body:{...req.body,participant_identity:'bob'}})).status,403));
test('unauthorized or ended room denied',async()=>assert.equal((await createTokenEndpoint(config)({...req,body:{room_name:'ended'}})).status,403));
test('client agent and room config rejected',async()=>assert.equal((await createTokenEndpoint(config)({...req,body:{...req.body,room_config:{agents:[]}}})).status,400));
test('rate limit enforced before issuing token',async()=>assert.equal((await createTokenEndpoint({...config,rateLimit:async()=>false})(req)).status,429));
test('lookup failure does not disclose details',async()=>{const r=await createTokenEndpoint({...config,authorizeRoom:async()=>{throw Error('private record');}})(req);assert.equal(r.status,503);assert.equal(JSON.stringify(r).includes('private'),false);});
test('HTTP method rejected',async()=>assert.equal((await createTokenEndpoint(config)({...req,method:'GET'})).status,405));
test('cannot initialize without authorization or rate limiting',()=>assert.throws(()=>createTokenEndpoint({...config,authorizeRoom:undefined})));

test('rate-limit datastore failure returns a generic unavailable response',async()=>{const r=await createTokenEndpoint({...config,rateLimit:async()=>{throw Error('private database details');}})(req);assert.equal(r.status,503);assert.equal(JSON.stringify(r).includes('private'),false);});
