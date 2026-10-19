/**
 * Build532 local Firestore emulator: active room names cannot be rotated and
 * departed call participants cannot be silently re-added to the same room.
 * No production Firebase or LiveKit access.
 */
import fs from 'node:fs';
import {
  initializeTestEnvironment,assertSucceeds,assertFails,
} from '@firebase/rules-unit-testing';
import {
  doc,setDoc,getDoc,updateDoc,arrayUnion,arrayRemove,serverTimestamp,Timestamp,
} from 'firebase/firestore';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',firestore:{
    host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')
  }
});
const initial=(room,extras={})=>({
  isGroup:true,members:['host','beta','gamma','delta'],
  admins:['host'],createdBy:'host',groupName:'Build532 group',
  callRoomName:room,callStartedBy:'host',callStatus:'active',
  callParticipants:['beta','gamma'],
  callConnectedAt:Timestamp.fromMillis(1760000000000),
  callCreatedAt:Timestamp.fromMillis(1760000000000),
  callExitedRoomName:room,callExitedUids:['host'],
  ...extras,
});
async function seed(id,data) {
  await env.withSecurityRulesDisabled(async ctx=>{
    await setDoc(doc(ctx.firestore(),'chats',id),data);
  });
}
try {
  await env.clearFirestore();
  const host=env.authenticatedContext('host').firestore();
  const beta=env.authenticatedContext('beta').firestore();
  const gamma=env.authenticatedContext('gamma').firestore();
  const delta=env.authenticatedContext('delta').firestore();
  const stranger=env.authenticatedContext('stranger').firestore();
  const ref=(db,id)=>doc(db,'chats',id);
  await seed('active532',initial('group_active532'));

  // A valid member (even creator/admin) cannot rotate an ongoing RTC room.
  for(const db of [host,beta,gamma]) {
    await assertFails(updateDoc(ref(db,'active532'),{
      callRoomName:'group_forged532',
    }));
    await assertFails(updateDoc(ref(db,'active532'),{
      callRoomName:'group_forged532',callStatus:'ended',
      callEndedAt:serverTimestamp(),
    }));
  }
  // Cannot bypass per-room exit prevention by adding a departed user into
  // participants while pretending the room never changed.
  await assertFails(updateDoc(ref(beta,'active532'),{
    callParticipants:arrayUnion('host'),
  }));
  await assertFails(updateDoc(ref(host,'active532'),{
    callParticipants:arrayUnion('host'),
  }));
  await assertFails(updateDoc(ref(gamma,'active532'),{
    callParticipants:['host','beta','gamma'],
  }));
  await assertFails(updateDoc(ref(stranger,'active532'),{
    callParticipants:arrayUnion('delta'),
  }));

  // A legitimate group member can add THEMSELVES via Build527.
  await assertSucceeds(updateDoc(ref(delta,'active532'),{
    callParticipants:arrayUnion('delta'),callStatus:'active',
  }));
  let state=(await getDoc(ref(host,'active532'))).data();
  if(state.callParticipants.join(',')!=='beta,gamma,delta'
    ||state.callExitedUids.join(',')!=='host')
    throw Error('Legitimate joining member disturbed protected exit');

  // Legitimate Build530/531 self-exit still appends only own marker.
  await assertSucceeds(updateDoc(ref(beta,'active532'),{
    callParticipants:arrayRemove('beta'),
    callExitedRoomName:'group_active532',
    callExitedUids:arrayUnion('beta'),callStatus:'active',
  }));
  state=(await getDoc(ref(gamma,'active532'))).data();
  if(state.callParticipants.join(',')!=='gamma,delta'
    ||state.callExitedUids.join(',')!=='host,beta')
    throw Error('Legitimate self-exit failed or removed another member');
  await assertFails(updateDoc(ref(gamma,'active532'),{
    callParticipants:arrayUnion('beta'),
  }));

  // Once a previous call is genuinely finished, a fresh group room may be
  // initialized. Build530 markers refer only to the old room.
  await seed('finished532',initial('group_old532',{
    callStatus:'ended',callEndedAt:Timestamp.fromMillis(1760000001000),
    callParticipants:[],callExitedUids:['host','beta','gamma','delta'],
  }));
  await assertSucceeds(updateDoc(ref(host,'finished532'),{
    callRoomName:'group_next532',callStatus:'ringing',
    callParticipants:['host'],callCreatedAt:serverTimestamp(),
    callConnectedAt:null,callEndedAt:null,
  }));
  state=(await getDoc(ref(host,'finished532'))).data();
  if(state.callRoomName!=='group_next532'||state.callParticipants[0]!=='host')
    throw Error('New call room blocked after prior call ended');

  // Private calls, ordinary metadata and chat group membership are not
  // coupled to the group-only RTC guard.
  await assertSucceeds(updateDoc(ref(host,'active532'),{
    updatedAt:serverTimestamp(),
  }));
  await seed('private532',{
    isGroup:false,members:['host','beta'],admins:['host'],createdBy:'host',
    callRoomName:'private_old532',callStatus:'active',
  });
  await assertSucceeds(updateDoc(ref(host,'private532'),{
    callRoomName:'private_next532',
  }));
  console.log('Build532 FIRESTORE PASS: room rotation blocked while group call active/ringing');
  console.log('Build532 FIRESTORE PASS: same-room departed UID replay denied, self join/leave preserved');
  console.log('Build532 FIRESTORE PASS: next call after ended, chat metadata and private calls unaffected');
} finally {
  await env.cleanup();
}
