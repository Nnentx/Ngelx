import test from 'node:test';import assert from 'node:assert/strict';
import {pkTotals589} from '../src/pk589-totals.mjs';
import {pkStorage588} from '../src/pk588-storage.mjs';
const row=values=>[{result:{aggregateFields:Object.fromEntries(Object.entries(values).map(([k,v])=>[k,{integerValue:String(v)}]))}}];
test('all aggregate queries use the same historical timestamp and preserve legacy single hearts',async()=>{
 const queries=[];const total=pkTotals589(async(path,body)=>{
  queries.push({path,body});if(body.structuredQuery)return [{document:{fields:{points:{integerValue:'275'}}}}];const names=body.structuredAggregationQuery.aggregations.map(a=>a.alias);
  return names.includes('all')?row({all:5}):names.includes('likes')?row({numbered:3,likes:20}):row({gifts:275});
 });
 assert.deepEqual(await total('live_a',1800000000000),{likeCount:22,giftPoints:275});assert.equal(queries.length,3);
 assert.ok(queries.every(q=>q.body.readTime==='2027-01-15T08:00:00.000Z'&&q.path.startsWith('/live_streams/live_a:run')));
 const gifts=queries.find(q=>q.body.structuredQuery);assert.equal(gifts.body.structuredQuery.where.fieldFilter.value.stringValue,'gift');assert.deepEqual(gifts.body.structuredQuery.select.fields,[{fieldPath:'points'}]);
});
test('empty collections return zero; invalid or unsafe snapshots fail closed',async()=>{
 assert.deepEqual(await pkTotals589(async(path,body)=>body.structuredQuery?[{readTime:body.readTime}]:row(Object.fromEntries(body.structuredAggregationQuery.aggregations.map(a=>[a.alias,0]))))('room',1800000000000),{likeCount:0,giftPoints:0});
 await assert.rejects(pkTotals589(async()=>[])('room',1800000000000),/invalid_score_snapshot/);
 await assert.rejects(pkTotals589(async()=>row({all:Number.MAX_SAFE_INTEGER+1,numbered:0,likes:0,gifts:0}))('room',1800000000000),/invalid_score_snapshot/);
 await assert.rejects(pkTotals589(async()=>row({all:1,numbered:2,likes:0,gifts:0}))('room',1800000000000),/invalid_score_snapshot/);
});
test('REST adapter authenticates snapshots and uses readTime rather than current transaction state',async()=>{
 const calls=[];const store=pkStorage588({FIREBASE_PROJECT_ID:'ngelx-44eed'},async(url,options)=>{
  const body=JSON.parse(options.body);calls.push([url,options.headers,body]);if(body.structuredQuery)return Response.json([{document:{fields:{points:{integerValue:'150'}}}}]);const aliases=body.structuredAggregationQuery.aggregations.map(a=>a.alias);
  return Response.json(row(Object.fromEntries(aliases.map(a=>[a,a==='likes'?7:a==='gifts'?150:a==='all'?3:2]))));
 },async()=> 'server-oauth');
 assert.deepEqual(await store.totalsAt('room',1800000000000),{likeCount:8,giftPoints:150});
 assert.ok(calls.every(([url,headers,body])=>url.includes('/live_streams/room:run')&&headers.authorization==='Bearer server-oauth'&&!body.transaction&&body.readTime));
});

test('gift snapshot includes only validated projected values and refuses partial oversized scores',async()=>{
 const mock=rows=>pkTotals589(async(path,body)=>body.structuredQuery?rows:row(Object.fromEntries(body.structuredAggregationQuery.aggregations.map(a=>[a.alias,0]))));
 await assert.rejects(mock([{document:{fields:{}}}])('room',1800000000000),/invalid_score_snapshot/);
 await assert.rejects(mock([{document:{fields:{points:{integerValue:'-1'}}}}])('room',1800000000000),/invalid_score_snapshot/);
 await assert.rejects(mock(Array.from({length:20001},()=>({document:{fields:{points:{integerValue:'1'}}}})))('room',1800000000000),/score_snapshot_too_large/);
});
