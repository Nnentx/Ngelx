import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,writeFileSync,readFileSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {resolve,join} from 'node:path';
import {spawnSync} from 'node:child_process';
const old={id:'old',versions:[{version_id:'59ca47cc-386e-4a0f-a6ba-69539fffe839',percentage:100}]};
const newer={id:'new',versions:[{version_id:'22222222-2222-2222-2222-222222222222',percentage:100}]};
function run(mode,scenario='',seed){
 const dir=mkdtempSync(join(tmpdir(),'guard576-')),state=join(dir,'build584-worker-state.json');
 if(seed)writeFileSync(state,JSON.stringify(seed));
 const script=`
 const old=${JSON.stringify(old)},newer=${JSON.stringify(newer)};
 const mode=${JSON.stringify(mode)},scenario=${JSON.stringify(scenario)};let restored=false,posts=0;
 process.argv[2]=mode;
 globalThis.fetch=async(url,options={})=>{
  const u=String(url);
  if(u.startsWith('https://api.github.com/')){
   const id=u.split('/').at(-1);
   return Response.json({status:'completed',conclusion:scenario==='bad-ci'?'failure':'success',head_sha:'c999d229d68ea9d79911d2e9821a711814d17455'});
  }
  if(u.startsWith('https://api.cloudflare.com/')){
   if(options.method==='POST'){
    posts++;const b=JSON.parse(options.body);
    if(b.versions[0].version_id!==old.versions[0].version_id)throw Error('Wrong rollback payload');
    restored=true;return Response.json({success:true,result:{}});
   }
   const current=mode==='prepare'||restored?old:newer;
   if(scenario==='baseline-changed')current.versions=newer.versions;
   if(scenario==='concurrent')current.id='someone-else';
   if(scenario==='weighted')current.versions=[{version_id:old.versions[0].version_id,percentage:50},{version_id:newer.versions[0].version_id,percentage:50}];
   return Response.json({success:true,result:{deployments:[{...current,created_on:'2026-10-26T00:00:00Z'}]}});
  }
  if(u.endsWith('/health'))return Response.json({ok:true,features:['community_delete556','ludo565','ludo568','ludo569'],ludo575:{sourceVersion:575,clientBuild:578,configured:scenario!=='unconfigured'&&!(scenario==='domain-old'&&u.includes('oyun.ngelxsocial.com')),rewardedAdsConfigured:false}});
  return new Response('{}',{status:401});
 };
 try{await import(${JSON.stringify(new URL('./build584_deployment_guard.mjs',import.meta.url).href)});console.log('POST_COUNT='+posts);}catch(e){console.error(e.message);console.error('POST_COUNT='+posts);process.exitCode=1;}
 `;
 try{
  const r=spawnSync(process.execPath,['--input-type=module','--eval',script],{env:{...process.env,RUNNER_TEMP:dir,CLOUDFLARE_API_TOKEN:'test-only-not-real',CLOUDFLARE_ACCOUNT_ID:'fake-account',GH_TOKEN:'test-only-not-real',NGELX_HEALTH_ATTEMPTS:'1'},encoding:'utf8'});
  let saved;try{saved=JSON.parse(readFileSync(state));}catch{}
  return {...r,saved};
 }finally{rmSync(dir,{recursive:true,force:true});}
}
test('prepare verifies prior acceptance and checkpoints without deployment writes',()=>{
 const r=run('prepare');assert.equal(r.status,0,r.stderr);assert.equal(r.saved.previous.id,'old');assert.match(r.stdout,/POST_COUNT=0/);
});
test('failed CI blocks deployment checkpoint',()=>{
 const r=run('prepare','bad-ci');assert.notEqual(r.status,0);assert.equal(r.saved,undefined);assert.match(r.stderr,/POST_COUNT=0/);
});
test('a changed production baseline cannot be overwritten by this release',()=>{
 const r=run('prepare','baseline-changed');assert.notEqual(r.status,0);assert.equal(r.saved,undefined);assert.match(r.stderr,/refusing to overwrite/);assert.match(r.stderr,/POST_COUNT=0/);
});
test('weighted rollout cannot be overwritten by single-version deployment',()=>{
 const r=run('prepare','weighted');assert.notEqual(r.status,0);assert.equal(r.saved,undefined);
});
test('record saves exact new deployment before failing a health check',()=>{
 const r=run('record','unconfigured',{previous:old});assert.notEqual(r.status,0);assert.equal(r.saved.deployed.id,'new');
});
test('rollback restores only the recorded prior version',()=>{
 const r=run('rollback','',{previous:old,deployed:newer});assert.equal(r.status,0,r.stderr);assert.equal(r.saved.rolledBack,true);assert.match(r.stdout,/POST_COUNT=1/);
});
test('rollback refuses to overwrite a concurrent deployment',()=>{
 const r=run('rollback','concurrent',{previous:old,deployed:newer});assert.notEqual(r.status,0);assert.match(r.stderr,/unrecognized\/concurrent/);assert.match(r.stderr,/POST_COUNT=0/);
});

test('custom game hostname must converge even when workers.dev is already new',()=>{
 const r=run('record','domain-old',{previous:old});assert.notEqual(r.status,0);assert.match(r.stderr,/both hostnames/);assert.equal(r.saved.deployed.id,'new');assert.match(r.stderr,/POST_COUNT=0/);
});
