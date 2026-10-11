import {test} from 'node:test';
import assert from 'node:assert/strict';
import {loginWithIdentifier, parseIdentifier} from '../identifier-login.mjs';

function fixture(overrides = {}) {
  const calls = [];
  const user = {uid:'u1', email:'private@example.com', disabled:false,
    phoneNumber:'+905551234567', providerData:[{providerId:'phone',phoneNumber:'+905551234567'}]};
  return {calls, adapters:{
    verifyAppCheck:async()=>{calls.push('app-check');},
    consumeRateLimit:async()=>{calls.push('rate-limit');},
    resolveUniqueUid:async()=>{calls.push('resolve');return 'u1';},
    getAuthUser:async()=>({...user}),
    verifyPassword:async(email,password)=>{calls.push(['password',email,password]);return {uid:'u1'};},
    createCustomToken:async uid=>{calls.push('mint');return 'signed-'+uid;},
    ...overrides,
  }};
}
const input = {identifier:'User.Name',password:' secret '};
test('returns only token after app check, rate limit and exact password verification',async()=>{
  const {calls,adapters}=fixture();
  assert.deepEqual(await loginWithIdentifier(input,{},adapters),{customToken:'signed-u1'});
  assert.deepEqual(calls.slice(0,3),['app-check','rate-limit','resolve']);
  assert.deepEqual(calls[3],['password','private@example.com',' secret ']);
});
test('numeric usernames stay usernames and phone needs country code',()=>{
  assert.equal(parseIdentifier('1234567890').kind,'username');
  assert.deepEqual(parseIdentifier('+90 (555) 123-45-67'),{kind:'phone',value:'+905551234567'});
  for(const v of ['ab','a'.repeat(21),'user name','a\nb','+05551234567','+90abc'])
    assert.throws(()=>parseIdentifier(v));
});
for(const [name,override] of Object.entries({
  missing:{resolveUniqueUid:async()=>null},
  ambiguous:{resolveUniqueUid:async()=>{throw Error('two matches');}},
  wrongPassword:{verifyPassword:async()=>{throw Error('secret provider detail');}},
  reassigned:{verifyPassword:async()=>({uid:'different'})},
  mfa:{verifyPassword:async()=>({uid:'u1',mfaPendingCredential:'pending'})},
  disabled:{getAuthUser:async()=>({uid:'u1',email:'private@example.com',disabled:true})},
  enrolledMfa:{getAuthUser:async()=>({uid:'u1',email:'private@example.com',multiFactor:{enrolledFactors:[{}]}})},
  tenant:{getAuthUser:async()=>({uid:'u1',email:'private@example.com',tenantId:'t'})},
})) test(name+' fails with generic credential error and never mints',async()=>{
  const {calls,adapters}=fixture(override);
  await assert.rejects(loginWithIdentifier(input,{},adapters),e=>e.code==='invalid-credential');
  assert.ok(!calls.includes('mint'));
});
test('unlinked profile phone cannot authenticate',async()=>{
  const {calls,adapters}=fixture({getAuthUser:async()=>({uid:'u1',email:'private@example.com',phoneNumber:'+905551234567',providerData:[]})});
  await assert.rejects(loginWithIdentifier({...input,identifier:'+905551234567'},{},adapters));
  assert.ok(!calls.includes('mint'));
});
test('verified linked phone can authenticate',async()=>{
  const {adapters}=fixture();
  assert.deepEqual(await loginWithIdentifier({...input,identifier:'+905551234567'},{},adapters),{customToken:'signed-u1'});
});
test('disabled account between verification and mint is denied',async()=>{
  let reads=0;
  const {calls,adapters}=fixture({getAuthUser:async()=>({uid:'u1',email:'private@example.com',disabled:++reads>1})});
  await assert.rejects(loginWithIdentifier(input,{},adapters));
  assert.ok(!calls.includes('mint'));
});
test('missing protections and failed App Check stop before lookup',async()=>{
  await assert.rejects(loginWithIdentifier(input,{},{}),e=>e.code==='unavailable');
  const {calls,adapters}=fixture({verifyAppCheck:async()=>{throw Error('invalid app check');}});
  await assert.rejects(loginWithIdentifier(input,{},adapters));
  assert.equal(calls.length,0);
});
test('rate limiting stops before lookup',async()=>{
  const {calls,adapters}=fixture({consumeRateLimit:async()=>{throw Error('rate limit');}});
  await assert.rejects(loginWithIdentifier(input,{},adapters));
  assert.deepEqual(calls,['app-check']);
});
