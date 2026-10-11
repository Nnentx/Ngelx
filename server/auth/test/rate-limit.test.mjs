import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createFirestoreRateLimiter} from '../rate-limit.mjs';

// Serialized transaction fake tests policy/ordering, not Firestore contention.
function fixture(options = {}) {
  const records = new Map();let tail=Promise.resolve();let time=100000;
  const db={collection:name=>({doc:id=>name+'/'+id}),runTransaction:fn=>{
    const task=tail.then(async()=>{
      const writes=[];let writing=false;
      await fn({get:async ref=>{assert.equal(writing,false);return {exists:records.has(ref),data:()=>records.get(ref)};},
        set:(ref,data)=>{writing=true;writes.push([ref,data]);}});
      for(const [ref,data] of writes)records.set(ref,data);
    });tail=task.catch(()=>{});return task;
  }};
  const consume=createFirestoreRateLimiter({db,secret:'x'.repeat(32),now:()=>time,...options});
  return {records,consume,setTime:v=>{time=v;}};
}
const identifier={kind:'username',value:'user'};
const context={trustedRemoteAddress:'192.0.2.1'};
test('five attempts permitted then denied without partial counter writes',async()=>{
  const {consume,records}=fixture();
  for(let i=0;i<5;i++)await consume(identifier,context);
  const before=structuredClone([...records]);
  await assert.rejects(consume(identifier,context),e=>e.code==='too-many-requests');
  assert.deepEqual([...records],before);
});
test('concurrent attempts obey shared identifier limit',async()=>{
  const {consume}=fixture();
  const results=await Promise.allSettled(Array.from({length:20},(_,i)=>consume(identifier,{trustedRemoteAddress:'192.0.2.'+(i+1)})));
  assert.equal(results.filter(x=>x.status==='fulfilled').length,5);
});
test('network limit applies across different accounts',async()=>{
  const {consume}=fixture({networkLimit:3});
  for(let i=0;i<3;i++)await consume({kind:'username',value:'user'+i},context);
  await assert.rejects(consume({kind:'username',value:'other'},context),e=>e.code==='too-many-requests');
});
test('window expiry resets counters even before TTL cleanup',async()=>{
  const {consume,setTime}=fixture({identifierLimit:1});
  await consume(identifier,context);setTime(159999);
  await assert.rejects(consume(identifier,context));setTime(160000);
  await consume(identifier,context);
});
test('persisted records contain no raw identifier or network address',async()=>{
  const {consume,records}=fixture();await consume(identifier,context);
  const text=JSON.stringify([...records]);
  assert.ok(!text.includes('192.0.2.1'));assert.ok(!text.includes('user'));
  for(const value of records.values())assert.deepEqual(Object.keys(value).sort(),['count','expiresAt','startedAtMs']);
});
test('equivalent IPv6 spellings and mapped IPv4 share network counter',async()=>{
  for(const pair of [['2001:db8::1','2001:0db8:0:0:0:0:0:1'],['192.0.2.1','::ffff:192.0.2.1']]){
    const {consume}=fixture({networkLimit:1});
    await consume(identifier,{trustedRemoteAddress:pair[0]});
    await assert.rejects(consume({kind:'username',value:'other'},{trustedRemoteAddress:pair[1]}),e=>e.code==='too-many-requests');
  }
});
test('missing trusted address or malformed identifier writes nothing',async()=>{
  const {consume,records}=fixture();
  for(const c of [{},{trustedRemoteAddress:'client-header'},{trustedRemoteAddress:'192.0.2.1, 192.0.2.2'}])await assert.rejects(consume(identifier,c));
  await assert.rejects(consume({kind:'phone',value:'1234567890'},context));
  assert.equal(records.size,0);
});
test('storage failure, corrupt count and clock rollback fail closed',async()=>{
  const broken=createFirestoreRateLimiter({secret:'x'.repeat(32),db:{collection:()=>({doc:x=>x}),runTransaction:async()=>{throw Error('offline');}}});
  await assert.rejects(broken(identifier,context),e=>e.code==='unavailable');
  const {consume,records,setTime}=fixture();await consume(identifier,context);
  setTime(99999);await assert.rejects(consume(identifier,context),e=>e.code==='unavailable');
  setTime(100000);records.values().next().value.count=-1;
  await assert.rejects(consume(identifier,context),e=>e.code==='unavailable');
});
