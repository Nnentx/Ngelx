// Build527 isolated emulator: a late LiveKit callback may not revive an
// ended, missed, replaced, kicked or disabled group room. No production writes.
import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds} from '@firebase/rules-unit-testing';
import {doc,getDoc,setDoc,runTransaction,arrayUnion,serverTimestamp,Timestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,
    rules:fs.readFileSync('firestore.rules','utf8')},
});
const base=(room,status='ringing',participants=['host'])=>({
  isGroup:true,groupName:'Build527',members:['host','beta','gamma'],admins:['host'],
  createdBy:'host',callStartedBy:'host',callRoomName:room,callStatus:status,
  callCreatedAt:Timestamp.fromMillis(Date.now()-30_000),
  callParticipants:participants,
});
async function seed(name,data){
  await env.withSecurityRulesDisabled(async c=>{
    await setDoc(doc(c.firestore(),'chats',name),data);
  });
}
async function join(db,name,room,uid,activate=true){
  return runTransaction(db,async tx=>{
    const ref=doc(db,'chats',name),sn=await tx.get(ref),d=sn.data();
    if(!d||d.callRoomName!==room||!['ringing','active'].includes(d.callStatus)||
      !d.members?.includes(uid))return false;
    if((d.callKickedUids??[]).includes(uid)&&
      (!d.callModerationRoom||d.callModerationRoom===room))return false;
    const active=activate||d.callStatus==='active';
    tx.update(ref,{
      callParticipants:arrayUnion(uid),callStatus:active?'active':'ringing',
      ...(active&&!d.callConnectedAt?{callConnectedAt:serverTimestamp()}:{})
    });
    return true;
  },{maxAttempts:5});
}
try{
  await env.clearFirestore();
  const host=env.authenticatedContext('host').firestore();
  const beta=env.authenticatedContext('beta').firestore();
  await seed('ended527',base('group_527_ended','ended',['host']));
  if(await assertSucceeds(join(beta,'ended527','group_527_ended','beta')))
    throw Error('Ended call resurrected');
  await seed('missed527',base('group_527_missed','missed',['host']));
  if(await assertSucceeds(join(beta,'missed527','group_527_missed','beta')))
    throw Error('Missed call resurrected');
  await seed('changed527',base('group_527_new','ringing',['host']));
  if(await assertSucceeds(join(beta,'changed527','group_527_old','beta')))
    throw Error('Stale room name revived a newer call');
  await seed('kick527',{...base('group_527_kicked','active',['host','gamma']),
    callModerationRoom:'group_527_kicked',callKickedUids:['beta']});
  if(await assertSucceeds(join(beta,'kick527','group_527_kicked','beta')))
    throw Error('Kicked participant rejoined same room');
  let record=(await assertSucceeds(getDoc(doc(host,'chats/kick527')))).data();
  if(record.callParticipants.includes('beta')||record.callStatus!=='active')
    throw Error('Kick changed peers incorrectly');
  await seed('active527',base('group_527_active','active',['host','gamma']));
  if(!await assertSucceeds(join(beta,'active527','group_527_active','beta')))
    throw Error('Valid third member cannot join');
  record=(await assertSucceeds(getDoc(doc(host,'chats/active527')))).data();
  if(record.callStatus!=='active'||record.callParticipants.length!==3)
    throw Error('Third join incorrectly affected active call');
  await seed('ringing527',base('group_527_ringing','ringing',['host']));
  if(!await assertSucceeds(join(beta,'ringing527','group_527_ringing','beta')))
    throw Error('Valid second participant cannot answer');
  record=(await assertSucceeds(getDoc(doc(host,'chats/ringing527')))).data();
  if(record.callStatus!=='active'||record.callParticipants.length!==2)
    throw Error('Ringing to active transition failed');
  await seed('oldkick527',{...base('group_527_new_again','ringing',['host']),
    callModerationRoom:'group_527_previous',callKickedUids:['beta']});
  if(!await assertSucceeds(join(beta,'oldkick527','group_527_new_again','beta')))
    throw Error('Historical kick incorrectly blocked new room');
  // The original caller's async remote callback cannot re-open room after
  // the last participant has ended it in a competing transaction.
  await seed('last527',base('group_527_last','active',['host']));
  await assertSucceeds(runTransaction(host,async tx=>{
    const ref=doc(host,'chats/last527'),snap=await tx.get(ref);
    if(snap.data().callStatus!=='active')throw Error('Bad fixture');
    tx.update(ref,{callStatus:'ended',callParticipants:[],callEndedAt:serverTimestamp()});
  }));
  if(await assertSucceeds(join(host,'last527','group_527_last','host')))
    throw Error('Last member departed but async callback revived room');
  record=(await assertSucceeds(getDoc(doc(host,'chats/last527')))).data();
  if(record.callStatus!=='ended'||record.callParticipants.length!==0)
    throw Error('Authoritative ended status was overwritten');
  console.log('Build527 EMULATOR PASS: stale callbacks cannot revive ended, missed, replaced, or kicked calls');
  console.log('Build527 EMULATOR PASS: healthy ringing 1→2 and active 2→3 retain state; old kick expires');
}finally{await env.cleanup();}
