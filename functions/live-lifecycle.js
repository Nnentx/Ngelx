import {finishPK} from './live-domain.js';

// A delayed deadline from a previous match must never finish the new match.
export function expiredPK(stream, deadline, now) {
  const pk = stream?.pk;
  if (stream?.active !== true || pk?.status !== 'active' || pk.id !== deadline?.pkId
      || !Number.isFinite(pk.endsAtMs) || pk.endsAtMs > now) return null;
  return finishPK(pk);
}

export async function finalizeDeadline(db, deadlineRef, streamRef, now) {
  return db.runTransaction(async tx => {
    const deadline = (await tx.get(deadlineRef)).data();
    if (!deadline || deadline.endsAtMs > now) return;
    const stream = (await tx.get(streamRef)).data();
    const result = expiredPK(stream, deadline, now);
    if (result) tx.update(streamRef, {pk: result});
    tx.delete(deadlineRef);
  });
}

export function endStream(stream, reason, endedAt) {
  return {active:false, guestUid:'', guestName:'', endedAt,
    ...(stream.pk ? {pk: stream.pk.status === 'active'
      ? {...finishPK(stream.pk), reason}
      : stream.pk.status === 'pending' ? {...stream.pk,status:'cancelled',reason} : stream.pk} : {})};
}

export function departureChanges(stream, identity, sid, endedAt) {
  if (stream?.active !== true || !sid) return null;
  if (identity === stream.ownerId && sid === stream.hostSession?.sid) {
    return endStream(stream, 'host_left', endedAt);
  }
  if (identity === stream.guestUid && sid === stream.guestSession?.sid) {
    return {guestUid:'',guestName:'',guestSession:null,
      ...(stream.pk ? {pk:stream.pk.status === 'active'
        ? {...finishPK(stream.pk),reason:'guest_left'}
        : stream.pk.status === 'pending' ? {...stream.pk,status:'cancelled',reason:'guest_left'} : stream.pk} : {})};
  }
  return null;
}

export function participantSession(participant, eventCreatedAt = 0) {
  const joinedAtMs = Number(participant?.joinedAtMs || Number(participant?.joinedAt || eventCreatedAt) * 1000);
  if (!participant?.sid || !Number.isFinite(joinedAtMs) || joinedAtMs <= 0) return null;
  return {sid:participant.sid,joinedAtMs};
}
export function joinedSessionChanges(stream, participant, eventCreatedAt) {
  if (stream?.active !== true) return null;
  const field = participant?.identity === stream.ownerId ? 'hostSession'
    : participant?.identity === stream.guestUid ? 'guestSession' : null;
  const session = participantSession(participant,eventCreatedAt);
  if (!field || !session || (stream[field] && session.joinedAtMs <= stream[field].joinedAtMs)) return null;
  return {[field]:session};
}
