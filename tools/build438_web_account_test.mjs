import fs from 'node:fs';
import assert from 'node:assert/strict';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import * as sdk from 'firebase/firestore';
import {requestAccountDeletion,supportPayload} from '../web/account-actions.mjs';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
try{
  await env.withSecurityRulesDisabled(async(ctx)=>{
    for(const uid of ['web438a','web438b'])await sdk.setDoc(sdk.doc(ctx.firestore(),'users/'+uid),{displayName:uid,deactivated:false});
  });
  const db=env.authenticatedContext('web438a').firestore(),other=env.authenticatedContext('web438b').firestore();
  const now=Date.UTC(2026,9,11),thirtyDays=30*24*60*60*1000;
  const first=await assertSucceeds(requestAccountDeletion(db,sdk,'web438a',now));
  assert.equal(first.alreadyScheduled,false);assert.equal(first.executeAfter.getTime(),now+thirtyDays);
  const profile=await sdk.getDoc(sdk.doc(db,'users/web438a'));
  assert.equal(profile.data().deactivated,true);
  assert.equal(profile.data().deletionScheduledFor.toMillis(),now+thirtyDays);
  const repeat=await requestAccountDeletion(db,sdk,'web438a',now+86400000);
  assert.equal(repeat.alreadyScheduled,true);assert.equal(repeat.executeAfter.getTime(),first.executeAfter.getTime());
  await assertFails(requestAccountDeletion(other,sdk,'web438a',now));
  await assertSucceeds(sdk.updateDoc(sdk.doc(db,'users/web438a'),{deactivated:false,deletionRequestedAt:sdk.deleteField(),deletionScheduledFor:sdk.deleteField()}));
  await assertSucceeds(sdk.updateDoc(sdk.doc(db,'account_deletion_requests/web438a'),{status:'cancelled'}));
  const concurrent=await Promise.all([requestAccountDeletion(db,sdk,'web438a',now+86400000),requestAccountDeletion(db,sdk,'web438a',now+86400000)]);
  assert.deepEqual(concurrent.map(x=>x.alreadyScheduled).sort(),[false,true]);
  for(const result of concurrent)assert.equal(result.executeAfter.getTime(),now+86400000+thirtyDays);
  const payload=supportPayload({uid:'web438a',email:'example@example.test'},'Hesap ve giriş','Giriş sırasında bir hata oluşuyor.',sdk);
  assert.equal('password' in payload,false);
  assert.throws(()=>supportPayload({uid:'web438a'},'Hesap ve giriş','kısa',sdk),/invalid-description/);
  assert.throws(()=>supportPayload({uid:'web438a'},'Unknown','Giriş sırasında bir hata oluşuyor.',sdk),/invalid-description/);
  assert.throws(()=>supportPayload(null,'Diğer','Açıklama yeterince uzun.',sdk),/sign-in-required/);
  const support=sdk.doc(db,'support_requests/web438support');
  await assertSucceeds(sdk.setDoc(support,payload));
  await assertSucceeds(sdk.getDoc(support));
  await assertFails(sdk.getDoc(sdk.doc(other,'support_requests/web438support')));
  await assertFails(sdk.setDoc(support,{...payload,description:'Changed request'}));
  await assertFails(sdk.setDoc(sdk.doc(other,'support_requests/web438spoof'),payload));
  console.log('Web account actions passed: atomic deletion, duplicate deadline preservation, cancelled retry, concurrent requests, owner authorization and support privacy.');
}finally{await env.cleanup();}
