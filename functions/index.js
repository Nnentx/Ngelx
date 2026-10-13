import {initializeApp} from 'firebase-admin/app';
import {getAuth} from 'firebase-admin/auth';
import {getFirestore, Timestamp} from 'firebase-admin/firestore';
import {onRequest} from 'firebase-functions/v2/https';
import {onSchedule} from 'firebase-functions/v2/scheduler';
import {sendLiveGift} from './live-gifts.js';
import {authorizePublish,reconcileJoinedPublisher} from './live-permissions.js';
import {finalizeDeadline, endStream, departureChanges, joinedSessionChanges} from './live-lifecycle.js';
import {defineSecret, defineString} from 'firebase-functions/params';
import {AccessToken, RoomServiceClient, WebhookReceiver} from 'livekit-server-sdk';
import {randomUUID} from 'node:crypto';
import {LiveError, gifts, requireActive, validRecipient, pkLive, finishPK, validId} from './live-domain.js';
initializeApp();
const db = getFirestore();
const apiKey = defineSecret('LIVEKIT_API_KEY');
const apiSecret = defineSecret('LIVEKIT_API_SECRET');
const liveUrl = defineString('LIVEKIT_URL');
const options = {region: 'europe-west1', secrets: [apiKey, apiSecret], maxInstances: 10, timeoutSeconds: 30};
function roomService() { return new RoomServiceClient(liveUrl.value(), apiKey.value(), apiSecret.value()); }
function streamRef(id) { return db.collection('live_streams').doc(validId(id, 'Yayın')); }
function owner(stream, uid) { if (stream.ownerId !== uid) throw new LiveError(403, 'Bu işlem yayıncıya ait.'); }
function actorName(user) { return String(user.username || user.displayName || 'NgelX kullanıcısı').slice(0, 50); }
async function token(stream, uid) {
  requireActive(stream);
  const profile = (await db.collection('users').doc(uid).get()).data() || {};
  // Every fresh token is read-only. The publish endpoint authorizes the live session.
  const canPublish = false;
  const access = new AccessToken(apiKey.value(), apiSecret.value(), {
    identity: uid, name: actorName(profile), ttl: '15m',
    attributes: {role: stream.ownerId === uid ? 'host' : stream.guestUid === uid ? 'guest' : 'viewer'},
  });
  access.addGrant({room: stream.roomName, roomJoin: true, canSubscribe: true, canPublish, canPublishData: false});
  return {serverUrl: liveUrl.value(), participantToken: await access.toJwt()};
}
async function transaction(ref, apply) {
  return db.runTransaction(async tx => {
    const snapshot = await tx.get(ref), stream = snapshot.data();
    requireActive(stream);
    return apply(tx, stream);
  });
}
async function dispatch(action, uid, data) {
  if (action === 'start') {
    const title = String(data.title || '').trim().slice(0, 100);
    if (title.length < 3) throw new LiveError(400, 'En az 3 karakterlik yayın başlığı yaz.');
    const profile = (await db.collection('users').doc(uid).get()).data() || {};
    const ref = streamRef(validId(data.requestId));
    const stream = await db.runTransaction(async tx => {
      const existing = await tx.get(ref);
      if (existing.exists) { owner(existing.data(), uid); requireActive(existing.data()); return existing.data(); }
      const value = {ownerId: uid, username: actorName(profile), title, active: true,
        roomName: `live_${ref.id}`, startedAt: Timestamp.now(), guestUid: '', backendVersion: 1};
      tx.create(ref, value); return value;
    });
    return {id: ref.id, ...await token(stream, uid)};
  }
  if (action === 'catalog') return {gifts};
  const ref = streamRef(data.streamId);
  if (action === 'token') return token((await ref.get()).data(), uid);
  if (action === 'publish') return authorizePublish(db,ref,roomService(),uid);
  if (action === 'request' || action === 'invite') {
    const target = action === 'invite' ? validId(data.targetUid) : uid;
    const targetProfile = await db.collection('users').doc(target).get();
    if (!targetProfile.exists) throw new LiveError(404, 'Kullanıcı bulunamadı.');
    const profile = targetProfile.data();
    await transaction(ref, async (tx, stream) => {
      if (action === 'invite') owner(stream, uid);
      if (validRecipient(stream, target)) throw new LiveError(409, 'Bu kişi zaten yayında.');
      if (stream.guestUid) throw new LiveError(409, 'İki kişilik yayın dolu.');
      const requestRef = ref.collection('join_requests').doc(target);
      const existing = await tx.get(requestRef);
      if (['pending', 'invited', 'accepted'].includes(existing.data()?.status)) return;
      tx.set(requestRef, {uid: target, name: actorName(profile), status: action === 'invite' ? 'invited' : 'pending', createdAt: Timestamp.now()});
    });
    return {ok: true};
  }
  if (action === 'approve' || action === 'accept') {
    const target = action === 'approve' ? validId(data.targetUid) : uid;
    await transaction(ref, async (tx, stream) => {
      if (action === 'approve') owner(stream, uid);
      const requestRef = ref.collection('join_requests').doc(target), request = (await tx.get(requestRef)).data();
      if (stream.guestUid === target && request?.status === 'accepted') return;
      if (stream.guestUid) throw new LiveError(409, 'Yayındaki ikinci yer dolu.');
      if (!request || request.status !== (action === 'approve' ? 'pending' : 'invited')) throw new LiveError(409, 'Bu istek artık geçerli değil.');
      tx.update(ref, {guestUid: target, guestName: request.name, guestSlotId:randomUUID(), guestSession:null, pk: null});
      tx.update(requestRef, {status: 'accepted', updatedAt: Timestamp.now()});
    });
    // The server grants publishing through the publish endpoint after acceptance.
    return {ok: true};
  }
  if (action === 'reject') {
    const target = data.targetUid ? validId(data.targetUid) : uid;
    await transaction(ref, async (tx, stream) => {
      if (target !== uid) owner(stream, uid);
      const r = ref.collection('join_requests').doc(target), snap = await tx.get(r);
      if (!snap.exists || !['pending','invited'].includes(snap.data().status)) throw new LiveError(409, 'İstek kapandı.');
      tx.update(r, {status: target === uid ? 'cancelled' : 'rejected', updatedAt: Timestamp.now()});
    });
    return {ok: true};
  }
  if (action === 'pk-propose') {
    await transaction(ref, (tx, stream) => {
      owner(stream, uid);
      if (!stream.guestUid) throw new LiveError(409, 'Önce ikinci yayıncı katılmalı.');
      if (!Number.isInteger(data.seconds) || ![60,180,300].includes(data.seconds)) throw new LiveError(400, 'PK süresi geçersiz.');
      if (['pending','active'].includes(stream.pk?.status)) throw new LiveError(409, 'PK zaten açık.');
      tx.update(ref, {pk: {id: randomUUID(), status:'pending', seconds:data.seconds, guestUid:stream.guestUid, hostScore:0, guestScore:0}});
    });
    return {ok:true};
  }
  if (action === 'pk-accept' || action === 'pk-reject') {
    await transaction(ref, (tx, stream) => {
      if (uid !== stream.guestUid || stream.pk?.status !== 'pending' || stream.pk.guestUid !== uid) throw new LiveError(409, 'PK daveti geçerli değil.');
      const pk = action === 'pk-reject' ? {...stream.pk,status:'cancelled'}
        : {...stream.pk,status:'active',endsAtMs:Date.now()+stream.pk.seconds*1000};
      tx.update(ref, {pk});
      if (action === 'pk-accept') tx.set(db.collection('live_pk_deadlines').doc(ref.id), {
        pkId:pk.id, endsAtMs:pk.endsAtMs,
      });
    });
    return {ok:true};
  }
  if (action === 'pk-finish') {
    await transaction(ref, (tx, stream) => {
      if (stream.pk?.status !== 'active') return;
      if (pkLive(stream.pk, Date.now())) throw new LiveError(409, 'PK süresi henüz bitmedi.');
      tx.update(ref, {pk: finishPK(stream.pk)});
    });
    return {ok:true};
  }
  if (action === 'gift') return sendLiveGift(db,ref,uid,data,()=>Timestamp.now());
  if (action === 'leave') {
    const stream = (await ref.get()).data();
    if (!stream) return {ok:true};
    if (stream.ownerId === uid) {
      await db.runTransaction(async tx => {
        const current = (await tx.get(ref)).data();
        if (current?.active) tx.update(ref,endStream(current,'host_left',Timestamp.now()));
      });
      // Throw on cleanup failure so a retry can close the media room as well.
      try { await roomService().deleteRoom(stream.roomName); } catch (e) { if (e.status !== 404 && e.code !== 'not_found') throw e; }
    } else {
      // Clear the role before media revocation; concurrent publish must recheck it.
      await db.runTransaction(async tx => {
        const current = (await tx.get(ref)).data();
        if (!current?.active || current.guestUid !== uid) return;
        tx.update(ref,{guestUid:'',guestName:'',guestSlotId:'',guestSession:null,pk:current.pk?.status==='active'?{...finishPK(current.pk),reason:'guest_left'}:current.pk?.status==='pending'?{...current.pk,status:'cancelled'}:current.pk??null});
        tx.set(ref.collection('join_requests').doc(uid),{status:'left',updatedAt:Timestamp.now()},{merge:true});
      });
      // Remove this identity even on retry after the role was already cleared.
      try { await roomService().removeParticipant(stream.roomName,uid); }
      catch (e) { if (e.status !== 404 && e.code !== 'not_found') throw e; }
    }
    return {ok:true};
  }
  throw new LiveError(404, 'İşlem bulunamadı.');
}
export const ngelxLive = onRequest({...options,cors:true}, async (req,res) => {
  if (req.method !== 'POST') return res.status(405).json({message:'POST gerekli.'});
  try {
    const auth = req.headers.authorization || '';
    if (!auth.startsWith('Bearer ')) throw new LiveError(401,'Oturum açmalısın.');
    let claims;
    try { claims = await getAuth().verifyIdToken(auth.slice(7),true); } catch (_) { throw new LiveError(401,'Oturum geçersiz.'); }
    if (claims.firebase?.sign_in_provider === 'anonymous') throw new LiveError(403,'Üye hesabı gerekli.');
    const action = req.path.split('/').filter(Boolean).at(-1);
    const result = await dispatch(action,claims.uid,req.body || {});
    res.json(result);
  } catch (error) {
    const status = error instanceof LiveError ? error.status : 500;
    if (status === 500) console.error('Live action failed',error);
    res.status(status).json({message:status===500?'İşlem tamamlanamadı. Yeniden dene.':error.message});
  }
});
export const ngelxLiveWebhook = onRequest(options, async (req,res) => {
  try {
    const receiver = new WebhookReceiver(apiKey.value(),apiSecret.value());
    const event = await receiver.receive(req.rawBody.toString(),req.headers.authorization);
    const roomName = event.room?.name || '';
    if (!roomName.startsWith('live_')) return res.sendStatus(200);
    const ref = streamRef(roomName.slice(5));
    if (event.event === 'participant_joined') {
      await reconcileJoinedPublisher(ref,roomService(),roomName,event.participant);
      await db.runTransaction(async tx => {
        const stream = (await tx.get(ref)).data();
        const changes = joinedSessionChanges(stream,event.participant,event.createdAt);
        if (changes) tx.update(ref,changes);
      });
    }
    if (event.event === 'room_finished') {
      await db.runTransaction(async tx => {
        const stream = (await tx.get(ref)).data();
        if (stream?.active) tx.update(ref,endStream(stream,'room_finished',Timestamp.now()));
      });
    }
    if (event.event === 'participant_left') {
      // Ignore an old session's departure after the same identity reconnects.
      let hostLeft = false;
      await db.runTransaction(async tx => {
        const stream = (await tx.get(ref)).data();
        const changes = departureChanges(stream,event.participant?.identity,event.participant?.sid,Timestamp.now());
        hostLeft = changes?.active === false;
        // Retry a failed room deletion even when a previous attempt already closed Firestore.
        if (!stream?.active && event.participant?.identity === stream?.ownerId
            && event.participant?.sid === stream?.hostSession?.sid) hostLeft = true;
        if (!changes) return;
        tx.update(ref,changes);
        if (!hostLeft) tx.set(ref.collection('join_requests').doc(event.participant.identity),{status:'left',updatedAt:Timestamp.now()},{merge:true});
      });
      if (hostLeft) {
        try { await roomService().deleteRoom(roomName); }
        catch (e) { if (e.status !== 404 && e.code !== 'not_found') throw e; }
      }
    }
    res.sendStatus(200);
  } catch (error) { console.error('Live webhook failed',error.message);res.sendStatus(400); }
});

// A server fallback finalizes matches even if all app screens are closed.
// Each run processes at most 500 due records; overlapping retries are transactional.
export const ngelxFinishExpiredPK = onSchedule({region:'europe-west1',schedule:'every 1 minutes',
  timeZone:'UTC',maxInstances:1,timeoutSeconds:120,retryCount:3}, async () => {
  const now = Date.now();
  for (let page=0;page<5;page++) {
    const due = await db.collection('live_pk_deadlines').where('endsAtMs','<=',now).orderBy('endsAtMs').limit(100).get();
    if (due.empty) break;
    for (let start=0;start<due.docs.length;start+=10) {
      await Promise.all(due.docs.slice(start,start+10).map(d => finalizeDeadline(db,d.ref,streamRef(d.id),now)));
    }
  }
});
