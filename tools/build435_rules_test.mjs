  await env.withSecurityRulesDisabled(async ctx=>{
    const db=ctx.firestore();
    await setDoc(doc(db,'chats/cleanup435'),{members:['alice','bob'],isGroup:false});
    await setDoc(doc(db,'chats/cleanup435/messages/photo'),{senderId:'alice',mediaUrl:'https://media.ngelxsocial.com/media/chats/alice/photo.jpg',text:'photo'});
  });
  const cleanupPath='chats/cleanup435/messages/photo';
  await assertSucceeds(updateDoc(doc(bob,cleanupPath),{hiddenFor:arrayUnion('bob')}));
  await assertFails(updateDoc(doc(bob,cleanupPath),{hiddenFor:arrayUnion('alice')}));
  await assertFails(updateDoc(doc(outsider,cleanupPath),{hiddenFor:arrayUnion('outsider')}));
  const deletion={deletedForEveryone:true,deletedBy:'alice',deletedAt:serverTimestamp(),mediaUrl:'',cleanupMediaUrls:['https://media.ngelxsocial.com/media/chats/alice/photo.jpg','','','','','','',''],mediaCleanupState:'pending'};
  await assertFails(updateDoc(doc(bob,cleanupPath),deletion));
  await assertFails(updateDoc(doc(alice,cleanupPath),{...deletion,cleanupMediaUrls:['https://media.ngelxsocial.com/media/chats/bob/private.jpg']}));
  await assertSucceeds(updateDoc(doc(alice,cleanupPath),deletion));
  await assertFails(updateDoc(doc(alice,cleanupPath),{cleanupMediaUrls:['other'],mediaCleanupState:'pending',deletedForEveryone:true}));
