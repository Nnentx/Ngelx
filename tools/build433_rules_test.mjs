  // Build433 host cleanup can remove other users' children; outsiders cannot.
  await env.withSecurityRulesDisabled(async context=>{
    const db=context.firestore();
    await setDoc(doc(db,'live_streams/ended433'),{ownerId:'alice',active:false,status:'ended'});
    await setDoc(doc(db,'live_streams/ended433/comments/bob'),{userId:'bob',text:'live comment'});
    await setDoc(doc(db,'live_streams/ended433/reactions/bob'),{uid:'bob',count:1});
    await setDoc(doc(db,'live_streams/ended433/viewers/bob'),{uid:'bob'});
  });
  for(const path of ['comments/bob','reactions/bob','viewers/bob']){
    await assertFails(deleteDoc(doc(outsider,'live_streams/ended433/'+path)));
    await assertSucceeds(deleteDoc(doc(alice,'live_streams/ended433/'+path)));
  }
  await assertFails(deleteDoc(doc(outsider,'live_streams/ended433')));
  await assertSucceeds(deleteDoc(doc(alice,'live_streams/ended433')));
