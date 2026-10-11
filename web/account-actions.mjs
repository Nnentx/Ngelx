// Shared with emulator tests; credentials never enter Firestore payloads.
export async function requestAccountDeletion(db, sdk, uid, now = Date.now()) {
  if (!uid) throw new Error('sign-in-required');
  const profile = sdk.doc(db, 'users', uid);
  const request = sdk.doc(db, 'account_deletion_requests', uid);
  return sdk.runTransaction(db, async tx => {
    const user = await tx.get(profile);
    const previous = await tx.get(request);
    if (!user.exists()) throw new Error('profile-unavailable');
    const old = previous.data();
    if (user.data().deactivated === true && user.data().deletionRequestedAt && old?.status === 'scheduled' && old.executeAfter instanceof sdk.Timestamp) {
      return {alreadyScheduled:true, executeAfter:old.executeAfter.toDate()};
    }
    const executeAfter = sdk.Timestamp.fromMillis(now + 30 * 24 * 60 * 60 * 1000);
    tx.set(profile, {deactivated:true, deletionRequestedAt:sdk.serverTimestamp(), deletionScheduledFor:executeAfter}, {merge:true});
    tx.set(request, {uid, status:'scheduled', requestedAt:sdk.serverTimestamp(), executeAfter, source:'web', policyVersion:'play-2026-10'});
    return {alreadyScheduled:false, executeAfter:executeAfter.toDate()};
  });
}

export function supportPayload(user, category, description, sdk) {
  const categories = ['Uygulama hatası','Hesap ve giriş','Güvenlik','Ödeme ve kazanç','Öneri','Diğer'];
  const text = description.trim();
  if (!user?.uid) throw new Error('sign-in-required');
  if (!categories.includes(category) || text.length < 10 || text.length > 1000) throw new Error('invalid-description');
  return {uid:user.uid, email:user.email || '', category, description:text, screenshotUrl:'', status:'open', source:'web', createdAt:sdk.serverTimestamp()};
}
