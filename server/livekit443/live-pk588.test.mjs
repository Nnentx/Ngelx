import test from 'node:test';import assert from 'node:assert/strict';
import {pkResult588,createPkFinish588} from './live-pk588.mjs';
const session={type:'live_pk',status:'active',members:['a','b'],inviterUid:'a',inviteeUid:'b',inviterLiveId:'ra',inviteeLiveId:'rb',clientStartedAt:1000000,endsAt:1180000,startLikeA:10,startLikeB:20,startGiftA:100,startGiftB:200};
const a={ownerId:'a',pkSessionId:'s',likeCount:15,giftPoints:200},b={ownerId:'b',pkSessionId:'s',likeCount:21,giftPoints:210};
test('win increments winner, resets loser, ties preserve both',()=>{
 const r=pkResult588(session,a,b,{streak:3},{streak:8},1180000);
 assert.deepEqual(r.finalScoreByUid,{a:15,b:2});assert.deepEqual(r.streakByUid,{a:4,b:0});
 const tie=pkResult588({...session,startLikeA:0,startLikeB:0,startGiftA:0,startGiftB:0},{likeCount:0},{likeCount:0},{streak:3},{streak:8},1180000);
 assert.equal(tie.winnerUid,null);assert.deepEqual(tie.streakByUid,{a:3,b:8});
});
test('no early win; cancellation does not change streak; end boundary settles',()=>{
 assert.throws(()=>pkResult588(session,a,b,{}, {},1179999),/not_finished/);
 assert.equal(pkResult588(session,a,b,{}, {},1179999,true).streakByUid,undefined);
 assert.equal(pkResult588(session,a,b,{}, {},1180000,true).winnerUid,'a');
});
test('negative deltas cannot produce negative scores',()=>assert.deepEqual(pkResult588(session,{likeCount:0,giftPoints:0},{likeCount:0,giftPoints:0},{},{},1180000).finalScoreByUid,{a:0,b:0}));
function fixture(){
 const data=new Map(Object.entries({'calls/s':structuredClone(session),'live_streams/ra':structuredClone(a),'live_streams/rb':structuredClone(b),'live_pk_stats588/a':{streak:3},'live_pk_stats588/b':{streak:8}}));
 let tail=Promise.resolve();
 const store={transact:fn=>{const next=tail.then(async()=>{const pending=[];const result=await fn({get:p=>Promise.resolve(structuredClone(data.get(p))),update:(p,v)=>pending.push([p,v])});for(const [p,v] of pending)data.set(p,{...data.get(p),...v});return result;});tail=next.catch(()=>{});return next;}};
 return {data,finish:createPkFinish588({store,now:()=>1180000})};
}
test('both clients finishing concurrently increment streak exactly once',async()=>{
 const {data,finish}=fixture();const [x,y]=await Promise.all([finish('a',{sessionId:'s'}),finish('b',{sessionId:'s'})]);
 assert.equal(x.status,200);assert.equal(y.status,200);assert.equal(data.get('live_pk_stats588/a').streak,4);assert.equal(data.get('live_pk_stats588/b').streak,0);
 assert.equal(data.get('live_streams/rb').pkActive,false);
});
test('unrelated accounts, score injection and malformed body rejected',async()=>{
 const {data,finish}=fixture();assert.equal((await finish('c',{sessionId:'s'})).status,403);assert.equal((await finish('a',{sessionId:'s',score:999})).status,400);assert.equal(data.get('live_pk_stats588/a').streak,3);
});
test('a new PK continues the persisted streak and a later loss resets it',async()=>{
 const {data,finish}=fixture();await finish('a',{sessionId:'s'});
 data.set('calls/next',{...session});data.set('live_streams/ra',{...a,pkSessionId:'next'});data.set('live_streams/rb',{...b,pkSessionId:'next',likeCount:100});
 assert.equal((await finish('b',{sessionId:'next'})).status,200);assert.equal(data.get('live_pk_stats588/a').streak,0);assert.equal(data.get('live_pk_stats588/b').streak,1);
});
test('stale sessions cannot overwrite a new active PK',async()=>{
 const {data,finish}=fixture();data.get('live_streams/ra').pkSessionId='new';assert.equal((await finish('a',{sessionId:'s'})).status,422);assert.equal(data.get('live_pk_stats588/a').streak,3);
});
