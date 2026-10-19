import {createHash} from 'node:crypto';
import {roomPermission, hostRequestKind, activeRoom, millis} from './room-policy.mjs';
const hash = text => createHash('sha256').update(text).digest('hex');
const value = snapshot => snapshot.exists ? snapshot.data() : null;

export function createFirestoreRoomAuthorizer({db, now=()=>Date.now()}) {
  return async ({uid, roomName}) => {
    const viewer = value(await db.collection('users').doc(uid).get());
    if (!viewer || viewer.deactivated === true || viewer.deleted === true) return null;
    for (const [kind, collection, field] of [
      ['call','chats','callRoomName'], ['audio','audio_rooms','roomName'], ['live','live_streams','roomName']]) {
      const matches = await db.collection(collection).where(field,'==',roomName).limit(2).get();
      if (matches.size > 1) return null;
      if (matches.empty) continue;
      const room = matches.docs[0].data();
      if(kind==='live'){
        const requests=matches.docs[0].ref.collection('guest_requests');
        room.guestRequest=value(await requests.doc(uid).get());
        const guest=room.guestRequest;
        if(guest?.status==='accepted'&&guest?.hostUid===room.ownerId&&
           guest?.guestUid===uid){
          // Build522: only ten accepted users may receive publish rights.
          // A deterministic document-id order makes repeated tokens stable
          // without trusting a client-supplied slot, role or guest count.
          // Query eleven to detect over-capacity records, never stream the
          // entire guest request collection to a viewer.
          const accepted=await requests.where('status','==','accepted')
            .orderBy('__name__').limit(11).get();
          room.guestCapacityAllowed=accepted.docs.slice(0,10)
            .some(record=>record.id===uid);
        }
      }
      const peerId = kind === 'call' && room.isGroup !== true
        ? room.members?.find(id=>id!==uid) : undefined;
      const ownerId = kind === 'call' ? peerId??room.callStartedBy : room.ownerId;
      if (typeof ownerId !== 'string' || !ownerId || ownerId.includes('/')) return null;
      const owner = value(await db.collection('users').doc(ownerId).get());
      return roomPermission({kind,room,uid,viewer,owner,peerId,now:now()});
    }
    // Prefix ownership only selects a reservation path; it never grants access.
    const kind = hostRequestKind(uid,roomName,now());
    if (!kind) return null;
    return db.runTransaction(async tx => {
      const userRef = db.collection('users').doc(uid);
      const lockRef = db.collection('_livekit_owner_locks').doc(hash(uid));
      const user = value(await tx.get(userRef));
      const lock = value(await tx.get(lockRef));
      if (!user || user.deactivated === true || user.deleted === true) return null;
      if (lock && millis(lock.expiresAt) > now() && lock.roomName !== roomName) return null;
      // Read existing app pointers before writes, including pre-deployment rooms.
      const pointers = [['audio_rooms',user.currentAudioRoomId], ['live_streams',user.currentLiveId]];
      for (const [collection,id] of pointers) {
        if (typeof id !== 'string' || !id || id.includes('/')) continue;
        const room = value(await tx.get(db.collection(collection).doc(id)));
        if (room && room.ownerId === uid && activeRoom(room,now()) && room.roomName !== roomName) return null;
      }
      if (lock?.roomName === roomName && millis(lock.expiresAt) <= now()) return null;
      // Retried initial requests never extend a pending reservation indefinitely.
      const expiresAt = lock?.roomName === roomName ? lock.expiresAt : new Date(now()+120_000);
      tx.set(lockRef,{uid,kind,roomName,expiresAt,updatedAt:new Date(now())});
      return {allowed:true,role:'host',displayName:String(user.displayName??user.username??uid).slice(0,80),
        canPublish:true,canPublishData:true};
    });
  };
}

export function createFirestoreRateLimiter({db, now=()=>Date.now()}) {
  return async (key, limit=30) => db.runTransaction(async tx => {
    const bucket = Math.floor(now()/60_000);
    const ref = db.collection('_livekit_rate_limits').doc(hash(key));
    const data = value(await tx.get(ref));
    const count = data?.bucket === bucket ? Number(data.count??0) : 0;
    if (!Number.isFinite(count) || count >= limit) return false;
    tx.set(ref,{bucket,count:count+1,expiresAt:new Date(now()+120_000)});
    return true;
  });
}
