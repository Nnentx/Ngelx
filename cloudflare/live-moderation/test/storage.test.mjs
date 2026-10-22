import {test} from 'node:test';
import assert from 'node:assert/strict';
import {storage} from '../src/storage.mjs';
const now=1800000000000;
const env={FIREBASE_PROJECT_ID:'ngelx-44eed'};
const doc=fields=>({fields,updateTime:new Date(now).toISOString()});
const live=doc({ownerId:{stringValue:'host'},roomName:{stringValue:'ngelx_host_1800000000000'},active:{booleanValue:true},lastHeartbeatAt:{timestampValue:new Date(now).toISOString()}});
const guest=doc({hostUid:{stringValue:'host'},guestUid:{stringValue:'guest'},status:{stringValue:'accepted'}});
function setup({foreign=false,overflow=false,conflicts=0}={}){
 const calls=[];let commits=0;
 const fetcher=async(url,options={})=>{
  const body=options.body?JSON.parse(options.body):null;calls.push({url,body});
  if(url.endsWith(':beginTransaction'))return Response.json({transaction:'tx'});
  if(url.endsWith(':rollback'))return Response.json({});
  if(url.endsWith(':commit')){if(commits++<conflicts)return new Response('',{status:409});return Response.json({});}
  if(url.endsWith(':runQuery'))return Response.json(Array.from({length:11},(_,i)=>({document:{name:'test/'+(i===0&&!overflow?'guest':'other'+i)}})));
  if(url.includes('_livekit_rate_limits'))return new Response('',{status:404});
  if(url.includes('guest_requests'))return Response.json(guest);
  return Response.json(foreign?doc({...live.fields,ownerId:{stringValue:'other'}}):live);
 };
 return {db:storage(env,fetcher,()=>now,async()=>'test'),calls};
}
test('capacity is derived from first ten accepted document ids',async()=>{
 assert.equal((await setup().db.getGuest('live','guest')).guestCapacityAllowed,true);
 assert.equal((await setup({overflow:true}).db.getGuest('live','guest')).guestCapacityAllowed,false);
});
test('mute transaction validates ownership and updates only array policy',async()=>{
 const {db,calls}=setup();
 await db.saveAction({liveId:'live',guestUid:'guest',ownerUid:'host',roomName:'ngelx_host_1800000000000',action:'mute'});
 const write=calls.find(c=>c.url.endsWith(':commit')).body.writes[0];
 assert.deepEqual(write.transform.fieldTransforms,[{fieldPath:'guestAudioMutedUids',appendMissingElements:{values:[{stringValue:'guest'}]}}]);
 assert.equal(calls.find(c=>c.url.includes('guest_requests')).url.includes('transaction=tx'),true);
});
test('kick preserves other guest fields through an update mask',async()=>{
 const {db,calls}=setup();
 await db.saveAction({liveId:'live',guestUid:'guest',ownerUid:'host',roomName:'ngelx_host_1800000000000',action:'kick'});
 const writes=calls.find(c=>c.url.endsWith(':commit')).body.writes;
 assert.deepEqual(writes[1].updateMask,{fieldPaths:['status']});assert.equal(writes[1].update.fields.status.stringValue,'rejected');
 assert.equal(writes[1].updateTransforms[0].setToServerValue,'REQUEST_TIME');
});
test('foreign owner is rejected and transaction is rolled back',async()=>{
 const {db,calls}=setup({foreign:true});
 await assert.rejects(db.saveAction({liveId:'live',guestUid:'guest',ownerUid:'host',roomName:'ngelx_host_1800000000000',action:'kick'}));
 assert.equal(calls.some(c=>c.url.endsWith(':commit')),false);assert.equal(calls.some(c=>c.url.endsWith(':rollback')),true);
});
test('shared rate limit retries Firestore conflicts with fresh transactions',async()=>{
 const {db,calls}=setup({conflicts:1});assert.equal(await db.rateLimit('host'),true);
 assert.equal(calls.filter(c=>c.url.endsWith(':beginTransaction')).length,2);
 assert.equal(calls.filter(c=>c.url.endsWith(':commit')).length,2);
});
