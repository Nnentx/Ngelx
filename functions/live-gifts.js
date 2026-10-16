import {LiveError,giftCost,giftReceipt,requireActive,validRecipient,validId,pkLive} from './live-domain.js';

export async function sendLiveGift(db,ref,uid,data,nowTimestamp,nowMs=Date.now) {
  const cost=giftCost(data.giftId,data.quantity), target=validId(data.targetUid);
  const eventRef=ref.collection('gifts').doc(`${uid}_${validId(data.requestId)}`);
  const senderRef=db.collection('wallets').doc(uid),recipientRef=db.collection('wallets').doc(target);
  await db.runTransaction(async tx=>{
    // A committed receipt is acknowledged even after the stream closes.
    const previous=(await tx.get(eventRef)).data();
    if(previous) {
      if(previous.giftId!==data.giftId||previous.quantity!==data.quantity||previous.recipientUid!==target) {
        throw new LiveError(409,'Gönderim kimliği başka bir işlemde kullanıldı.');
      }
      return;
    }
    const stream=(await tx.get(ref)).data();
    requireActive(stream);
    if(target===uid||!validRecipient(stream,target))throw new LiveError(400,'Hediye alıcısı yayında değil.');
    const sender=(await tx.get(senderRef)).data()||{},recipient=(await tx.get(recipientRef)).data()||{};
    if(!Number.isSafeInteger(sender.coins)||sender.coins<cost)throw new LiveError(409,'Jeton bakiyen yetersiz.');
    const earned=recipient.earnedCoins??0;
    if(!Number.isSafeInteger(earned)||earned<0||!Number.isSafeInteger(earned+cost))throw new LiveError(409,'Cüzdan güncellenemedi.');
    const scoring=pkLive(stream.pk,nowMs());
    const field=target===stream.ownerId?'hostScore':'guestScore';
    if(scoring&&(!Number.isSafeInteger(stream.pk[field])||stream.pk[field]<0||!Number.isSafeInteger(stream.pk[field]+cost))) {
      throw new LiveError(409,'PK puanı güncellenemedi.');
    }
    const createdAt=nowTimestamp();
    tx.set(senderRef,{coins:sender.coins-cost,updatedAt:createdAt},{merge:true});
    tx.set(recipientRef,{earnedCoins:earned+cost,updatedAt:createdAt},{merge:true});
    tx.create(eventRef,{senderUid:uid,recipientUid:target,createdAt,...giftReceipt(data.giftId,data.quantity)});
    if(scoring)tx.update(ref,{pk:{...stream.pk,[field]:stream.pk[field]+cost}});
  });
  return {ok:true,coins:cost};
}
