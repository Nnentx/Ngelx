import fs from 'node:fs';
import {initializeTestEnvironment,assertSucceeds,assertFails} from '@firebase/rules-unit-testing';
import {doc,setDoc,updateDoc} from 'firebase/firestore';

const env=await initializeTestEnvironment({projectId:'demo-ngelx',firestore:{
  host:'127.0.0.1',port:8080,rules:fs.readFileSync('firestore.rules','utf8')}});
const db=uid=>env.authenticatedContext(uid).firestore();
const community='communities450/legacy-owner457';
const fixture={
  name:'Legacy owner',description:'Legacy founder cover update',rules:'',category:'Sohbet',
  photoUrl:'',coverUrl:'',founderId:'owner',members:['owner','admin','member'],
  admins:['admin'],visibility:'public',joinApproval:false,postApproval:false,
  lastJoinCode:'',createdAt:new Date(),
};
try {
  await env.clearFirestore();
  // A legacy dataset may be missing the founder in its admins array.
  await env.withSecurityRulesDisabled(async ctx=>
    setDoc(doc(ctx.firestore(),community),fixture));
  await assertSucceeds(updateDoc(doc(db('owner'),community),{coverAlignment:.35}));
  await assertSucceeds(updateDoc(doc(db('owner'),community),{coverUrl:'https://example.com/cover.jpg'}));
  await assertSucceeds(updateDoc(doc(db('admin'),community),{coverAlignment:.45}));
  await assertFails(updateDoc(doc(db('owner'),community),{admins:['owner','admin']}));
  await assertFails(updateDoc(doc(db('owner'),community),{visibility:'private'}));
  await assertFails(updateDoc(doc(db('member'),community),{coverAlignment:.15}));
  await assertFails(updateDoc(doc(db('outsider'),community),{coverAlignment:.2}));
  console.log('Build457: legacy founder can edit cover only, not members or visibility');
}finally{await env.cleanup();}
