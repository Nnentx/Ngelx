import fs from 'node:fs';import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';import {doc,setDoc,updateDoc,getDoc,getDocs,collection,serverTimestamp} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
try{
 await env.clearFirestore();await env.withSecurityRulesDisabled(async c=>{const db=c.firestore();await setDoc(doc(db,'live_streams/l448'),{ownerId:'host',active:true,visibility:'public'});});
 const host=env.authenticatedContext('host').firestore(),guest=env.authenticatedContext('guest').firestore(),attacker=env.authenticatedContext('attacker').firestore();
 const gr=doc(guest,'live_streams/l448/guest_requests/guest'),gp={liveId:'l448',hostUid:'host',guestUid:'guest',status:'pending',startedBy:'guest',updatedAt:serverTimestamp()};
 await assertFails(setDoc(gr,{...gp,status:'accepted'}));await assertFails(setDoc(doc(attacker,'live_streams/l448/guest_requests/guest'),gp));await assertSucceeds(setDoc(gr,gp));await assertFails(updateDoc(gr,{status:'accepted'}));await assertSucceeds(updateDoc(doc(host,'live_streams/l448/guest_requests/guest'),{status:'accepted'}));await assertSucceeds(updateDoc(gr,{status:'rejected'}));await assertSucceeds(setDoc(doc(host,'live_streams/l448/guest_requests/guest'),{...gp,status:'invited',startedBy:'host'}));await assertSucceeds(updateDoc(gr,{status:'accepted'}));await assertFails(updateDoc(gr,{hostUid:'guest'}));await assertFails(getDocs(collection(guest,'live_streams/l448/guest_requests')));
 const privateGuest=env.authenticatedContext('privateGuest').firestore();
 const privateProfile=doc(privateGuest,'users/privateGuest');
 const privateRequest=doc(host,'live_streams/l448/guest_requests/privateGuest');
 const invitation={...gp,guestUid:'privateGuest',status:'invited',startedBy:'host'};
 await assertSucceeds(setDoc(privateProfile,{allowLiveInvites:false}));
 await assertFails(setDoc(privateRequest,invitation));
 const ownRequest=doc(privateGuest,'live_streams/l448/guest_requests/privateGuest');
 await assertSucceeds(setDoc(ownRequest,{...invitation,status:'pending',startedBy:'privateGuest'}));
 await assertSucceeds(updateDoc(ownRequest,{status:'rejected'}));
 await assertFails(setDoc(privateRequest,invitation));
 await assertSucceeds(updateDoc(privateProfile,{allowLiveInvites:true}));
 await assertSucceeds(setDoc(privateRequest,invitation));
 console.log('Live guest consent and invitation privacy passed');
}finally{await env.cleanup();}
