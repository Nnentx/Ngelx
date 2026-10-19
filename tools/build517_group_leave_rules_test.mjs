// Build517 three-member group call leave/firestore transaction emulator.
// Uses demo-ngelx local rules only. No production Firebase reads/writes.
import fs from 'node:fs';
import {
  initializeTestEnvironment,assertSucceeds,assertFails,
} from '@firebase/rules-unit-testing';
import {
  doc,setDoc,getDoc,updateDoc,runTransaction,arrayRemove,arrayUnion,
  serverTimestamp,Timestamp,
} from 'firebase/firestore';

const env=await initializeTestEnvironment({
  projectId:'demo-ngelx',
  firestore:{host:'127.0.0.1',port:8080,
    rules:fs.readFileSync('firestore.rules','utf8')},
});

const initial=(room)=>({
  isGroup:true,
  members:['host','beta','gamma'],
  admins:['host'],
  createdBy:'host',
  groupName:'517 emulator room',
  callRoomName:room,
  callStartedBy:'host',
  callStatus:'active',
  callParticipants:['host','beta','gamma'],
  callConnectedAt:Timestamp.fromMillis(1760000000000),
});
async function leave(db,chat,room,user) {
  return runTransaction(db,async tx=>{
    const d=await tx.get(doc(db,'chats',chat));
    const data=d.data()??{};
    if(data.callRoomName!==room||
       ['ended','rejected','missed'].includes(data.callStatus)) return 'stale';
    const participants=data.callParticipants??[];
    if(!participants.includes(user))return 'stale';
    const isLast=participants.filter(p=>p!==user).length===0;
    // Build530+531: the current client records its own same-room exit
    // marker atomically. Test the integrated behavior, not the pre-530 one.
    tx.update(doc(db,'chats',chat),{
      callParticipants:arrayRemove(user),
      callExitedRoomName:room,
      callExitedUids:data.callExitedRoomName===room
        ?arrayUnion(user):[user],
      callStatus:isLast?'ended':'active',
      ...(isLast?{callEndedAt:serverTimestamp()}:{})
    });
    return isLast?'last':'left';
  });
}
async function seed(chat,room) {
  await env.withSecurityRulesDisabled(async ctx=>{
    await setDoc(doc(ctx.firestore(),'chats',chat),initial(room));
  });
}
async function read(db,chat){
  const d=await getDoc(doc(db,'chats',chat));
  return d.data();
}
try{
  await env.clearFirestore();
  const host=env.authenticatedContext('host').firestore();
  const beta=env.authenticatedContext('beta').firestore();
  const gamma=env.authenticatedContext('gamma').firestore();
  const stranger=env.authenticatedContext('stranger').firestore();
  await seed('group517','group_517');
  // The original caller leaving must never terminate the peers' call.
  if(await assertSucceeds(leave(host,'group517','group_517','host'))!=='left')
    throw Error('Initiator must leave without global termination');
  let state=await read(beta,'group517');
  if(state.callStatus!=='active'||state.callParticipants.join(',')!=='beta,gamma')
    throw Error('B/C must remain connected when host leaves');
  // Moderation removes only the nominated member, preserving call state.
  await assertSucceeds(updateDoc(doc(host,'chats/group517'),{
    callModerationRoom:'group_517',
    callKickedUids:arrayUnion('gamma'),
    callParticipants:arrayRemove('gamma'),
  }));
  state=await read(beta,'group517');
  if(state.callStatus!=='active'||state.callParticipants.join(',')!=='beta')
    throw Error('Moderator action ended unaffected beta');
  if(await assertSucceeds(leave(gamma,'group517','group_517','gamma'))!=='stale')
    throw Error('Removed member should not end peer call');
  if((await read(beta,'group517')).callStatus!=='active')
    throw Error('A stale client ended beta call');
  if(await assertSucceeds(leave(beta,'group517','group_517','beta'))!=='last')
    throw Error('Only beta should be last');
  state=await read(beta,'group517');
  if(state.callStatus!=='ended'||state.callParticipants.length!==0||
     !state.callEndedAt)
    throw Error('Last member must close call exactly once');

  await seed('group517_concurrent','group_517_concurrent');
  await assertSucceeds(leave(host,'group517_concurrent','group_517_concurrent','host'));
  // Firestore retries optimistic conflicting transactions. One of these
  // must observe the other's leave and close only after the second leaves.
  const results=await Promise.all([
    assertSucceeds(leave(beta,'group517_concurrent','group_517_concurrent','beta')),
    assertSucceeds(leave(gamma,'group517_concurrent','group_517_concurrent','gamma')),
  ]);
  if(results.filter(x=>x==='last').length!==1)
    throw Error('Concurrent departure must have precisely one last member');
  state=await read(host,'group517_concurrent');
  if(state.callStatus!=='ended'||state.callParticipants.length!==0)
    throw Error('Concurrent final participants must close correctly');
  // A non-owner cannot update the call message created by the initiator.
  // The final member must still be able to publish the call-end notice.
  await env.withSecurityRulesDisabled(async ctx=>{
    await setDoc(doc(ctx.firestore(),'chats/group517/messages/call_original'),{
      senderId:'host',type:'call',callStatus:'active',
      callRoomName:'group_517',createdAt:Timestamp.fromMillis(1760000000000),
    });
  });
  await assertFails(updateDoc(doc(beta,'chats/group517/messages/call_original'),{
    callStatus:'ended',
  }));
  await assertSucceeds(setDoc(doc(beta,'chats/group517/messages/call_end_group_517'),{
    senderId:'beta',actorUid:'beta',type:'system',systemAction:'call_end',
    callVideo:true,text:'Arama sona erdi.',createdAt:serverTimestamp(),
  },{merge:true}));
  await assertFails(updateDoc(doc(stranger,'chats/group517'),{callStatus:'active'}));
  console.log('Build517 FIRESTORE EMULATOR PASS: host leave 3→2 and admin kick 2→1 keep call active');
  console.log('Build517 FIRESTORE EMULATOR PASS: stale removals ignored, last leave closes once');
  console.log('Build517 FIRESTORE EMULATOR PASS: concurrent final departures and outsider deny');
}finally{await env.cleanup();}
