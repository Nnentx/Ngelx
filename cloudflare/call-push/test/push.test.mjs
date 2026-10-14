import test from 'node:test';import assert from 'node:assert/strict';
import {createHandler} from '../src/handler.mjs';import {eventFor,validBody} from '../src/policy.mjs';import {decode,document} from '../src/google.mjs';
const now=1700000000000;
const chat=()=>({members:['a','b','b'],callStartedBy:'a',callRoomName:'private_452',callStatus:'ringing',callCreatedAt:now,callParticipants:['a','b'],isGroup:false});
function fixture(extra={}){let sends=[],claims=new Set();const io={now:()=>now,authenticate:async()=> 'a',getChat:async()=>chat(),rateLimit:async()=>true,getUser:async uid=>({uid,displayName:uid,blocked:[]}),tokens:async()=>['valid_device_token_1234567890'],claim:async(c,r,k,u)=>{const key=c+r+k+u;if(claims.has(key))return null;claims.add(key);return key;},complete:async()=>{},send:async(token,data)=>{sends.push({token,data});return true;},...extra};return {io,sends,handler:createHandler(io)};}
const req=(body={chatId:'chat',roomName:'private_452',offset:0})=>new Request('https://example.test/call',{method:'POST',body:JSON.stringify(body)});
test('only unique recipients receive trusted server-derived data',async()=>{const f=fixture();assert.equal((await f.handler(req())).status,200);assert.equal(f.sends.length,1);assert.equal(f.sends[0].data.recipientUid,'b');assert.equal(f.sends[0].data.title,'a');});
test('anonymous or invalid login does not read chats or send',async()=>{const f=fixture({authenticate:async()=>{throw Error();},getChat:async()=>{throw Error('should not read');}});assert.equal((await f.handler(req())).status,401);assert.equal(f.sends.length,0);});
test('outsider and non-caller cannot trigger ringing',async()=>{for(const uid of ['b','outsider']){const f=fixture({authenticate:async()=>uid});assert.equal((await f.handler(req())).status,403);assert.equal(f.sends.length,0);}});
test('wrong room, stale call and unknown state are rejected',async()=>{for(const patch of [{callRoomName:'other'},{callCreatedAt:now-61000},{callStatus:'unknown'}]){const f=fixture({getChat:async()=>({...chat(),...patch})});assert.equal((await f.handler(req())).status,403);}});
test('client cannot choose tokens, recipients or notification text',async()=>{for(const k of ['token','recipients','title']){const f=fixture();assert.equal((await f.handler(req({chatId:'chat',roomName:'private_452',[k]:'evil'}))).status,400);}});
test('both block directions and recipient settings suppress alerts',async()=>{for(const patch of [{blocked:['a']},{notificationsEnabled:false},{deactivated:true},{deleted:true}]){const f=fixture({getUser:async uid=>uid==='b'?{...patch}:{uid,blocked:[]}});await f.handler(req());assert.equal(f.sends.length,0);}const f=fixture({getUser:async uid=>({uid,blocked:uid==='a'?['b']:[]})});await f.handler(req());assert.equal(f.sends.length,0);});
test('replayed request does not alert a recipient twice',async()=>{const f=fixture();await f.handler(req());await f.handler(req());assert.equal(f.sends.length,1);});
test('call ending before dispatch suppresses stale incoming notification',async()=>{let n=0;const f=fixture({getChat:async()=>({...chat(),callStatus:++n===1?'ringing':'ended'})});await f.handler(req());assert.equal(f.sends.length,0);});
test('rate limiting fails closed before token access',async()=>{const f=fixture({rateLimit:async()=>false,tokens:async()=>{throw Error();}});assert.equal((await f.handler(req())).status,429);});
test('large groups are chunked and at most two devices per recipient',async()=>{const f=fixture({getChat:async()=>({...chat(),members:['a',...Array.from({length:12},(_,i)=>'u'+i)],isGroup:true}),tokens:async()=>['one','two','three']});const r=await f.handler(req());assert.equal((await r.json()).nextOffset,4);assert.equal(f.sends.length,8);});
test('member may cancel a fresh accepted call but not an old one',()=>{assert.equal(eventFor('b',{...chat(),callStatus:'active',callAnsweredAt:now},'private_452',now).kind,'call_end');assert.equal(eventFor('b',{...chat(),callStatus:'active',callAnsweredAt:now-61000},'private_452',now),null);});
test('invalid identifiers and nonchunk offsets rejected',()=>{for(const body of [{chatId:'../../users',roomName:'ok'},{chatId:'ok',roomName:'bad/room'},{chatId:'ok',roomName:'ok',offset:3}])assert.equal(validBody(body),false);});
test('datastore or push errors do not leak tokens or credentials',async()=>{const f=fixture({send:async()=>{throw Error('secret');}});const r=await f.handler(req());assert.equal(r.status,503);assert.doesNotMatch(await r.text(),/secret/);});
test('health is public and write paths require POST',async()=>{const f=fixture();assert.equal((await f.handler(new Request('https://example.test/health'))).status,200);assert.equal((await f.handler(new Request('https://example.test/call'))).status,404);});
test('Firestore REST values preserve false, zero, timestamps and arrays',()=>{assert.equal(decode({booleanValue:false}),false);assert.equal(decode({integerValue:'0'}),0);assert.deepEqual(decode({arrayValue:{values:[{stringValue:'a'}]}}),['a']);assert.equal(document({fields:{at:{timestampValue:'2023-11-14T22:13:20Z'}}}).at,now);});

test('oversized body is rejected before authentication even without content-length',async()=>{const f=fixture({authenticate:async()=>{throw Error('must not authenticate');}});assert.equal((await f.handler(new Request('https://example.test/call',{method:'POST',body:'x'.repeat(4096)}))).status,413);});

test('other group members cannot fan out duplicate cancellation requests',()=>{const c={...chat(),members:['a','b','c'],isGroup:true,callStatus:'active',callAnsweredAt:now};assert.equal(eventFor('c',c,'private_452',now),null);assert.equal(eventFor('b',c,'private_452',now).kind,'call_end');assert.equal(eventFor('a',c,'private_452',now).kind,'call_end');});

test('missing device registration is reported without claiming delivery',async()=>{
 let claimed=false;const f=fixture({tokens:async()=>[],claim:async()=>{claimed=true;return 'lease';}});
 const response=await f.handler(req());assert.equal(response.status,200);const body=await response.json();
 assert.equal(body.sent,0);assert.equal(body.missingDevices,1);assert.equal(claimed,false);assert.equal(f.sends.length,0);
});
test('unregistered devices are removed and never marked as successfully dispatched',async()=>{
 const completed=[],discarded=[];
 const f=fixture({send:async()=>false,complete:async(lease,ok)=>completed.push(ok),discardToken:async(uid,token)=>discarded.push({uid,token})});
 const response=await f.handler(req());const body=await response.json();
 assert.equal(body.sent,0);assert.equal(body.invalidDevices,1);assert.deepEqual(completed,[false]);
 assert.deepEqual(discarded,[{uid:'b',token:'valid_device_token_1234567890'}]);
});
