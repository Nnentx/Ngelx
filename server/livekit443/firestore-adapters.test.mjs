import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createFirestoreRoomAuthorizer,createFirestoreRateLimiter} from './firestore-adapters.mjs';
import {roomPermission} from './room-policy.mjs';
const now=1800000000000;

// Transaction harness serializes concurrent writers, just as a retried Firestore
// transaction does; production emulator/device verification remains required.
function database(initial={}) {
 const records=new Map(Object.entries(initial)); let tail=Promise.resolve();
 const snap=key=>({
  id:key.split('/').at(-1),exists:records.has(key),data:()=>records.get(key),
  ref:{collection(name){
   const prefix=key+'/'+name+'/';
   return {
    doc(id){return {get:async()=>snap(prefix+id)};},
    where(field,op,expected){
     assert.equal(op,'==');
     return {orderBy(order){
      assert.equal(order,'__name__');
      return {limit(limit){return {get:async()=>{
       const docs=[...records].filter(([k,v])=>k.startsWith(prefix)&&
         !k.slice(prefix.length).includes('/')&&v[field]===expected)
         .sort(([a],[b])=>a.localeCompare(b)).slice(0,limit)
         .map(([k])=>snap(k));
       return {docs,empty:docs.length===0,size:docs.length};
      }};}};}
    }
   };
  }}
 });
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

test('live guest token reads host moderation state from the matched room document',async()=>{
 const db=database({'users/alice':user,'users/host':user,
  'live_streams/live':{ownerId:'host',roomName:'live448',active:true,lastHeartbeatAt:new Date(now),
    visibility:'public',guestAudioMutedUids:['alice']},
  'live_streams/live/guest_requests/alice':{hostUid:'host',guestUid:'alice',status:'accepted'}});
 const auth=createFirestoreRoomAuthorizer({db,now:()=>now});
 const muted=await auth({uid:'alice',roomName:'live448'});
 assert.equal(muted.canPublish,true);
 assert.deepEqual(muted.canPublishSources,['camera']);
 db.records.get('live_streams/live').guestAudioMutedUids=[];
 assert.equal((await auth({uid:'alice',roomName:'live448'})).canPublishSources,undefined);
});

test('Build522 never issues publish rights to an 11th accepted live guest',async()=>{
 const guests=Array.from({length:11},(_,i)=>'guest'+String(i).padStart(2,'0'));
 const initial={
  'users/host':user,
  'live_streams/live522':{ownerId:'host',roomName:'live522',
    active:true,lastHeartbeatAt:new Date(now),visibility:'public'},
 };
 for(const uid of guests){
  initial['users/'+uid]={displayName:uid,blocked:[]};
  initial['live_streams/live522/guest_requests/'+uid]={
    hostUid:'host',guestUid:uid,status:'accepted'};
 }
 const db=database(initial),authorize=createFirestoreRoomAuthorizer({db,now:()=>now});
 for(const uid of guests.slice(0,10)){
  const p=await authorize({uid,roomName:'live522'});
  assert.equal(p.allowed,true,uid);
  assert.equal(p.role,'speaker',uid);
  assert.equal(p.canPublish,true,uid);
 }
 const overflow=await authorize({uid:'guest10',roomName:'live522'});
 assert.equal(overflow.allowed,true,'public viewer remains allowed');
 assert.equal(overflow.role,'listener','no eleventh publisher');
 assert.equal(overflow.canPublish,false);
 const host=await authorize({uid:'host',roomName:'live522'});
 assert.equal(host.role,'host');
 assert.equal(host.canPublish,true);
 // Revoke one of the ten accepted requests: one waiting guest takes the
 // vacated server slot, without trusting any client-side counter.
 db.records.get('live_streams/live522/guest_requests/guest02').status='rejected';
 const promoted=await authorize({uid:'guest10',roomName:'live522'});
 assert.equal(promoted.canPublish,true);
 const removed=await authorize({uid:'guest02',roomName:'live522'});
 assert.equal(removed.canPublish,false);
});

test('Build522 capacity policy cannot be bypassed by a client-supplied slot',()=>{
 const live={ownerId:'host',active:true,lastHeartbeatAt:new Date(now),
  visibility:'public',guestRequest:{hostUid:'host',guestUid:'guest',status:'accepted'},
  guestCapacityAllowed:false,guestSlot:1,guestCount:0};
 const p=roomPermission({kind:'live',uid:'guest',viewer:user,owner:user,room:live,now});
 assert.equal(p.role,'listener');
 assert.equal(p.canPublish,false);
});
