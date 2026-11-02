import test from 'node:test';import assert from 'node:assert/strict';
import {createPkFinish588} from './live-pk588.mjs';
const start=1800000000000,end=start+180000;
function fixture({now=end+1000,fail=false}={}){
 const session={type:'live_pk',status:'active',inviterUid:'a',inviteeUid:'b',inviterLiveId:'ra',inviteeLiveId:'rb',startedAt:start,clientStartedAt:start-500,endsAt:end,startLikeA:999999,startGiftA:999999};
 const data=new Map(Object.entries({'calls/s':session,'live_streams/ra':{ownerId:'a',pkSessionId:'s',likeCount:100,giftPoints:100},'live_streams/rb':{ownerId:'b',pkSessionId:'s',likeCount:999999,giftPoints:999999},'live_pk_stats588/a':{streak:3},'live_pk_stats588/b':{streak:8}}));
 const reads=[],writes=[];
 const store={totalsAt:async(id,time)=>{reads.push([id,time]);if(fail)throw Error('unavailable');
  return id==='ra'?{likeCount:100,giftPoints:time===start?100:250}:{likeCount:time===start?200:210,giftPoints:0};},
  transact:async fn=>{const pending=[];const result=await fn({get:async p=>structuredClone(data.get(p)),update:(p,v)=>pending.push([p,v])});
   for(const [p,v] of pending){data.set(p,{...data.get(p),...v});writes.push([p,v]);}return result;}};
 return {data,reads,writes,finish:createPkFinish588({store,now:()=>now})};
}
test('last-second gift changes winner despite stale host counters',async()=>{
 const f=fixture(),r=await f.finish('a',{sessionId:'s'});
 assert.equal(r.status,200);assert.deepEqual(r.body.finalScoreByUid,{a:15,b:10});assert.equal(r.body.winnerUid,'a');
 assert.equal(f.data.get('live_pk_stats588/a').streak,4);assert.equal(f.data.get('live_pk_stats588/b').streak,0);
 assert.deepEqual(f.reads.sort(),[['ra',start],['ra',end],['rb',start],['rb',end]].sort());
 assert.equal(r.body.scoreSource589,'firestore_read_time');
});
test('late changes and client baselines do not alter the frozen result',async()=>{
 const f=fixture();f.data.get('live_streams/rb').giftPoints=10**9;
 const r=await f.finish('b',{sessionId:'s'});assert.equal(r.body.winnerUid,'a');
 f.data.get('live_streams/ra').giftPoints=10**9;
 const retry=await f.finish('a',{sessionId:'s'});assert.deepEqual(retry.body.finalScoreByUid,r.body.finalScoreByUid);assert.equal(f.reads.length,4);
});
test('historical query failure cannot fall back to stale counters or write WIN',async()=>{
 const f=fixture({fail:true});assert.equal((await f.finish('a',{sessionId:'s'})).status,503);assert.equal(f.writes.length,0);assert.equal(f.data.get('live_pk_stats588/a').streak,3);
});
test('early finish is rejected without historical reads; explicit cancellation preserves WIN',async()=>{
 const f=fixture({now:end-1});assert.equal((await f.finish('a',{sessionId:'s'})).status,409);assert.equal(f.reads.length,0);
 const r=await f.finish('a',{sessionId:'s',cancel:true});assert.equal(r.status,200);assert.equal(r.body.endReason,'cancelled');assert.equal(f.reads.length,0);assert.equal(f.data.get('live_pk_stats588/a').streak,3);
});
test('abandoned session outside the history window cancels without inventing a winner',async()=>{
 const f=fixture({now:start+56*60*1000});const r=await f.finish('a',{sessionId:'s'});
 assert.equal(r.status,200);assert.equal(r.body.endReason,'cancelled');assert.equal(r.body.detail589,'history_expired');assert.equal(f.reads.length,0);assert.equal(f.data.get('live_pk_stats588/a').streak,3);
});
test('a score adapter is mandatory; no cached-counter fallback',()=>assert.throws(()=>createPkFinish588({store:{transact:async()=>{}}}),/Canonical score store/));

test('server start timestamp wins over an incorrect client clock',async()=>{
 const f=fixture();f.data.get('calls/s').clientStartedAt=start-86400000;
 const result=await f.finish('a',{sessionId:'s'});assert.equal(result.status,200);assert.equal(result.body.winnerUid,'a');
});
