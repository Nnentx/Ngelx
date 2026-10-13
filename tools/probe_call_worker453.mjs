// Authenticated integration probe uses only temporary synthetic users/chat.
// It never registers a device token or delivers a notification to a person.
import fs from 'node:fs';
import {sign} from 'node:crypto';
import {accessToken} from '../cloudflare/call-push/src/google.mjs';
const raw=process.env.FIREBASE_SERVICE_ACCOUNT_NGELX_44EED||process.env.FIREBASE_SERVICE_ACCOUNT||process.env.GOOGLE_APPLICATION_CREDENTIALS_JSON;
if(!raw)throw Error('Existing server credential unavailable');
let account;try{account=JSON.parse(raw);}catch{account=JSON.parse(Buffer.from(raw,'base64').toString());}
if(account.project_id!=='ngelx-44eed')throw Error('Unexpected project');
const config=JSON.parse(fs.readFileSync('app/android/app/google-services.json','utf8'));
const apiKey=config.client[0].api_key[0].current_key;
const id='__ngelx453_probe_'+Date.now(),peer=id+'_peer';
const base='https://firestore.googleapis.com/v1/projects/ngelx-44eed/databases/(default)/documents/';
const paths=['users/'+id,'users/'+peer,'chats/'+id];
const bearer=await accessToken({FIREBASE_PROJECT_ID:'ngelx-44eed',GOOGLE_SERVICE_ACCOUNT:JSON.stringify(account)});
const adminHeaders={authorization:'Bearer '+bearer,'content-type':'application/json'};
async function call(url,body,headers={}){const r=await fetch(url,{method:'POST',headers:{'content-type':'application/json',...headers},body:JSON.stringify(body),signal:AbortSignal.timeout(20000)});if(!r.ok)throw Error('Probe request failed (HTTP '+r.status+')');return r.json();}
const encode=v=>typeof v==='string'?{stringValue:v}:typeof v==='boolean'?{booleanValue:v}:Array.isArray(v)?{arrayValue:{values:v.map(encode)}}:v instanceof Date?{timestampValue:v.toISOString()}:{integerValue:String(v)};
let login;const written=[];
try{
 const now=Math.floor(Date.now()/1000);
 const b64=x=>Buffer.from(JSON.stringify(x)).toString('base64url');
 const unsigned=b64({alg:'RS256',typ:'JWT'})+'.'+b64({iss:account.client_email,sub:account.client_email,aud:'https://identitytoolkit.googleapis.com/google.identity.identitytoolkit.v1.IdentityToolkit',iat:now,exp:now+600,uid:id});
 const custom=unsigned+'.'+sign('RSA-SHA256',Buffer.from(unsigned),account.private_key).toString('base64url');
 login=await call('https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key='+apiKey,{token:custom,returnSecureToken:true});
 if(JSON.parse(Buffer.from(login.idToken.split('.')[1],'base64url').toString()).sub!==id)throw Error('Synthetic probe identity mismatch');
 const payloads=[{displayName:'Internal call probe',discoverable:false,testAccount:true},{displayName:'Internal no-device probe',discoverable:false,testAccount:true},{members:[id,peer],isGroup:true,callGroup:true,callStartedBy:id,callRoomName:id,callStatus:'ringing',callCreatedAt:new Date(),callTitle:'Internal probe',callVideo:false}];
 for(let n=0;n<paths.length;n++){
  const r=await fetch(base+paths[n]+'?currentDocument.exists=false',{method:'PATCH',headers:adminHeaders,body:JSON.stringify({fields:Object.fromEntries(Object.entries(payloads[n]).map(([k,v])=>[k,encode(v)]))})});
  if(!r.ok)throw Error('Synthetic fixture write failed (HTTP '+r.status+')');written.push(paths[n]);
 }
 const result=await call('https://ngelx-call-push.alihancaglar76.workers.dev/call',{chatId:id,roomName:id,offset:0},{authorization:'Bearer '+login.idToken});
 if(result.sent!==0||result.nextOffset!==null)throw Error('Unexpected no-device dispatch result');
 console.log('Authenticated Worker request, Firebase login lookup and group authorization passed; zero notifications delivered');
}finally{
 const cleanup=[...written,'_call_push_rate452/'+id];let failed=false;
 for(const path of cleanup){const r=await fetch(base+path,{method:'DELETE',headers:adminHeaders});if(!r.ok&&r.status!==404)failed=true;}
 if(login){try{await call('https://identitytoolkit.googleapis.com/v1/accounts:delete?key='+apiKey,{idToken:login.idToken});}catch{failed=true;}}
 if(failed)throw Error('Synthetic probe cleanup incomplete');
 console.log('Synthetic probe records cleaned up');
}
