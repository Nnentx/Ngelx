// Add only the exact composite index required by canonical gift aggregation.
import assert from 'node:assert/strict';
import {accessToken} from '../cloudflare/call-push/src/google.mjs';
const raw=process.env.FIREBASE_SERVICE_ACCOUNT_NGELX_44EED||process.env.FIREBASE_SERVICE_ACCOUNT;
let service;try{service=JSON.parse(raw);}catch{service=JSON.parse(Buffer.from(raw,'base64').toString());}
assert.equal(service.project_id,'ngelx-44eed');
const env={FIREBASE_PROJECT_ID:service.project_id,GOOGLE_SERVICE_ACCOUNT:JSON.stringify(service)};
const base='https://firestore.googleapis.com/v1/projects/ngelx-44eed/databases/(default)/collectionGroups/comments/indexes';
async function api(url,method='GET',body){
 const r=await fetch(url,{method,headers:{authorization:'Bearer '+await accessToken(env),'content-type':'application/json'},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(20000)});
 const value=await r.json();if(!r.ok)throw Error('Index API '+r.status+' '+JSON.stringify(value));return value;
}
const matches=index=>index.queryScope==='COLLECTION'&&JSON.stringify(index.fields?.filter(x=>x.fieldPath!=='__name__'))===JSON.stringify([{fieldPath:'kind',order:'ASCENDING'},{fieldPath:'points',order:'ASCENDING'}]);
async function find(){let pageToken;do{const result=await api(base+(pageToken?'?pageToken='+encodeURIComponent(pageToken):''));const index=result.indexes?.find(matches);if(index)return index;pageToken=result.nextPageToken;}while(pageToken);}
let index=await find();
if(!index){await api(base,'POST',{queryScope:'COLLECTION',fields:[{fieldPath:'kind',order:'ASCENDING'},{fieldPath:'points',order:'ASCENDING'},{fieldPath:'__name__',order:'ASCENDING'}]});console.log('Created required comments kind/points index');}
for(let attempt=0;attempt<80;attempt++){
 index=await find();if(index?.state==='READY'){console.log('Historical gift aggregation index READY');process.exit(0);}
 if(index?.state==='NEEDS_REPAIR')throw Error('Gift aggregation index needs repair');
 console.log('Waiting for gift aggregation index: '+(index?.state??'PENDING'));
 await new Promise(resolve=>setTimeout(resolve,10000));
}
throw Error('Gift aggregation index not ready before deadline');
