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
      createdBy: 'admin',
      formerMembers: ['bob'],
      hiddenFor: ['bob'],
      onlyAdminsCanPost: false,
      onlyAdminsCanAddMembers: false,
      onlyAdminsCanEditGroup: true,
      onlyAdminsCanPin: true,
      onlyAdminsCanMentionAll: false,
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
      createdBy: 'admin',
      formerMembers: ['carol'],
      hiddenFor: ['carol'],
      onlyAdminsCanPost: false,
      onlyAdminsCanAddMembers: false,
      onlyAdminsCanEditGroup: true,
      onlyAdminsCanPin: true,
      onlyAdminsCanMentionAll: false,
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

    await setDoc(doc(db, 'chats/group_solo'), {
      isGroup: true,
      groupName: 'Tek Kişilik Grup',
      groupPhotoUrl: '',
      groupDescription: '',
      members: ['solo'],
      admins: ['solo'],
      moderators: [],
      createdBy: 'solo',
      formerMembers: [],
      hiddenFor: [],
      onlyAdminsCanPost: false,
      onlyAdminsCanAddMembers: false,
      onlyAdminsCanEditGroup: true,
      onlyAdminsCanPin: true,
      onlyAdminsCanMentionAll: false,
      newMembersSeeHistory: true,
      joinApproval: false,
      inviteCode: '',
      groupDeleted: false,
    });

    await setDoc(doc(db, 'chats/group_founder_multi'), {
      isGroup: true,
      groupName: 'Kuruculu Grup',
      groupPhotoUrl: '',
      groupDescription: '',
      members: ['founder', 'bob'],
      admins: ['founder', 'bob'],
      moderators: [],
      createdBy: 'founder',
      formerMembers: [],
      hiddenFor: [],
      onlyAdminsCanPost: false,
      onlyAdminsCanAddMembers: false,
      onlyAdminsCanEditGroup: true,
      onlyAdminsCanPin: true,
      onlyAdminsCanMentionAll: false,
      newMembersSeeHistory: true,
      joinApproval: false,
      inviteCode: '',
      groupDeleted: false,
    });
    await setDoc(doc(db, 'users/alice'), {
      messagePermission: 'all',
      friends: [],
      following: [],
    });
    await setDoc(doc(db, 'users/friend_target'), {
      messagePermission: 'friends',
      friends: ['bob'],
      following: [],
    });
    await setDoc(doc(db, 'users/following_target'), {
      messagePermission: 'following',
      friends: [],
      following: ['bob'],
    });
    await setDoc(doc(db, 'users/closed_target'), {
      messagePermission: 'none',
      friends: [],
      following: [],
    });
    await setDoc(doc(db, 'users/stranger_target'), {
      messagePermission: 'friends',
      friends: [],
      following: [],
    });
  });
}

try {
  await seed();

  const bob = env.authenticatedContext('bob').firestore();
  const outsider = env.authenticatedContext('outsider').firestore();
  const admin = env.authenticatedContext('admin').firestore();
  const carol = env.authenticatedContext('carol').firestore();
  const solo = env.authenticatedContext('solo').firestore();
  const founder = env.authenticatedContext('founder').firestore();

  // Özel sohbet oluşturma, hedef hesabın mesaj gizliliğini sunucu tarafında da uygular.
  await assertSucceeds(setDoc(doc(bob, 'chats/dm_all'), {
    isGroup: false,
    members: ['alice', 'bob'],
    lastMessage: '',
  }));
  await assertSucceeds(setDoc(doc(bob, 'chats/dm_friend'), {
    isGroup: false,
    members: ['bob', 'friend_target'],
    lastMessage: '',
  }));
  await assertSucceeds(setDoc(doc(bob, 'chats/dm_following'), {
    isGroup: false,
    members: ['bob', 'following_target'],
    lastMessage: '',
  }));
  await assertFails(setDoc(doc(bob, 'chats/dm_closed'), {
    isGroup: false,
    members: ['bob', 'closed_target'],
    lastMessage: '',
  }));
  await assertFails(setDoc(doc(bob, 'chats/dm_stranger'), {
    isGroup: false,
    members: ['bob', 'stranger_target'],
    lastMessage: '',
  }));
  await assertFails(setDoc(doc(bob, 'chats/fake_private_group'), {
    isGroup: false,
    members: ['alice', 'bob', 'outsider'],
    lastMessage: '',
  }));


  // Davet kodu sadece doğrudan belge olarak okunabilir; tüm davetler listelenemez.
  await assertSucceeds(getDoc(doc(bob, 'group_invites/CODE123')));
  await assertFails(getDocs(collection(bob, 'group_invites')));

  // Üye veya eski üye olmayan kişi grup belgesini doğrudan okuyamaz.
  await assertFails(getDoc(doc(outsider, 'chats/group_open')));

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
    formerMembers: arrayRemove('bob'),
    hiddenFor: arrayRemove('bob'),
    updatedAt: serverTimestamp(),
  }));

  const joined = await assertSucceeds(getDoc(doc(bob, 'chats/group_open')));
  assert.equal(joined.exists(), true);
  assert.equal(joined.data().formerMembers.includes('bob'), false);

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

  // Granüler grup izinleri: açık grupta üye ekleme serbestken normal üye yeni üye ekleyebilir.
  await assertSucceeds(updateDoc(doc(bob, 'chats/group_open'), {
    members: arrayUnion('eve'),
    hiddenFor: arrayRemove('eve'),
    updatedAt: serverTimestamp(),
  }));

  // Yönetici üye eklemeyi yalnızca yöneticilere kapatınca normal üye artık ekleyemez.
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_open'), {
    onlyAdminsCanAddMembers: true,
    updatedAt: serverTimestamp(),
  }));
  await assertFails(updateDoc(doc(bob, 'chats/group_open'), {
    members: arrayUnion('mallory'),
    hiddenFor: arrayRemove('mallory'),
    updatedAt: serverTimestamp(),
  }));

  // Grup bilgisi varsayılan olarak yöneticiye özel; açılırsa normal üye açıklamayı değiştirebilir.
  await assertFails(updateDoc(doc(bob, 'chats/group_open'), {
    groupDescription: 'Yetkisiz değişiklik',
    updatedAt: serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_open'), {
    onlyAdminsCanEditGroup: false,
    updatedAt: serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(bob, 'chats/group_open'), {
    groupDescription: 'Üye tarafından izinli değişiklik',
    updatedAt: serverTimestamp(),
  }));

  // Mesaj sabitleme yöneticilere özelken üye sabitleyemez, yönetici sabitleyebilir.
  await assertSucceeds(setDoc(doc(bob, 'chats/group_open/messages/msg1'), {
    senderId: 'bob',
    type: 'text',
    text: 'Merhaba',
    createdAt: serverTimestamp(),
  }));
  await assertFails(updateDoc(doc(bob, 'chats/group_open/messages/msg1'), {
    pinned: true,
    pinnedAt: serverTimestamp(),
    pinnedBy: 'bob',
  }));
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_open/messages/msg1'), {
    pinned: true,
    pinnedAt: serverTimestamp(),
    pinnedBy: 'admin',
  }));

  // Yönetici herkesten sil işleminde belgeyi yok etmek yerine tombstone bırakabilir.
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_open/messages/msg1'), {
    deletedForEveryone: true,
    deletedAt: serverTimestamp(),
    deletedBy: 'admin',
    text: '',
    mediaUrl: '',
    audioUrl: '',
    fileUrl: '',
    fileName: '',
    reactions: {},
    pinned: false,
    pinnedAt: null,
    pinnedBy: null,
  }));

  // Anket özelliği kaldırıldı: eski/yanlış istemciler poll mesajı oluşturamaz.
  await assertFails(setDoc(doc(bob, 'chats/group_open/messages/poll_removed'), {
    senderId: 'bob',
    type: 'poll',
    text: 'Bu oluşturulmamalı',
    createdAt: serverTimestamp(),
  }));

  // Sadece yöneticiler yazsın açıldığında normal üye mesaj oluşturamaz.
  await assertSucceeds(updateDoc(doc(admin, 'chats/group_open'), {
    onlyAdminsCanPost: true,
    updatedAt: serverTimestamp(),
  }));
  await assertFails(setDoc(doc(bob, 'chats/group_open/messages/blocked_msg'), {
    senderId: 'bob',
    type: 'text',
    text: 'Gönderilememeli',
    createdAt: serverTimestamp(),
  }));
  await assertSucceeds(setDoc(doc(admin, 'chats/group_open/messages/admin_msg'), {
    senderId: 'admin',
    type: 'text',
    text: 'Yönetici mesajı',
    createdAt: serverTimestamp(),
  }));

  // Normal mesaj kapalı olsa bile üyelik/arama sistem olayları aktörün kendi kimliğiyle yazılabilir.
  await assertSucceeds(setDoc(doc(bob, 'chats/group_open/messages/member_event'), {
    senderId: 'bob',
    type: 'system',
    systemAction: 'call_join',
    actorUid: 'bob',
    callVideo: true,
    text: 'Bobby görüntülü aramaya katıldı.',
    createdAt: serverTimestamp(),
  }));
  await assertFails(setDoc(doc(bob, 'chats/group_open/messages/forged_event'), {
    senderId: 'bob',
    type: 'system',
    systemAction: 'call_join',
    actorUid: 'admin',
    text: 'Sahte olay',
    createdAt: serverTimestamp(),
  }));
  await assertFails(setDoc(doc(bob, 'chats/group_open/messages/unknown_event'), {
    senderId: 'bob',
    type: 'system',
    systemAction: 'owner_override',
    actorUid: 'bob',
    text: 'Bilinmeyen olay',
    createdAt: serverTimestamp(),
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
    formerMembers: arrayRemove('carol'),
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
  assert.equal(approved.data().formerMembers.includes('carol'), false);

  // Kurucu tek üyeyse grubu güvenli biçimde kapatabilir.
  await assertSucceeds(updateDoc(doc(solo, 'chats/group_solo'), {
    members: arrayRemove('solo'),
    admins: arrayRemove('solo'),
    groupDeleted: true,
    deletedAt: serverTimestamp(),
  }));

  // Kurucu, başka üyeler varken kuruculuğu devretmeden kendisini çıkaramaz.
  await assertFails(updateDoc(doc(founder, 'chats/group_founder_multi'), {
    members: arrayRemove('founder'),
    admins: arrayRemove('founder'),
    formerMembers: arrayUnion('founder'),
    removedAt_founder: serverTimestamp(),
    updatedAt: serverTimestamp(),
  }));

  console.log('Firestore rules testleri başarılı.');
} finally {
  await env.cleanup();
}
