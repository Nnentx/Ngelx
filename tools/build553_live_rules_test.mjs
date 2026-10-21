import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,getDoc,updateDoc,deleteDoc,Timestamp,serverTimestamp,runTransaction} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('live553-candidate.rules','utf8')}});
try{
 await env.clearFirestore();
 await env.withSecurityRulesDisabled(async c=>{
  const db=c.firestore();
  await setDoc(doc(db,'live_streams/live'),{ownerId:'host',active:true,moderatorUids553:['mod'],bannedUsers:[],mutedUsers:[],commentMuteUntil553:{muted:Timestamp.fromMillis(Date.now()+300000),expired:Timestamp.fromMillis(Date.now()-1000)}});
  await setDoc(doc(db,'live_streams/live/comments/message'),{userId:'guest',uid:'guest',kind:'comment',text:'test'});
  await setDoc(doc(db,'live_streams/live/guest_requests/guest'),{liveId:'live',hostUid:'host',guestUid:'guest',status:'accepted',startedBy:'guest',updatedAt:Timestamp.now()});
 });
 const instances=new Map();
 const db=id=>{if(!instances.has(id))instances.set(id,env.authenticatedContext(id).firestore());return instances.get(id);};
 const comment=(id,author)=>doc(db(author),'live_streams/live/comments/'+id);
 const payload=author=>({userId:author,uid:author,kind:'comment',text:'hello',createdAt:serverTimestamp()});
 await assertFails(setDoc(comment('muted','muted'),payload('muted')));
 await assertSucceeds(setDoc(comment('expired','expired'),payload('expired')));
 await assertSucceeds(deleteDoc(doc(db('mod'),'live_streams/live/comments/message')));
 await assertFails(updateDoc(doc(db('guest'),'live_streams/live'),{moderatorUids553:['guest']}));
 await assertFails(updateDoc(doc(db('mod'),'live_streams/live'),{moderatorUids553:['mod','guest']}));
 await assertFails(updateDoc(doc(db('mod'),'live_streams/live'),{ownerId:'mod'}));
 await assertFails(updateDoc(doc(db('mod'),'live_streams/live'),{bannedUsers:['host']}));
 await assertFails(updateDoc(doc(db('mod'),'live_streams/live'),{bannedUsers:['mod']}));
 await assertSucceeds(updateDoc(doc(db('mod'),'live_streams/live'),{bannedUsers:['guest']}));
 await assertFails(setDoc(comment('banned','guest'),payload('guest')));
 await assertFails(updateDoc(doc(db('mod'),'live_streams/live'),{bannedUsers:[]}));
 await assertSucceeds(updateDoc(doc(db('host'),'live_streams/live'),{bannedUsers:[]}));
 for(const [name,points] of [['Aslan',150],['Evren',200],['Galaksi',100]]){
  const ref=comment(name,'guest');
  const gift={...payload('guest'),kind:'gift',giftName:name,giftEmoji:'gift',username:'Guest',quantity:1,points};
  await assertSucceeds(setDoc(ref,gift));
  await assertFails(updateDoc(ref,{points:99999}));
  await assertFails(deleteDoc(doc(db('mod'),'live_streams/live/comments/'+name)));
  await assertFails(setDoc(comment(name+'fake','guest'),{...gift,points:points+1}));
 }
 await assertFails(getDoc(doc(db('host'),'calls/nonexistent')));
 await assertSucceeds(runTransaction(db('host'),async tx=>{
  const own=doc(db('host'),'live_streams/live');await tx.get(own);
  tx.set(doc(db('host'),'calls/new553'),{members:['host','other'],startedBy:'host',type:'live_pk',status:'pending'});
  tx.update(own,{pkInviteStatus:'pending',pkInviteSessionId:'new553'});
 }));
 const gr=doc(db('guest'),'live_streams/live/guest_requests/guest');
 await assertSucceeds(updateDoc(gr,{status:'rejected',updatedAt:serverTimestamp()}));
 await assertSucceeds(updateDoc(gr,{status:'pending',startedBy:'guest',updatedAt:serverTimestamp()}));
 await assertFails(updateDoc(gr,{status:'accepted'}));
 await assertSucceeds(updateDoc(doc(db('host'),'live_streams/live/guest_requests/guest'),{status:'accepted',updatedAt:serverTimestamp()}));
 console.log('Build553: PK creation, guest reapproval, timed comments, role escalation denial, moderator limits, gift integrity PASS');
}finally{await env.cleanup();}
