import test from 'node:test';
import assert from 'node:assert/strict';
import {sendLiveGift} from '../live-gifts.js';
function harness() {
 const pathRef=path=>({path,collection:name=>({doc:id=>pathRef(`${path}/${name}/${id}`)})});
 const ref=pathRef('live_streams/s');
 const records=new Map([['live_streams/s',{active:true,ownerId:'host',guestUid:'guest',pk:{id:'p',status:'active',endsAtMs:1000,hostScore:0,guestScore:0}}],['wallets/sender',{coins:1000}],['wallets/host',{earnedCoins:0}]]);
 let queue=Promise.resolve();
 const db={collection:name=>({doc:id=>pathRef(`${name}/${id}`)}),runTransaction:fn=>{
  const execute=async()=>{
   const writes=[];
   const tx={get:async r=>({data:()=>structuredClone(records.get(r.path))}),set:(r,v)=>writes.push(()=>records.set(r.path,{...records.get(r.path),...v})),create:(r,v)=>writes.push(()=>{assert.equal(records.has(r.path),false);records.set(r.path,v);}),update:(r,v)=>writes.push(()=>records.set(r.path,{...records.get(r.path),...v}))};
   const result=await fn(tx);for(const write of writes)write();return result;
  };
  const result=queue.then(execute);queue=result.catch(()=>{});return result;
 }};
 const data={giftId:'rose',quantity:5,targetUid:'host',requestId:'request1'};
 const send=(changes={},now=999)=>sendLiveGift(db,ref,'sender',{...data,...changes},()=>123,()=>now);
 return {records,send};
}
test('gift debit, receipt, recipient earnings and PK score commit together',async()=>{
 const h=harness();await h.send();
 assert.equal(h.records.get('wallets/sender').coins,950);
 assert.equal(h.records.get('wallets/host').earnedCoins,50);
 assert.equal(h.records.get('live_streams/s').pk.hostScore,50);
 assert.equal(h.records.get('live_streams/s/gifts/sender_request1').coins,50);
});
test('retry after stream closure acknowledges committed receipt without charging again',async()=>{
 const h=harness();await h.send();h.records.get('live_streams/s').active=false;
 assert.deepEqual(await h.send(),{ok:true,coins:50});assert.equal(h.records.get('wallets/sender').coins,950);
 await assert.rejects(h.send({requestId:'new'}));
});
test('duplicate concurrent attempts produce one debit and one receipt',async()=>{
 const h=harness();await Promise.all([h.send(),h.send(),h.send()]);
 assert.equal(h.records.get('wallets/sender').coins,950);assert.equal(h.records.get('wallets/host').earnedCoins,50);
});
test('changed payload cannot reuse a committed request identity',async()=>{
 const h=harness();await h.send();await assert.rejects(h.send({quantity:10}));
 await assert.rejects(h.send({targetUid:'guest'}));assert.equal(h.records.get('wallets/sender').coins,950);
});
test('insufficient wallet, self-gift and invalid recipient create no receipt',async()=>{
 for(const changes of [{giftId:'rocket',quantity:5},{targetUid:'sender'},{targetUid:'outsider'}]) {
  const h=harness();await assert.rejects(h.send(changes));
  assert.equal(h.records.get('wallets/sender').coins,1000);assert.equal(h.records.has('live_streams/s/gifts/sender_request1'),false);
 }
});
test('gift at PK deadline debits normally but does not add PK score',async()=>{
 const h=harness();await h.send({},1000);assert.equal(h.records.get('wallets/sender').coins,950);assert.equal(h.records.get('live_streams/s').pk.hostScore,0);
});
test('invalid earnings or overflowing score cannot partially debit sender',async()=>{
 for(const invalid of ['earnings','score']) {
  const h=harness();
  if(invalid==='earnings')h.records.get('wallets/host').earnedCoins=-1;
  else h.records.get('live_streams/s').pk.hostScore=Number.MAX_SAFE_INTEGER;
  await assert.rejects(h.send());assert.equal(h.records.get('wallets/sender').coins,1000);
 }
});
