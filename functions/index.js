import {initializeApp} from 'firebase-admin/app';
import {getAuth} from 'firebase-admin/auth';
import {getFirestore, Timestamp} from 'firebase-admin/firestore';
import {onRequest} from 'firebase-functions/v2/https';
import {defineSecret, defineString} from 'firebase-functions/params';
import {AccessToken, RoomServiceClient, WebhookReceiver} from 'livekit-server-sdk';
import {randomUUID} from 'node:crypto';
import {LiveError, gifts, giftCost, requireActive, validRecipient, pkLive, finishPK, validId} from './live-domain.js';
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
  const canPublish = validRecipient(stream, uid);
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
  if (action === 'publish') {
    const stream = (await ref.get()).data();
    requireActive(stream);
    if (!validRecipient(stream, uid)) throw new LiveError(403, 'Yayıncı iznin yok.');
    await roomService().updateParticipant(stream.roomName, uid, {permission: {canPublish:true, canSubscribe:true, canPublishData:false}});
    return {ok:true};
  }
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
      tx.update(ref, {guestUid: target, guestName: request.name, pk: null});
      tx.update(requestRef, {status: 'accepted', updatedAt: Timestamp.now()});
    });
    // Accepted users reconnect with a newly authorized token. Publishing is never enabled by a client write.
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
      tx.update(ref, {pk: action === 'pk-reject' ? {...stream.pk,status:'cancelled'} : {...stream.pk,status:'active',endsAtMs:Date.now()+stream.pk.seconds*1000}});
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
  if (action === 'gift') {
    const cost = giftCost(data.giftId, data.quantity), target = validId(data.targetUid);
    const eventRef = ref.collection('gifts').doc(`${uid}_${validId(data.requestId)}`);
    const senderRef = db.collection('wallets').doc(uid), recipientRef = db.collection('wallets').doc(target);
    await transaction(ref, async (tx, stream) => {
      const previous = await tx.get(eventRef);
      if (previous.exists) {
        const old = previous.data();
        if (old.giftId !== data.giftId || old.quantity !== data.quantity || old.recipientUid !== target) throw new LiveError(409, 'Gönderim kimliği başka bir işlemde kullanıldı.');
        return;
      }
      if (target === uid || !validRecipient(stream, target)) throw new LiveError(400, 'Hediye alıcısı yayında değil.');
      const sender = (await tx.get(senderRef)).data() || {}, recipient = (await tx.get(recipientRef)).data() || {};
      if (!Number.isSafeInteger(sender.coins) || sender.coins < cost) throw new LiveError(409, 'Jeton bakiyen yetersiz.');
      const earned = recipient.earnedCoins || 0;
      if (!Number.isSafeInteger(earned) || !Number.isSafeInteger(earned + cost)) throw new LiveError(409,'Cüzdan güncellenemedi.');
      tx.set(senderRef, {coins:sender.coins-cost, updatedAt:Timestamp.now()}, {merge:true});
      tx.set(recipientRef, {earnedCoins:earned+cost, updatedAt:Timestamp.now()}, {merge:true});
      tx.create(eventRef, {senderUid:uid, recipientUid:target, giftId:data.giftId, quantity:data.quantity, coins:cost, createdAt:Timestamp.now(), ...gifts[data.giftId]});
      if (pkLive(stream.pk, Date.now())) {
        const field = target === stream.ownerId ? 'hostScore' : 'guestScore';
        tx.update(ref, {pk:{...stream.pk,[field]:stream.pk[field]+cost}});
      }
    });
    return {ok:true, coins:cost};
  }
  if (action === 'leave') {
    const stream = (await ref.get()).data();
    if (!stream) return {ok:true};
    if (stream.ownerId === uid) {
      await ref.update({active:false,guestUid:'',endedAt:Timestamp.now(),pk:stream.pk?.status === 'active' ? {...finishPK(stream.pk),reason:'host_left'} : null});
      try { await roomService().deleteRoom(stream.roomName); } catch (e) { if (e.status !== 404 && e.code !== 'not_found') console.error('Room cleanup failed', e.message); }
    } else if (stream.guestUid === uid) {
      // Revoke publishing first so a former guest cannot retain a publish-capable connection.
      try { await roomService().removeParticipant(stream.roomName,uid); } catch (e) { if (e.status !== 404 && e.code !== 'not_found') throw e; }
      await transaction(ref, (tx,current) => {
        if (current.guestUid !== uid) return;
        tx.update(ref,{guestUid:'',guestName:'',pk:current.pk?.status==='active'?{...finishPK(current.pk),reason:'guest_left'}:null});
        tx.set(ref.collection('join_requests').doc(uid),{status:'left',updatedAt:Timestamp.now()},{merge:true});
      });
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
    if (event.event === 'room_finished') {
      await db.runTransaction(async tx => {const snap=await tx.get(ref);if(snap.data()?.active)tx.update(ref,{active:false,guestUid:'',endedAt:Timestamp.now()});});
    }
    if (event.event === 'participant_left') {
      // Reconnection gets a short grace period in LiveKit. This event represents actual departure.
      await db.runTransaction(async tx => {
        const snap = await tx.get(ref), stream=snap.data();
        if (!stream?.active || stream.guestUid !== event.participant?.identity) return;
        tx.update(ref,{guestUid:'',guestName:'',pk:stream.pk?.status==='active'?{...finishPK(stream.pk),reason:'guest_left'}:null});
        tx.set(ref.collection('join_requests').doc(stream.guestUid),{status:'left',updatedAt:Timestamp.now()},{merge:true});
      });
    }
    res.sendStatus(200);
  } catch (error) { console.error('Live webhook failed',error.message);res.sendStatus(400); }
});
