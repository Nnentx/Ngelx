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
    getGuest:async (liveId,uid)=>{
      const guest=dataOf(await guestRef(liveId,uid).get());
      if(guest?.status!=='accepted')return guest;
      // Build529: never trust a client-provided slot/count/capability. The
      // same document-id ordering as the token endpoint limits publication
      // to the first ten accepted guest requests. Overflow may still be
      // kicked, but mute/unmute must never elevate an 11th viewer.
      const accepted=await liveRef(liveId).collection('guest_requests')
        .where('status','==','accepted')
        .orderBy('__name__').limit(11).get();
      return {...guest,
        guestCapacityAllowed:accepted.docs.slice(0,10).some(d=>d.id===uid)};
    },
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
