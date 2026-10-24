import {getApps,initializeApp} from 'firebase-admin/app';
import {getAuth} from 'firebase-admin/auth';
import {getFirestore} from 'firebase-admin/firestore';
import {onRequest} from 'firebase-functions/v2/https';
import {defineSecret,defineString} from 'firebase-functions/params';
import {createFirestoreRateLimiter} from '../livekit443/firestore-adapters.mjs';
import {createVerificationHandler561} from './handler.mjs';
if(!getApps().length)initializeApp();
const emailKey=defineSecret('NGELX_EMAIL_API_KEY');
const emailFrom=defineString('NGELX_EMAIL_FROM');
export const verificationEmail561=onRequest({region:'europe-west1',memory:'256MiB',timeoutSeconds:30,maxInstances:2,cors:false,secrets:[emailKey]},async(req,res)=>{
  res.set('Cache-Control','no-store');
  if(req.method!=='POST'){res.status(405).json({error:'method-not-allowed'});return;}
  if(!req.is('application/json')||(req.rawBody?.length??0)>2048){res.status(400).json({error:'invalid-request'});return;}
  const handler=createVerificationHandler561({
    verifyToken:token=>getAuth().verifyIdToken(token,true),
    rateLimit:uid=>createFirestoreRateLimiter({db:getFirestore()})(`verification561:${uid}`,3),
    getUser:uid=>getAuth().getUser(uid),
    generateLink:email=>getAuth().generateEmailVerificationLink(email),
    send:async({to,...template})=>{
      const from=emailFrom.value();
      if(!/^NgelX <[^\s<>@]+@[^\s<>@]+\.[^\s<>@]+>$/.test(from))throw Error('sender-not-configured');
      const response=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${emailKey.value()}`,'Content-Type':'application/json'},body:JSON.stringify({from,to:[to],...template}),signal:AbortSignal.timeout(12000)});
      if(!response.ok)throw Error('delivery-failed');
    },
  });
  const result=await handler({token:/^Bearer (\S+)$/.exec(req.get('authorization')??'')?.[1],body:req.body});
  res.status(result.status).json(result.body);
});
