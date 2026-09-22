import fs from 'node:fs';
import assert from 'node:assert/strict';
import {
  initializeTestEnvironment,
  assertSucceeds,
  assertFails,
} from '@firebase/rules-unit-testing';
import {
  arrayRemove,
  arrayUnion,
  collection,
  doc,
  getDoc,
  getDocs,
  serverTimestamp,
  setDoc,
  updateDoc,
} from 'firebase/firestore';

const projectId = 'demo-ngelx';
const rules = fs.readFileSync('firestore.rules', 'utf8');

const env = await initializeTestEnvironment({
  projectId,
  firestore: {
    host: '127.0.0.1',
    port: 8080,
    rules,
  },
});

async function seed() {
  await env.withSecurityRulesDisabled(async (ctx) => {
    const db = ctx.firestore();

    await setDoc(doc(db, 'chats/group_open'), {
      isGroup: true,
      groupName: 'Açık Grup',
      groupPhotoUrl: '',
      groupDescription: '',
      members: ['admin'],
      admins: ['admin'],
      moderators: [],
      hiddenFor: ['bob'],
      onlyAdminsCanPost: false,
      onlyAdminsCanEdit: false,
      newMembersSeeHistory: true,
      joinApproval: false,
      inviteCode: 'CODE123',
      groupDeleted: false,
    });
    await setDoc(doc(db, 'group_invites/CODE123'), {
      chatId: 'group_open',
      groupName: 'Açık Grup',
      groupPhotoUrl: '',
      joinApproval: false,
      admins: ['admin'],
      memberCount: 1,
    });

    await setDoc(doc(db, 'chats/group_approval'), {
      isGroup: true,
      groupName: 'Onaylı Grup',
      groupPhotoUrl: '',
      groupDescription: '',
      members: ['admin'],
      admins: ['admin'],
      moderators: [],
      hiddenFor: ['carol'],
      onlyAdminsCanPost: false,
      onlyAdminsCanEdit: false,
      newMembersSeeHistory: true,
      joinApproval: true,
      inviteCode: 'CODE999',
      groupDeleted: false,
    });
    await setDoc(doc(db, 'group_invites/CODE999'), {
      chatId: 'group_approval',
      groupName: 'Onaylı Grup',
      groupPhotoUrl: '',
      joinApproval: true,
      admins: ['admin'],
      memberCount: 1,
    });
  });
}

try {
  await seed();

  const bob = env.authenticatedContext('bob').firestore();
  const admin = env.authenticatedContext('admin').firestore();
  const carol = env.authenticatedContext('carol').firestore();

  // Davet kodu sadece doğrudan belge olarak okunabilir; tüm davetler listelenemez.
  await assertSucceeds(getDoc(doc(bob, 'group_invites/CODE123')));
  await assertFails(getDocs(collection(bob, 'group_invites')));

  // Üye olmayan kişi grup belgesini doğrudan okuyamaz.
  await assertFails(getDoc(doc(bob, 'chats/group_open')));

  // Geçerli davet kodu ile autojoin talebi oluşturulabilir.
  await assertSucceeds(setDoc(doc(bob, 'chats/group_open/joinRequests/bob'), {
    uid: 'bob',
    status: 'autojoin',
    inviteCode: 'CODE123',
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp(),
  }));

  // Sahte/yanlış kod reddedilir.
  await assertFails(setDoc(doc(bob, 'chats/group_open/joinRequests/bad'), {
    uid: 'bob',
    status: 'autojoin',
    inviteCode: 'WRONG',
    createdAt: serverTimestamp(),
  }));

  // Autojoin isteği olan kullanıcı kendisini gruba ekleyebilir.
  await assertSucceeds(updateDoc(doc(bob, 'chats/group_open'), {
    members: arrayUnion('bob'),
    hiddenFor: arrayRemove('bob'),
    updatedAt: serverTimestamp(),
  }));

  const joined = await assertSucceeds(getDoc(doc(bob, 'chats/group_open')));
  assert.equal(joined.exists(), true);

  // Normal üye grup yönetim metadatasını değiştiremez.
  await assertFails(updateDoc(doc(bob, 'chats/group_open'), {
    inviteCode: 'HACKED',
  }));

  // Ancak kullanıcıya özel sohbet tercihleri/takma ad/arka plan gibi alanlar çalışır.
  await assertSucceeds(updateDoc(doc(bob, 'chats/group_open'), {
    nickname_bob: 'Bobby',
    backgroundUrl_bob: 'https://example.test/bg.jpg',
    backgroundOpacity_bob: 0.35,
    readReceipts_bob: false,
    typingIndicator_bob: false,
  }));

  // Yönetici onaylı grupta katılma isteği oluşturulabilir ama kullanıcı kendini ekleyemez.
  await assertSucceeds(setDoc(doc(carol, 'chats/group_approval/joinRequests/carol'), {
    uid: 'carol',
    status: 'pending',
    inviteCode: 'CODE999',
    createdAt: serverTimestamp(),
    updatedAt: serverTimestamp(),
  }));
  await assertFails(updateDoc(doc(carol, 'chats/group_approval'), {
    members: arrayUnion('carol'),
    hiddenFor: arrayRemove('carol'),
    updatedAt: serverTimestamp(),
  }));

  // Yönetici istekleri görebilir, onaylayabilir ve kullanıcıyı ekleyebilir.
  const pending = await assertSucceeds(getDocs(collection(admin, 'chats/group_approval/joinRequests')));
  assert.equal(pending.size, 1);
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_approval'), {
    members: arrayUnion('carol'),
    hiddenFor: arrayRemove('carol'),
    updatedAt: serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_approval/joinRequests/carol'), {
    status: 'accepted',
    decidedBy: 'admin',
    decidedAt: serverTimestamp(),
  }));

  // Kullanıcı artık grup üyesi olarak grubu okuyabilir.
  const approved = await assertSucceeds(getDoc(doc(carol, 'chats/group_approval')));
  assert.equal(approved.exists(), true);

  console.log('Firestore rules testleri başarılı.');
} finally {
  await env.cleanup();
}
