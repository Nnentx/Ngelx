import {accessToken,document} from '../cloudflare/call-push/src/google.mjs';
import {createHash} from 'node:crypto';
const raw=process.env.FIREBASE_SERVICE_ACCOUNT_NGELX_44EED||process.env.FIREBASE_SERVICE_ACCOUNT||process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON;
let account;try{account=JSON.parse(raw);}catch{account=JSON.parse(Buffer.from(raw,'base64').toString());}
if(account.project_id!=='ngelx-44eed')throw Error('Unexpected project');
const token=await accessToken({FIREBASE_PROJECT_ID:'ngelx-44eed',GOOGLE_SERVICE_ACCOUNT:JSON.stringify(account)});
const base='https://firestore.googleapis.com/v1/projects/ngelx-44eed/databases/(default)/documents';
async function read(url,options={}){const r=await fetch(url,{...options,headers:{authorization:'Bearer '+token,'content-type':'application/json'}});if(r.status===404)return null;if(!r.ok)throw Error('Read-only call diagnostics failed HTTP '+r.status);return r.json();}
const query=await read(base+':runQuery',{method:'POST',body:JSON.stringify({structuredQuery:{from:[{collectionId:'chats'}],orderBy:[{field:{fieldPath:'callCreatedAt'},direction:'DESCENDING'}],limit:3}})});
for(const row of query){
 const chat=document(row.document);if(!chat||String(chat.callStartedBy??'').startsWith('__ngelx453_probe_'))continue;
 const id=row.document.name.split('/').pop();
 const peers=[...new Set(chat.members??[])].filter(x=>x!==chat.callStartedBy);let registered=0,disabled=0,delivered=0;
 for(const uid of peers){
  const devices=await read(base+'/_call_devices/'+encodeURIComponent(uid)+'/tokens?pageSize=2&orderBy=updatedAt%20desc');
  if((devices?.documents??[]).some(d=>typeof document(d)?.token==='string'))registered++;
  const profile=document(await read(base+'/users/'+encodeURIComponent(uid)));
  if(profile?.notificationsEnabled===false)disabled++;
  const hash=createHash('sha256').update(id+':incoming_call:'+uid).digest('base64url');
  const lease=document(await read(base+'/_call_push452/'+hash));
  if(lease?.room===chat.callRoomName&&lease.state==='sent')delivered++;
 }
 const rate=document(await read(base+'/_call_push_rate452/'+encodeURIComponent(chat.callStartedBy)));
 console.log(JSON.stringify({group:chat.isGroup===true||chat.callGroup===true,state:chat.callStatus,ageSeconds:Math.floor((Date.now()-chat.callCreatedAt)/1000),recipients:peers.length,registeredRecipients:registered,missingDeviceRegistrations:peers.length-registered,notificationsDisabled:disabled,completedDispatchRecipients:delivered,callerDispatchRequestsInLatestWindow:rate?.count??0}));
}
console.log('Read-only diagnostics complete; no names, messages, UIDs or device tokens printed; no notifications sent');
