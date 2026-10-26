import {test} from 'node:test';
import assert from 'node:assert/strict';
import {probeNgelxBuild575Live} from '../../../tools/check_build575_live.mjs';

test('preflight does not mistake successful health of old Worker for deployed Build575',async()=>{
 let calls=0;
 const report=await probeNgelxBuild575Live({fetcher:async(url,options)=>{
  calls++;assert.equal(options.method,'GET');assert.equal(options.redirect,'error');
  assert.equal(options.headers.accept,'application/json');
  assert.ok(url.endsWith('/health'));
  return Response.json({ok:true,service:'ngelx-live-moderation',features:['ludo565']});
 }});
 assert.equal(calls,1);
 assert.equal(report.workerReady,false);
 assert.equal(report.configurationReady,false);
 assert.equal(report.releaseReady,false);
 assert.ok(report.missing.includes('build575_worker_not_deployed'));
});
test('live probe requires matching Firebase and explicit enabled AdMob/moderator flags',async()=>{
 const full=async()=>Response.json({ok:true,ludo575:{sourceVersion:575,configured:true,
  rewardedAdsConfigured:true,moderationAllowlistConfigured:true},
  privateKey:'never-echo-this-in-report',moderatorUids:['secret-user-id']});
 const report=await probeNgelxBuild575Live({fetcher:full});
 assert.equal(report.configurationReady,true);
 assert.equal(report.workerReady,true);
 assert.equal(report.releaseReady,false,'A health endpoint cannot verify physical phones');
 assert.equal(JSON.stringify(report).includes('never-echo-this-in-report'),false);
 assert.equal(JSON.stringify(report).includes('secret-user-id'),false);
 const missing=await probeNgelxBuild575Live({
  fetcher:async()=>Response.json({ok:true,ludo575:{sourceVersion:575,configured:true,
   rewardedAdsConfigured:false,moderationAllowlistConfigured:false}})});
 assert.equal(missing.workerReady,true);
 assert.equal(missing.configurationReady,false);
 assert.deepEqual(missing.missing,['rewarded_ads_disabled','moderator_allowlist_disabled']);
});
test('health request is read-only and never redirected to attacker-controlled URL',async()=>{
 let called=false;
 await assert.rejects(probeNgelxBuild575Live({
  url:'https://evil.example.test/health',fetcher:async()=>{called=true;return Response.json({ok:true});}
 }),/untrusted_health_endpoint/);
 assert.equal(called,false);
 const noService=await probeNgelxBuild575Live({fetcher:async()=>new Response('down',{status:503})});
 assert.equal(noService.configurationReady,false);
 assert.equal(noService.httpStatus,503);
 const timeout=await probeNgelxBuild575Live({fetcher:async()=>{throw Error('timeout')}});
 assert.equal(timeout.configurationReady,false);
 assert.equal(timeout.reason,'worker_unreachable');
});
test('malformed JSON and missing features can never attest a released game',async()=>{
 const a=await probeNgelxBuild575Live({fetcher:async()=>new Response('not json',{status:200})});
 assert.equal(a.releaseReady,undefined);
 assert.equal(a.configurationReady,false);
 const b=await probeNgelxBuild575Live({fetcher:async()=>Response.json({ok:true,ludo575:{
  sourceVersion:574,configured:true,rewardedAdsConfigured:true,moderationAllowlistConfigured:true}})});
 assert.equal(b.configurationReady,false);
 assert.ok(b.missing.includes('build575_worker_not_deployed'));
});
