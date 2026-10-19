// Build524: a retried live comment request never creates two events.
import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,getDoc,getDocs,collection,serverTimestamp,runTransaction} from 'firebase/firestore';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}
});
try{
  await env.clearFirestore();
  await env.withSecurityRulesDisabled(async ctx=>{
    await setDoc(doc(ctx.firestore(),'live_streams/build524'),{ownerId:'host',active:true});
  });
  const user=env.authenticatedContext('viewer524').firestore();
  const other=env.authenticatedContext('stranger524').firestore();
  const event=doc(user,'live_streams/build524/comments/stable524');
  const send=()=>runTransaction(user,async tx=>{
    const snap=await tx.get(event);
    if(snap.exists()){
      const prior=snap.data();
      if(prior.kind!=='comment'||prior.uid!=='viewer524'||
         prior.userId!=='viewer524'||prior.text!=='hello')throw Error('bad retry');
      return 'already';
    }
    tx.set(event,{uid:'viewer524',userId:'viewer524',username:'viewer524',
      kind:'comment',text:'hello',isHost:false,role:'viewer',
      createdAt:serverTimestamp()});
    return 'created';
  },{maxAttempts:4});
  if(await assertSucceeds(send())!=='created')throw Error('first attempt should create');
  if(await assertSucceeds(send())!=='already')throw Error('same event must not create twice');
  const stored=await assertSucceeds(getDoc(event));
  if(stored.data().text!=='hello')throw Error('retry mutated comment');
  const all=await assertSucceeds(getDocs(collection(user,'live_streams/build524/comments')));
  if(all.docs.length!==1)throw Error('one send must count as one comment');
  await assertFails(updateDoc(doc(other,'live_streams/build524/comments/stable524'),{text:'spoof'}));
  await assertFails(setDoc(doc(other,'live_streams/build524/comments/stranger'),{
    uid:'viewer524',userId:'viewer524',text:'spoof',kind:'comment',
    createdAt:serverTimestamp(),
  }));
  await assertSucceeds(setDoc(doc(user,'live_streams/build524/comments/new524'),{
    uid:'viewer524',userId:'viewer524',text:'another intentional comment',
    kind:'comment',createdAt:serverTimestamp(),
  }));
  const refreshed=await assertSucceeds(getDocs(collection(user,'live_streams/build524/comments')));
  if(refreshed.docs.length!==2)throw Error('intentional new comment must have new ID');
  console.log('Build524 FIRESTORE EMULATOR PASS: retry same id, distinct new send, denied spoof');
}finally{await env.cleanup();}
