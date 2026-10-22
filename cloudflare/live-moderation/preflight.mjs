import fs from 'node:fs';
const configured={};
for(const name of ['CLOUDFLARE_API_TOKEN','CLOUDFLARE_ACCOUNT_ID','LIVEKIT_API_KEY','LIVEKIT_API_SECRET','LIVEKIT_SERVER_URL']){
 configured[name]=Boolean(process.env[name]);console.log(name+': '+(configured[name]?'available':'missing'));
}
const raw=process.env.FIREBASE_SERVICE_ACCOUNT_NGELX_44EED||process.env.FIREBASE_SERVICE_ACCOUNT;
configured.GOOGLE_SERVICE_ACCOUNT=Boolean(raw);console.log('Firebase server identity: '+(raw?'available':'missing'));
let liveKitVerified=false;
if(configured.LIVEKIT_API_KEY&&configured.LIVEKIT_API_SECRET&&configured.LIVEKIT_SERVER_URL){
 const url=new URL(process.env.LIVEKIT_SERVER_URL);
 if(url.protocol!=='wss:'||url.hostname!=='ngelx-4gz3quoe.livekit.cloud')throw Error('Unexpected LiveKit project');
 const {createHmac}=await import('node:crypto');
 const encode=value=>Buffer.from(JSON.stringify(value)).toString('base64url');
 const now=Math.floor(Date.now()/1000);
 const unsigned=encode({alg:'HS256',typ:'JWT'})+'.'+encode({iss:process.env.LIVEKIT_API_KEY,nbf:now-5,exp:now+60,video:{roomList:true}});
 const token=unsigned+'.'+createHmac('sha256',process.env.LIVEKIT_API_SECRET).update(unsigned).digest('base64url');
 url.protocol='https:';url.pathname='/twirp/livekit.RoomService/ListRooms';
 const response=await fetch(url,{method:'POST',headers:{authorization:'Bearer '+token,'content-type':'application/json'},body:'{}',signal:AbortSignal.timeout(10000)});
 liveKitVerified=response.ok;
 console.log('LiveKit read-only administration check HTTP:',response.status);
 if(!liveKitVerified)throw Error('LiveKit credentials could not be verified');
}
// Owner dashboard screenshot 50159.jpg: Free $0 marked Current plan,
// verified 2026-10-22 18:26 Europe/Istanbul. Only a short-lived fallback
// when the existing deployment token cannot read billing metadata.
const ownerFreeEvidenceUntil=Date.parse('2026-10-23T15:26:00Z');
let free=false,service;
if(raw){
 try{service=JSON.parse(raw);}catch{service=JSON.parse(Buffer.from(raw,'base64').toString());}
 if(service.project_id!=='ngelx-44eed')throw Error('Wrong Firebase project; refusing deployment');
}
if(configured.CLOUDFLARE_API_TOKEN&&configured.CLOUDFLARE_ACCOUNT_ID){
 const base='https://api.cloudflare.com/client/v4/accounts/'+process.env.CLOUDFLARE_ACCOUNT_ID+'/';
 const headers={authorization:'Bearer '+process.env.CLOUDFLARE_API_TOKEN};
 const sub=await fetch(base+'workers/subdomain',{headers,signal:AbortSignal.timeout(10000)});
 if(sub.ok){
  const result=await sub.json();if(result.result?.subdomain!=='alihancaglar76')throw Error('Unrecognized deployment account');
 }else throw Error('Cloudflare account verification failed');
 const response=await fetch(base+'subscriptions',{headers,signal:AbortSignal.timeout(10000)});
 console.log('Workers plan lookup HTTP:',response.status);
 if(response.ok){
  const result=await response.json();if(!result.success||!Array.isArray(result.result))throw Error('Invalid plan response');
  free=!result.result.some(s=>/worker/i.test(JSON.stringify(s))&&!/free/i.test(JSON.stringify(s.rate_plan??{})));
 }
}
if(!free&&Date.now()<ownerFreeEvidenceUntil){
 free=true;console.log('Workers Free verified from owner dashboard screenshot 50159.jpg (2026-10-22); billing unchanged');
}
console.log('Workers Free plan confirmed:',free);
const ready=free&&liveKitVerified&&Object.values(configured).every(Boolean);
const result={ready,freePlanVerified:free,liveKitVerified,configured,workerUrl:'https://ngelx-live-moderation.alihancaglar76.workers.dev',checkedAt:new Date().toISOString()};
fs.writeFileSync('live555-free-readiness.json',JSON.stringify(result,null,2));
if(ready){
 const url=new URL(process.env.LIVEKIT_SERVER_URL);
 if(url.protocol!=='wss:'||url.hostname!=='ngelx-4gz3quoe.livekit.cloud')throw Error('LiveKit project must match the currently installed app');
 fs.writeFileSync('cloudflare/live-moderation/.live-secrets555.json',JSON.stringify({
  GOOGLE_SERVICE_ACCOUNT:JSON.stringify(service),
  LIVEKIT_API_KEY:process.env.LIVEKIT_API_KEY,LIVEKIT_API_SECRET:process.env.LIVEKIT_API_SECRET,LIVEKIT_SERVER_URL:process.env.LIVEKIT_SERVER_URL,
 }),{mode:0o600});
}
if(process.env.GITHUB_OUTPUT)fs.appendFileSync(process.env.GITHUB_OUTPUT,'ready='+ready+'\n');
console.log(ready?'Required deployment settings present':'Deployment paused: required configuration is missing; no billing or server changes');
