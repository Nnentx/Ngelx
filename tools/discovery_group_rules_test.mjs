import {assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,getDoc,serverTimestamp} from 'firebase/firestore';

export async function testDiscoveryGroupRules(env) {
  const base={isGroup:true,discoverable:true,joinApproval:true,groupDeleted:false,createdBy:'discoverAdmin',admins:['discoverAdmin'],members:['discoverAdmin'],formerMembers:[],hiddenFor:[],maxMembers:60};
  await env.withSecurityRulesDisabled(async ctx=>{
    const db=ctx.firestore();
    for(const [id,extra] of [['discover_approval',{}],['discover_private',{discoverable:false}],['discover_deleted',{groupDeleted:true}],['discover_full',{maxMembers:1}],['discover_open',{joinApproval:false}],['discover_deleted_open',{joinApproval:false,groupDeleted:true}]]) {
      await setDoc(doc(db,`chats/${id}`),{...base,...extra});
    }
  });
  const user=env.authenticatedContext('discoverUser').firestore(),admin=env.authenticatedContext('discoverAdmin').firestore();
  const other=env.authenticatedContext('discoverOther').firestore();
  const pending=()=>({uid:'discoverUser',status:'pending',source:'discover',createdAt:serverTimestamp(),updatedAt:serverTimestamp()});
  const request=doc(user,'chats/discover_approval/joinRequests/discoverUser');
  await assertSucceeds(getDoc(request));
  await assertSucceeds(setDoc(request,pending()));
  await assertSucceeds(getDoc(request));
  await assertFails(getDoc(doc(other,'chats/discover_approval/joinRequests/discoverUser')));
  await assertFails(updateDoc(request,{status:'accepted',updatedAt:serverTimestamp()}));
  await assertFails(updateDoc(doc(user,'chats/discover_approval'),{members:['discoverAdmin','discoverUser'],updatedAt:serverTimestamp()}));
  await assertSucceeds(updateDoc(request,{status:'cancelled',updatedAt:serverTimestamp()}));
  await assertSucceeds(setDoc(request,pending()));
  await assertSucceeds(updateDoc(doc(admin,'chats/discover_approval/joinRequests/discoverUser'),{status:'rejected',updatedAt:serverTimestamp()}));
  await assertSucceeds(setDoc(request,pending()));
  await assertFails(setDoc(doc(other,'chats/discover_approval/joinRequests/discoverOther'),{...pending(),uid:'discoverUser'}));
  await assertFails(setDoc(doc(other,'chats/discover_approval/joinRequests/discoverUser'),{...pending(),uid:'discoverOther'}));
  await assertFails(setDoc(doc(user,'chats/discover_approval/joinRequests/discoverUser'),{...pending(),status:'accepted'}));
  for(const id of ['discover_private','discover_deleted','discover_full','discover_open']) {
    await assertFails(setDoc(doc(user,`chats/${id}/joinRequests/discoverUser`),pending()));
  }
  await assertFails(setDoc(doc(other,'chats/discover_approval/joinRequests/discoverOther'),{...pending(),uid:'discoverOther',admin:true}));
  await assertSucceeds(updateDoc(doc(admin,'chats/discover_approval/joinRequests/discoverUser'),{status:'accepted',updatedAt:serverTimestamp()}));
  await assertFails(setDoc(request,pending()));
  await assertSucceeds(updateDoc(doc(admin,'chats/discover_approval'),{members:['discoverAdmin','discoverUser'],updatedAt:serverTimestamp()}));
  await assertFails(setDoc(request,pending()));
  await assertSucceeds(updateDoc(doc(user,'chats/discover_open'),{members:['discoverAdmin','discoverUser'],updatedAt:serverTimestamp()}));
  await assertFails(updateDoc(doc(user,'chats/discover_deleted_open'),{members:['discoverAdmin','discoverUser'],updatedAt:serverTimestamp()}));
  console.log('Keşfet grup onay/iptal/yeniden istek/özel-silinmiş-dolu grup kuralları emülatör testleri geçti.');
}
