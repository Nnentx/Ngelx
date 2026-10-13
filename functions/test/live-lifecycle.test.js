import test from 'node:test';
import assert from 'node:assert/strict';
import {expiredPK, finalizeDeadline, departureChanges, endStream} from '../live-lifecycle.js';
const match = () => ({active:true,ownerId:'host',guestUid:'guest',hostSession:{sid:'host-new'},guestSession:{sid:'guest-new'},pk:{id:'pk-new',status:'active',endsAtMs:1000,hostScore:25,guestScore:10}});
test('deadline finalization includes exact boundary but not early time', () => {
 assert.equal(expiredPK(match(),{pkId:'pk-new'},999),null);
 assert.equal(expiredPK(match(),{pkId:'pk-new'},1000).result,'host');
});
test('late old deadline cannot finish a replacement PK or a closed stream', () => {
 assert.equal(expiredPK(match(),{pkId:'pk-old'},5000),null);
 assert.equal(expiredPK({...match(),active:false},{pkId:'pk-new'},5000),null);
 assert.equal(expiredPK({...match(),pk:{...match().pk,status:'ended'}},{pkId:'pk-new'},5000),null);
});
test('duplicate deadlines read fresh scores and are harmless after completion',async()=>{
 const records=new Map([['deadline',{pkId:'pk-new',endsAtMs:1000}],['stream',match()]]);
 const db={runTransaction:async fn=>fn({get:async id=>({data:()=>records.get(id)}),update:(id,patch)=>records.set(id,{...records.get(id),...patch}),delete:id=>records.delete(id)})};
 records.get('stream').pk.guestScore=50;
 await finalizeDeadline(db,'deadline','stream',1000);
 assert.equal(records.get('stream').pk.result,'guest');
 assert.equal(records.has('deadline'),false);
 await finalizeDeadline(db,'deadline','stream',1001);
 assert.equal(records.get('stream').pk.guestScore,50);
});
test('old deadline cleanup preserves a new match',async()=>{
 const stream=match(), records=new Map([['deadline',{pkId:'pk-old',endsAtMs:500}],['stream',stream]]);
 const db={runTransaction:async fn=>fn({get:async id=>({data:()=>records.get(id)}),update:()=>assert.fail('new match was changed'),delete:id=>records.delete(id)})};
 await finalizeDeadline(db,'deadline','stream',1000);
 assert.equal(records.get('stream'),stream);assert.equal(records.has('deadline'),false);
});
test('future deadline remains queued',async()=>{
 const db={runTransaction:async fn=>fn({get:async()=>({data:()=>({pkId:'pk-new',endsAtMs:1001})}),update:()=>assert.fail(),delete:()=>assert.fail()})};
 await finalizeDeadline(db,'deadline','stream',1000);
});
test('stale or missing connection SID cannot remove a reconnected host or guest',()=>{
 assert.equal(departureChanges(match(),'host','host-old',123),null);
 assert.equal(departureChanges(match(),'guest','guest-old',123),null);
 assert.equal(departureChanges(match(),'host','',123),null);
 assert.equal(departureChanges(match(),'viewer','host-new',123),null);
});
test('current host departure ends the stream and settles the PK',()=>{
 const result=departureChanges(match(),'host','host-new',123);
 assert.equal(result.active,false);assert.equal(result.guestUid,'');assert.equal(result.pk.result,'host');assert.equal(result.endedAt,123);
 assert.equal(departureChanges({...match(),...result},'host','host-new',123),null);
});
test('guest departure preserves host stream and settles pending/active PK',()=>{
 const result=departureChanges(match(),'guest','guest-new',123);
 assert.equal(result.active,undefined);assert.equal(result.guestUid,'');assert.equal(result.pk.status,'ended');
 const pending={...match(),pk:{id:'p',status:'pending'}};
 assert.equal(departureChanges(pending,'guest','guest-new',123).pk.status,'cancelled');
});
test('room closure preserves settled results and cancels pending invitations',()=>{
 const ended={...match(),pk:{...match().pk,status:'ended',result:'guest'}};
 assert.equal(endStream(ended,'room_finished',123).pk.result,'guest');
 assert.equal(endStream({...match(),pk:{status:'pending'}},'room_finished',123).pk.status,'cancelled');
});

import {participantSession,joinedSessionChanges} from '../live-lifecycle.js';
test('session timestamps distinguish reconnections within the same second',()=>{
 const stream={...match(),hostSession:{sid:'old',joinedAtMs:1000001}};
 assert.equal(joinedSessionChanges(stream,{identity:'host',sid:'new',joinedAt:100n,joinedAtMs:1000002n}).hostSession.sid,'new');
});
test('delayed duplicate or older join cannot replace a newer session',()=>{
 const stream={...match(),hostSession:{sid:'new',joinedAtMs:1000002}};
 assert.equal(joinedSessionChanges(stream,{identity:'host',sid:'old',joinedAtMs:1000001n}),null);
 assert.equal(joinedSessionChanges(stream,{identity:'host',sid:'new',joinedAtMs:1000002n}),null);
 assert.equal(joinedSessionChanges(stream,{identity:'viewer',sid:'v',joinedAtMs:1000003n}),null);
});
test('older LiveKit timestamps normalize seconds to milliseconds; invalid sessions reject',()=>{
 assert.deepEqual(participantSession({sid:'s',joinedAt:123n}),{sid:'s',joinedAtMs:123000});
 assert.equal(participantSession({joinedAt:123n}),null);
 assert.equal(participantSession({sid:'s'}),null);
});
