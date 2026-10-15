import fs from 'node:fs';
import {
  initializeTestEnvironment,
  assertSucceeds,
  assertFails,
} from '@firebase/rules-unit-testing';
import {
  arrayUnion,
  collection,
  deleteDoc,
  doc,
  getDoc,
  getDocs,
  serverTimestamp,
  setDoc,
  updateDoc,
} from 'firebase/firestore';

const env = await initializeTestEnvironment({
  projectId: 'demo-ngelx-community450',
  firestore: {
    host: '127.0.0.1',
    port: 8080,
    rules: fs.readFileSync('firestore.rules', 'utf8'),
  },
});

try {
  await env.withSecurityRulesDisabled(async (c) => {
    const db = c.firestore();
    for (const [id, visibility] of [['public', 'public'], ['private', 'private']]) {
      await setDoc(doc(db, 'communities450', id), {
        name: 'Example community',
        description: '',
        rules: '',
        founderId: 'founder',
        admins: ['founder', 'admin'],
        members: ['founder', 'admin', 'member'],
        moderators: ['moderator'],
        visibility,
        joinApproval: false,
        postApproval: false,
      });
    }
    await setDoc(doc(db, 'communities450/public/posts/post1'), {
      authorId: 'member', authorName: 'Member', authorPhoto: '',
      text: 'Hello', mediaType: '', mediaUrl: '', status: 'approved',
      pinned: false, commentsClosed: false,
    });
    await setDoc(doc(db, 'communityInvites450/TESTCODE'), {
      communityId: 'private', name: 'Example community',
      joinApproval: false, createdBy: 'founder',
      expiresAt: new Date(Date.now() + 60000),
    });
  });

  const founder = env.authenticatedContext('founder').firestore();
  const admin = env.authenticatedContext('admin').firestore();
  const member = env.authenticatedContext('member').firestore();
  const moderator = env.authenticatedContext('moderator').firestore();
  const guest = env.authenticatedContext('guest').firestore();
  const publicDb = env.unauthenticatedContext().firestore();

  const publicRoot = 'communities450/public';
  const privateRoot = 'communities450/private';
  const post = publicRoot + '/posts/post1';

  await assertSucceeds(getDoc(doc(publicDb, publicRoot)));
  await assertFails(getDoc(doc(guest, privateRoot)));
  await assertSucceeds(getDoc(doc(member, privateRoot)));
  await assertSucceeds(getDocs(collection(admin, privateRoot + '/requests')));
  await assertFails(getDocs(collection(guest, privateRoot + '/requests')));

  await assertSucceeds(updateDoc(doc(admin, publicRoot), { joinApproval: true }));
  await assertFails(updateDoc(doc(guest, publicRoot), { joinApproval: false }));
  await assertFails(updateDoc(doc(admin, publicRoot), { admins: arrayUnion('guest') }));
  await assertFails(updateDoc(doc(founder, publicRoot), { founderId: 'guest' }));
  await assertFails(deleteDoc(doc(founder, publicRoot)));

  await assertSucceeds(updateDoc(doc(admin, post), { commentsClosed: true }));
  await assertFails(updateDoc(doc(guest, post), { commentsClosed: false }));
  await assertFails(setDoc(doc(member, post + '/comments/rejected'), {
    uid: 'member', name: 'Member', text: 'Not allowed', createdAt: serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(admin, post), { commentsClosed: false }));
  await assertSucceeds(setDoc(doc(member, post + '/comments/accepted'), {
    uid: 'member', name: 'Member', text: 'Allowed', createdAt: serverTimestamp(),
  }));
  await assertFails(setDoc(doc(guest, post + '/comments/fake'), {
    uid: 'member', name: 'Member', text: 'Impersonation', createdAt: serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(moderator, post), { slowSeconds: 300 }));
  await assertSucceeds(getDocs(collection(publicDb, post + '/comments')));

  await assertSucceeds(setDoc(doc(member, privateRoot + '/requests/member'), {
    uid: 'member', status: 'pending', inviteCode: '', createdAt: serverTimestamp(),
  }));
  await assertSucceeds(updateDoc(doc(admin, privateRoot + '/requests/member'), { status: 'approved' }));
  await assertFails(updateDoc(doc(guest, privateRoot + '/requests/member'), { status: 'approved' }));

  await assertSucceeds(getDoc(doc(guest, 'communityInvites450/TESTCODE')));
  await assertFails(getDocs(collection(guest, 'communityInvites450')));

  console.log('Community450 permission emulator tests passed.');
} finally {
  await env.cleanup();
}
