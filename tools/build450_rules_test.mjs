import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,getDoc,getDocs,collection,query,where,arrayUnion,arrayRemove,serverTimestamp,Timestamp,writeBatch,deleteDoc,runTransaction} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
const owner=env.authenticatedContext('owner').firestore(),member=env.authenticatedContext('member').firestore(),stranger=env.authenticatedContext('stranger').firestore();
const community=(extra={})=>({name:'Doğa sohbeti',description:'Doğa tutkunları',rules:'Saygılı paylaş',category:'Sohbet',photoUrl:'',coverUrl:'',founderId:'owner',members:['owner'],admins:['owner'],visibility:'public',joinApproval:false,postApproval:true,lastJoinCode:'',createdAt:serverTimestamp(),...extra});
const post=(extra={})=>({authorId:'member',authorName:'Member',authorPhoto:'',text:'Merhaba',mediaUrl:'',mediaType:'',status:'pending',pinned:false,createdAt:serverTimestamp(),...extra});
try{
 await env.clearFirestore();
 await assertSucceeds(setDoc(doc(owner,'communities450/public'),community()));
 await assertFails(setDoc(doc(stranger,'communities450/rogue'),community()));
 await assertFails(updateDoc(doc(stranger,'communities450/public'),{admins:arrayUnion('stranger')}));
 await assertSucceeds(getDocs(query(collection(stranger,'communities450'),where('visibility','==','public'))));
 await assertSucceeds(updateDoc(doc(member,'communities450/public'),{members:arrayUnion('member'),lastJoinCode:''}));
 await assertFails(updateDoc(doc(member,'communities450/public'),{admins:arrayUnion('member')}));
 await assertFails(setDoc(doc(stranger,'communities450/public/posts/outsider'),post({authorId:'stranger'})));
 await assertSucceeds(setDoc(doc(member,'communities450/public/posts/p'),post()));
 await assertFails(setDoc(doc(member,'communities450/public/posts/bypass'),post({status:'approved'})));
 await assertFails(getDoc(doc(stranger,'communities450/public/posts/p')));
 await assertSucceeds(getDoc(doc(owner,'communities450/public/posts/p')));
 await assertSucceeds(updateDoc(doc(owner,'communities450/public/posts/p'),{status:'approved'}));
 await assertSucceeds(getDoc(doc(stranger,'communities450/public/posts/p')));
 await assertSucceeds(setDoc(doc(member,'communities450/public/posts/p/likes/member'),{uid:'member',createdAt:serverTimestamp()}));
 await assertFails(setDoc(doc(stranger,'communities450/public/posts/p/likes/member'),{uid:'member',createdAt:serverTimestamp()}));
 await assertSucceeds(setDoc(doc(member,'communities450/public/posts/p/comments/c'),{uid:'member',name:'Member',text:'Güzel',createdAt:serverTimestamp()}));
 await assertFails(setDoc(doc(stranger,'communities450/public/posts/p/comments/evil'),{uid:'stranger',name:'S',text:'X',createdAt:serverTimestamp()}));
 await assertFails(updateDoc(doc(member,'communities450/public/posts/p'),{pinned:true}));
 await assertSucceeds(updateDoc(doc(owner,'communities450/public/posts/p'),{pinned:true}));
 await assertSucceeds(setDoc(doc(member,'communities450/public/reports/p_member'),{uid:'member',postId:'p',status:'open',createdAt:serverTimestamp()}));
 await assertFails(getDocs(collection(member,'communities450/public/reports')));
 await assertSucceeds(getDocs(collection(owner,'communities450/public/reports')));
 await assertSucceeds(setDoc(doc(owner,'communities450/private'),community({visibility:'private',joinApproval:true})));
 await assertFails(getDoc(doc(stranger,'communities450/private')));
 await assertFails(setDoc(doc(stranger,'communities450/private/requests/stranger'),{uid:'stranger',status:'pending',inviteCode:'wrong',createdAt:serverTimestamp()}));
 await assertSucceeds(setDoc(doc(owner,'communityInvites450/secure-invite'),{communityId:'private',name:'Doğa sohbeti',joinApproval:true,createdBy:'owner',expiresAt:Timestamp.fromMillis(Date.now()+3600000)}));
 await assertSucceeds(getDoc(doc(stranger,'communityInvites450/secure-invite')));
 await assertFails(getDocs(collection(stranger,'communityInvites450')));
 await assertSucceeds(setDoc(doc(stranger,'communities450/private/requests/stranger'),{uid:'stranger',status:'pending',inviteCode:'secure-invite',createdAt:serverTimestamp()}));
 await assertFails(updateDoc(doc(stranger,'communities450/private'),{members:arrayUnion('stranger'),lastJoinCode:'secure-invite'}));
 await assertFails(updateDoc(doc(stranger,'communities450/private/requests/stranger'),{status:'approved'}));
 const batch=writeBatch(owner);batch.update(doc(owner,'communities450/private'),{members:arrayUnion('stranger')});batch.update(doc(owner,'communities450/private/requests/stranger'),{status:'approved'});await assertSucceeds(batch.commit());
 await assertSucceeds(getDoc(doc(stranger,'communities450/private')));
 await assertSucceeds(updateDoc(doc(stranger,'communities450/private'),{members:arrayRemove('stranger'),admins:arrayRemove('stranger')}));
 await assertFails(getDoc(doc(stranger,'communities450/private')));
 await assertFails(updateDoc(doc(owner,'communities450/public'),{members:arrayRemove('owner')}));
 await assertFails(updateDoc(doc(member,'communities450/public'),{founderId:'member'}));
 await assertSucceeds(updateDoc(doc(owner,'communities450/public'),{admins:arrayUnion('member')}));
 await assertFails(updateDoc(doc(member,'communities450/public'),{admins:arrayRemove('owner')}));
 await assertSucceeds(updateDoc(doc(member,'communities450/public'),{members:arrayRemove('member'),admins:arrayRemove('member')}));
 await assertFails(setDoc(doc(member,'communities450/public/posts/late'),post()));

 await assertSucceeds(setDoc(doc(owner,'communities450/bulk451'),community({joinApproval:true})));
 for(const uid of ['member','stranger']){
  const db=uid==='member'?member:stranger;
  await assertSucceeds(setDoc(doc(db,`communities450/bulk451/requests/${uid}`),{uid,status:'pending',inviteCode:'',createdAt:serverTimestamp()}));
 }
 await assertFails(updateDoc(doc(member,'communities450/bulk451/requests/member'),{status:'approved'}));
 await assertSucceeds(runTransaction(owner,async tx=>{
  const root=doc(owner,'communities450/bulk451');await tx.get(root);
  const refs=['member','stranger'].map(uid=>doc(owner,`communities450/bulk451/requests/${uid}`));
  for(const ref of refs)await tx.get(ref);
  tx.update(root,{members:arrayUnion('member','stranger')});
  for(const ref of refs)tx.update(ref,{status:'approved'});
 }));
 for(const uid of ['member','stranger']){
  const result=await getDoc(doc(owner,`communities450/bulk451/requests/${uid}`));
  if(result.data().status!=='approved')throw new Error('Bulk approval did not commit');
 }
 console.log('Build450: community privacy, membership approval, post moderation, reactions, reports and immutable owner checks passed');
}finally{await env.cleanup();}
