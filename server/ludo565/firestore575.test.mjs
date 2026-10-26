import {test} from 'node:test';
import assert from 'node:assert/strict';
import {ludoStore565} from '../../cloudflare/live-moderation/src/ludo565.mjs';

const env={FIREBASE_PROJECT_ID:'ngelx-44eed'};
const root='projects/ngelx-44eed/databases/(default)/documents/_ngelx_ludo565/';
const commit='https://firestore.googleapis.com/v1/projects/ngelx-44eed/databases/(default)/documents:commit';
const create=(fetcher)=>ludoStore565(env,{fetcher,authorize:async()=>'review-only-bearer'});

test('Firestore wallet reads decode stored JSON and return CAS update timestamp',async()=>{
 const calls=[],version='2026-10-26T12:00:00.000Z';
 const db=create(async(url,options)=>{
  calls.push([url,options]);
  return Response.json({name:root+'wallet575_test',updateTime:version,
   fields:{state:{stringValue:JSON.stringify({chips:130,xp:90,receipts:{}})}}});
 });
 const record=await db.get('wallet575_test');
 assert.equal(record.stamp,version);
 assert.deepEqual(record.room,{chips:130,xp:90,receipts:{}});
 assert.equal(calls[0][0], 'https://firestore.googleapis.com/v1/'+root+'wallet575_test');
 assert.equal(calls[0][1].headers.authorization,'Bearer review-only-bearer');
});

test('two-document AdMob reservation uses an all-or-nothing Firestore REST commit',async()=>{
 const calls=[],db=create(async(url,options)=>{
  calls.push([url,options]);return Response.json({writeResults:[{},{}]});
 });
 await db.putMany([
  {id:'wallet575_example',room:{adPending:'token'},stamp:'2026-10-26T12:00:00Z'},
  {id:'ad_session575_testtoken',room:{used:false},stamp:undefined},
 ]);
 assert.equal(calls.length,1);
 const [url,options]=calls[0],body=JSON.parse(options.body);
 assert.equal(url,commit);
 assert.equal(options.method,'POST');
 assert.equal(options.headers.authorization,'Bearer review-only-bearer');
 assert.equal(body.writes.length,2);
 assert.equal(body.writes[0].update.name,root+'wallet575_example');
 assert.deepEqual(body.writes[0].currentDocument,{updateTime:'2026-10-26T12:00:00Z'});
 assert.deepEqual(body.writes[1].currentDocument,{exists:false});
 assert.equal(JSON.parse(body.writes[0].update.fields.state.stringValue).adPending,'token');
});

test('three-document paid gift and SSV payout use the same verified atomic CAS contract',async()=>{
 const calls=[],db=create(async(url,options)=>{
  calls.push([url,options]);return Response.json({writeResults:[{},{},{}]});
 });
 await db.putMany([
  {id:'wallet575_sender',room:{chips:30},stamp:'version1'},
  {id:'wallet575_recipient',room:{giftsReceived:{flower:1}},stamp:'version2'},
  {id:'room575',room:{gifts:[{emoji:'🌹'}]},stamp:'version3'},
 ]);
 const body=JSON.parse(calls[0][1].body);
 assert.equal(calls[0][0],commit);
 assert.equal(body.writes.length,3);
 assert.deepEqual(body.writes.map(x=>x.currentDocument.updateTime),['version1','version2','version3']);
 assert.deepEqual(body.writes.map(x=>x.update.name),
  ['wallet575_sender','wallet575_recipient','room575'].map(id=>root+id));
});

test('Firestore REST conflict yields retryable 409; invalid CAS scope is never sent',async()=>{
 let calls=0;
 const db=create(async()=>{calls++;return Response.json({error:'conflict'},{status:409});});
 await assert.rejects(db.putMany([
  {id:'a',room:{},stamp:'old'},{id:'b',room:{},stamp:undefined},
 ]),e=>e.status===409&&e.message==='state_changed');
 assert.equal(calls,1);
 await assert.rejects(db.putMany([{id:'only',room:{}}]),e=>e.status===400);
 await assert.rejects(db.putMany([
  {id:'a',room:{}},{id:'a',room:{}},
 ]),e=>e.status===400);
 assert.equal(calls,1);
 assert.throws(()=>ludoStore565({FIREBASE_PROJECT_ID:'untrusted'}),/Wrong project/);
});

test('Ludo Firestore adapter never reads or writes arbitrary service-account document paths',async()=>{
 const called=[];
 const db=create(async(url,options)=>{called.push(url);return Response.json({});});
 const invalid=[
  '../users/privileged', 'wallet575_a/b', 'wallet575_a?mask.fieldPaths=x',
  '%2e%2e%2fusers', 'room#fragment', 'a%2Fb', '..', '.', '',
  'a'.repeat(181), 'space in key', 'a:b', '\\u0000evil',
 ];
 for(const id of invalid){
  await assert.rejects(db.get(id),e=>e.status===400&&e.message==='invalid_document_id');
  await assert.rejects(db.put(id,{chips:0}),e=>e.status===400&&e.message==='invalid_document_id');
  await assert.rejects(db.putMany([
   {id:'wallet575_safe',room:{chips:1},stamp:undefined},
   {id,room:{chips:2},stamp:undefined},
  ]),e=>e.status===400&&e.message==='invalid_document_id');
 }
 assert.equal(called.length,0,'No invalid ID may cause an upstream Firestore call');
 const validIds=[
  '123456', 'ABCDEF0123456789', 'view570_ABCDEF0123456789',
  'wallet575_'+'a'.repeat(64),
  'report575_'+'d'.repeat(64),
  'moderation_queue575_2026-10-26',
 ];
 for(const id of validIds)await db.get(id);
 assert.equal(called.length,validIds.length);
 assert.ok(called.every(url=>url.startsWith('https://firestore.googleapis.com/v1/'+root)));
});
