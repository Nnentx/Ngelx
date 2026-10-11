import assert from 'node:assert/strict';
import {initializeApp,deleteApp} from 'firebase-admin/app';
import {getFirestore} from 'firebase-admin/firestore';
import {createFirestoreRateLimiter} from '../rate-limit.mjs';
import {claimUsername} from '../username-ownership.mjs';

// Never run this fixture against production, even with inherited credentials.
if (!/^127\.0\.0\.1:\d+$/.test(process.env.FIRESTORE_EMULATOR_HOST || '')) {
  throw Error('Local Firestore emulator required');
}
const app=initializeApp({projectId:'demo-ngelx-auth'});
const db=getFirestore(app);
try {
  let instant=100000;
  const consume=createFirestoreRateLimiter({db,secret:'test-only-secret-'.repeat(3),
    now:()=>instant,identifierLimit:5,networkLimit:30});
  const identifier={kind:'username',value:'concurrent'};
  const attempts=await Promise.allSettled(Array.from({length:20},(_,i)=>
    consume(identifier,{trustedRemoteAddress:'192.0.2.'+(i+1)})));
  assert.equal(attempts.filter(r=>r.status==='fulfilled').length,5);
  for (const result of attempts.filter(r=>r.status==='rejected')) {
    assert.equal(result.reason.code,'too-many-requests');
  }
  const docs=await db.collection('login_attempt_limits').get();
  assert.equal(docs.size,6); // One shared identifier and five permitted networks.
  assert.equal(docs.docs.find(d=>d.id.startsWith('identifier-')).data().count,5);
  for(const doc of docs.docs){
    assert.ok(!JSON.stringify(doc.data()).includes('concurrent'));
    assert.deepEqual(Object.keys(doc.data()).sort(),['count','expiresAt','startedAtMs']);
  }
  instant=160000;
  await consume(identifier,{trustedRemoteAddress:'192.0.2.1'});
  const networkConsume=createFirestoreRateLimiter({db,secret:'different-test-secret-'.repeat(3),
    now:()=>instant,identifierLimit:5,networkLimit:3});
  const networkResults=await Promise.allSettled(Array.from({length:10},(_,i)=>
    networkConsume({kind:'username',value:'network'+i},{trustedRemoteAddress:'198.51.100.1'})));
  assert.equal(networkResults.filter(r=>r.status==='fulfilled').length,3);
  assert.ok(networkResults.filter(r=>r.status==='rejected').every(r=>r.reason.code==='too-many-requests'));
  console.log('Firestore limiter passed: simultaneous attempts, atomic counters, shared network limit, expiry and record privacy.');
  for(let i=0;i<10;i++)await db.collection('users').doc('claim'+i).set({displayName:'Preserved '+i});
  const claims=await Promise.allSettled(Array.from({length:10},(_,i)=>claimUsername(db,'claim'+i,'Race.Name')));
  assert.equal(claims.filter(r=>r.status==='fulfilled').length,1);
  assert.ok(claims.filter(r=>r.status==='rejected').every(r=>r.reason.code==='username-taken'));
  const owner=(await db.collection('login_usernames').doc('race.name').get()).data().uid;
  const ownerProfile=(await db.collection('users').doc(owner).get()).data();
  assert.equal(ownerProfile.usernameLower,'race.name');
  assert.equal(ownerProfile.displayName,'Preserved '+owner.slice(5));
  await claimUsername(db,owner,'Race.Name'); // Same-owner retry is idempotent.
  await claimUsername(db,owner,'Renamed.User');
  assert.equal((await db.collection('login_usernames').doc('race.name').get()).data().status,'retired');
  await assert.rejects(claimUsername(db,'claim9'===owner?'claim8':'claim9','Race.Name'),e=>e.code==='username-taken');
  await db.collection('users').doc('legacy').set({usernameLower:'legacy.name'});
  await assert.rejects(claimUsername(db,'claim0','legacy.name'),e=>e.code==='username-taken');
  await claimUsername(db,'legacy','legacy.name');
  await db.collection('users').doc('duplicate1').set({usernameLower:'duplicate'});
  await db.collection('users').doc('duplicate2').set({usernameLower:'duplicate'});
  await assert.rejects(claimUsername(db,'duplicate1','duplicate'),e=>e.code==='username-taken');
  assert.equal((await db.collection('login_usernames').doc('duplicate').get()).exists,false);
  await assert.rejects(claimUsername(db,'missing-profile','missing.name'),e=>e.code==='profile-required');
  console.log('Username ownership passed: concurrent single owner, retry, atomic rename, retired name, legacy protection and duplicate rejection.');
} finally {
  await db.terminate();await deleteApp(app);
}
