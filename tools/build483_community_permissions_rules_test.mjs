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
const authenticated=new Map();
const db=(uid)=>{if(!authenticated.has(uid))authenticated.set(uid,env.authenticatedContext(uid).firestore());return authenticated.get(uid);};
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
  // Match the production settings toggles exactly: each write changes one
  // community field and must preserve the creator and unrelated fields.
  await assertSucceeds(updateDoc(root('founder'),{visibility:'private'}));
  await assertSucceeds(updateDoc(root('founder'),{joinApproval:true}));
  await assertSucceeds(updateDoc(root('founder'),{postApproval:false}));
  await assertSucceeds(updateDoc(root('founder'),{name:'Legacy updated community'}));
  await assertSucceeds(updateDoc(root('founder'),{description:'Updated description'}));
  await assertSucceeds(updateDoc(root('founder'),{rules:'Updated community rules'}));
  await assertFails(updateDoc(root('ordinary'),{visibility:'public'}));
  await assertFails(updateDoc(root('mod'),{joinApproval:false}));
  await assertFails(updateDoc(root('stranger'),{postApproval:true}));
  // Revert to the original public state for the remaining scenarios.
  await assertSucceeds(updateDoc(root('founder'),{visibility:'public'}));
  await assertSucceeds(updateDoc(root('founder'),{joinApproval:false}));

  // Managers may update the community avatar but must not silently change
  // its banner, owner, security settings or other unrelated fields.
  await assertFails(updateDoc(root('admin'),{
    photoUrl:'https://images.example.com/admin-new.jpg',coverUrl:'https://images.example.com/new-banner.jpg'
  }));

  // Production role change + matching audit event should commit atomically.
  // Admins cannot promote another admin even if they add a matching audit log.
  const adminPromote = writeBatch(db('admin'));
  adminPromote.update(root('admin'),{admins:arrayUnion('mod')});
  adminPromote.set(doc(db('admin'),path+'/audit456/invalid-admin-483'),{
    actor:'admin',target:'mod',action:'admin',createdAt:serverTimestamp(),
  });
  await assertFails(adminPromote.commit());

  // Moderators may close comments on approved posts but not change community
  // membership, founder, or role arrays.
  await assertSucceeds(updateDoc(item('mod'),{commentsClosed:true}));
  await assertSucceeds(updateDoc(item('mod'),{commentsClosed:false}));
  await assertFails(updateDoc(root('mod'),{admins:arrayUnion('mod')}));

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
