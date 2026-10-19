/**
 * Build534 local Firestore emulator: explicit same-room own rejoin only.
 * Tests ONLY authenticated database effects; UI confirmation must be
 * supplied by a real button/dialog and cannot be proven by Firestore rules.
 * No production services or secrets.
 */
import fs from 'node:fs';
import {initializeTestEnvironment,assertFails,assertSucceeds} from '@firebase/rules-unit-testing';
import {doc,setDoc,getDoc,updateDoc,arrayRemove,arrayUnion,Timestamp} from 'firebase/firestore';
import {roomPermission} from '../server/livekit443/room-policy.mjs';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,
    rules:fs.readFileSync('firestore.rules','utf8')},
});
const now=Date.now();
const base=(room,more={})=>({
  isGroup:true,members:['host','beta','gamma','delta'],admins:['host'],
  createdBy:'host',groupName:'Build534 QA',
  callStartedBy:'host',callRoomName:room,
  callCreatedAt:Timestamp.fromMillis(now-30_000),
  callConnectedAt:Timestamp.fromMillis(now-25_000),callStatus:'active',
  callParticipants:['beta','gamma'],callExitedRoomName:room,
  callExitedUids:['host'],...more,
});
async function seed(id,data){
  await env.withSecurityRulesDisabled(async context=>
    setDoc(doc(context.firestore(),'chats',id),data));
}
const authorization=(room,uid)=>roomPermission({
  kind:'call',room,uid,now,viewer:{displayName:uid},owner:{displayName:'host'}
});
try{
  await env.clearFirestore();
  const host=env.authenticatedContext('host').firestore();
  const beta=env.authenticatedContext('beta').firestore();
  const gamma=env.authenticatedContext('gamma').firestore();
  const delta=env.authenticatedContext('delta').firestore();
  const outsider=env.authenticatedContext('outsider').firestore();
  const ref=(db,id)=>doc(db,'chats',id);
  const state=async id=>(await getDoc(ref(host,id))).data();
  await seed('rejoin534',base('group_rejoin534'));
  let before=await state('rejoin534');
  if(authorization(before,'host')!==null)throw Error('Exited host obtained token before consent');

  // A reconnect / remote track callback may never revive a room by
  // altering participants without an explicit own marker-clearing write.
  await assertFails(updateDoc(ref(host,'rejoin534'),{
    callParticipants:arrayUnion('host')
  }));
  await assertFails(updateDoc(ref(beta,'rejoin534'),{
    callParticipants:arrayUnion('host'),
    callExitedUids:arrayRemove('host')
  }));
  await assertFails(updateDoc(ref(host,'rejoin534'),{
    callExitedUids:arrayRemove('host')
  }));
  await assertFails(updateDoc(ref(host,'rejoin534'),{
    callExitedUids:arrayRemove('host'),
    callParticipants:arrayUnion('host'),callStatus:'ended'
  }));
  await assertFails(updateDoc(ref(outsider,'rejoin534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));
  await assertFails(updateDoc(ref(host,'rejoin534'),{
    callExitedUids:[],callParticipants:['host']
  }));

  // Only the same authenticated user can atomically undo their own exit.
  await assertSucceeds(updateDoc(ref(host,'rejoin534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));
  let after=await state('rejoin534');
  if(after.callStatus!=='active'||after.callRoomName!=='group_rejoin534'||
     after.callParticipants.join(',')!=='beta,gamma,host'||
     after.callExitedUids.length!==0)throw Error('Self rejoin disrupted active peer call');
  if(authorization(after,'host')?.role!=='caller')
    throw Error('Fresh RTC token remains blocked after authorized rejoin');
  // An old confirmation cannot add the same UID twice.
  await assertFails(updateDoc(ref(host,'rejoin534'),{
    callParticipants:arrayUnion('host'),callExitedUids:arrayRemove('host')
  }));

  await seed('peers534',base('group_peers534',{
    callExitedUids:['host','delta'],callParticipants:['beta','gamma']
  }));
  await assertSucceeds(updateDoc(ref(host,'peers534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));
  after=await state('peers534');
  if(after.callExitedUids.join(',')!=='delta'||!after.callParticipants.includes('host'))
    throw Error('Explicit rejoin cleared an unrelated caller exit');
  if(authorization(after,'delta')!==null)throw Error('Peer still exited obtained token');
  // Preserved exits cannot be directly replayed into participants.
  await assertFails(updateDoc(ref(beta,'peers534'),{
    callParticipants:arrayUnion('delta')
  }));

  // Moderation wins over a user confirmation, including legacy records.
  for (const [id,moderationRoom] of [
    ['kicked534','group_kicked534'],['legacyKick534','']
  ]) {
    await seed(id,base(id==='kicked534'?'group_kicked534':'group_legacyKick534',{
      callKickedUids:['host'],callModerationRoom:moderationRoom
    }));
    await assertFails(updateDoc(ref(host,id),{
      callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
    }));
  }
  // Historical moderation for a different call must not punish this room.
  await seed('oldKick534',base('group_newKick534',{
    callKickedUids:['host'],callModerationRoom:'group_previous534'
  }));
  await assertSucceeds(updateDoc(ref(host,'oldKick534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));

  // No remaining caller / ended call / previous-room exit cannot be revived.
  await seed('ended534',base('group_ended534',{
    callStatus:'ended',callParticipants:[],
  }));
  await assertFails(updateDoc(ref(host,'ended534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));
  await seed('solo534',base('group_solo534',{callParticipants:[]}));
  await assertFails(updateDoc(ref(host,'solo534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));
  await seed('stale534',base('group_new534',{
    callExitedRoomName:'group_old534'
  }));
  await assertFails(updateDoc(ref(host,'stale534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));
  await seed('notExited534',base('group_notExited534',{
    callExitedUids:['delta']
  }));
  await assertFails(updateDoc(ref(host,'notExited534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));
  await seed('memberGone534',base('group_memberGone534',{
    members:['beta','gamma','delta']
  }));
  await assertFails(updateDoc(ref(host,'memberGone534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));

  // Server would refuse new tokens when the call age exceeds 12 hours.
  // Firestore must not un-exit the caller into such a zombie room.
  await seed('aged534',base('group_aged534',{
    callCreatedAt:Timestamp.fromMillis(now-13*3600_000)
  }));
  await assertFails(updateDoc(ref(host,'aged534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));
  await seed('missingAge534',base('group_missingAge534',{
    callCreatedAt:null
  }));
  await assertFails(updateDoc(ref(host,'missingAge534'),{
    callExitedUids:arrayRemove('host'),callParticipants:arrayUnion('host')
  }));

  // Ordinary chat updates and ongoing callers remain unaffected.
  await assertSucceeds(updateDoc(ref(beta,'rejoin534'),{
    updatedAt:Timestamp.fromMillis(now)
  }));
  const stable=await state('rejoin534');
  if(authorization(stable,'beta')?.role!=='caller')
    throw Error('Peer lost RTC access after other member rejoined');

  console.log('Build534 FIRESTORE PASS: own atomic explicit rejoin restores fresh RTC access');
  console.log('Build534 FIRESTORE PASS: replay, forged actor, replay of other exits and moderation denied');
  console.log('Build534 FIRESTORE PASS: ended/missing/stale room and absent member fail closed');
}finally{
  await env.cleanup();
}
