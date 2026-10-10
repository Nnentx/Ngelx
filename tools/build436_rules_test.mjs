  // Test exact null/missing manifests, blocked shared writes, reopen and two-sided requests.
  await env.withSecurityRulesDisabled(async(ctx)=>{
    const db=ctx.firestore();
    for(const id of ['qa436a','qa436b'])await setDoc(doc(db,'users/'+id),{blocked:[],friends:[],following:[],followers:[]});
    await setDoc(doc(db,'chats/qa436'),{isGroup:false,members:['qa436a','qa436b']});
    await setDoc(doc(db,'chats/qa436/messages/null-media'),{senderId:'qa436a',type:'text',text:'hello',mediaUrl:null,createdAt:serverTimestamp()});
  });
  const a436=env.authenticatedContext('qa436a').firestore(),b436=env.authenticatedContext('qa436b').firestore();
  await assertSucceeds(getDoc(doc(a436,'friend_requests/qa436b/outgoing/qa436a')));
  for(const [kind,type] of [['friend_requests','friend_request'],['follow_requests','follow_request']]){
    await assertSucceeds(setDoc(doc(a436,kind+'/qa436a/outgoing/qa436b'),{fromUid:'qa436a',toUid:'qa436b',type,status:'pending',notificationId:'qa436-'+type,requestGeneration:'1',createdAt:serverTimestamp(),updatedAt:serverTimestamp()}));
  }
  await assertSucceeds(updateDoc(doc(a436,'chats/qa436/messages/null-media'),{
    deletedForEveryone:true,deletedAt:serverTimestamp(),deletedBy:'qa436a',cleanupMediaUrls:[null,'','','','','','',''],mediaCleanupState:'pending',text:'',mediaUrl:'',videoUrl:'',audioUrl:'',fileUrl:'',thumbnailUrl:'',posterUrl:'',coverUrl:'',imageUrl:'',fileName:'',linkUrl:'',reactions:{},pinned:false,pinnedAt:null,pinnedBy:null,
  }));
  await assertSucceeds(updateDoc(doc(a436,'chats/qa436'),{nicknames:{qa436b:'Nickname'},theme:123,backgroundUrl:''}));
  await env.withSecurityRulesDisabled(async(ctx)=>{await updateDoc(doc(ctx.firestore(),'users/qa436a'),{blocked:['qa436b']});});
  await assertFails(updateDoc(doc(b436,'chats/qa436'),{backgroundUrl:'https://example.test/new.jpg'}));
  await assertFails(updateDoc(doc(a436,'chats/qa436'),{nicknames:{qa436b:'Blocked nickname'}}));
  await assertFails(setDoc(doc(b436,'chats/qa436/messages/blocked-system'),{senderId:'qa436b',actorUid:'qa436b',type:'system',systemAction:'background_changed',text:'changed'}));
  await assertFails(setDoc(doc(b436,'friend_requests/qa436b/outgoing/qa436a'),{fromUid:'qa436b',toUid:'qa436a',type:'friend_request',status:'pending'}));
  await assertFails(updateDoc(doc(b436,'friend_requests/qa436a/outgoing/qa436b'),{status:'accepted'}));
  await assertSucceeds(updateDoc(doc(b436,'follow_requests/qa436a/outgoing/qa436b'),{status:'cancelled'}));
  await assertSucceeds(updateDoc(doc(a436,'friend_requests/qa436a/outgoing/qa436b'),{status:'cancelled'}));
  await env.withSecurityRulesDisabled(async(ctx)=>{await updateDoc(doc(ctx.firestore(),'users/qa436a'),{blocked:[]});});
  await assertSucceeds(updateDoc(doc(b436,'chats/qa436'),{backgroundUrl:'https://example.test/restored.jpg'}));
