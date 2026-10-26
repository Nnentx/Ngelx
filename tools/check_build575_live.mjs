// Read-only public release readiness check. Never sends credentials or writes to Cloudflare.
// A successful bundle is NOT proof that this Worker version was deployed.
import {pathToFileURL} from 'node:url';
const HEALTH='https://ngelx-live-moderation.alihancaglar76.workers.dev/health';
export async function probeNgelxBuild575Live({fetcher=fetch,timeout=8000,url=HEALTH}={}){
 const target=new URL(url);
 if(target.href!==HEALTH)throw Error('untrusted_health_endpoint');
 let response;
 try{
  response=await fetcher(HEALTH,{method:'GET',redirect:'error',cache:'no-store',
   headers:{accept:'application/json'},signal:AbortSignal.timeout(timeout)});
 }catch{
  return {configurationReady:false,reason:'worker_unreachable',checkedEndpoint:HEALTH};
 }
 if(!response.ok)return {ready:false,reason:'worker_health_http_error',httpStatus:response.status,
  checkedEndpoint:HEALTH};
 let data;
 try{data=await response.json();}catch{
  return {ready:false,reason:'invalid_worker_health_response',checkedEndpoint:HEALTH};
 }
 if(!data||typeof data!=='object'||Array.isArray(data))
  return {ready:false,reason:'invalid_worker_health_response',checkedEndpoint:HEALTH};
 const ludo=data.ludo575;
 const deployed=ludo?.sourceVersion===575;
 const configured=ludo?.configured===true;
 const serviceConfigured=data.ok===true;
 const missing=[];
 if(!deployed)missing.push('build575_worker_not_deployed');
 if(!serviceConfigured||!configured)missing.push('firebase_or_worker_not_configured');
 // Ads and moderator UID configuration are separate release decisions, NOT proof
 // of successful real AdMob SSV, live Firestore writes or two-device QA.
 const ads=ludo?.rewardedAdsConfigured===true;
 const moderator=ludo?.moderationAllowlistConfigured===true;
 if(!ads)missing.push('rewarded_ads_disabled');
 if(!moderator)missing.push('moderator_allowlist_disabled');
 return {configurationReady:deployed&&configured&&serviceConfigured&&ads&&moderator,
  workerReady:deployed&&configured&&serviceConfigured,
  releaseReady:false, // Real-device QA and provider verification cannot be checked by a GET.
  rewardedAdsConfigured:ads,moderatorAllowlistConfigured:moderator,
  missing,checkedEndpoint:HEALTH};
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 probeNgelxBuild575Live().then(result=>{
  process.stdout.write(JSON.stringify(result,null,2)+'\n');
  if(!result.workerReady)process.stdout.write(
   'Build575 live Worker is not confirmed deployed. Build574 updater MUST remain unchanged.\n');
  else process.stdout.write(
   'Worker settings detected. This does not certify AdMob or physical-device QA.\n');
 }).catch(e=>{
  process.stderr.write('Read-only release preflight failed: '+e.message+'\n');
  process.exitCode=1;
 });
}
