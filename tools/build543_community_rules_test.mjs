import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,deleteDoc,Timestamp,serverTimestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
const data={founderId:'founder',members:['founder','admin','mod','ordinary'],admins:['admin'],moderators:['mod'],visibility:'public',joinApproval:false,postApproval:false,name:'Community543',description:'Test',rules:'Be kind',category:'Sohbet',photoUrl:'',coverUrl:'',lastJoinCode:'',createdAt:Timestamp.fromMillis(1730000000000)};
const path='communities450/lifecycle543';
const db=uid=>env.authenticatedContext(uid).firestore();
try{
 await env.clearFirestore();
 await env.withSecurityRulesDisabled(async c=>{await setDoc(doc(c.firestore(),path),data);});
 for(const uid of ['founder','admin'])await assertSucceeds(updateDoc(doc(db(uid),path),{paused:true}));
 for(const uid of ['mod','ordinary','stranger'])await assertFails(updateDoc(doc(db(uid),path),{paused:false}));
 await assertFails(updateDoc(doc(db('admin'),path),{founderId:'admin'}));
 await assertFails(updateDoc(doc(db('ordinary'),path),{admins:['ordinary'],moderators:[],createdAt:serverTimestamp()}));
 await assertFails(updateDoc(doc(db('founder'),path),{deletion543:{state:'deleting',ownerUid:'founder'}}));
 await assertFails(setDoc(doc(db('founder'),'community_deletions543/lifecycle543'),{ownerUid:'founder'}));
 for(const uid of ['founder','admin','ordinary'])await assertFails(deleteDoc(doc(db(uid),path)));
 await env.withSecurityRulesDisabled(async c=>{await updateDoc(doc(c.firestore(),path),{deletion543:{state:'deleting',ownerUid:'founder'},joinApproval:true});});
 await assertFails(setDoc(doc(db('outsider'),path+'/requests/outsider'),{uid:'outsider',status:'pending',inviteCode:'',createdAt:serverTimestamp()}));
 for(const uid of ['founder','admin'])await assertFails(updateDoc(doc(db(uid),path),{name:'Renamed543'}));
 await assertFails(setDoc(doc(db('ordinary'),path+'/posts/new'),{authorId:'ordinary',authorName:'Ordinary',authorPhoto:'',text:'Cannot race deletion',mediaUrl:'',mediaType:'',status:'approved',pinned:false,createdAt:serverTimestamp()}));
 await env.withSecurityRulesDisabled(async c=>{await setDoc(doc(c.firestore(),'community_deletions543/lifecycle543'),{ownerUid:'founder',state:'deleting'});await deleteDoc(doc(c.firestore(),path));});
 await assertFails(setDoc(doc(db('ordinary'),path),{...data,founderId:'ordinary',members:['ordinary'],admins:['ordinary'],moderators:[],createdAt:serverTimestamp()}));
 console.log('Build543: legacy settings, no escalation, server-only deletion and tombstone race guards passed');
}finally{await env.cleanup();}
