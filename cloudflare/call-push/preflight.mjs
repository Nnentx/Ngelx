import fs from 'node:fs';import {accessToken} from './src/google.mjs';
const token=process.env.CLOUDFLARE_API_TOKEN,account=process.env.CLOUDFLARE_ACCOUNT_ID;
if(!token||!account)throw Error('Existing Cloudflare deployment credentials unavailable');
async function cf(path){const r=await fetch(`https://api.cloudflare.com/client/v4/accounts/${account}/${path}`,{headers:{authorization:'Bearer '+token}});if(!r.ok)throw Error('Cloudflare read permission missing for '+path.split('/')[0]);const v=await r.json();if(!v.success)throw Error('Cloudflare lookup failed');return v.result;}
const raw=process.env.FIREBASE_SERVICE_ACCOUNT_NGELX_44EED||process.env.FIREBASE_SERVICE_ACCOUNT||process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON;
if(!raw)throw Error('Existing Firebase server credentials unavailable');
let service;try{service=JSON.parse(raw);}catch{service=JSON.parse(Buffer.from(raw,'base64').toString());}
const env={FIREBASE_PROJECT_ID:'ngelx-44eed',GOOGLE_SERVICE_ACCOUNT:JSON.stringify(service)};
const bearer=await accessToken(env);
const headers={authorization:'Bearer '+bearer,'content-type':'application/json'};
const db='https://firestore.googleapis.com/v1/projects/ngelx-44eed/databases/(default)/documents/_call_push_rate452/__preflight';
const created=await fetch(db,{method:'PATCH',headers,body:JSON.stringify({fields:{window:{integerValue:'0'},count:{integerValue:'0'}}})});if(!created.ok)throw Error('Firebase service account requires Firestore data read/write permission');
const deleted=await fetch(db,{method:'DELETE',headers});if(!deleted.ok)throw Error('Preflight record cleanup failed');
const lookup=await fetch('https://identitytoolkit.googleapis.com/v1/projects/ngelx-44eed/accounts:lookup',{method:'POST',headers,body:JSON.stringify({localId:['__ngelx_preflight_no_such_user__']})});if(!lookup.ok)throw Error('Firebase Authentication user lookup permission unavailable');
const push=await fetch('https://fcm.googleapis.com/v1/projects/ngelx-44eed/messages:send',{method:'POST',headers,body:JSON.stringify({validate_only:true,message:{token:'__invalid_preflight_token_no_device__',data:{kind:'preflight'}}})});
if(![200,400,404].includes(push.status))throw Error('FCM API or Firebase Messaging permission unavailable (HTTP '+push.status+')');
console.log('Firebase data access, authentication lookup and FCM dry-run verified');
const subscriptions=await cf('subscriptions');
for(const s of subscriptions){const text=JSON.stringify(s.rate_plan??{}).toLowerCase();if(text.includes('worker')&&!text.includes('free'))throw Error('Workers Free plan could not be confirmed; paid deployment refused');}
const settings=await cf('workers/account-settings');
if(['standard','unbound'].includes(settings.default_usage_model))throw Error('Paid Workers usage model detected; deployment refused');
const sub=await cf('workers/subdomain');if(!sub.subdomain)throw Error('Existing workers.dev subdomain unavailable');
fs.writeFileSync('backend452-preflight.json',JSON.stringify({freePlanVerified:true,workerUrl:`https://ngelx-call-push.${sub.subdomain}.workers.dev`,firebaseAccessVerified:true,checkedAt:new Date().toISOString()},null,2));
// Secret is only staged for wrangler, never printed or uploaded as an artifact.
fs.writeFileSync('cloudflare/call-push/.secrets452.json',JSON.stringify({GOOGLE_SERVICE_ACCOUNT:JSON.stringify(service)}),{mode:0o600});
console.log('Workers Free and required Firebase permissions verified; no message sent');
