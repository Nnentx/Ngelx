/**
 * Build499: server-only live guest moderation, with injected Firebase/LiveKit APIs.
 * NO Flutter client or untrusted Firestore write may authorize room admin actions.
 * QA candidate only; no production deployment here.
 */
import {activeRoom} from './room-policy.mjs';

const validId = value => typeof value === 'string' && value.length > 0 &&
  value.length <= 128 && !value.includes('/') && !/\s/.test(value);
const response = (status, body) => ({
  status, headers:{'Content-Type':'application/json','Cache-Control':'no-store'}, body
});
const isAudio = (track, audioTrackType) =>
  track?.type === audioTrackType && typeof track.sid === 'string' && track.sid.length > 0;

/**
 * Backend adapters are injected and independently testable. The trusted room
 * name comes from Firestore, never the request. LiveKit updateParticipant is
 * deliberately called BEFORE muting any remaining audio tracks.
 */
export function createGuestModeration({
  verifyFirebaseToken, getRoom, getGuest, saveAction, rateLimit, roomService,
  cameraSource, microphoneSource, audioTrackType, now=()=>Date.now(),
}) {
  if ([verifyFirebaseToken,getRoom,getGuest,saveAction,rateLimit].some(fn=>typeof fn!=='function') ||
      !roomService || !['listParticipants','updateParticipant','mutePublishedTrack','removeParticipant']
        .every(key=>typeof roomService[key]==='function') ||
      cameraSource === undefined || microphoneSource === undefined ||
      audioTrackType === undefined) throw Error('Trusted moderation dependencies required');

  return async function moderate({method,authorization,body}) {
    if (method !== 'POST') return response(405,{error:'method_not_allowed'});
    const bearer = /^Bearer ([^\s]+)$/.exec(authorization??'');
    if (!bearer) return response(401,{error:'unauthorized'});
    let claims;
    try { claims=await verifyFirebaseToken(bearer[1],true); }
    catch { return response(401,{error:'unauthorized'}); }
    const uid=claims?.uid;
    if (!validId(uid) || claims.firebase?.sign_in_provider==='anonymous' || claims.disabled)
      return response(401,{error:'unauthorized'});
    const liveId=body?.liveId, guestUid=body?.guestUid, action=body?.action;
    if (!validId(liveId) || !validId(guestUid) ||
        !['mute','unmute','kick'].includes(action) || guestUid===uid ||
        Object.keys(body??{}).some(key=>!['liveId','guestUid','action'].includes(key)))
      return response(400,{error:'invalid_request'});
    try { if (!await rateLimit(uid)) return response(429,{error:'rate_limited'}); }
    catch { return response(503,{error:'temporarily_unavailable'}); }

    let room,guest;
    try {
      room=await getRoom(liveId);
      // The stored server-side room owner is the ONLY moderation authority.
      if (!room || room.ownerId!==uid || !activeRoom(room,now()) ||
          typeof room.roomName!=='string' || !/^[\w-]{1,160}$/.test(room.roomName))
        return response(403,{error:'forbidden'});
      guest=await getGuest(liveId,guestUid);
    } catch { return response(503,{error:'temporarily_unavailable'}); }
    if (guest?.hostUid!==uid || guest?.guestUid!==guestUid || guest?.status!=='accepted')
      return response(409,{error:'guest_not_accepted'});

    // RTC changes and Firestore transactions cannot be globally atomic.
    // Report any failure; never claim the remote action succeeded if it did not.
    try {
      const participants=await roomService.listParticipants(room.roomName);
      const connected=Array.isArray(participants) &&
        participants.some(p=>p.identity===guestUid);
      if (action==='kick') {
        if (connected) await roomService.removeParticipant(room.roomName,guestUid);
      } else if (connected) {
        await roomService.updateParticipant(room.roomName,guestUid,{
          permission:{
            // LiveKit applies permission updates as a complete replacement,
            // not a patch. Keep existing essential subscribe/data/publish rights.
            canSubscribe:true,
            canPublish:true,
            canPublishData:true,
            canUpdateMetadata:false,
            canPublishSources:action==='mute'
              ? [cameraSource] : [cameraSource,microphoneSource],
          }
        });
        if (action==='mute') {
          const updated=await roomService.listParticipants(room.roomName);
          const p=Array.isArray(updated)?updated.find(x=>x.identity===guestUid):null;
          for (const track of p?.tracks??[]) {
            if (isAudio(track,audioTrackType))
              await roomService.mutePublishedTrack(room.roomName,guestUid,track.sid,true);
          }
        }
      }
      // Server-only update, revalidated in a Firestore transaction.
      await saveAction({liveId,guestUid,ownerUid:uid,roomName:room.roomName,action,now:now()});
      return response(200,{ok:true,action});
    } catch {
      return response(503,{error:'temporarily_unavailable'});
    }
  };
}
