  // Closed phone round: former members see only pre-exit messages.
  await env.withSecurityRulesDisabled(async c=>{
    const db=c.firestore();
    await setDoc(doc(db,'chats/closed438'),{
      isGroup:true,members:['closed438owner','closed438admin'],
      admins:['closed438owner','closed438admin'],createdBy:'closed438owner',
      formerMembers:['closed438former'],removedAt_closed438former:100,
    });
    await setDoc(doc(db,'chats/closed438/messages/before'),{senderId:'closed438owner',type:'text',text:'old',createdAt:99});
    await setDoc(doc(db,'chats/closed438/messages/after'),{senderId:'closed438owner',type:'text',text:'new',createdAt:101});
    await setDoc(doc(db,'chats/closed438/joinRequests/closed438target'),{type:'member_add',uid:'closed438target',targetUid:'closed438target',requestedBy:'closed438admin',status:'pending'});
  });
  const formerClosed438=env.authenticatedContext('closed438former').firestore();
  await assertSucceeds(getDoc(doc(formerClosed438,'chats/closed438/messages/before')));
  await assertFails(getDoc(doc(formerClosed438,'chats/closed438/messages/after')));
  await assertFails(setDoc(doc(formerClosed438,'chats/closed438/messages/send'),{senderId:'closed438former',type:'text',text:'denied',createdAt:serverTimestamp()}));
  await assertFails(updateDoc(doc(formerClosed438,'chats/closed438'),{callStatus:'ringing',callStartedBy:'closed438former'}));
  const approvalClosed438=env.authenticatedContext('closed438owner').firestore();
  console.log('Closed438: checking administrator chat update');
  await assertSucceeds(updateDoc(doc(approvalClosed438,'chats/closed438'),{lastMessage:'diagnostic'}));
  console.log('Closed438: checking administrator system event');
  await assertSucceeds(setDoc(doc(approvalClosed438,'chats/closed438/messages/diagnostic'),{senderId:'closed438owner',type:'system',systemAction:'member_added',actorUid:'closed438owner',text:'diagnostic',createdAt:serverTimestamp()}));
  console.log('Closed438: checking administrator request update');
  await assertSucceeds(updateDoc(doc(approvalClosed438,'chats/closed438/joinRequests/closed438target'),{status:'pending'}));
  console.log('Closed438: checking atomic approval race');
  const approvalEvents438=[];
  const approveClosed438=()=>{
    const event=doc(collection(approvalClosed438,'chats/closed438/messages'));
    approvalEvents438.push(event);
    return runTransaction(approvalClosed438,async tx=>{
    const request=doc(approvalClosed438,'chats/closed438/joinRequests/closed438target');
    const chat=doc(approvalClosed438,'chats/closed438');
    const state=await tx.get(request);await tx.get(chat);
    if(state.data().status!=='pending')return false;
    tx.update(request,{status:'accepted',decidedBy:'closed438owner',decidedAt:serverTimestamp()});
    tx.update(chat,{members:arrayUnion('closed438target'),lastMessage:'member added',updatedAt:serverTimestamp()});
    tx.set(event,{senderId:'closed438owner',type:'system',systemAction:'member_added',actorUid:'closed438owner',targetUids:['closed438target'],text:'member added',createdAt:serverTimestamp()});
    return true;
  });};
  const closedRace438=await Promise.all([approveClosed438(),approveClosed438()]);
  assert.equal(closedRace438.filter(Boolean).length,1);
  assert.equal((await getDoc(doc(approvalClosed438,'chats/closed438/joinRequests/closed438target'))).data().status,'accepted');
  const eventResults438=await Promise.all(approvalEvents438.map(r=>getDoc(r)));
  assert.equal(eventResults438.filter(d=>d.exists()).length,1);
