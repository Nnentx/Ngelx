// Build483 Firestore emulator-only rights regression. Never touches live Firebase.
import fs from 'node:fs';
import {initializeTestEnvironment, assertSucceeds, assertFails} from '@firebase/rules-unit-testing';
import {doc, setDoc, updateDoc, deleteDoc, Timestamp, serverTimestamp, writeBatch, arrayRemove, arrayUnion} from 'firebase/firestore';

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
  // Restore ordinary-member role after the legitimate promotion scenario.
  await assertSucceeds(updateDoc(root('founder'),{admins:['admin']}));
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
  // Real member management writes a community update AND an audit log
  // atomically. A permission rule for only one of these writes is insufficient.
  const auditedFounder = writeBatch(db('founder'));
  auditedFounder.update(root('founder'), {
    'moderators': arrayRemove('mod'),
  });
  auditedFounder.set(doc(db('founder'),path+'/audit456/role-483'), {
    actor:'founder',target:'mod',action:'moderator',
    createdAt:serverTimestamp(),
  });
  await assertSucceeds(auditedFounder.commit());

  // An ordinary member must never be able to manipulate roles by pairing
  // their write with a forged audit record in a batch.
  const forged = writeBatch(db('ordinary'));
  forged.update(root('ordinary'), {
    'admins': arrayUnion('ordinary'),
  });
  forged.set(doc(db('ordinary'),path+'/audit456/forged-483'), {
    actor:'founder',target:'ordinary',action:'admin',
    createdAt:serverTimestamp(),
  });
  await assertFails(forged.commit());

  // A verified founder may revoke membership and ban that member, with an
  // audit record, without accidentally changing the cover or other settings.
  const auditedBan = writeBatch(db('founder'));
  auditedBan.update(root('founder'), {
    members:arrayRemove('ordinary'),
    admins:arrayRemove('ordinary'),
    moderators:arrayRemove('ordinary'),
    muted:arrayRemove('ordinary'),
    banned:arrayUnion('ordinary'),
  });
  auditedBan.set(doc(db('founder'),path+'/audit456/ban-483'), {
    actor:'founder',target:'ordinary',action:'ban',
    createdAt:serverTimestamp(),
  });
  await assertSucceeds(auditedBan.commit());
  await assertFails(updateDoc(root('ordinary'),{photoUrl:'https://images.example.com/unauthorized.jpg'}));
  await assertFails(updateDoc(root('ordinary'),{admins:['admin','ordinary']}));

  console.log('Build483 legacy founder/member roles, avatar, moderation and negative permission tests PASS');
} finally { await env.cleanup(); }
