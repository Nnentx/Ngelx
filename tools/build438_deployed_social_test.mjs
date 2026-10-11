import fs from 'node:fs';
import assert from 'node:assert/strict';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,getDoc,setDoc,runTransaction,serverTimestamp,Timestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
try {
  await env.withSecurityRulesDisabled(async(ctx)=>{
    for(const uid of ['social438a','social438b','social438blocked']){
      await setDoc(doc(ctx.firestore(),'users/'+uid),{blocked:uid==='social438blocked'?['social438a']:[],friends:[],following:[],followers:[],deactivated:false});
    }
  });
  const a=env.authenticatedContext('social438a').firestore();
  const b=env.authenticatedContext('social438b').firestore();
  const outsider=env.authenticatedContext('social438outside').firestore();
  function send(kind,type,target,notificationId){
    const request=doc(a,`${kind}/social438a/outgoing/${target}`);
    const notification=doc(a,'notifications/'+notificationId);
    return runTransaction(a,async(tx)=>{
      const latest=await tx.get(request);
      if(latest.data()?.status==='pending')return false;
      tx.set(request,{fromUid:'social438a',toUid:target,type,status:'pending',notificationId,requestGeneration:'438',createdAt:serverTimestamp(),updatedAt:serverTimestamp()},{merge:true});
      tx.set(notification,{toUid:target,fromUid:'social438a',type,senderName:'Test A',photoUrl:'',text:'Test request',status:'pending',read:false,createdAt:serverTimestamp(),clientCreatedAt:Timestamp.now(),updatedAt:serverTimestamp(),eventKind:type,requestPath:request.path,requestKey:`${type}_social438a_${target}`,requestGeneration:'438'});
      return true;
    });
  }
  for(const [kind,type] of [['follow_requests','follow_request'],['friend_requests','friend_request']]){
    const id='social438-'+type;
    await assertSucceeds(getDoc(doc(a,kind+'/social438a/outgoing/social438b')));
    assert.equal(await assertSucceeds(send(kind,type,'social438b',id)),true);
    const request=await assertSucceeds(getDoc(doc(b,kind+'/social438a/outgoing/social438b')));
    assert.equal(request.data().notificationId,id);
    assert.equal((await assertSucceeds(getDoc(doc(b,'notifications/'+id)))).data().requestGeneration,'438');
    await assertFails(getDoc(doc(outsider,'notifications/'+id)));
    assert.equal(await assertSucceeds(send(kind,type,'social438b',id+'-duplicate')),false);
    await assertFails(send(kind,type,'social438blocked',id+'-blocked'));
    await env.withSecurityRulesDisabled(async(ctx)=>{
      assert.equal((await getDoc(doc(ctx.firestore(),'notifications/'+id+'-duplicate'))).exists(),false);
      assert.equal((await getDoc(doc(ctx.firestore(),'notifications/'+id+'-blocked'))).exists(),false);
    });
  }
  console.log('Active deployed social rules: atomic request + notification, recipient access, duplicate prevention and blocked-pair rollback passed. Phone delivery and provider quotas remain separate.');
} finally { await env.cleanup(); }
