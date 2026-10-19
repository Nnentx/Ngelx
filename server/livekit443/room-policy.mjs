const list = value => Array.isArray(value) ? value : [];
export const millis = value => typeof value?.toMillis === 'function' ? value.toMillis() :
  value instanceof Date ? value.getTime() : typeof value === 'number' ? value : NaN;
export const fresh = (value, now, maxAge) => {
  const age = now - millis(value);
  return Number.isFinite(age) && age >= -30_000 && age <= maxAge;
};
export const activeRoom = (room, now) => room?.active === true &&
  fresh(room.lastHeartbeatAt ?? room.startedAt, now, 120_000);
const blocked = (uid, ownerId, viewer, owner) =>
  list(viewer.blocked).includes(ownerId) || list(owner.blocked).includes(uid);
const usable = user => user && user.deactivated !== true && user.deleted !== true;

// No client role/name/publish attributes are accepted by this policy.
export function roomPermission({kind, room, uid, viewer, owner, peerId, now}) {
  if (!usable(viewer) || !usable(owner)) return null;
  const displayName = String(viewer.displayName ?? viewer.username ?? uid).slice(0, 80);
  if (kind === 'call') {
    const members = list(room.members);
    if (!members.includes(uid) || !members.includes(room.callStartedBy) ||
        !['ringing', 'active'].includes(room.callStatus) ||
        !fresh(room.callCreatedAt, now, room.callStatus === 'ringing' ? 120_000 : 12 * 3600_000)) return null;
    if (room.isGroup === true) {
      // Build517: leaving and moderation must be participant-scoped. Chat
      // membership alone must not let an explicitly removed caller obtain
      // a fresh LiveKit token for the same current call.
      const moderationRoom = room.callModerationRoom;
      const currentRoom = room.callRoomName;
      if (list(room.callKickedUids).includes(uid) &&
          (!moderationRoom || moderationRoom === currentRoom)) return null;
    }
    if (room.isGroup !== true && (members.length !== 2 || !peerId || !members.includes(peerId) ||
        peerId === uid || blocked(uid, peerId, viewer, owner))) return null;
    return {allowed:true, role:'caller', displayName, canPublish:true, canPublishData:true};
  }
  const ownerId = room.ownerId;
  if (!activeRoom(room, now) || !ownerId || blocked(uid, ownerId, viewer, owner) ||
      list(room.bannedUserIds).includes(uid) || list(room.bannedUsers).includes(uid)) return null;
  if (uid === ownerId) return {allowed:true, role:'host', displayName, canPublish:true, canPublishData:true};
  const visibility = room.visibility;
  const visible = ['public', 'Herkese açık'].includes(visibility) ||
      (['friends', 'Arkadaşlar'].includes(visibility) && list(owner.friends).includes(uid)) ||
      (['followers', 'Takipçiler'].includes(visibility) && list(owner.followers).includes(uid));
  if (!visible) return null;
  const guest=room.guestRequest;
  const speaker = kind === 'audio' && list(room.speakerIds).includes(uid) || kind==='live' && guest?.status==='accepted' && guest.hostUid===ownerId && guest.guestUid===uid;
  // A host-moderated guest may keep the camera while the microphone
  // publication source is denied on a fresh/reconnected LiveKit token.
  // This is not a substitute for server-side muting of existing audio tracks.
  const microphoneBlocked = kind === 'live' && speaker &&
    list(room.guestAudioMutedUids).includes(uid);
  return {allowed:true, role:speaker ? 'speaker' : 'listener', displayName,
    canPublish:speaker, canPublishData:true,
    ...(microphoneBlocked ? {canPublishSources:['camera']} : {})};
}

export function hostRequestKind(uid, roomName, now) {
  for (const [kind, prefix] of [['audio', `ngelx_audio_${uid}_`], ['live', `ngelx_${uid}_`]]) {
    if (!roomName.startsWith(prefix)) continue;
    const suffix = roomName.slice(prefix.length);
    if (!/^\d{13}$/.test(suffix) || !fresh(Number(suffix), now, 60_000)) return null;
    return kind;
  }
  return null;
}
