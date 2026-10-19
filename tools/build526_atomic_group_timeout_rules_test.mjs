// Build526 emulator: stale 2-minute timer cannot terminate an active 3→2 call.
// Pure demo-ngelx Firestore emulator. NO production Firebase access.
import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds} from '@firebase/rules-unit-testing';
import {doc,getDoc,setDoc,runTransaction,serverTimestamp,Timestamp} from 'firebase/firestore';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,
    rules:fs.readFileSync('firestore.rules','utf8')},
});
const old=Timestamp.fromMillis(Date.now()-130_000);
const fresh=Timestamp.fromMillis(Date.now()-2_000);
const base=(room,participants,stamp=old)=>({
  isGroup:true,members:['host','beta','gamma'],admins:['host'],
  createdBy:'host',groupName:'Build526',
  callRoomName:room,callStartedBy:'host',callStatus:'ringing',
  callParticipants:participants,callCreatedAt:stamp,callVideo:false,
});
async function seed(name,data){
  await env.withSecurityRulesDisabled(async c=>
    setDoc(doc(c.firestore(),'chats',name),data));
}
async function expire(db,name,expectedRoom){
  try{
    return await runTransaction(db,async tx=>{
    const ref=doc(db,'chats',name),snap=await tx.get(ref);
    const data=snap.data();
    if(!data||data.callRoomName!==expectedRoom||data.callStatus!=='ringing'||
       (data.callParticipants??[]).length>1)return false;
    if(data.callCreatedAt instanceof Timestamp &&
       Date.now()-data.callCreatedAt.toMillis()<120_000)return false;
    tx.update(ref,{
      callStatus:'missed',callEndedAt:serverTimestamp(),
      callAutoEnded:true,callAutoEndedReason:'no_participants_2m'});
    return true;
    },{maxAttempts:5});
  }catch(error){
    if(error.code!=='permission-denied')throw error;
    // Another concurrent timer, a joining peer, or room replacement may
    // have made this attempt obsolete. It is only safe to ignore the denial
    // if an authoritative new snapshot proves the predicate changed.
    const current=(await getDoc(doc(db,'chats',name))).data();
    if(!current||current.callRoomName!==expectedRoom||
       current.callStatus!=='ringing'||
       current.callConnectedAt instanceof Timestamp||
       (current.callParticipants??[]).length>1){
      console.log('Build526 tx collision resolved as stale',name,
        current?.callStatus??'missing');
      return false;
    }
    throw error;
  }
}
try{
  await env.clearFirestore();
  const host=env.authenticatedContext('host').firestore();
  const beta=env.authenticatedContext('beta').firestore();
  await seed('joined526',base('group_526_joined',['host','beta','gamma']));
  if(await assertSucceeds(expire(host,'joined526','group_526_joined')))
    throw Error('timer closed a 3-member call');
  let current=(await assertSucceeds(getDoc(doc(beta,'chats/joined526')))).data();
  if(current.callStatus!=='ringing'||current.callParticipants.length!==3)
    throw Error('3 people should be preserved');
  await seed('active526',{...base('group_526_active',['host','beta']),'callStatus':'active'});
  if(await assertSucceeds(expire(host,'active526','group_526_active')))
    throw Error('timer closed active 2-member call');
  current=(await assertSucceeds(getDoc(doc(beta,'chats/active526')))).data();
  if(current.callStatus!=='active'||current.callParticipants.length!==2)
    throw Error('active 2-member call ended incorrectly');
  await seed('fresh526',base('group_526_fresh',['host'],fresh));
  if(await assertSucceeds(expire(host,'fresh526','group_526_fresh')))
    throw Error('timer closed a call before 120 seconds');
  await seed('reused526',base('group_526_new',['host']));
  if(await assertSucceeds(expire(host,'reused526','group_526_old')))
    throw Error('old timer closed a newer room');
  await seed('missed526',base('group_526_missed',['host']));
  const [one,two]=await Promise.all([
    assertSucceeds(expire(host,'missed526','group_526_missed')),
    assertSucceeds(expire(host,'missed526','group_526_missed'))]);
  if([one,two].filter(Boolean).length!==1)
    throw Error('only one timer may expire unanswered room');
  current=(await assertSucceeds(getDoc(doc(beta,'chats/missed526')))).data();
  if(current.callStatus!=='missed'||current.callAutoEnded!==true||
     current.callAutoEndedReason!=='no_participants_2m')
    throw Error('eligible unanswered call was not closed once');
  console.log('Build526 EMULATOR PASS: three members, active two, fresh room, changed room protected');
  console.log('Build526 EMULATOR PASS: exactly one concurrent 120-second expiration');
}finally{await env.cleanup();}
