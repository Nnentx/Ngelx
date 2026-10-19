/**
 * Build531: Firestore emulator acceptance of Build530 group exit markers.
 * All writes use the local demo-ngelx emulator and isolated test identities.
 * No production resources, deployment, or Firebase credentials are used.
 */
import fs from 'node:fs';
import {
  initializeTestEnvironment, assertSucceeds, assertFails
} from '@firebase/rules-unit-testing';
import {
  doc, setDoc, getDoc, updateDoc, runTransaction, arrayRemove, arrayUnion,
  Timestamp, serverTimestamp
} from 'firebase/firestore';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,
    rules:fs.readFileSync('firestore.rules','utf8')},
});
const connected=Timestamp.fromMillis(1760000000000);
const initial=(room,overrides={})=>({
  isGroup:true,members:['host','beta','gamma'],admins:['host'],createdBy:'host',
  groupName:'Build531 emulator group',callRoomName:room,callStartedBy:'host',
  callStatus:'active',callConnectedAt:connected,
  callParticipants:['host','beta','gamma'],...overrides,
});
const users=['host','beta','gamma'];
const paths=id=>doc(env.authenticatedContext('host').firestore(),'chats',id);
async function seed(id,record) {
  await env.withSecurityRulesDisabled(async ctx=>{
    await setDoc(doc(ctx.firestore(),'chats',id),record);
  });
}
async function state(db,id) {
  return (await getDoc(doc(db,'chats',id))).data();
}
async function leave(db,id,room,uid) {
  return runTransaction(db,async tx=>{
    const ref=doc(db,'chats',id);
    const snap=await tx.get(ref), data=snap.data()??{};
    if(data.callRoomName!==room || ['ended','missed','rejected'].includes(data.callStatus))
      return 'stale';
    const participants=data.callParticipants??[];
    if(!participants.includes(uid))return 'stale';
    const remaining=participants.filter(member=>member!==uid);
    const isLast=remaining.length===0;
    const oldExitRoom=data.callExitedRoomName??'';
    tx.update(ref,{
      callParticipants:arrayRemove(uid),
      callExitedRoomName:room,
      callExitedUids:oldExitRoom===room?arrayUnion(uid):[uid],
      callStatus:isLast?(data.callConnectedAt instanceof Timestamp?'ended':'missed'):'active',
      ...(isLast?{callEndedAt:serverTimestamp()}:{})
    });
    return isLast?'last':'left';
  });
}
try {
  await env.clearFirestore();
  const host=env.authenticatedContext('host').firestore();
  const beta=env.authenticatedContext('beta').firestore();
  const gamma=env.authenticatedContext('gamma').firestore();
  const stranger=env.authenticatedContext('stranger').firestore();
  const ref=(db,id)=>doc(db,'chats',id);
  await seed('exit531',initial('group_531'));

  // Forged marker creation without the caller's own atomic leave is denied.
  await assertFails(updateDoc(ref(beta,'exit531'),{
    callExitedRoomName:'group_531',callExitedUids:['host'],
  }));
  await assertFails(updateDoc(ref(beta,'exit531'),{
    callExitedRoomName:'group_531',callExitedUids:['host'],
    callParticipants:arrayRemove('host'),callStatus:'active'
  }));
  // Signed out and unrelated users retain the old denial.
  await assertFails(updateDoc(ref(stranger,'exit531'),{
    callExitedRoomName:'group_531',callExitedUids:['stranger'],
    callParticipants:arrayRemove('stranger'),
  }));

  if(await assertSucceeds(leave(host,'exit531','group_531','host'))!=='left')
    throw Error('Initiator must be able to leave without ending peers');
  let s=await state(beta,'exit531');
  if(s.callStatus!=='active'||s.callParticipants.join(',')!=='beta,gamma'
    ||s.callExitedRoomName!=='group_531'||s.callExitedUids.join(',')!=='host')
    throw Error('Host exit did not persist its authorization marker');
  for(const fields of [
    {callExitedUids:[]},
    {callExitedRoomName:'other_group'},
    {callExitedUids:['beta']},
    {callExitedRoomName:'group_531',callExitedUids:['beta','gamma']},
  ]) await assertFails(updateDoc(ref(beta,'exit531'),fields));

  // Peer can leave, but cannot edit another user's exit or close both peers.
  await assertFails(updateDoc(ref(beta,'exit531'),{
    callExitedUids:arrayUnion('gamma'),
    callParticipants:arrayRemove('gamma'),
    callStatus:'active'
  }));
  if(await assertSucceeds(leave(beta,'exit531','group_531','beta'))!=='left')
    throw Error('Second peer exit should keep gamma connected');
  s=await state(gamma,'exit531');
  if(s.callStatus!=='active'||s.callParticipants.join(',')!=='gamma'||
     s.callExitedUids.join(',')!=='host,beta')
    throw Error('Second exit must append without erasing prior exit');
  if(await assertSucceeds(leave(gamma,'exit531','group_531','gamma'))!=='last')
    throw Error('Only last participant may close current call');
  s=await state(host,'exit531');
  if(s.callStatus!=='ended'||s.callParticipants.length!==0||
     s.callExitedUids.join(',')!=='host,beta,gamma'||!s.callEndedAt)
    throw Error('Last departure must retain all exits and close the room');

  // Old call's exits must not poison a new room. The first exit in the new
  // room establishes its own marker set; the former list is not carried over.
  await seed('next531',initial('group_next531',{
    callExitedRoomName:'group_previous531',callExitedUids:['host','beta'],
  }));
  if(await assertSucceeds(leave(beta,'next531','group_next531','beta'))!=='left')
    throw Error('First new-room exit must be allowed');
  s=await state(host,'next531');
  if(s.callExitedRoomName!=='group_next531'||s.callExitedUids.join(',')!=='beta'
    ||s.callParticipants.join(',')!=='host,gamma')
    throw Error('New room inherited historical exit marker');

  // Unrelated ordinary chat updates keep working with the new outer guard.
  await assertSucceeds(updateDoc(ref(host,'next531'),{updatedAt:serverTimestamp()}));
  // Private chats cannot start recording fake group exit markers.
  await seed('private531',{isGroup:false,members:['host','beta'],admins:['host'],
    createdBy:'host',callRoomName:'private_531',callParticipants:['host','beta']});
  await assertFails(updateDoc(ref(host,'private531'),{
    callExitedRoomName:'private_531',callExitedUids:['host'],
    callParticipants:arrayRemove('host'),callStatus:'active'
  }));
  console.log('Build531 FIRESTORE PASS: atomic host 3→2, peer 2→1 and final 1→0');
  console.log('Build531 FIRESTORE PASS: peer forgery, exit tampering and private marker injection denied');
  console.log('Build531 FIRESTORE PASS: new call room resets exits; ordinary chat updates preserved');
} finally {
  await env.cleanup();
}
