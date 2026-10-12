import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,getDoc,writeBatch,updateDoc,arrayUnion,serverTimestamp,Timestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
try {
 await env.clearFirestore();
 await env.withSecurityRulesDisabled(async ctx=>{
  const db=ctx.firestore();
  await setDoc(doc(db,'chats/group446'),{isGroup:true,members:['owner','admin','member'],admins:['owner','admin'],createdBy:'owner',callRoomName:'group_446',callParticipants:['owner','admin','member']});
  await setDoc(doc(db,'videos/story446'),{type:'story',ownerId:'owner',mediaUrl:'https://media.ngelxsocial.com/media/stories/owner/446.jpg'});
 });
 const owner=env.authenticatedContext('owner').firestore(),admin=env.authenticatedContext('admin').firestore(),member=env.authenticatedContext('member').firestore();
 await assertSucceeds(updateDoc(doc(admin,'chats/group446'),{callModerationRoom:'group_446',callMutedUids:arrayUnion('member')}));
 await assertFails(updateDoc(doc(member,'chats/group446'),{callMutedUids:[]}));
 await assertFails(updateDoc(doc(member,'chats/group446'),{callKickedUids:['owner']}));
 await assertSucceeds(updateDoc(doc(owner,'chats/group446'),{callModerationRoom:'group_446',callKickedUids:['member'],callParticipants:['owner','admin']}));
 const story=doc(owner,'videos/story446'),job=doc(owner,'_media_cleanup435/story_story446');
 const payload={sourcePath:'videos/story446',storyId:'story446',kind:'story',ownerId:'owner',urls:['https://media.ngelxsocial.com/media/stories/owner/446.jpg','','','','','','',''],createdAt:serverTimestamp(),lastAttemptAt:Timestamp.fromMillis(0)};
 await assertFails(setDoc(job,payload)); // Cleanup cannot target a story still visible.
 const attack=writeBatch(member);attack.set(doc(member,'_media_cleanup435/story_story446'),payload);attack.delete(doc(member,'videos/story446'));
 await assertFails(attack.commit());
 const forged=writeBatch(owner);forged.set(job,{...payload,urls:['https://media.ngelxsocial.com/media/stories/member/other.jpg','','','','','','','']});forged.delete(story);
 await assertFails(forged.commit());
 const batch=writeBatch(owner);batch.set(job,payload);batch.delete(story);
 await assertSucceeds(batch.commit());
 await assertFails(getDoc(job));
 console.log('Build446 moderation and atomic owned-story cleanup tests passed');
} finally { await env.cleanup(); }
