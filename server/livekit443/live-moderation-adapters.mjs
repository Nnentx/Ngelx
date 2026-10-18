/** Firebase Admin storage adapter for Build499 moderation (server-only). */
import {activeRoom} from './room-policy.mjs';

const dataOf = snapshot => snapshot?.exists ? snapshot.data() : null;

export function createGuestModerationStorage({db,FieldValue,now=()=>Date.now()}) {
  if (!db || !FieldValue?.arrayUnion || !FieldValue?.arrayRemove || !FieldValue?.serverTimestamp)
    throw Error('Firestore Admin dependencies required');
  const liveRef=liveId=>db.collection('live_streams').doc(liveId);
  const guestRef=(liveId,uid)=>liveRef(liveId).collection('guest_requests').doc(uid);
  return {
    getRoom:async liveId=>dataOf(await liveRef(liveId).get()),
    getGuest:async (liveId,uid)=>dataOf(await guestRef(liveId,uid).get()),
    saveAction:async ({liveId,guestUid,ownerUid,roomName,action})=>
      db.runTransaction(async tx=>{
        const r=liveRef(liveId),g=guestRef(liveId,guestUid);
        const room=dataOf(await tx.get(r)),guest=dataOf(await tx.get(g));
        if (!room || room.ownerId!==ownerUid || room.roomName!==roomName ||
            !activeRoom(room,now()) ||
            !guest || guest.hostUid!==ownerUid || guest.guestUid!==guestUid ||
            guest.status!=='accepted') throw Error('moderation_state_changed');
        if(action==='mute') tx.update(r,{guestAudioMutedUids:FieldValue.arrayUnion(guestUid)});
        else if(action==='unmute') tx.update(r,{guestAudioMutedUids:FieldValue.arrayRemove(guestUid)});
        else if(action==='kick'){
          tx.update(r,{guestAudioMutedUids:FieldValue.arrayRemove(guestUid)});
          tx.update(g,{status:'rejected',updatedAt:FieldValue.serverTimestamp()});
        } else throw Error('invalid_moderation_action');
      })
  };
}
