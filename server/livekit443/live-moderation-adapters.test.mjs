import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createGuestModerationStorage} from './live-moderation-adapters.mjs';
const now=1800000000000;
function database(){
 const records=new Map([
  ['live_streams/live1',{ownerId:'host',roomName:'lk_room',active:true,
   lastHeartbeatAt:new Date(now),guestAudioMutedUids:[]}],
  ['live_streams/live1/guest_requests/alice',{guestUid:'alice',hostUid:'host',status:'accepted'}]
 ]);
 const FieldValue={
  arrayUnion:uid=>({__op:'union',uid}),
  arrayRemove:uid=>({__op:'remove',uid}),
  serverTimestamp:()=>new Date(now)
 };
 const makeRef=key=>({
  key,
  collection:name=>({
    doc:uid=>makeRef(key+'/'+name+'/'+uid),
    where:(field,op,wanted)=>{
      assert.equal(field,'status');
      assert.equal(op,'==');
      return {orderBy:order=>{
        assert.equal(order,'__name__');
        return {limit:max=>({get:async()=>({
          docs:[...records.entries()]
            .filter(([path,v])=>path.startsWith(key+'/'+name+'/') &&
              !path.slice((key+'/'+name+'/').length).includes('/') &&
              v[field]===wanted)
            .sort(([a],[b])=>a.localeCompare(b))
            .slice(0,max).map(([path])=>({id:path.split('/').at(-1)})),
        })})};
      }};
    }
  }),
  get:async()=>snapshot(key)
 });
 const snapshot=key=>({exists:records.has(key),data:()=>records.get(key)});
 const db={
  collection:name=>({doc:id=>makeRef(name+'/'+id)}),
  runTransaction:async fn=>{
   let wrote=false;
   const writes=[];
   const result=await fn({
    get:async ref=>{assert.equal(wrote,false);return snapshot(ref.key);},
    update:(ref,fields)=>{wrote=true;writes.push([ref.key,fields]);}
   });
   for(const [key,fields] of writes){
    const obj={...records.get(key)};
    for(const [field,value] of Object.entries(fields)){
     if(value && value.__op==='union'){
      obj[field]=[...new Set([...(obj[field]??[]),value.uid])];
     }else if(value && value.__op==='remove'){
      obj[field]=(obj[field]??[]).filter(id=>id!==value.uid);
     }else obj[field]=value;
    }
    records.set(key,obj);
   }
   return result;
  }
 };
 return {db,FieldValue,records};
}
const action={liveId:'live1',guestUid:'alice',ownerUid:'host',roomName:'lk_room'};
test('server moderation persists and clears host mute policy',async()=>{
 const d=database(),a=createGuestModerationStorage({...d,now:()=>now});
 assert.equal((await a.getRoom('live1')).ownerId,'host');
 assert.equal((await a.getGuest('live1','alice')).status,'accepted');
 await a.saveAction({...action,action:'mute'});
 await a.saveAction({...action,action:'mute'});
 assert.deepEqual(d.records.get('live_streams/live1').guestAudioMutedUids,['alice']);
 await a.saveAction({...action,action:'unmute'});
 assert.deepEqual(d.records.get('live_streams/live1').guestAudioMutedUids,[]);
});
test('server kick rejects guest and clears prior mute',async()=>{
 const d=database(),a=createGuestModerationStorage({...d,now:()=>now});
 await a.saveAction({...action,action:'mute'});
 await a.saveAction({...action,action:'kick'});
 assert.equal(d.records.get('live_streams/live1/guest_requests/alice').status,'rejected');
 assert.deepEqual(d.records.get('live_streams/live1').guestAudioMutedUids,[]);
});
test('transaction rechecks owner, room name, acceptance and active heartbeat',async()=>{
 for(const change of [
  {ownerId:'attacker'}, {roomName:'different'}, {active:false},
  {lastHeartbeatAt:new Date(now-120001)}
 ]){
  const d=database();
  Object.assign(d.records.get('live_streams/live1'),change);
  const a=createGuestModerationStorage({...d,now:()=>now});
  await assert.rejects(a.saveAction({...action,action:'mute'}));
  assert.deepEqual(d.records.get('live_streams/live1').guestAudioMutedUids,[]);
 }
 const d=database();
 d.records.get('live_streams/live1/guest_requests/alice').status='pending';
 const a=createGuestModerationStorage({...d,now:()=>now});
 await assert.rejects(a.saveAction({...action,action:'mute'}));
});
test('reject invalid server admin fields',async()=>{
 const d=database(),a=createGuestModerationStorage({...d,now:()=>now});
 await assert.rejects(a.saveAction({...action,action:'invented'}));
 await assert.rejects(a.saveAction({...action,ownerUid:'attacker',action:'mute'}));
});

test('Build529 accepted guest moderation query respects first-ten document IDs',async()=>{
 const d=database();
 d.records.delete('live_streams/live1/guest_requests/alice');
 for(let n=0;n<11;n++){
  const uid='guest'+String(n).padStart(2,'0');
  d.records.set('live_streams/live1/guest_requests/'+uid,{guestUid:uid,
    hostUid:'host',status:'accepted',guestCapacityAllowed:true});
 }
 const storage=createGuestModerationStorage({...d,now:()=>now});
 for(let n=0;n<10;n++){
  const uid='guest'+String(n).padStart(2,'0');
  assert.equal((await storage.getGuest('live1',uid)).guestCapacityAllowed,true,uid);
 }
 assert.equal((await storage.getGuest('live1','guest10')).guestCapacityAllowed,false);
 // A forged stored guestCapacityAllowed flag is never trusted over the
 // indexed server query result.
 d.records.get('live_streams/live1/guest_requests/guest10').guestCapacityAllowed=true;
 assert.equal((await storage.getGuest('live1','guest10')).guestCapacityAllowed,false);
 d.records.get('live_streams/live1/guest_requests/guest02').status='rejected';
 assert.equal((await storage.getGuest('live1','guest10')).guestCapacityAllowed,true);
});

test('Build529 unaccepted guest does not trigger capacity query',async()=>{
 const d=database(),storage=createGuestModerationStorage({...d,now:()=>now});
 d.records.get('live_streams/live1/guest_requests/alice').status='rejected';
 assert.equal((await storage.getGuest('live1','alice')).status,'rejected');
 assert.equal(await storage.getGuest('live1','missing'),null);
});
