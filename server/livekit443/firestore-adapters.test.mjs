import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createFirestoreRoomAuthorizer,createFirestoreRateLimiter} from './firestore-adapters.mjs';
const now=1800000000000;

// Transaction harness serializes concurrent writers, just as a retried Firestore
// transaction does; production emulator/device verification remains required.
function database(initial={}) {
 const records=new Map(Object.entries(initial)); let tail=Promise.resolve();
 const snap=key=>({exists:records.has(key),data:()=>records.get(key),ref:{collection(name){return {doc(id){return {get:async()=>snap(key+'/'+name+'/'+id)};}};}}});
 const db={records,collection(name){return {
  doc(id){const key=name+'/'+id;return {key,get:async()=>snap(key)};},
  where(field,op,expected){assert.equal(op,'==');return {limit(limit){return {get:async()=>{
   const docs=[...records].filter(([key,data])=>key.startsWith(name+'/')&&data[field]===expected)
     .slice(0,limit).map(([key])=>snap(key));return {empty:!docs.length,size:docs.length,docs};
  }};}};},
 };},runTransaction(fn){
  const work=tail.then(async()=>{let wrote=false;return fn({
   async get(ref){assert.equal(wrote,false,'all reads precede transaction writes');return snap(ref.key);},
   set(ref,data){wrote=true;records.set(ref.key,data);},
  });}); tail=work.catch(()=>{});return work;
 }}; return db;
}
const user={displayName:'Alice',blocked:[]};
test('fresh first host request obtains a server-owned reservation',async()=>{
 const db=database({'users/alice':user});
 const auth=createFirestoreRoomAuthorizer({db,now:()=>now});
 const p=await auth({uid:'alice',roomName:`ngelx_audio_alice_${now}`});
 assert.equal(p.role,'host');
 assert.equal([...db.records.keys()].filter(k=>k.startsWith('_livekit_owner_locks/')).length,1);
});
test('concurrent host starts cannot both acquire the owner lock',async()=>{
 const db=database({'users/alice':user});const auth=createFirestoreRoomAuthorizer({db,now:()=>now});
 const result=await Promise.all([now,now+1].map(n=>auth({uid:'alice',roomName:`ngelx_audio_alice_${n}`})));
 assert.equal(result.filter(Boolean).length,1);
});
test('reservation retry does not extend expiry',async()=>{
 let time=now;const db=database({'users/alice':user});const auth=createFirestoreRoomAuthorizer({db,now:()=>time});
 const roomName=`ngelx_audio_alice_${now}`;
 await auth({uid:'alice',roomName});time+=1000;await auth({uid:'alice',roomName});
 const lock=[...db.records].find(([key])=>key.startsWith('_livekit_owner_locks/'))[1];
 assert.equal(lock.expiresAt.getTime(),now+120000);
});
test('an existing active profile room prevents another initial host token',async()=>{
 const db=database({'users/alice':{...user,currentLiveId:'active'},
  'live_streams/active':{ownerId:'alice',roomName:'old',active:true,lastHeartbeatAt:new Date(now)}});
 assert.equal(await createFirestoreRoomAuthorizer({db,now:()=>now})({uid:'alice',roomName:`ngelx_audio_alice_${now}`}),null);
});
test('missing users and foreign room names cannot reserve',async()=>{
 const db=database({'users/alice':user});const auth=createFirestoreRoomAuthorizer({db,now:()=>now});
 assert.equal(await auth({uid:'alice',roomName:`ngelx_audio_bob_${now}`}),null);
 assert.equal(await auth({uid:'unknown',roomName:`ngelx_audio_unknown_${now}`}),null);
});
test('duplicate room records fail closed',async()=>{
 const db=database({'users/alice':user,'audio_rooms/a':{roomName:'duplicate'},'audio_rooms/b':{roomName:'duplicate'}});
 assert.equal(await createFirestoreRoomAuthorizer({db,now:()=>now})({uid:'alice',roomName:'duplicate'}),null);
});
test('private caller is denied when the other member blocks them',async()=>{
 const db=database({'users/alice':user,'users/bob':{blocked:['alice']},
  'chats/c':{callRoomName:'private',members:['alice','bob'],callStartedBy:'alice',callStatus:'active',callCreatedAt:new Date(now)}});
 assert.equal(await createFirestoreRoomAuthorizer({db,now:()=>now})({uid:'alice',roomName:'private'}),null);
});
test('shared rate limiter cannot exceed quota under concurrent calls',async()=>{
 const db=database();const limit=createFirestoreRateLimiter({db,now:()=>now});
 const result=await Promise.all(Array.from({length:35},()=>limit('uid:alice',30)));
 assert.equal(result.filter(Boolean).length,30);
 assert.equal([...db.records.keys()].some(k=>k.includes('alice')),false);
});
test('quota resets at the next minute and separates UID/IP scopes',async()=>{
 let time=now;const db=database();const limit=createFirestoreRateLimiter({db,now:()=>time});
 assert.equal(await limit('uid:alice',1),true);assert.equal(await limit('uid:alice',1),false);
 assert.equal(await limit('ip:example',1),true);time+=60000;assert.equal(await limit('uid:alice',1),true);
});


test('live guest token is authorized from only the current guest request',async()=>{
 const db=database({'users/alice':user,'users/host':user,'live_streams/live':{ownerId:'host',roomName:'live448',active:true,lastHeartbeatAt:new Date(now),visibility:'public'},'live_streams/live/guest_requests/alice':{hostUid:'host',guestUid:'alice',status:'accepted'}});
 const auth=createFirestoreRoomAuthorizer({db,now:()=>now});
 assert.equal((await auth({uid:'alice',roomName:'live448'})).canPublish,true);
 db.records.get('live_streams/live/guest_requests/alice').status='rejected';
 assert.equal((await auth({uid:'alice',roomName:'live448'})).canPublish,false);
});
