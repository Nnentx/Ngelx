export class LiveError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
export const gifts = Object.freeze({
  rose: {name: 'Gül', emoji: '🌹', coins: 10},
  heart: {name: 'Kalp', emoji: '💗', coins: 25},
  clap: {name: 'Alkış', emoji: '👏', coins: 50},
  star: {name: 'Yıldız', emoji: '⭐', coins: 100},
  crown: {name: 'Taç', emoji: '👑', coins: 250},
  rocket: {name: 'Roket', emoji: '🚀', coins: 500},
});
export function requireActive(stream) {
  if (!stream || stream.active !== true) throw new LiveError(409, 'Yayın sona erdi.');
}
export function giftCost(id, quantity) {
  if (!Object.hasOwn(gifts, id) || !Number.isInteger(quantity) || quantity < 1 || quantity > 99) {
    throw new LiveError(400, 'Hediye ve adet geçersiz.');
  }
  return gifts[id].coins * quantity;
}
export function validRecipient(stream, uid) {
  return Boolean(uid) && [stream.ownerId, stream.guestUid].includes(uid);
}
export function pkLive(pk, now) {
  return pk?.status === 'active' && Number.isFinite(pk.endsAtMs) && now < pk.endsAtMs;
}
export function finishPK(pk) {
  const hostScore = pk.hostScore || 0, guestScore = pk.guestScore || 0;
  return {...pk, status: 'ended', result: hostScore === guestScore ? 'draw' : hostScore > guestScore ? 'host' : 'guest'};
}
export function validId(value, label = 'Kimlik') {
  if (typeof value !== 'string' || !/^[a-zA-Z0-9_-]{1,128}$/.test(value)) throw new LiveError(400, `${label} geçersiz.`);
  return value;
}

export function giftReceipt(giftId, quantity) {
  const cost = giftCost(giftId, quantity), gift = gifts[giftId];
  return {name:gift.name,emoji:gift.emoji,giftId,quantity,unitCoins:gift.coins,coins:cost};
}
