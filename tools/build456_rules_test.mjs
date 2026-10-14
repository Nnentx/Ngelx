import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,getDocs,collection,serverTimestamp,Timestamp,writeBatch} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
const db=(uid)=>env.authenticatedContext(uid).firestore();
const path='communities450/test456',post=path+'/posts/p';
const community={name:'Test community',description:'Test',rules:'',category:'Sohbet',photoUrl:'',coverUrl:'',founderId:'owner',members:['owner','admin','mod','member'],admins:['owner','admin'],moderators:['mod'],visibility:'public',joinApproval:false,postApproval:false,lastJoinCode:'',createdAt:Timestamp.now()};
try{
 await env.clearFirestore();await env.withSecurityRulesDisabled(async c=>{await setDoc(doc(c.firestore(),path),community);await setDoc(doc(c.firestore(),post),{status:'approved',authorId:'member',pinned:false});await setDoc(doc(c.firestore(),post+'/comments/c'),{uid:'member',name:'Member',text:'Hi',createdAt:Timestamp.now()});await setDoc(doc(c.firestore(),post+'/comments/c/reactions/member'),{uid:'member',emoji:'👍',createdAt:Timestamp.now()});});
 await assertSucceeds(getDocs(collection(db('member'),post+'/comments/c/reactions')));
 await assertSucceeds(updateDoc(doc(db('admin'),path),{coverAlignment:.6}));
 await assertFails(updateDoc(doc(db('mod'),path),{coverAlignment:.4}));
 await assertFails(updateDoc(doc(db('member'),path),{admins:['owner','admin','member']}));
 await assertFails(updateDoc(doc(db('admin'),path),{admins:['owner','admin','member']}));
 await assertSucceeds(updateDoc(doc(db('owner'),path),{admins:['owner','admin','member']}));
 await assertFails(updateDoc(doc(db('admin'),path),{muted:['owner']}));
 await assertSucceeds(updateDoc(doc(db('mod'),post),{commentsClosed:true,slowSeconds:300}));
 const comment={uid:'mod',name:'Mod',text:'Comment',photoUrl:'',replyTo:'',replyName:'',createdAt:serverTimestamp()};
 await assertFails(setDoc(doc(db('mod'),post+'/comments/closed'),comment));
 await assertSucceeds(updateDoc(doc(db('mod'),post),{commentsClosed:false}));
 const batch=writeBatch(db('mod'));batch.set(doc(db('mod'),post+'/comments/slow'),comment);batch.set(doc(db('mod'),post+'/commentLimits456/mod'),{uid:'mod',at:serverTimestamp(),commentId:'slow'});await assertSucceeds(batch.commit());
 const fast=writeBatch(db('mod'));fast.set(doc(db('mod'),post+'/comments/too-fast'),comment);fast.set(doc(db('mod'),post+'/commentLimits456/mod'),{uid:'mod',at:serverTimestamp(),commentId:'too-fast'});await assertFails(fast.commit());
 await assertSucceeds(updateDoc(doc(db('admin'),path),{paused:true}));
 await assertFails(setDoc(doc(db('mod'),post+'/comments/paused'),comment));
 await assertFails(updateDoc(doc(db('mod'),path),{paused:false}));
 console.log('Build456 roles, cover permission, reaction query, closed/slow comments and pause passed');
}finally{await env.cleanup();}
