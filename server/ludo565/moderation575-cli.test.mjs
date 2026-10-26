import {test} from 'node:test';
import assert from 'node:assert/strict';
import {runModeratorCommand575} from '../../tools/ludo575_moderator_cli.mjs';

const token='valid-id-token-with-adequate-length';
const env={LUDO_REVIEW_ENDPOINT_URL:'https://review.example.test/ludo',LUDO_MODERATOR_ID_TOKEN:token};
const id='report575_'+'a'.repeat(64);

test('moderator CLI sends scoped authenticated report page requests without leaking token',async()=>{
 const requests=[];
 const result=await runModeratorCommand575(['list','2026-10-26','2'],{
  env,fetcher:async(url,options)=>{
   requests.push({url,options});return Response.json({room:{reports:[{id,status:'pending'}],page:2}});
  }
 });
 assert.equal(requests[0].url,env.LUDO_REVIEW_ENDPOINT_URL);
 assert.equal(requests[0].options.method,'POST');
 assert.equal(requests[0].options.headers.authorization,'Bearer '+token);
 assert.deepEqual(JSON.parse(requests[0].options.body),{action:'moderation_queue',day:'2026-10-26',page:2});
 assert.equal(result.page,2);
 assert.equal(result.reports[0].status,'pending');
});
test('moderator CLI resolves only known pending report formats and enum decisions',async()=>{
 let sent;
 await runModeratorCommand575(['resolve',id,'reviewed'],{
  env,fetcher:async(url,options)=>{sent=JSON.parse(options.body);return Response.json({room:{changed:true,status:'reviewed'}});}
 });
 assert.deepEqual(sent,{action:'moderation_resolve',reportId:id,decision:'reviewed'});
});
test('CLI rejects credentials in URL, plaintext transport and missing ID token',async()=>{
 const bad=[
  {LUDO_REVIEW_ENDPOINT_URL:'http://review.example.test/ludo',LUDO_MODERATOR_ID_TOKEN:token},
  {LUDO_REVIEW_ENDPOINT_URL:'https://user:pass@review.example.test/ludo',LUDO_MODERATOR_ID_TOKEN:token},
  {LUDO_REVIEW_ENDPOINT_URL:'https://review.example.test/ludo?token=secret',LUDO_MODERATOR_ID_TOKEN:token},
  {LUDO_REVIEW_ENDPOINT_URL:'https://review.example.test/moderate',LUDO_MODERATOR_ID_TOKEN:token},
  {LUDO_REVIEW_ENDPOINT_URL:'https://review.example.test/ludo'},
 ];
 for(const settings of bad){
  await assert.rejects(runModeratorCommand575(['list'],{env:settings}),/endpoint|token/i);
 }
});
test('CLI cannot silently retry a review decision or leak bearer token on HTTP errors',async()=>{
 for(const status of [401,403,404,503]){
  let calls=0;
  const opts={env,fetcher:async()=>{calls++;return Response.json({error:'internal:'+token},{status});}};
  await assert.rejects(runModeratorCommand575(['resolve',id,'dismissed'],opts),
    e=>!String(e.message).includes(token));
  assert.equal(calls,1);
 }
});
test('CLI refuses out-of-range list pages and malformed report IDs before making requests',async()=>{
 let calls=0;
 const opts={env,fetcher:async()=>{calls++;return Response.json({room:{}});}};
 for(const args of [
  ['list','2026-10-26','-1'],['list','2026-10-26','999'],['list','today'],
  ['list','2026-10-26','0','extra'],['resolve','report575_bad','reviewed'],
  ['resolve',id,'ban'],['delete',id],[],
 ]){
  await assert.rejects(runModeratorCommand575(args,opts));
 }
 assert.equal(calls,0);
});
