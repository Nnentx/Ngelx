import {LiveError,requireActive,validRecipient} from './live-domain.js';
import {participantSession} from './live-lifecycle.js';

export function requirePublisher(stream,uid) {
  requireActive(stream);
  if (!validRecipient(stream,uid)) throw new LiveError(403,'Yayıncı iznin yok.');
}

// Network calls stay outside transactions. Both role and connection are checked
// again after granting permission, so an intervening leave cannot retain access.
export async function authorizePublish(db,ref,service,uid) {
  const stream = (await ref.get()).data();
  requirePublisher(stream,uid);
  const participant = await service.getParticipant(stream.roomName,uid);
  const session = participantSession(participant);
  if (!session) throw new LiveError(409,'Yayın bağlantısı hazır değil.');
  const slot = stream.ownerId === uid ? 'host' : stream.guestSlotId;
  try {
    await service.updateParticipant(stream.roomName,uid,{permission:{canPublish:true,canSubscribe:true,canPublishData:false}});
    const connected = await service.getParticipant(stream.roomName,uid);
    if (connected.sid !== session.sid) throw new LiveError(409,'Yayın bağlantısı değişti. Tekrar dene.');
    await db.runTransaction(async tx => {
      const current = (await tx.get(ref)).data();
      requirePublisher(current,uid);
      const currentSlot = current.ownerId === uid ? 'host' : current.guestSlotId;
      if (currentSlot !== slot) throw new LiveError(409,'Katılım iznin değişti. Tekrar dene.');
      const field = current.ownerId === uid ? 'hostSession' : 'guestSession';
      if (current[field] && current[field].joinedAtMs > session.joinedAtMs) throw new LiveError(409,'Yeni bağlantı zaten açıldı.');
      tx.update(ref,{[field]:session});
    });
  } catch (error) {
    // Do not swallow a failed revocation: remove the participant as a fallback.
    try { await service.updateParticipant(stream.roomName,uid,{permission:{canPublish:false}}); }
    catch (revokeError) {
      try { await service.removeParticipant(stream.roomName,uid); }
      catch (removeError) { if (removeError.status !== 404 && removeError.code !== 'not_found') throw removeError; }
    }
    throw error;
  }
  return {ok:true};
}

export async function reconcileJoinedPublisher(ref,service,roomName,participant) {
  const stream = (await ref.get()).data();
  if (stream?.active !== true) {
    try { await service.deleteRoom(roomName); }
    catch (error) { if (error.status !== 404 && error.code !== 'not_found') throw error; }
    return;
  }
  if (!validRecipient(stream,participant?.identity) && participant?.permission?.canPublish) {
    // Old tokens may still be valid until expiry; publishing is revoked on join.
    await service.updateParticipant(roomName,participant.identity,{permission:{canPublish:false}});
  }
}
