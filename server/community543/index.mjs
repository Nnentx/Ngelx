// PREPARED ONLY. No production deploy is part of Build543.
import {getAuth} from 'firebase-admin/auth';
import {getFirestore,FieldValue} from 'firebase-admin/firestore';
import {initializeApp,getApps} from 'firebase-admin/app';
import {onRequest} from 'firebase-functions/v2/https';
import {createFirestoreRateLimiter} from '../livekit443/firestore-adapters.mjs';
import {createCommunityDelete543,validateDelete543} from './delete-policy.mjs';
if(!getApps().length)initializeApp();
export const communityDelete543=onRequest({region:'europe-west1',memory:'256MiB',timeoutSeconds:540,maxInstances:2,cors:false},async(req,res)=>{
 res.set('Cache-Control','no-store');
 if(!req.is('application/json')||(req.rawBody?.length??0)>4096){res.status(400).json({error:'invalid_request'});return;}
 const db=getFirestore(),limiter=createFirestoreRateLimiter({db});
 const root=id=>db.collection('communities450').doc(id),job=id=>db.collection('community_deletions543').doc(id);
 const handle=createCommunityDelete543({
  verify:token=>getAuth().verifyIdToken(token,true),
  rateLimit:uid=>limiter('community-delete543:'+uid,5),
  lookup:async id=>{const [c,j]=await Promise.all([root(id).get(),job(id).get()]);return {community:c.data(),job:j.data()};},
  begin:async(identity,body)=>db.runTransaction(async tx=>{
   const c=await tx.get(root(body.communityId));
   if(!validateDelete543(identity,c.data(),body))return false;
   tx.set(job(body.communityId),{ownerUid:identity.uid,name:c.data().name,state:'deleting',requestedAt:FieldValue.serverTimestamp()},{merge:true});
   tx.update(root(body.communityId),{deletion543:{state:'deleting',ownerUid:identity.uid},paused:true});return true;
  }),
  // Firestore's recursive delete includes posts and all nested comments, likes,
  // reports, requests, invites and audit records. Never delete unrelated users,
  // chats or externally shared media URLs using an untrusted client URL.
  erase:async id=>{await db.recursiveDelete(root(id));},
  finish:async(id,uid)=>{await job(id).set({ownerUid:uid,state:'done',completedAt:FieldValue.serverTimestamp()},{merge:true});},
 });
 const result=await handle({method:req.method,authorization:req.get('authorization'),body:req.body});
 res.status(result.status).json(result.body);
});
