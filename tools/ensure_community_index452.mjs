import fs from 'node:fs';
import {accessToken} from '../cloudflare/call-push/src/google.mjs';
const raw=process.env.FIREBASE_SERVICE_ACCOUNT_NGELX_44EED||process.env.FIREBASE_SERVICE_ACCOUNT||process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON;
if(!raw)throw Error('Existing Firebase deployment credential unavailable');
let service;try{service=JSON.parse(raw);}catch{service=JSON.parse(Buffer.from(raw,'base64').toString());}
if(service.project_id!=='ngelx-44eed')throw Error('Unexpected Firebase project');
const bearer=await accessToken({FIREBASE_PROJECT_ID:'ngelx-44eed',GOOGLE_SERVICE_ACCOUNT:JSON.stringify(service)});
const base='https://firestore.googleapis.com/v1/projects/ngelx-44eed/databases/(default)/collectionGroups/posts/indexes';
async function request(url,options={}){
 const r=await fetch(url,{...options,headers:{authorization:'Bearer '+bearer,'content-type':'application/json'}});
 if(r.status===403)throw Error('Index administration denied (HTTP 403). Existing deployment service account needs roles/datastore.indexAdmin, or owner must create posts COLLECTION index: status ASCENDING, createdAt DESCENDING in Firebase console. No rules or billing changed.');
 if(!r.ok)throw Error('Index API failed (HTTP '+r.status+')');
 return r.json();
}
const fields=[{fieldPath:'status',order:'ASCENDING'},{fieldPath:'createdAt',order:'DESCENDING'}];
const matches=i=>i.queryScope==='COLLECTION'&&JSON.stringify((i.fields??[]).filter(f=>f.fieldPath!=='__name__'))===JSON.stringify(fields);
async function find(){
 let page;do{const j=await request(base+(page?'?pageToken='+encodeURIComponent(page):''));const found=(j.indexes??[]).find(matches);if(found)return found;page=j.nextPageToken;}while(page);
}
let found=await find();
if(!found){await request(base,{method:'POST',body:JSON.stringify({queryScope:'COLLECTION',fields})});console.log('Only missing community feed index creation requested');}
for(let n=0;n<60;n++){
 found=await find();
 if(found?.state==='READY'){fs.writeFileSync('community-index-status.json',JSON.stringify({project:'ngelx-44eed',collectionGroup:'posts',queryScope:'COLLECTION',fields,state:'READY',checkedAt:new Date().toISOString()},null,2));console.log('Community feed index READY');process.exit(0);}
 if(found?.state==='NEEDS_REPAIR')throw Error('Community feed index needs repair');
 await new Promise(r=>setTimeout(r,10000));
}
throw Error('Community feed index is still building; no other indexes changed');
