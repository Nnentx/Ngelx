// Build521 isolated Firebase emulator: no production money/coin writes.
import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,getDoc,getDocs,collection,serverTimestamp,runTransaction} from 'firebase/firestore';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')},
});
const id='b521-stable-request-id';
try{
  await env.clearFirestore();
  await env.withSecurityRulesDisabled(async c=>{
    await setDoc(doc(c.firestore(),'live_streams/g521'),{ownerId:'host',active:true});
  });
  const guest=env.authenticatedContext('guest').firestore();
  const stranger=env.authenticatedContext('stranger').firestore();
  const gift=doc(guest,'live_streams/g521/comments/'+id);
  const payload={uid:'guest',userId:'guest',username:'Tester',text:'🌹 Gül ×5',
    kind:'gift',giftName:'Gül',giftEmoji:'🌹',quantity:5,points:5,
    createdAt:serverTimestamp()};
  const send=async ()=>{
    return runTransaction(guest,async tx=>{
      const current=await tx.get(gift);
      if(current.exists()){
        const data=current.data();
        if(data.kind!=='gift'||data.uid!=='guest'||data.giftName!=='Gül'||
          data.quantity!==5||data.points!==5)throw Error('request mismatch');
        return 'already';
      }
      tx.set(gift,payload);
      return 'created';
    },{maxAttempts:4});
  };
  const first=await assertSucceeds(send());
  if(first!=='created')throw Error('The first event should create exactly once');
  const second=await assertSucceeds(send());
  if(second!=='already')throw Error('Same id must not create a second gift');
  const current=await assertSucceeds(getDoc(gift));
  if(current.data().quantity!==5||current.data().points!==5)
    throw Error('Retry changed authoritative gift payload');
  const all=await assertSucceeds(getDocs(collection(guest,'live_streams/g521/comments')));
  if(all.docs.length!==1)throw Error('A retried request must count as exactly one gift event');
  await assertFails(updateDoc(gift,{quantity:10,points:10}));
  await assertFails(setDoc(doc(stranger,'live_streams/g521/comments/'+id),payload));
  // Distinct confirmed send is a distinct user intention with a new ID.
  await assertSucceeds(setDoc(doc(guest,'live_streams/g521/comments/b521-next-send'),payload));
  const actual=await assertSucceeds(getDocs(collection(guest,'live_streams/g521/comments')));
  if(actual.docs.length!==2)throw Error('New intentional send must remain distinct');
  console.log('Build521 EMULATOR PASS: same stable event ID retried without duplicate or mutation');
  console.log('Build521 EMULATOR PASS: spoof denied, new intentional event counted separately');
}finally{await env.cleanup();}
