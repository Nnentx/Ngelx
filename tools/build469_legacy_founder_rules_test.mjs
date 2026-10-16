// Build469: Firestore emulator-only regression for legacy community founder.
// Never run on a live project. No production user data is touched.
import fs from 'node:fs';
import { initializeTestEnvironment, assertSucceeds, assertFails } from '@firebase/rules-unit-testing';
import { doc, setDoc, updateDoc, deleteDoc, Timestamp } from 'firebase/firestore';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}
});
try {
  await env.clearFirestore();
  const id='communities450/legacy-verified-founder';
  const legacy={
    founderId:'founder', members:['founder','admin','ordinary'],admins:['admin'],
    visibility:'public',joinApproval:false,postApproval:false,paused:false,
    name:'Legacy founder sample',description:'test',rules:'be respectful',
    category:'Sohbet',photoUrl:'',coverUrl:'',lastJoinCode:'',
    createdAt:Timestamp.fromMillis(1730000000000)
  };
  await env.withSecurityRulesDisabled(async ctx=>{
    await setDoc(doc(ctx.firestore(),id),legacy);
  });
  const founder=env.authenticatedContext('founder').firestore();
  const member=env.authenticatedContext('ordinary').firestore();
  const admin=env.authenticatedContext('admin').firestore();
  const outsider=env.authenticatedContext('stranger').firestore();
  // Only the original verified founder may repair legacy settings.
  await assertSucceeds(updateDoc(doc(founder,id),{postApproval:true}));
  await assertSucceeds(updateDoc(doc(founder,id),{joinApproval:true}));
  await assertSucceeds(updateDoc(doc(founder,id),{paused:true}));
  // Preserve the earlier safe cover-only legacy fallback.
  await assertSucceeds(updateDoc(doc(founder,id),{coverAlignment:.35}));
  await assertFails(updateDoc(doc(member,id),{paused:false}));
  await assertFails(updateDoc(doc(member,id),{coverAlignment:.2}));
  await assertFails(updateDoc(doc(outsider,id),{paused:false}));
  await assertFails(updateDoc(doc(admin,id),{paused:false}));
  // Not a backdoor to add admins, remove members or delete whole community.
  await assertFails(updateDoc(doc(founder,id),{admins:['founder','admin']}));
  await assertFails(updateDoc(doc(founder,id),{members:['founder']}));
  await assertFails(deleteDoc(doc(founder,id)));
  console.log('Build469 legacy founder: settings allowed; admin escalation and deletion rejected');
} finally {
  await env.cleanup();
}
