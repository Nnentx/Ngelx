import test from 'node:test';import assert from 'node:assert/strict';import {callPushEvent} from './push-policy.mjs';
const now=Date.now(),t={toMillis:()=>now};const call={members:['a','b','b'],callStartedBy:'a',callRoomName:'private_448',callStatus:'ringing',callCreatedAt:t};
test('incoming call goes only to distinct recipients, never caller',()=>assert.deepEqual(callPushEvent(null,call,now).recipients,['b']));
test('heartbeat updates do not ring again',()=>assert.equal(callPushEvent(call,{...call,callHeartbeatAt:t},now),null));
test('old or malformed calls cannot trigger notifications',()=>{assert.equal(callPushEvent(null,call,now+61_000),null);assert.equal(callPushEvent(null,{...call,callStartedBy:'outsider'},now),null);});
test('answer/reject cancels incoming alert',()=>assert.equal(callPushEvent(call,{...call,callStatus:'active'},now).kind,'call_end'));
