import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createGuestModeration} from './live-moderation.mjs';
const clock=1800000000000;
const room={ownerId:'host',active:true,lastHeartbeatAt:new Date(clock),roomName:'ngelx_host_1800000000000'};
const guest={hostUid:'host',guestUid:'alice',status:'accepted'};
const request={method:'POST',authorization:'Bearer valid',body:{
  liveId:'live1',guestUid:'alice',action:'mute'
}};
function setup(overrides={}) {
 const events=[];
 const participants=overrides.participants??[{
  identity:'alice',tracks:[{sid:'audio_1',type:0},{sid:'video_1',type:1}]
 }];
 const service={
  listParticipants:async()=>{events.push('list');return participants;},
  updateParticipant:async (roomName,uid,opts)=>{events.push(['permission',roomName,uid,opts]);},
  mutePublishedTrack:async (roomName,uid,sid,muted)=>{events.push(['mute',roomName,uid,sid,muted]);},
  removeParticipant:async (roomName,uid)=>{events.push(['kick',roomName,uid]);}
 };
 const deps={
  verifyFirebaseToken:async token=>{
    if(token!=='valid')throw Error('revoked test token');
    return {uid:'host',firebase:{sign_in_provider:'password'}};
  },
  getRoom:async()=>room,getGuest:async()=>guest,
  saveAction:async args=>{events.push(['saved',args]);},
  rateLimit:async()=>true,roomService:service,
  cameraSource:1,microphoneSource:2,audioTrackType:0,now:()=>clock,
  ...overrides
 };
 return {run:createGuestModeration(deps),events,service};
}
test('host mute restricts future microphone tracks and mutes remaining current audio',async()=>{
 const {run,events}=setup();
 const result=await run(request);
 assert.equal(result.status,200);
 assert.equal(result.body.ok,true);
 assert.deepEqual(events.filter(x=>Array.isArray(x)&&x[0]==='permission')[0],
  ['permission','ngelx_host_1800000000000','alice',{permission:{
    canSubscribe:true,canPublish:true,canPublishData:true,
    canUpdateMetadata:false,canPublishSources:[1]}}]);
 assert.deepEqual(events.filter(x=>Array.isArray(x)&&x[0]==='mute'),
  [['mute','ngelx_host_1800000000000','alice','audio_1',true]]);
 assert.equal(events.filter(x=>Array.isArray(x)&&x[0]==='saved').length,1);
 assert.equal(events.at(-1)[0],'saved');
});
test('unmute restores publishing permission, never forces a microphone to enable remotely',async()=>{
 const {run,events}=setup();
 const r=await run({...request,body:{...request.body,action:'unmute'}});
 assert.equal(r.status,200);
 assert.deepEqual(events.find(x=>Array.isArray(x)&&x[0]==='permission')[3],
  {permission:{
    canSubscribe:true,canPublish:true,canPublishData:true,
    canUpdateMetadata:false,canPublishSources:[1,2]}});
 assert.equal(events.some(x=>Array.isArray(x)&&x[0]==='mute'),false);
});
test('kick removes the connected participant before marking the guest rejected',async()=>{
 const {run,events}=setup();
 assert.equal((await run({...request,body:{...request.body,action:'kick'}})).status,200);
 assert.deepEqual(events.filter(x=>Array.isArray(x)&&x[0]==='kick'),
  [['kick','ngelx_host_1800000000000','alice']]);
 assert.equal(events.at(-1)[0],'saved');
});
test('offline accepted guest can be muted or kicked in trusted Firestore without live API operations',async()=>{
 const {run,events}=setup({participants:[]});
 assert.equal((await run(request)).status,200);
 assert.equal((await run({...request,body:{...request.body,action:'kick'}})).status,200);
 assert.equal(events.filter(x=>Array.isArray(x)&&x[0]!=='saved').length,0);
 assert.equal(events.filter(x=>Array.isArray(x)&&x[0]==='saved').length,2);
});
test('anonymous, missing and revoked authentication cannot moderate',async()=>{
 const {run,events}=setup();
 assert.equal((await run({...request,authorization:''})).status,401);
 assert.equal((await run({...request,authorization:'Bearer expired'})).status,401);
 const anon=setup({verifyFirebaseToken:async()=>({uid:'host',firebase:{sign_in_provider:'anonymous'}})});
 assert.equal((await anon.run(request)).status,401);
 assert.equal(events.length,0);
});
test('an arbitrary guest or other host cannot invoke remote administration',async()=>{
 const {run,events}=setup({verifyFirebaseToken:async()=>({uid:'alice'})});
 assert.equal((await run(request)).status,400); // self-moderation rejected
 const other=setup({verifyFirebaseToken:async()=>({uid:'other'})});
 assert.equal((await other.run(request)).status,403);
 assert.equal(events.length,0);
 assert.equal(other.events.length,0);
});
test('pending guests, stale rooms, deleted rooms and forged room ids fail closed',async()=>{
 for(const guestStatus of ['pending','rejected','invited']){
  const {run,events}=setup({getGuest:async()=>({...guest,status:guestStatus})});
  assert.equal((await run(request)).status,409);
  assert.equal(events.length,0);
 }
 for(const stored of [null,{...room,active:false},
   {...room,lastHeartbeatAt:new Date(clock-120001)},
   {...room,roomName:'not/allowed'}]){
  const {run,events}=setup({getRoom:async()=>stored});
  assert.equal((await run(request)).status,403);
  assert.equal(events.length,0);
 }
});
test('caller cannot choose LiveKit room or grant privileges',async()=>{
 const {run,events}=setup();
 const cases=[
  {...request.body,roomName:'other'},
  {...request.body,guestUid:'../host'},
  {...request.body,guestUid:'host'},
  {...request.body,action:'removeAll'},
  {...request.body,canPublishSources:['microphone']},
 ];
 for(const body of cases) assert.equal((await run({...request,body})).status,400);
 assert.equal(events.length,0);
});
test('method validation, rate limiting, remote errors, and database failures are safe',async()=>{
 assert.equal((await setup().run({...request,method:'GET'})).status,405);
 assert.equal((await setup({rateLimit:async()=>false}).run(request)).status,429);
 const unavailable=setup({roomService:{
  listParticipants:async()=>{throw Error('private RTC credential');},
  updateParticipant:async()=>{},mutePublishedTrack:async()=>{},removeParticipant:async()=>{}
 }});
 const fail=await unavailable.run(request);
 assert.equal(fail.status,503);
 assert.equal(JSON.stringify(fail).includes('credential'),false);
 const save=setup({saveAction:async()=>{throw Error('private Firestore path');}});
 const bad=await save.run(request);assert.equal(bad.status,503);
 assert.equal(JSON.stringify(bad).includes('Firestore'),false);
});
test('untrusted dependency injection is rejected at setup',()=>{
 assert.throws(()=>createGuestModeration({}),/Trusted/);
});

test('Firestore owner cannot target another hosts LiveKit room by editing roomName',async()=>{
 const other='ngelx_victim_1800000000000';
 const {run,events}=setup({getRoom:async()=>({...room,roomName:other})});
 const result=await run(request);
 assert.equal(result.status,403);
 assert.equal(events.length,0);
});
test('owner prefix must contain exactly a 13-digit millisecond timestamp',async()=>{
 for (const invalid of ['arbitrary_live_room','ngelx_host_notatime','ngelx_host_0123',
   'ngelx_host_1800000000000_extra','ngelx_host_1800000000000/other']) {
  const {run,events}=setup({getRoom:async()=>({...room,roomName:invalid})});
  assert.equal((await run(request)).status,403,invalid);
  assert.equal(events.length,0);
 }
});
