import test from 'node:test';
import assert from 'node:assert/strict';
import {authorizePublish,reconcileJoinedPublisher} from '../live-permissions.js';
function harness(options={}) {
 const state={active:true,ownerId:'host',guestUid:'guest',guestSlotId:'slot-1',roomName:'live_x',...options.stream};
 const calls=[];
 let readCount=0;
 const ref={get:async()=>({data:()=>({...state})})};
 const db={runTransaction:async fn=>fn({get:ref.get,update:(_,patch)=>Object.assign(state,patch)})};
 const service={
  getParticipant:async()=>({identity:'guest',sid:options.changedConnection&&readCount++>0?'new':'old',joinedAtMs:1000n}),
  updateParticipant:async(_room,_uid,params)=>{
   calls.push(params.permission.canPublish?'grant':'revoke');
   if(params.permission.canPublish&&options.afterGrant) options.afterGrant(state);
   if(params.permission.canPublish&&options.grantError) throw Error('grant response lost');
   if(!params.permission.canPublish&&options.revokeError) throw Error('revoke failed');
  },
  removeParticipant:async()=>{calls.push('remove');},
  deleteRoom:async()=>{calls.push('delete');},
 };
 return {state,calls,ref,db,service};
}
test('host and accepted guest get publishing bound to current SID',async()=>{
 for(const uid of ['host','guest']) {
  const h=harness();await authorizePublish(h.db,h.ref,h.service,uid);
  assert.deepEqual(h.calls,['grant']);assert.equal(h.state[uid==='host'?'hostSession':'guestSession'].sid,'old');
 }
});
test('viewers and closed streams never reach permission grant',async()=>{
 for(const [uid,stream] of [['viewer',{}],['host',{active:false}]]) {
  const h=harness({stream});await assert.rejects(authorizePublish(h.db,h.ref,h.service,uid));assert.deepEqual(h.calls,[]);
 }
});
test('concurrent guest leave revokes an in-flight publishing grant',async()=>{
 const h=harness({afterGrant:s=>{s.guestUid='';}});
 await assert.rejects(authorizePublish(h.db,h.ref,h.service,'guest'));
 assert.deepEqual(h.calls,['grant','revoke']);assert.equal(h.state.guestSession,undefined);
});
test('same user reaccepted in another slot cannot reuse old authorization',async()=>{
 const h=harness({afterGrant:s=>{s.guestSlotId='slot-2';}});
 await assert.rejects(authorizePublish(h.db,h.ref,h.service,'guest'));assert.deepEqual(h.calls,['grant','revoke']);
});
test('connection changing during grant requires a retry',async()=>{
 const h=harness({changedConnection:true});await assert.rejects(authorizePublish(h.db,h.ref,h.service,'guest'));
 assert.deepEqual(h.calls,['grant','revoke']);assert.equal(h.state.guestSession,undefined);
});
test('failed revocation removes the participant instead of hiding failure',async()=>{
 const h=harness({afterGrant:s=>{s.active=false;},revokeError:true});
 await assert.rejects(authorizePublish(h.db,h.ref,h.service,'guest'));assert.deepEqual(h.calls,['grant','revoke','remove']);
});
test('lost grant response still attempts permission revocation',async()=>{
 const h=harness({grantError:true});await assert.rejects(authorizePublish(h.db,h.ref,h.service,'guest'));
 assert.deepEqual(h.calls,['grant','revoke']);
});
test('joining with an old publishing token reconciles current role or closed room',async()=>{
 const h=harness();await reconcileJoinedPublisher(h.ref,h.service,'live_x',{identity:'viewer',permission:{canPublish:true}});
 assert.deepEqual(h.calls,['revoke']);
 h.calls.length=0;await reconcileJoinedPublisher(h.ref,h.service,'live_x',{identity:'guest',permission:{canPublish:true}});
 assert.deepEqual(h.calls,[]);
 h.state.active=false;await reconcileJoinedPublisher(h.ref,h.service,'live_x',{identity:'host',permission:{canPublish:true}});
 assert.deepEqual(h.calls,['delete']);
});
