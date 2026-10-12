import {onDocumentWritten} from 'firebase-functions/v2/firestore';
import {getFirestore} from 'firebase-admin/firestore';
import {getMessaging} from 'firebase-admin/messaging';
import {callPushEvent} from './push-policy.mjs';
export const incomingCall448=onDocumentWritten({document:'chats/{chatId}',region:'europe-west1',memory:'256MiB',timeoutSeconds:60,maxInstances:3,retry:true},async event=>{
 const before=event.data?.before.data(),after=event.data?.after.data();
 const push=callPushEvent(before,after,Date.now());if(!push)return;
 const current=(await event.data.after.ref.get()).data();
 if(current?.callRoomName!==after.callRoomName||current?.callStatus!==after.callStatus)return;
 const db=getFirestore(),sender=(await db.collection('users').doc(after.callStartedBy).get()).data();
 if(!sender||sender.deleted||sender.deactivated)return;
 if(after.isGroup!==true)push.title=String(sender.displayName??sender.username??'NgelX araması').slice(0,100);
 for(const uid of push.recipients){
  const user=(await db.collection('users').doc(uid).get()).data();
  if(!user||user.deleted||user.deactivated||user.notificationsEnabled===false||user.blocked?.includes(after.callStartedBy)||sender.blocked?.includes(uid))continue;
  const devices=await db.collection('_call_devices').doc(uid).collection('tokens').limit(20).get();
  const tokens=[...new Set(devices.docs.map(d=>d.data().token).filter(t=>typeof t==='string'&&t.length>20&&t.length<4096))];
  if(!tokens.length)continue;
  const {recipients,...data}=push;
  const response=await getMessaging().sendEachForMulticast({tokens,data:{...data,recipientUid:uid,chatId:event.params.chatId},android:{priority:'high',ttl:60_000,collapseKey:push.roomName.slice(0,64)}});
  await Promise.all(response.responses.map(async(r,i)=>{if(['messaging/registration-token-not-registered','messaging/invalid-registration-token'].includes(r.error?.code)){for(const d of devices.docs.filter(d=>d.data().token===tokens[i]))await d.ref.delete();}}));
 }
});
