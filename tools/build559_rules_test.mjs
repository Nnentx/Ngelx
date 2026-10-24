import {readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {initializeTestEnvironment,assertFails,assertSucceeds} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc,deleteDoc,getDoc} from 'firebase/firestore';
const env=await initializeTestEnvironment({projectId:'demo-ngelx559',firestore:{host:'127.0.0.1',port:8080,rules:readFileSync('firestore.rules','utf8')}});
try{
 await env.withSecurityRulesDisabled(async c=>{
  await setDoc(doc(c.firestore(),'users/owner'),{displayName:'Original',username:'original',usernameLower:'original',bio:'Old',followers:[],following:[],friends:[]});
  await setDoc(doc(c.firestore(),'login_usernames/original'),{uid:'owner',status:'active'});
 });
 const me=env.authenticatedContext('owner').firestore(),other=env.authenticatedContext('other').firestore();
 await assertSucceeds(updateDoc(doc(me,'users/owner'),{bio:'Changed'}));
 for(const patch of [{displayName:'Bypass'},{username:'bypass'},{usernameLower:'bypass'},{displayNameChangedAt559:null},{usernameChangedAt559:null}])await assertFails(updateDoc(doc(me,'users/owner'),patch));
 await assertFails(deleteDoc(doc(me,'users/owner')));
 await assertFails(updateDoc(doc(other,'users/owner'),{bio:'Attack'}));
 await assertFails(getDoc(doc(me,'login_usernames/original')));
 await assertFails(setDoc(doc(me,'login_usernames/newname'),{uid:'owner',status:'active'}));
 await assertSucceeds(updateDoc(doc(other,'users/owner'),{followers:['other']}));
 const fresh=env.authenticatedContext('fresh').firestore();
 await assertFails(setDoc(doc(fresh,'users/fresh'),{displayName:'Fresh',username:'fresh',displayNameChangedAt559:null}));
 await assertSucceeds(setDoc(doc(fresh,'users/fresh'),{displayName:'Fresh',username:'fresh'}));
 assert.equal((await getDoc(doc(me,'users/owner'))).data().displayName,'Original');
 console.log('Build559 rules passed: identity/reset/index bypasses denied, normal profile and relationship writes preserved.');
}finally{await env.cleanup();}
