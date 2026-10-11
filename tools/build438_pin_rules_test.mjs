  // Build438 transactional pin coverage.
  await env.withSecurityRulesDisabled(async(ctx)=>{
    const db=ctx.firestore();
    await setDoc(doc(db,'chats/pin438'),{isGroup:true,members:['pin438owner','pin438admin','pin438member'],admins:['pin438admin'],createdBy:'pin438owner'});
    await setDoc(doc(db,'chats/pin438/messages/message'),{senderId:'pin438owner',type:'text',text:'pin me',pinned:false});
  });
  const pinOwner438=env.authenticatedContext('pin438owner').firestore();
  const pinAdmin438=env.authenticatedContext('pin438admin').firestore();
  const pinMember438=env.authenticatedContext('pin438member').firestore();
  const togglePin438=db=>runTransaction(db,async(tx)=>{
    await tx.get(doc(db,'chats/pin438'));
    const ref=doc(db,'chats/pin438/messages/message');
    const snap=await tx.get(ref);
    const target=snap.data().pinned!==true;
    tx.update(ref,{pinned:target,pinnedAt:serverTimestamp(),pinnedBy:db===pinOwner438?'pin438owner':'pin438admin'});
    return target;
  });
  await assertFails(updateDoc(doc(pinMember438,'chats/pin438/messages/message'),{pinned:true,pinnedBy:'pin438member',pinnedAt:serverTimestamp()}));
  const pinRace438=await Promise.all([togglePin438(pinOwner438),togglePin438(pinAdmin438)]);
  assert.deepEqual([...pinRace438].sort(),[false,true]);
  assert.equal((await getDoc(doc(pinOwner438,'chats/pin438/messages/message'))).data().pinned,false);
  await env.withSecurityRulesDisabled(async(ctx)=>{
    await updateDoc(doc(ctx.firestore(),'chats/pin438'),{admins:[],onlyAdminsCanPin:true});
  });
  await assertFails(togglePin438(pinAdmin438));
  await env.withSecurityRulesDisabled(async(ctx)=>{
    await updateDoc(doc(ctx.firestore(),'chats/pin438'),{onlyAdminsCanPin:false});
  });
  await assertSucceeds(updateDoc(doc(pinMember438,'chats/pin438/messages/message'),{pinned:true,pinnedBy:'pin438member',pinnedAt:serverTimestamp()}));
  await assertFails(updateDoc(doc(env.authenticatedContext('pin438outside').firestore(),'chats/pin438/messages/message'),{pinned:false,pinnedBy:'pin438outside'}));
