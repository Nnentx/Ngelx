// Local emulator only. No production credentials or database writes.
import fs from 'node:fs';
import {initializeTestEnvironment,assertFails,assertSucceeds} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,serverTimestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
try{
  const urls=['https://media.ngelxsocial.com/media/chats/alice/one.jpg','https://media.ngelxsocial.com/media/chats/alice/two.jpg'];
  const path='chats/album558/messages/album';
  await env.withSecurityRulesDisabled(async ctx=>{
    await setDoc(doc(ctx.firestore(),'chats/album558'),{members:['alice','bob','admin'],admins:['admin'],createdBy:'admin',isGroup:true});
    await setDoc(doc(ctx.firestore(),path),{senderId:'alice',type:'photo',mediaUrl:urls[0],albumItems558:urls.map(url=>({url,type:'photo'})),mediaUrls:urls,text:''});
  });
  const db=uid=>env.authenticatedContext(uid).firestore();
  const deletion={deletedForEveryone:true,deletedBy:'alice',deletedAt:serverTimestamp(),mediaUrl:'',albumItems558:[],mediaUrls:[],cleanupMediaUrls:[urls[0],'','','','','','','',...urls],mediaCleanupState:'pending'};
  await assertFails(updateDoc(doc(db('outsider'),path),deletion));
  await assertFails(updateDoc(doc(db('bob'),path),deletion));
  await assertFails(updateDoc(doc(db('alice'),path),{...deletion,cleanupMediaUrls:['https://media.ngelxsocial.com/media/chats/bob/other.jpg']}));
  await assertFails(updateDoc(doc(db('alice'),path),{...deletion,albumItems558:[{url:urls[1],type:'photo'}]}));
  await assertSucceeds(updateDoc(doc(db('admin'),path),{...deletion,deletedBy:'admin'}));
  await assertFails(updateDoc(doc(db('alice'),path),{deletedForEveryone:true,cleanupMediaUrls:['other'],mediaCleanupState:'pending'}));
  await env.withSecurityRulesDisabled(async ctx=>{
    await setDoc(doc(ctx.firestore(),path),{senderId:'alice',type:'photo',mediaUrl:urls[0],albumItems558:urls.map(url=>({url,type:'photo'})),mediaUrls:urls,text:''});
  });
  await assertSucceeds(updateDoc(doc(db('alice'),path),deletion));
  console.log('Build558 album deletion: sender/admin boundary and exact manifest checks passed');
}finally{await env.cleanup();}
