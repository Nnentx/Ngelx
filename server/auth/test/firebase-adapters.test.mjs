import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createPasswordVerifier,createAdminIdentityAdapters} from '../firebase-adapters.mjs';

const success = {localId:'u1',idToken:'secret-id',refreshToken:'secret-refresh',email:'private@example.com'};
test('password REST request preserves password and returns UID only',async()=>{
  let request;
  const verify=createPasswordVerifier({apiKey:'key',fetchImpl:async(url,options)=>{
    request={url,...options};return {ok:true,json:async()=>success};
  }});
  assert.deepEqual(await verify('private@example.com',' secret '),{uid:'u1'});
  assert.equal(request.url,'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=key');
  assert.deepEqual(JSON.parse(request.body),{email:'private@example.com',password:' secret ',returnSecureToken:true});
  assert.equal(request.redirect,'error');assert.equal(request.cache,'no-store');
});
for (const [name,result] of Object.entries({
  missingUid:{idToken:'token'},missingToken:{localId:'u1'},
  mfa:{...success,mfaPendingCredential:'pending'},
  mfaInfo:{...success,mfaInfo:[{}]},unknownAccount:{...success,registered:false},
})) test(name+' response fails closed',async()=>{
  const verify=createPasswordVerifier({apiKey:'key',fetchImpl:async()=>({ok:true,json:async()=>result})});
  await assert.rejects(verify('e','password'),e=>e.code==='invalid-credential');
});
test('provider errors are generic without reading raw body',async()=>{
  const verify=createPasswordVerifier({apiKey:'key',fetchImpl:async()=>({ok:false,json:()=>{throw Error('should not read');}})});
  await assert.rejects(verify('e','password'),e=>e.message==='invalid-credential');
});
test('network and malformed body failures are generic',async()=>{
  for(const fetchImpl of [async()=>{throw Error('private detail');},async()=>({ok:true,json:async()=>{throw Error('bad json');}})]){
    await assert.rejects(createPasswordVerifier({apiKey:'key',fetchImpl})('e','password'),e=>e.code==='unavailable');
  }
});
test('deadline aborts upstream even if fetch ignores signal',async()=>{
  let signal;
  const verify=createPasswordVerifier({apiKey:'key',timeoutMs:10,fetchImpl:async(_,o)=>{signal=o.signal;return new Promise(()=>{});}});
  await assert.rejects(verify('e','password'),e=>e.code==='unavailable');
  assert.equal(signal.aborted,true);
});
test('deadline also bounds slow response body',async()=>{
  const verify=createPasswordVerifier({apiKey:'key',timeoutMs:10,fetchImpl:async()=>({ok:true,json:()=>new Promise(()=>{})})});
  await assert.rejects(verify('e','password'),e=>e.code==='unavailable');
});
function adminFixture({index={uid:'u1',status:'active'},profile={usernameLower:'user'},appId='allowed'}={}) {
  const calls=[];
  const adapters=createAdminIdentityAdapters({
    auth:{getUserByEmail:async e=>{calls.push(['email',e]);return {uid:'email-uid'};},getUserByPhoneNumber:async p=>{calls.push(['phone',p]);return {uid:'phone-uid'};},getUser:async uid=>({uid}),createCustomToken:async uid=>'token-'+uid},
    db:{collection:name=>({doc:id=>({get:async()=>{calls.push([name,id]);const data=name==='login_usernames'?index:profile;return {exists:!!data,data:()=>data};}})})},
    appCheck:{verifyToken:async()=>({appId})},allowedAppIds:['allowed'],apiKey:'key',consumeRateLimit:async()=>{},
  });return {adapters,calls};
}
test('resolves email and phone exclusively through Admin Auth',async()=>{
  const {adapters,calls}=adminFixture();
  assert.equal(await adapters.resolveUniqueUid({kind:'phone',value:'+905551234567'}),'phone-uid');
  assert.equal(await adapters.resolveUniqueUid({kind:'email',value:'e@example.com'}),'email-uid');
  assert.deepEqual(calls,[['phone','+905551234567'],['email','e@example.com']]);
});
test('username requires active index and matching current profile',async()=>{
  assert.equal(await adminFixture().adapters.resolveUniqueUid({kind:'username',value:'user'}),'u1');
  for(const options of [{index:null},{index:{uid:'u1',status:'conflict'}},{profile:{usernameLower:'renamed'}}]){
    await assert.rejects(adminFixture(options).adapters.resolveUniqueUid({kind:'username',value:'user'}));
  }
});
test('App Check rejects missing token and unexpected app',async()=>{
  await assert.rejects(adminFixture().adapters.verifyAppCheck({}));
  await assert.rejects(adminFixture({appId:'other'}).adapters.verifyAppCheck({appCheckToken:'token'}));
  await adminFixture().adapters.verifyAppCheck({appCheckToken:'token'});
});
