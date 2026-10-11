  // Build438 canonical request coverage: pending targets cannot be overwritten.
  await env.withSecurityRulesDisabled(async(ctx)=>{
    await setDoc(doc(ctx.firestore(),'chats/pending438'),{isGroup:true,members:['qa438a','qa438b'],admins:['qa438a'],createdBy:'qa438a'});
  });
  const a438=env.authenticatedContext('qa438a').firestore(),b438=env.authenticatedContext('qa438b').firestore();
  const out438=env.authenticatedContext('qa438outside').firestore();
  const payload438={type:'member_add',uid:'qa438target',targetUid:'qa438target',targetName:'Target',targetPhoto:'',requestedBy:'qa438b',requestedByName:'B',requestedByPhoto:'',status:'pending',createdAt:serverTimestamp(),updatedAt:serverTimestamp()};
  await assertSucceeds(getDoc(doc(b438,'chats/pending438/joinRequests/qa438target')));
  await assertSucceeds(setDoc(doc(b438,'chats/pending438/joinRequests/qa438target'),payload438));
  await assertSucceeds(getDocs(collection(b438,'chats/pending438/joinRequests')));
  await assertFails(getDocs(collection(out438,'chats/pending438/joinRequests')));
  await assertFails(setDoc(doc(b438,'chats/pending438/joinRequests/qa438b_qa438target'),payload438));
  await assertFails(setDoc(doc(b438,'chats/pending438/joinRequests/qa438target'),{...payload438,targetName:'Overwritten'}));
  await assertSucceeds(updateDoc(doc(a438,'chats/pending438/joinRequests/qa438target'),{status:'rejected'}));
  await assertSucceeds(setDoc(doc(b438,'chats/pending438/joinRequests/qa438target'),payload438));
  await assertFails(setDoc(doc(out438,'chats/pending438/joinRequests/qa438other'),{...payload438,uid:'qa438other',targetUid:'qa438other',requestedBy:'qa438outside'}));
  // Two members concurrently request the same target: exactly one creates it.
  await env.withSecurityRulesDisabled(async(ctx)=>{
    await updateDoc(doc(ctx.firestore(),'chats/pending438'),{members:arrayUnion('qa438c')});
  });
  const c438=env.authenticatedContext('qa438c').firestore();
  const requestOnce438=(db,uid)=>runTransaction(db,async(tx)=>{
    const target=doc(db,'chats/pending438/joinRequests/qa438race');
    const existing=await tx.get(target);
    if(existing.data()?.status==='pending')return false;
    tx.set(target,{...payload438,uid:'qa438race',targetUid:'qa438race',requestedBy:uid});
    return true;
  });
  const race438=await Promise.all([requestOnce438(b438,'qa438b'),requestOnce438(c438,'qa438c')]);
  assert.equal(race438.filter(Boolean).length,1);
  const raceDoc438=await getDoc(doc(b438,'chats/pending438/joinRequests/qa438race'));
  assert.equal(raceDoc438.data().status,'pending');
  assert.ok(['qa438b','qa438c'].includes(raceDoc438.data().requestedBy));
