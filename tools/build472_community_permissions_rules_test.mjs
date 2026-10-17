// Build472 emulator-only permission regression. Production Firestore is NOT touched.
import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,getDoc,Timestamp,serverTimestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({
 projectId:'demo-ngelx',
 firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}
});
try{
 await env.clearFirestore();
 const cid='legacy-472',pid='post-472';
 await env.withSecurityRulesDisabled(async c=>{
   await setDoc(doc(c.firestore(),'communities450',cid),{
    founderId:'founder',members:['founder','admin','member'],admins:['admin'],
    visibility:'public',joinApproval:false,postApproval:false,paused:false,
    name:'Legacy management QA',description:'Verified founder test',rules:'Respect people',
    category:'Sohbet',photoUrl:'',coverUrl:'',lastJoinCode:'',
    createdAt:Timestamp.fromMillis(1730000000000)
   });
   await setDoc(doc(c.firestore(),'communities450',cid,'posts',pid),{
    authorId:'member',authorName:'Member',authorPhoto:'',text:'A post',
    mediaUrl:'',mediaType:'',status:'approved',pinned:false,
    createdAt:Timestamp.fromMillis(1730000000000)
   });
 });
 const founder=env.authenticatedContext('founder').firestore();
 const member=env.authenticatedContext('member').firestore();
 const outsider=env.authenticatedContext('stranger').firestore();
 const post=who=>doc(who,'communities450',cid,'posts',pid);
 const root=who=>doc(who,'communities450',cid);
 await assertSucceeds(updateDoc(post(founder),{commentsClosed:true}));
 await assertSucceeds(updateDoc(post(founder),{slowSeconds:300}));
 await assertSucceeds(updateDoc(post(founder),{pinned:true}));
 await assertFails(updateDoc(post(member),{commentsClosed:false}));
 await assertFails(updateDoc(post(outsider),{slowSeconds:0}));
 await assertSucceeds(updateDoc(root(founder),{postApproval:true}));
 await assertFails(updateDoc(root(member),{postApproval:false}));
 const notify=doc(member,'communities450',cid,'posts',pid,'subscribers456','member');
 await assertSucceeds(setDoc(notify,{uid:'member',enabled:true}));
 await assertSucceeds(getDoc(notify));
 await assertFails(setDoc(doc(outsider,'communities450',cid,'posts',pid,'subscribers456','member'),{uid:'member',enabled:false}));
 const feedback=doc(founder,'communities450',cid,'posts',pid,'feedback456','feedback-1');
 await assertSucceeds(setDoc(feedback,{uid:'founder',text:'Please clarify',createdAt:serverTimestamp()}));
 await assertFails(setDoc(doc(member,'communities450',cid,'posts',pid,'feedback456','feedback-2'),{uid:'member',text:'no moderation',createdAt:serverTimestamp()}));
 console.log('Build472: founder moderation and bounded member subscriptions pass; unauthorized writes denied');
}finally{await env.cleanup();}
