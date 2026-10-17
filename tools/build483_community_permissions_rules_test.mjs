// Build483 Firestore emulator-only rights regression. Never touches live Firebase.
import fs from 'node:fs';
import {initializeTestEnvironment, assertSucceeds, assertFails} from '@firebase/rules-unit-testing';
import {doc, setDoc, updateDoc, deleteDoc, Timestamp, serverTimestamp} from 'firebase/firestore';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}
});
const path='communities450/legacy-483';
const post=path+'/posts/post';
const db=(uid)=>env.authenticatedContext(uid).firestore();
const root=(uid)=>doc(db(uid),path);
const item=(uid)=>doc(db(uid),post);
const community={
  founderId:'founder',
  members:['founder','admin','mod','ordinary'],
  admins:['admin'],moderators:['mod'],
  visibility:'public',joinApproval:false,postApproval:false,paused:false,
  name:'Legacy community',description:'A legacy community',rules:'Be kind',
  category:'Sohbet',photoUrl:'',coverUrl:'',lastJoinCode:'',
  createdAt:Timestamp.fromMillis(1730000000000)
};
try {
  await env.clearFirestore();
  await env.withSecurityRulesDisabled(async c=>{
    await setDoc(doc(c.firestore(),path),community);
    await setDoc(doc(c.firestore(),post),{
      authorId:'ordinary',authorName:'Ordinary',authorPhoto:'',
      text:'Legacy post',mediaUrl:'',mediaType:'',
      status:'approved',pinned:false,createdAt:Timestamp.fromMillis(1730000000000)
    });
  });
  await assertSucceeds(updateDoc(root('founder'),{photoUrl:'https://images.example.com/new.jpg'}));
  await assertSucceeds(updateDoc(root('admin'),{photoUrl:'https://images.example.com/admin.jpg'}));
  await assertFails(updateDoc(root('mod'),{photoUrl:'https://images.example.com/no.jpg'}));
  await assertFails(updateDoc(root('ordinary'),{photoUrl:'https://images.example.com/no.jpg'}));
  await assertFails(updateDoc(root('stranger'),{photoUrl:'https://images.example.com/no.jpg'}));
  await assertFails(updateDoc(root('founder'),{founderId:'stranger'}));
  await assertFails(updateDoc(root('founder'),{photoUrl:90}));
  await assertSucceeds(updateDoc(root('founder'),{admins:['admin','ordinary']}));
  await assertFails(updateDoc(root('admin'),{admins:['admin','mod']}));
  await assertFails(updateDoc(root('founder'),{admins:['stranger']}));
  await assertSucceeds(updateDoc(root('founder'),{moderators:[]}));
  await assertSucceeds(updateDoc(root('founder'),{moderators:['mod']}));
  await assertSucceeds(updateDoc(root('founder'),{muted:['mod']}));
  await assertFails(updateDoc(root('ordinary'),{muted:['founder']}));
  await assertFails(updateDoc(root('founder'),{members:['admin','ordinary']}));
  await assertFails(deleteDoc(root('founder')));
  await assertSucceeds(updateDoc(root('founder'),{postApproval:true}));
  await assertSucceeds(updateDoc(root('founder'),{paused:true}));
  await assertFails(updateDoc(root('ordinary'),{paused:false}));
  await assertSucceeds(updateDoc(root('founder'),{paused:false}));

  // The 456 rules must also authorize post moderation for verified founders.
  await assertSucceeds(updateDoc(item('founder'),{commentsClosed:true}));
  await assertFails(updateDoc(item('ordinary'),{commentsClosed:false}));
  await assertFails(updateDoc(item('stranger'),{slowSeconds:300}));
  const comment={uid:'ordinary',name:'Ordinary',text:'Comment',photoUrl:'',
    replyTo:'',replyName:'',createdAt:serverTimestamp()};
  await assertFails(setDoc(doc(db('ordinary'),post+'/comments/closed'),comment));
  await assertSucceeds(updateDoc(item('founder'),{commentsClosed:false}));
  await assertSucceeds(setDoc(doc(db('ordinary'),post+'/comments/open'),comment));
  await assertSucceeds(updateDoc(item('founder'),{slowSeconds:300}));
  await assertSucceeds(updateDoc(item('founder'),{slowSeconds:0}));
  console.log('Build483 legacy founder/member roles, avatar, moderation and negative permission tests PASS');
} finally { await env.cleanup(); }
