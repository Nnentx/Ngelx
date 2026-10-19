/**
 * Build533: group-call terminal transitions in local Firestore emulator.
 * Explicitly tests adversarial writes and valid Build517/526/527 flows.
 * Never uses real Firebase or LiveKit services.
 */
import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails}
  from '@firebase/rules-unit-testing';
import {doc,setDoc,getDoc,updateDoc,arrayRemove,arrayUnion,
  Timestamp,serverTimestamp} from 'firebase/firestore';

const env=await initializeTestEnvironment({projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,
    rules:fs.readFileSync('firestore.rules','utf8')}});
const now=Date.now();
const old=Timestamp.fromMillis(now-180_000);
const recent=Timestamp.fromMillis(now-25_000);
const connected=Timestamp.fromMillis(now-15_000);
const base=(room,extra={})=>({
  isGroup:true,members:['host','beta','gamma'],admins:['host'],
  createdBy:'host',groupName:'Build533 QA group',
  callRoomName:room,callStartedBy:'host',
  callCreatedAt:old,callConnectedAt:connected,
  callStatus:'active',callParticipants:['host','beta','gamma'],...extra,
});
const refs=(db,id)=>doc(db,'chats',id);
async function seed(id,data) {
  await env.withSecurityRulesDisabled(async ctx=>{
    await setDoc(doc(ctx.firestore(),'chats',id),data);
  });
}
async function state(db,id) {
  return (await getDoc(refs(db,id))).data();
}
async function selfLeave(db,id,uid,room,extra={}) {
  const data=await state(db,id);
  const participants=data.callParticipants;
  const remaining=participants.filter(x=>x!==uid);
  const isLast=remaining.length===0;
  const lastConnected=data.callConnectedAt instanceof Timestamp;
  return updateDoc(refs(db,id),{
    callParticipants:arrayRemove(uid),
    callExitedRoomName:room,
    callExitedUids:data.callExitedRoomName===room?arrayUnion(uid):[uid],
    callStatus:isLast?(lastConnected?'ended':'missed'):'active',
    ...(isLast?{callEndedAt:serverTimestamp()}:{}),
    ...extra,
  });
}
async function expire(db,id) {
  return updateDoc(refs(db,id),{
    callStatus:'missed',callEndedAt:serverTimestamp(),
    callAutoEnded:true,callAutoEndedReason:'no_participants_2m',
  });
}

try {
  await env.clearFirestore();
  const host=env.authenticatedContext('host').firestore();
  const beta=env.authenticatedContext('beta').firestore();
  const gamma=env.authenticatedContext('gamma').firestore();
  const stranger=env.authenticatedContext('stranger').firestore();
  await seed('active533',base('group_active533'));

  // No member, including founder/admin, may close their peers' connected call
  // by directly setting an ending status, even with an end timestamp.
  for (const db of [host,beta,gamma]) {
    for(const status of ['ended','missed','rejected']) {
      await assertFails(updateDoc(refs(db,'active533'),{
        callStatus:status,callEndedAt:serverTimestamp(),
      }));
    }
    await assertFails(updateDoc(refs(db,'active533'),{
      callStatus:'ringing',
    }));
    await assertFails(updateDoc(refs(db,'active533'),{
      callEndedAt:serverTimestamp(),
    }));
    await assertFails(updateDoc(refs(db,'active533'),{
      callAutoEnded:true,callAutoEndedReason:'no_participants_2m',
    }));
    await assertFails(updateDoc(refs(db,'active533'),{
      callStatus:'ended',callRoomName:'group_forged533',
      callEndedAt:serverTimestamp(),
    }));
  }
  await assertFails(updateDoc(refs(stranger,'active533'),{callStatus:'ended'}));
  const open=await state(host,'active533');
  if(open.callStatus!=='active'||open.callParticipants.length!==3)
    throw Error('Rejected spoof affected active call');

  // 3 -> 2 -> 1 -> 0: normal self leave remains independently authorized.
  await assertSucceeds(selfLeave(host,'active533','host','group_active533'));
  await assertSucceeds(selfLeave(beta,'active533','beta','group_active533'));
  let ongoing=await state(gamma,'active533');
  if(ongoing.callStatus!=='active'||ongoing.callParticipants.join(',')!=='gamma')
    throw Error('Group should keep its remaining peer active');
  await assertSucceeds(selfLeave(gamma,'active533','gamma','group_active533'));
  const ended=await state(host,'active533');
  if(ended.callStatus!=='ended'||ended.callParticipants.length!==0||!ended.callEndedAt)
    throw Error('Last leave did not end connected group');
  await assertFails(updateDoc(refs(host,'active533'),{callStatus:'active'}));
  await assertFails(updateDoc(refs(host,'active533'),{callEndedAt:null}));

  // Unanswered timer only closes an aged ringing call with <=1 participant
  // and no completed connection. A naive status write may NOT imitate it.
  const unanswered=room=>base(room,{
    callStatus:'ringing',callParticipants:['host'],callConnectedAt:null
  });
  await seed('aged533',unanswered('group_aged533'));
  await assertFails(updateDoc(refs(beta,'aged533'),{
    callStatus:'missed',callEndedAt:serverTimestamp(),
  }));
  await assertSucceeds(expire(beta,'aged533'));
  let missed=await state(host,'aged533');
  if(missed.callStatus!=='missed'||!missed.callAutoEnded||!missed.callEndedAt)
    throw Error('Valid unanswered timer not persisted');

  await seed('fresh533',{...unanswered('group_fresh533'),callCreatedAt:recent});
  await assertFails(expire(host,'fresh533'));
  await seed('missing533',{...unanswered('group_missing533'),callCreatedAt:null});
  await assertFails(expire(host,'missing533'));
  await seed('peers533',{...unanswered('group_peers533'),callParticipants:['host','beta']});
  await assertFails(expire(host,'peers533'));
  await seed('connected533',{...unanswered('group_connected533'),callConnectedAt:connected});
  await assertFails(expire(host,'connected533'));
  await seed('activeTimer533',base('group_activeTimer533',{
    callParticipants:['host'],
  }));
  await assertFails(expire(host,'activeTimer533'));

  // A ringing call can still become active when a real group member joins.
  await seed('join533',unanswered('group_join533'));
  await assertSucceeds(updateDoc(refs(beta,'join533'),{
    callParticipants:arrayUnion('beta'),callStatus:'active',
    callConnectedAt:serverTimestamp(),
  }));
  if((await state(host,'join533')).callStatus!=='active')
    throw Error('Authorized ringing to active flow denied');

  // Terminal statuses are final for that room, but a new room is permitted.
  await assertFails(updateDoc(refs(beta,'aged533'),{
    callStatus:'active',callParticipants:['host'],
  }));
  await assertSucceeds(updateDoc(refs(host,'aged533'),{
    callRoomName:'group_next533',callStatus:'ringing',
    callParticipants:['host'],callCreatedAt:serverTimestamp(),
    callConnectedAt:null,callEndedAt:null,callAutoEnded:false,
    callAutoEndedReason:'',
  }));
  await assertSucceeds(updateDoc(refs(host,'aged533'),{
    updatedAt:serverTimestamp(),
  }));
  await seed('private533',{
    isGroup:false,members:['host','beta'],admins:['host'],createdBy:'host',
    callStatus:'active',callRoomName:'private_533',callParticipants:['host','beta']
  });
  await assertSucceeds(updateDoc(refs(host,'private533'),{
    callStatus:'ended',callEndedAt:serverTimestamp(),
  }));
  console.log('Build533 FIRESTORE PASS: founder/member spoof cannot terminate active group');
  console.log('Build533 FIRESTORE PASS: only valid last departure or aged never-answered timeout ends call');
  console.log('Build533 FIRESTORE PASS: answered, recent, multi-peer timeout rejected');
  console.log('Build533 FIRESTORE PASS: join, next-room restart and private calls preserved');
} finally {
  await env.cleanup();
}
