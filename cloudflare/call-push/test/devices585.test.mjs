import test from 'node:test';
import assert from 'node:assert/strict';
import {loadDeviceTokens585} from '../src/google.mjs';
const doc=(id,token)=>({name:id,fields:{token:{stringValue:token}}});
const a='token_a_12345678901234567890',b='token_b_12345678901234567890';
test('duplicate newest documents do not hide another registered device',async()=>{
 const selected=[];
 const tokens=await loadDeviceTokens585(async()=>({documents:[doc('new',a),doc('old',a),doc('other-phone',b)]}),(...args)=>selected.push(args));
 assert.deepEqual(tokens,[a,b]);assert.deepEqual(selected,[[a,'new'],[b,'other-phone']]);
});
test('reads the next page when old duplicate registrations fill the first page',async()=>{
 const calls=[];const tokens=await loadDeviceTokens585(async cursor=>{
  calls.push(cursor);return cursor?{documents:[doc('other',b)]}:{documents:Array.from({length:100},(_,i)=>doc('duplicate'+i,a)),nextPageToken:'page/2'};
 });assert.deepEqual(tokens,[a,b]);assert.deepEqual(calls,[undefined,'page/2']);
});
test('malformed tokens are skipped and reads stay bounded with duplicates',async()=>{
 let reads=0;const tokens=await loadDeviceTokens585(async()=>{reads++;return {documents:[doc('bad','short'),doc('ok',a)],nextPageToken:'more'};});
 assert.deepEqual(tokens,[a]);assert.equal(reads,4);
});
