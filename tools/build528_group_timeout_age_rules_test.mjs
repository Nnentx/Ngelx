// Build528 QA: simulate timestampless and partially connected group timeout.
// Uses demo-ngelx Firestore emulator, not production state.
import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds} from '@firebase/rules-unit-testing';
import {doc,setDoc,getDoc,runTransaction,serverTimestamp,Timestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
const aged=Timestamp.fromMillis(Date.now()-180_000);
const base=(room)=>({
  isGroup:true,groupName:'528 QA',
  members:['host','beta','gamma'],admins:['host'],createdBy:'host',
  callRoomName:room,callStartedBy:'host',callStatus:'ringing',callParticipants:['host'],
  callCreatedAt:aged,
});
async function seed(id,data){await env.withSecurityRulesDisabled(async c=>{
  await setDoc(doc(c.firestore(),'chats',id),data);
});}
async function expire(db,id,room){
  return runTransaction(db,async tx=>{
    const ref=doc(db,'chats',id),d=(await tx.get(ref)).data();
    if(!d||d.callRoomName!==room||d.callStatus!=='ringing'||
      (d.callParticipants??[]).length>1)return false;
    // Same safety predicates as Build528 Dart helper.
    if(d.callConnectedAt instanceof Timestamp)return false;
    if(!(d.callCreatedAt instanceof Timestamp))return false;
    if(Date.now()-d.callCreatedAt.toMillis()<120_000)return false;
    tx.update(ref,{callStatus:'missed',callAutoEnded:true,
      callAutoEndedReason:'no_participants_2m',callEndedAt:serverTimestamp()});
    return true;
  });
}
try{
  await env.clearFirestore();
  const host=env.authenticatedContext('host').firestore();
  await seed('missing528',{...base('group_missing528'),callCreatedAt:null});
  if(await assertSucceeds(expire(host,'missing528','group_missing528')))
    throw Error('Missing server call age incorrectly allowed timeout');
  await seed('connected528',{...base('group_connected528'),
    callConnectedAt:Timestamp.fromMillis(Date.now()-20_000)});
  if(await assertSucceeds(expire(host,'connected528','group_connected528')))
    throw Error('LiveKit-confirmed call incorrectly marked missed');
  await seed('two528',{...base('group_two528'),callParticipants:['host','beta']});
  if(await assertSucceeds(expire(host,'two528','group_two528')))
    throw Error('Active peer incorrectly timed out');
  await seed('newer528',base('group_newer528'));
  if(await assertSucceeds(expire(host,'newer528','group_previous528')))
    throw Error('Old timer closed newer room');
  await seed('valid528',base('group_valid528'));
  if(!await assertSucceeds(expire(host,'valid528','group_valid528')))
    throw Error('Valid 3-minute unanswered group should be missed');
  const state=(await assertSucceeds(getDoc(doc(host,'chats/valid528')))).data();
  if(state.callStatus!=='missed'||!state.callAutoEnded)
    throw Error('Valid missed call did not close');
  console.log('Build528 FIRESTORE EMULATOR PASS: absent age and connected media fail closed');
  console.log('Build528 FIRESTORE EMULATOR PASS: 2 participants and changed room safe, aged one-member missed');
}finally{await env.cleanup();}
