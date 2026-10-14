import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,deleteDoc,serverTimestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
const member=env.authenticatedContext('member').firestore(),other=env.authenticatedContext('other').firestore(),guest=env.authenticatedContext('guest').firestore();
const base='communities450/comments455/posts/p';
try {
  await env.clearFirestore();
  await env.withSecurityRulesDisabled(async c=>{
    const db=c.firestore();
    await setDoc(doc(db,'communities450/comments455'),{visibility:'public',members:['member','other'],admins:['member']});
    await setDoc(doc(db,base),{status:'approved',authorId:'member'});
  });
  const comment={uid:'member',name:'Member',text:'Merhaba',photoUrl:'',replyTo:'',replyName:'',createdAt:serverTimestamp()};
  await assertSucceeds(setDoc(doc(member,`${base}/comments/c`),comment));
  await assertSucceeds(setDoc(doc(other,`${base}/comments/reply`),{...comment,uid:'other',name:'Other',replyTo:'c',replyName:'Member'}));
  await assertFails(setDoc(doc(member,`${base}/comments/invalid`),{...comment,replyTo:'missing'}));
  await assertFails(setDoc(doc(guest,`${base}/comments/guest`),{...comment,uid:'guest'}));
  const reaction={uid:'other',emoji:'👍',createdAt:serverTimestamp()};
  const path=`${base}/comments/c/reactions/other`;
  await assertSucceeds(setDoc(doc(other,path),reaction));
  await assertSucceeds(setDoc(doc(other,path),{...reaction,emoji:'😂'}));
  await assertFails(setDoc(doc(member,path),reaction));
  await assertFails(setDoc(doc(other,path),{...reaction,emoji:'invalid'}));
  await assertFails(setDoc(doc(guest,`${base}/comments/c/reactions/guest`),{...reaction,uid:'guest'}));
  await assertFails(deleteDoc(doc(other,`${base}/comments/c`)));
  await assertSucceeds(deleteDoc(doc(other,path)));
  await assertSucceeds(setDoc(doc(other,`${base}/likes/other`),reaction));
  await assertFails(setDoc(doc(member,`${base}/likes/other`),reaction));
  console.log('Build455: replies and reactions enforce membership, ownership and valid targets');
} finally { await env.cleanup(); }
