import {test} from 'node:test';
import assert from 'node:assert/strict';
import {roomPermission, hostRequestKind} from './room-policy.mjs';
const now=1800000000000;
const viewer={displayName:'Alice',blocked:[]};
const owner={displayName:'Bob',blocked:[],friends:['alice'],followers:['alice']};
const room={ownerId:'bob',active:true,lastHeartbeatAt:new Date(now),visibility:'public',speakerIds:[]};
const permission=changes=>roomPermission({kind:'audio',uid:'alice',viewer,owner,room,now,...changes});
test('public listeners cannot publish even when the client calls them host',()=>{
 const p=permission();assert.equal(p.role,'listener');assert.equal(p.canPublish,false);
});
test('speaker permission originates from the stored speaker list',()=>{
 const p=permission({room:{...room,speakerIds:['alice']}});assert.equal(p.role,'speaker');assert.equal(p.canPublish,true);
});
test('live listener cannot publish through an audio speaker list',()=>assert.equal(permission({kind:'live',room:{...room,speakerIds:['alice']}}).canPublish,false));
test('ended and stale rooms are denied',()=>{
 assert.equal(permission({room:{...room,active:false}}),null);
 assert.equal(permission({room:{...room,lastHeartbeatAt:new Date(now-120001)}}),null);
});
test('both block directions and bans are enforced',()=>{
 assert.equal(permission({viewer:{...viewer,blocked:['bob']}}),null);
 assert.equal(permission({owner:{...owner,blocked:['alice']}}),null);
 assert.equal(permission({room:{...room,bannedUserIds:['alice']}}),null);
});
test('private audiences and unknown visibility fail closed',()=>{
 for(const visibility of ['friends','followers','Arkadaşlar','Takipçiler']) {
  assert.equal(permission({room:{...room,visibility}}).allowed,true);
  assert.equal(permission({room:{...room,visibility},owner:{...owner,friends:[],followers:[]}}),null);
 }
 assert.equal(permission({room:{...room,visibility:'invented'}}),null);
});
test('deleted or deactivated accounts are denied',()=>{
 assert.equal(permission({owner:{...owner,deactivated:true}}),null);
 assert.equal(permission({viewer:null}),null);
});
const call={members:['alice','bob'],callStartedBy:'alice',callCreatedAt:new Date(now),callStatus:'active',isGroup:false};
test('private call checks current membership and the opposite account block list',()=>{
 const args={kind:'call',uid:'alice',peerId:'bob',room:call,viewer,owner,now};
 assert.equal(roomPermission(args).role,'caller');
 assert.equal(roomPermission({...args,owner:{...owner,blocked:['alice']}}),null);
 assert.equal(roomPermission({...args,uid:'stranger'}),null);
 assert.equal(roomPermission({...args,room:{...call,callStatus:'ended'}}),null);
 assert.equal(roomPermission({...args,room:{...call,callStartedBy:'outsider'}}),null);
});
test('ringing call expiry is bounded',()=>assert.equal(roomPermission({kind:'call',uid:'alice',peerId:'bob',room:{...call,callStatus:'ringing',callCreatedAt:new Date(now-120001)},viewer,owner,now}),null));
test('host prefix selects only fresh own reservations',()=>{
 assert.equal(hostRequestKind('alice',`ngelx_audio_alice_${now}`,now),'audio');
 assert.equal(hostRequestKind('alice',`ngelx_alice_${now}`,now),'live');
 assert.equal(hostRequestKind('alice',`ngelx_audio_bob_${now}`,now),null);
 assert.equal(hostRequestKind('alice',`ngelx_audio_alice_${now-60001}`,now),null);
 assert.equal(hostRequestKind('alice','ngelx_audio_alice_fake',now),null);
});
