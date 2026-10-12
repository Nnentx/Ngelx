import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,getDoc,getDocs,collection,updateDoc,runTransaction,serverTimestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
try{
 await env.clearFirestore();
 await env.withSecurityRulesDisabled(async ctx=>{await setDoc(doc(ctx.firestore(),'chats/member447'),{isGroup:true,members:['owner','member'],admins:['owner'],createdBy:'owner'});});
 const owner=env.authenticatedContext('owner').firestore(),member=env.authenticatedContext('member').firestore(),outside=env.authenticatedContext('outsider').firestore();
 const payload={type:'member_add',uid:'target',targetUid:'target',targetName:'Target',targetPhoto:'',requestedBy:'member',requestedByName:'Member',requestedByPhoto:'',status:'pending',createdAt:serverTimestamp(),updatedAt:serverTimestamp()};
 const ref=doc(member,'chats/member447/joinRequests/target');
 await assertSucceeds(runTransaction(member,async tx=>{const group=await tx.get(doc(member,'chats/member447'));const previous=await tx.get(ref);if(!previous.exists())tx.set(ref,payload);}));
 await assertFails(updateDoc(ref,{status:'accepted'}));
 await assertFails(getDocs(collection(member,'chats/member447/joinRequests')));
 await assertSucceeds(getDocs(collection(owner,'chats/member447/joinRequests')));
 await assertFails(getDoc(doc(outside,'chats/member447/joinRequests/target')));
 await assertSucceeds(updateDoc(doc(owner,'chats/member447/joinRequests/target'),{status:'rejected'}));
 await assertSucceeds(setDoc(ref,payload));
 console.log('Normal member requests require admin approval; existing list privacy retained');
}finally{await env.cleanup();}
