// Prepared account services. Deploy only these exports with reviewed user rules.
import {getApps,initializeApp} from 'firebase-admin/app';
import {getAuth} from 'firebase-admin/auth';
import {getFirestore} from 'firebase-admin/firestore';
import {onRequest} from 'firebase-functions/v2/https';
import {defineSecret,defineString} from 'firebase-functions/params';
import {createFirestoreRateLimiter} from '../livekit443/firestore-adapters.mjs';
import {updateIdentity,verificationEmail} from './policy.mjs';
if(!getApps().length)initializeApp();
const emailKey=defineSecret('NGELX_EMAIL_API_KEY');
const emailFrom=defineString('NGELX_EMAIL_FROM');
const options={region:'europe-west1',memory:'256MiB',timeoutSeconds:30,maxInstances:2,cors:false};
function endpoint(work,extra={}){return onRequest({...options,...extra},async(req,res)=>{
 res.set('Cache-Control','no-store');
 if(req.method!=='POST'){res.status(405).json({error:'method-not-allowed'});return;}
 if(!req.is('application/json')||(req.rawBody?.length??0)>2048){res.status(400).json({error:'invalid-request'});return;}
 let user;
 try{const token=/^Bearer (\S+)$/.exec(req.get('authorization')??'')?.[1];if(!token)throw Error();user=await getAuth().verifyIdToken(token,true);}catch{res.status(401).json({error:'unauthenticated'});return;}
 try{
  const allowed=await createFirestoreRateLimiter({db:getFirestore()})(`account559:${req.path}:${user.uid}`,3);
  if(!allowed){res.status(429).json({error:'rate-limit'});return;}
  res.status(200).json(await work(user,req.body));
 }catch(e){
  const known=['cooldown','username-taken','invalid-username','invalid-name','invalid-request','profile-required','ownership-conflict'];
  res.status(known.includes(e.message)?409:503).json({error:known.includes(e.message)?e.message:'unavailable'});
 }
});}
export const profileIdentity559=endpoint(async(user,body)=>updateIdentity({db:getFirestore(),uid:user.uid,body}));
export const verificationEmail559=endpoint(async(user,body)=>{
 if(!body||Array.isArray(body)||Object.keys(body).length)throw Error('invalid-request');
 const account=await getAuth().getUser(user.uid);
 if(account.disabled||!account.email)throw Error('invalid-request');
 if(account.emailVerified)return {verified:true};
 const link=await getAuth().generateEmailVerificationLink(account.email);
 const action=new URL(link);action.searchParams.set('lang','tr');
 const template=verificationEmail({name:account.displayName,link:action.toString()});
 const from=emailFrom.value();
 if(!/^NgelX <[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+>$/.test(from))throw Error('sender-not-configured');
 const response=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${emailKey.value()}`,'Content-Type':'application/json'},body:JSON.stringify({from,to:[account.email],...template}),signal:AbortSignal.timeout(12000)});
 if(!response.ok)throw Error('delivery-failed');
 return {sent:true};
},{secrets:[emailKey]});
