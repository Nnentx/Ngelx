import fs from 'node:fs';
import assert from 'node:assert/strict';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,getDoc,runTransaction,arrayUnion,arrayRemove,serverTimestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
try{
 await env.clearFirestore();
 await env.withSecurityRulesDisabled(async context=>{
  const db=context.firestore();
  await setDoc(doc(db,'users/alice'),{blocked:[],pinnedChats:['rojin'],pinnedChatAt:{rojin:1}});
  await setDoc(doc(db,'users/bob'),{blocked:[]});
  await setDoc(doc(db,'chats/group'),{isGroup:true,members:['alice','bob'],admins:['alice'],createdBy:'alice',callRoomName:'group_first',callStartedBy:'alice',callStatus:'ringing',callVideo:true,callMessageId:'first',callParticipants:['alice']});
  await setDoc(doc(db,'chats/group/messages/first'),{senderId:'alice',type:'call',callRoomName:'group_first',callStatus:'ringing',callVideo:true});
 });
 const alice=env.authenticatedContext('alice').firestore(),bob=env.authenticatedContext('bob').firestore();
 await assertSucceeds(setDoc(doc(alice,'users/alice'),{pinnedChats:arrayUnion('selma'),pinnedChatAt:{selma:2}},{merge:true}));
 const prefs=(await getDoc(doc(alice,'users/alice'))).data();
 assert.deepEqual(prefs.pinnedChats,['rojin','selma']);assert.deepEqual(prefs.pinnedChatAt,{rojin:1,selma:2});
 const chat=doc(alice,'chats/group');
 const settle=(db,room,uid)=>runTransaction(db,async tx=>{
  const ref=doc(db,'chats/group'),latest=await tx.get(ref),data=latest.data();
  if(data.callRoomName!==room)return false;
  tx.set(ref,{callStatus:'missed',callVideo:true,callEndedAt:serverTimestamp(),callParticipants:arrayRemove(uid)},{merge:true});
  if(data.callStartedBy===uid)tx.set(doc(db,'chats/group/messages/'+data.callMessageId),{callStatus:'missed',callVideo:true,callEndedAt:serverTimestamp(),durationSeconds:0},{merge:true});
  return true;
 });
 await assertSucceeds(settle(alice,'group_first','alice'));
 assert.equal((await getDoc(chat)).data().callStatus,'missed');
 assert.equal((await getDoc(doc(alice,'chats/group/messages/first'))).data().callVideo,true);
 assert.equal((await getDoc(doc(alice,'chats/group/messages/first'))).data().callStatus,'missed');
 await setDoc(chat,{callRoomName:'group_new',callStatus:'active',callMessageId:'new',callParticipants:['bob']},{merge:true});
 assert.equal(await settle(alice,'group_first','alice'),false);
 assert.equal((await getDoc(chat)).data().callStatus,'active');
 await assertSucceeds(settle(bob,'group_new','bob'));
 assert.equal((await getDoc(chat)).data().callStatus,'missed');
 await assertFails(settle(env.authenticatedContext('outside').firestore(),'group_new','outside'));
 console.log('Build440 durable pin metadata, video-call settlement, stale-room guard, last-member closure and outsider denial passed.');
}finally{await env.cleanup();}
