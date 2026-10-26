// Restricted deployment checkpoint/rollback. Never reads or prints secret values.
import fs from 'node:fs';
const statePath=process.env.RUNNER_TEMP+'/build576-worker-state.json';
const token=process.env.CLOUDFLARE_API_TOKEN,account=process.env.CLOUDFLARE_ACCOUNT_ID;
if(!token||!account)throw Error('Missing deployment credentials');
const api='https://api.cloudflare.com/client/v4/accounts/'+encodeURIComponent(account)+'/workers/scripts/ngelx-live-moderation/deployments';
async function cloudflare(method='GET',body){
 const r=await fetch(api,{method,headers:{authorization:'Bearer '+token,'content-type':'application/json'},...(body?{body:JSON.stringify(body)}:{}),signal:AbortSignal.timeout(30000)});
 const d=await r.json();if(!r.ok||!d.success)throw Error('Deployment metadata HTTP '+r.status);return d.result;
}
async function latest(){
 const d=await cloudflare(),all=d.deployments;
 if(!Array.isArray(all)||!all.length)throw Error('Missing current deployment');
 const first=[...all].sort((a,b)=>Date.parse(b.created_on)-Date.parse(a.created_on))[0];
 if(!first.id||!Array.isArray(first.versions)||first.versions.length!==1||first.versions[0].percentage!==100||!/^[-a-f0-9]{36}$/.test(first.versions[0].version_id))throw Error('Unsafe/nonstandard current rollout; no deployment allowed');
 return {id:first.id,versions:first.versions};
}
async function health(expectNew){
 const results=[];
 for(const base of ['https://ngelx-live-moderation.alihancaglar76.workers.dev','https://oyun.ngelxsocial.com']){
  const r=await fetch(base+'/health',{cache:'no-store',signal:AbortSignal.timeout(15000)}),h=await r.json();
  if(!r.ok||h.ok!==true||!['community_delete556','ludo565','ludo568','ludo569'].every(f=>h.features?.includes(f)))throw Error('Core health/capabilities changed');
  if(expectNew&&(h.ludo575?.sourceVersion!==575||h.ludo575?.clientBuild!==578||h.ludo575?.configured!==true))throw Error('New Ludo runtime not configured on both hostnames');
  if(expectNew&&h.ludo575?.rewardedAdsConfigured===true)throw Error('Release requires rewarded ads disabled');
  for(const path of ['/ludo','/community/delete','/moderate']){
   const denied=await fetch(base+path,{method:'POST',headers:{'content-type':'application/json'},body:'{}',signal:AbortSignal.timeout(15000)});
   if(denied.status!==401)throw Error('Anonymous security boundary changed: '+path);
  }
  results.push({hostname:new URL(base).hostname,ok:h.ok,features:h.features,newLudoConfigured:h.ludo575?.configured===true,rewardedAdsConfigured:h.ludo575?.rewardedAdsConfigured===true});
 }
 return {endpoints:results};
}
async function converge(){
 const attempts=Math.max(1,Math.min(18,Number(process.env.NGELX_HEALTH_ATTEMPTS)||18));let last;
 for(let i=0;i<attempts;i++){
  try{
   const first=await health(true);
   if(attempts>1){await new Promise(r=>setTimeout(r,5000));await health(true);}
   return first;
  }catch(e){last=e;console.log('Waiting for both hostnames to converge ('+(i+1)+'/'+attempts+').');}
  if(i+1<attempts)await new Promise(r=>setTimeout(r,5000));
 }
 throw last;
}
function save(s){fs.writeFileSync(statePath,JSON.stringify(s,null,2)+'\n');}
const mode=process.argv[2];
if(mode==='prepare'){
 for(const [id,sha] of [['40379566732','389059e2227d94814bae7fc9f1f21cdee19e70ca'],['40378761157','48669221cd5e0e0e46c12e3e0105546fa84f00bd']]){
  const r=await fetch('https://api.github.com/repos/Nnentx/Ngelx/actions/runs/'+id,{headers:{authorization:'Bearer '+process.env.GH_TOKEN,accept:'application/vnd.github+json'},signal:AbortSignal.timeout(15000)});
  if(!r.ok)throw Error('Cannot verify acceptance run');const d=await r.json();
  if(d.status!=='completed'||d.conclusion!=='success'||d.head_sha!==sha)throw Error('Required acceptance run did not pass');
 }
 const before=await latest(),baseline=await health(false);
 save({previous:before,baseline,startedAt:new Date().toISOString(),apkRun:40379566732,stagingRun:40378761157});
 console.log('APK/staging acceptance passed; prior 100% deployment checkpoint recorded; core boundaries healthy.');
}else if(mode==='record'){
 const s=JSON.parse(fs.readFileSync(statePath)),current=await latest();
 if(current.id===s.previous.id)throw Error('No new deployment observed');
 s.deployed=current;save(s);console.log('New deployment recorded for conditional rollback.');
 s.health=await converge();save(s);console.log('New Ludo configured; original core endpoints reject anonymous access; ads disabled.');
}else if(mode==='accept'){
 const s=JSON.parse(fs.readFileSync(statePath)),current=await latest();
 if(current.id!==s.deployed?.id)throw Error('Concurrent rollout detected; acceptance invalid');
 s.health=await health(true);s.acceptedAt=new Date().toISOString();s.apiAcceptance=true;s.physicalDeviceAcceptance=false;s.updaterPublished=false;save(s);
 console.log('Live API acceptance complete. Physical Android checks remain; updater unchanged.');
}else if(mode==='rollback'){
 if(!fs.existsSync(statePath))throw Error('No safe rollback checkpoint');
 const s=JSON.parse(fs.readFileSync(statePath)),current=await latest();
 if(current.id===s.previous.id){console.log('Previous deployment remains active; rollback not needed.');process.exit(0);}
 if(!s.deployed||current.id!==s.deployed.id)throw Error('Cannot safely roll back an unrecognized/concurrent deployment');
 await cloudflare('POST',{strategy:'percentage',versions:s.previous.versions,annotations:{'workers/message':'Restore prior deployment after Build576 acceptance failure'}});
 const restored=await latest();
 if(restored.versions[0].version_id!==s.previous.versions[0].version_id)throw Error('Rollback version not confirmed');
 await health(false);s.rolledBack=true;save(s);console.log('Prior Worker version restored and basic health/security checked.');
}else throw Error('Unsupported guard mode');
