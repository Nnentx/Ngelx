import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,deleteDoc,serverTimestamp} from 'firebase/firestore';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}
});
try {
  await env.clearFirestore();
  await env.withSecurityRulesDisabled(async ctx=>{
    const db=ctx.firestore();
    await setDoc(doc(db,'live_streams/g511'),{ownerId:'host',active:true});
    await setDoc(doc(db,'live_streams/ended511'),{ownerId:'host',active:false});
  });
  const guest=env.authenticatedContext('guest').firestore();
  const thief=env.authenticatedContext('thief').firestore();
  const unauth=env.unauthenticatedContext().firestore();
  const payload=(over={})=>({
    uid:'guest',userId:'guest',username:'Viewer',text:'🌹 Gül ×5',
    kind:'gift',giftName:'Gül',giftEmoji:'🌹',
    quantity:5,points:5,createdAt:serverTimestamp(),...over
  });
  const gift=id=>doc(guest,'live_streams/g511/comments/'+id);
  await assertSucceeds(setDoc(gift('valid5'),payload()));
  await assertSucceeds(setDoc(gift('valid10'),payload({quantity:10,points:10})));
  await assertSucceeds(setDoc(gift('validOne'),payload({quantity:1,points:1})));
  await assertSucceeds(setDoc(gift('diamond'),payload({quantity:2,points:30,giftName:'Elmas',giftEmoji:'💎'})));
  await assertFails(setDoc(gift('none'),payload({quantity:0,points:0})));
  await assertFails(setDoc(gift('tooMany'),payload({quantity:11,points:11})));
  await assertFails(setDoc(gift('spoofPoints'),payload({quantity:3,points:9000})));
  await assertFails(setDoc(gift('spoofOwner'),payload({uid:'host',userId:'host'})));
  await assertFails(setDoc(gift('unknownGift'),payload({giftName:'Fake'})));
  await assertFails(setDoc(doc(thief,'live_streams/g511/comments/thief'),payload()));
  await assertFails(setDoc(doc(unauth,'live_streams/g511/comments/guest'),payload()));
  await assertFails(setDoc(doc(guest,'live_streams/ended511/comments/late'),payload()));
  await assertFails(updateDoc(gift('valid5'),{points:999}));
  await assertFails(deleteDoc(gift('valid5')));
  await assertFails(setDoc(gift('valid5'),payload({quantity:6,points:6})));
  await assertSucceeds(setDoc(gift('regularComment'),{
    uid:'guest',userId:'guest',kind:'comment',text:'Merhaba',
    createdAt:serverTimestamp()
  }));
  await assertSucceeds(deleteDoc(gift('regularComment')));
  console.log('Build511 PASS: gift quantity bounds, price catalog, owner, immutability, ended room and ordinary comments');
} finally {
  await env.cleanup();
}
