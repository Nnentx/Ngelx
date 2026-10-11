import fs from 'node:fs';
import assert from 'node:assert/strict';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,getDoc,getDocs,query,collection,where,limit,writeBatch,arrayUnion,arrayRemove,Timestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
try{
 await env.clearFirestore();
 await env.withSecurityRulesDisabled(async c=>{
  const db=c.firestore();
  await setDoc(doc(db,'users/alice'),{blocked:[],archivedChats:['old','missing','ordinary']});
  await setDoc(doc(db,'users/bob'),{blocked:[]});
  await setDoc(doc(db,'chats/old'),{members:['bob'],isGroup:false});
  await setDoc(doc(db,'chats/ordinary'),{members:['alice','bob'],isGroup:false});
  await setDoc(doc(db,'group_archives/alice/items/old'),{chatId:'old',groupName:'Old group'});
  const batch=writeBatch(db);
  for(let i=0;i<101;i++)batch.set(doc(db,'videos/aaa'+String(i).padStart(3,'0')),{ownerId:'alice',type:'story',highlighted:false,createdAt:Timestamp.fromMillis(1),expiresAt:Timestamp.fromMillis(2)});
  batch.set(doc(db,'videos/zzzFresh'),{ownerId:'alice',type:'story',highlighted:true,createdAt:Timestamp.now(),expiresAt:Timestamp.fromMillis(Date.now()+86400000)});
  await batch.commit();
 });
 const db=env.authenticatedContext('alice').firestore();
 await assertFails(getDoc(doc(db,'chats/old')));
 const dismiss=writeBatch(db);
 dismiss.set(doc(db,'users/alice'),{archivedChats:arrayRemove('old','missing'),dismissedArchiveChats:arrayUnion('old','missing')},{merge:true});
 dismiss.delete(doc(db,'group_archives/alice/items/old'));
 await assertSucceeds(dismiss.commit());
 assert.deepEqual((await getDoc(doc(db,'users/alice'))).data().archivedChats,['ordinary']);
 assert.deepEqual((await getDoc(doc(db,'users/alice'))).data().dismissedArchiveChats,['old','missing']);
 await assertFails(setDoc(doc(db,'chats/old'),{hiddenFor:arrayUnion('alice')},{merge:true}));
 const outsider=env.authenticatedContext('bob').firestore();
 await assertFails(setDoc(doc(outsider,'users/alice'),{dismissedArchiveChats:['ordinary']},{merge:true}));
 const highlights=await assertSucceeds(getDocs(query(collection(db,'videos'),where('ownerId','==','alice'),where('highlighted','==',true),limit(30))));
 assert.equal(highlights.size,1);assert.equal(highlights.docs[0].id,'zzzFresh');
 await assertSucceeds(setDoc(doc(db,'videos/zzzFresh'),{highlighted:false},{merge:true}));
 assert.equal((await getDocs(query(collection(db,'videos'),where('ownerId','==','alice'),where('highlighted','==',true),limit(30)))).size,0);
 console.log('Build441 own archive dismissal, inaccessible chat isolation, outsider denial and >100-story highlight tests passed.');
}finally{await env.cleanup();}
