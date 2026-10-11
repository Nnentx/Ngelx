import fs from 'node:fs';
import assert from 'node:assert/strict';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,getDoc,writeBatch,arrayRemove,deleteField} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
try{
 await env.clearFirestore();
 await env.withSecurityRulesDisabled(async context=>{
  const db=context.firestore();
  await setDoc(doc(db,'users/alice'),{blocked:[],archivedChats:['chat'],mutedChats:['chat'],mutedChatUntil:{chat:'2099-01-01'}});
  await setDoc(doc(db,'users/bob'),{blocked:[]});
  await setDoc(doc(db,'chats/chat'),{isGroup:false,members:['alice','bob'],mutedFor:['alice','bob']});
  await setDoc(doc(db,'group_archives/alice/items/chat'),{chatId:'chat',targetUid:'alice'});
 });
 const db=env.authenticatedContext('alice').firestore();
 const restore=writeBatch(db);
 restore.set(doc(db,'users/alice'),{archivedChats:arrayRemove('chat')},{merge:true});
 restore.delete(doc(db,'group_archives/alice/items/chat'));
 await assertSucceeds(restore.commit());
 assert.deepEqual((await getDoc(doc(db,'users/alice'))).data().archivedChats,[]);
 assert.equal((await getDoc(doc(db,'group_archives/alice/items/chat'))).exists(),false);
 const unmute=writeBatch(db);
 unmute.set(doc(db,'users/alice'),{mutedChats:arrayRemove('chat'),mutedChatUntil:{chat:deleteField()}},{merge:true});
 unmute.set(doc(db,'chats/chat'),{mutedFor:arrayRemove('alice')},{merge:true});
 await assertSucceeds(unmute.commit());
 assert.deepEqual((await getDoc(doc(db,'users/alice'))).data().mutedChats,[]);
 assert.equal((await getDoc(doc(db,'users/alice'))).data().mutedChatUntil?.chat,undefined);
 assert.deepEqual((await getDoc(doc(db,'chats/chat'))).data().mutedFor,['bob']);
 const stranger=env.authenticatedContext('stranger').firestore();
 const forbidden=writeBatch(stranger);
 forbidden.set(doc(stranger,'users/alice'),{archivedChats:[]},{merge:true});
 forbidden.delete(doc(stranger,'group_archives/alice/items/chat'));
 await assertFails(forbidden.commit());
 console.log('Build439: atomic archive restore, both mute records, other-member preservation and outsider denial passed.');
}finally{await env.cleanup();}
