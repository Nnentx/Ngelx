import fs from 'node:fs';
import {accessToken} from '../call-push/src/google.mjs';
const cfToken=process.env.CLOUDFLARE_API_TOKEN,account=process.env.CLOUDFLARE_ACCOUNT_ID;
if(!cfToken||!account||!process.env.NGELX_EMAIL_API_KEY)throw Error('Required deployment secrets missing');
async function cf(path){const r=await fetch(`https://api.cloudflare.com/client/v4/accounts/${account}/${path}`,{headers:{Authorization:'Bearer '+cfToken},signal:AbortSignal.timeout(10000)});if(!r.ok)throw Error(`Free plan cannot be verified: ${path} HTTP ${r.status}`);const j=await r.json();if(!j.success)throw Error('Cloudflare verification failed');return j.result;}
const sub=await cf('workers/subdomain');if(sub.subdomain!=='alihancaglar76')throw Error('Unexpected account; refused');
let planError;let subscriptions=[];try{subscriptions=await cf('subscriptions');}catch(error){planError=error;console.log('Workers plan check blocked; continuing read-only Firebase diagnostics.');}
if(!Array.isArray(subscriptions))throw Error('Cannot verify subscriptions');
for(const s of subscriptions){const rate=JSON.stringify(s.rate_plan??{}).toLowerCase();if(rate.includes('worker')&&!rate.includes('free'))throw Error('Workers paid subscription detected; refused');}
const raw=process.env.FIREBASE_SERVICE_ACCOUNT_NGELX_44EED;if(!raw)throw Error('Firebase identity missing');
let sa;try{sa=JSON.parse(raw);}catch{sa=JSON.parse(Buffer.from(raw,'base64').toString());}
if(sa.project_id!=='ngelx-44eed')throw Error('Wrong project');
const env={FIREBASE_PROJECT_ID:'ngelx-44eed',GOOGLE_SERVICE_ACCOUNT:JSON.stringify(sa)};
const auth=await accessToken(env);const headers={Authorization:'Bearer '+auth,'Content-Type':'application/json'};
const lookup=await fetch('https://identitytoolkit.googleapis.com/v1/projects/ngelx-44eed/accounts:lookup',{method:'POST',headers,body:JSON.stringify({localId:['__free_email_preflight_nonexistent__']})});if(!lookup.ok)throw Error('Auth lookup permission unavailable: '+lookup.status);
const oob=await fetch('https://identitytoolkit.googleapis.com/v1/projects/ngelx-44eed/accounts:sendOobCode',{method:'POST',headers,body:JSON.stringify({requestType:'VERIFY_EMAIL',email:'__free_email_preflight_nonexistent__@example.invalid',returnOobLink:true})});const oobResult=await oob.json();
if(oob.status!==400||oobResult.error?.message!=='EMAIL_NOT_FOUND')throw Error('Auth link permission not verified: '+oob.status);
const read=await fetch('https://firestore.googleapis.com/v1/projects/ngelx-44eed/databases/(default)/documents/_verification_free/__preflight_nonexistent__',{headers});if(![200,404].includes(read.status))throw Error('Quota datastore permission unavailable: '+read.status);
if(planError)throw planError;
fs.writeFileSync('cloudflare/verification-email/.secrets-email.json',JSON.stringify({RESEND_API_KEY:process.env.NGELX_EMAIL_API_KEY,GOOGLE_SERVICE_ACCOUNT:JSON.stringify(sa)}),{mode:0o600});
fs.writeFileSync('free-email-preflight.json',JSON.stringify({freePlanVerified:true,subdomain:sub.subdomain,authLookup:true,authLinkPermission:true,checkedAt:new Date().toISOString()}));
console.log('Free plan and Firebase permissions verified. No email sent, no billing change.');
