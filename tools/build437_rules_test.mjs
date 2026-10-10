  // Automatic receipts and shared emoji do not require a friendship/follow relationship.
  await env.withSecurityRulesDisabled(async(ctx)=>{
    const db=ctx.firestore();
    for(const id of ['qa437a','qa437b'])await setDoc(doc(db,'users/'+id),{blocked:[],friends:[],following:[],followers:[]});
    await setDoc(doc(db,'chats/qa437private'),{isGroup:false,members:['qa437a','qa437b'],readReceipts_qa437a:false,typingIndicator_qa437a:false});
    await setDoc(doc(db,'chats/qa437group'),{isGroup:true,members:['qa437a','qa437b'],admins:['qa437a'],createdBy:'qa437a',groupName:'Preserved group'});
  });
  const a437=env.authenticatedContext('qa437a').firestore(),b437=env.authenticatedContext('qa437b').firestore();
  for(const id of ['qa437private','qa437group']){
    await assertSucceeds(updateDoc(doc(b437,'chats/'+id),{quickEmoji:'❤️',quickEmojiUpdatedBy:'qa437b',quickEmojiUpdatedAt:serverTimestamp()}));
    const selected=await assertSucceeds(getDoc(doc(a437,'chats/'+id)));
    if(selected.data().quickEmoji!=='❤️')throw new Error('Shared emoji does not reach the other member');
    await assertSucceeds(updateDoc(doc(a437,'chats/'+id),{lastReadAt_qa437a:serverTimestamp(),unread_qa437a:0,typing_qa437a:serverTimestamp()}));
  }
  await env.withSecurityRulesDisabled(async(ctx)=>{await updateDoc(doc(ctx.firestore(),'users/qa437a'),{blocked:['qa437b']});});
  await assertFails(updateDoc(doc(b437,'chats/qa437private'),{quickEmoji:'😂'}));
  await assertFails(updateDoc(doc(b437,'chats/qa437private'),{lastReadAt_qa437b:serverTimestamp()}));
