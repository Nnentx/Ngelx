import {test} from 'node:test';
import assert from 'node:assert/strict';
import {communityDeleteStorage,createCommunityDelete556} from '../src/community-delete.mjs';
import {document} from '../../call-push/src/google.mjs';
import worker from '../src/index.mjs';
const database='projects/ngelx-44eed/databases/(default)/documents/';
const identity={uid:'owner',firebase:{sign_in_provider:'password'}};
const body={communityId:'community-556',confirmName:'PARLAMENT',confirmDelete:true};
const encodeFields=data=>Object.fromEntries(Object.entries(data).map(([key,v])=>[key,Array.isArray(v)?{arrayValue:{values:v.map(x=>({stringValue:x}))}}:typeof v==='number'?{integerValue:String(v)}:typeof v==='boolean'?{booleanValue:v}:{stringValue:v}]));
function fixture(count=3){
 let clock=1000,version=0,failAt=0;
 const docs=new Map(),calls=[];
 function set(path,value){docs.set(path,{name:database+path,fields:encodeFields(value),updateTime:'v'+(++version)});}
 set('communities450/community-556',{name:'PARLAMENT',founderId:'owner',members:['owner','member']});
 set('users/unrelated',{name:'Unrelated user'});
 for(let i=0;i<count;i++){
  const post='communities450/community-556/posts/p'+i;set(post,{text:'post'});set(post+'/comments/c',{text:'comment'});set(post+'/comments/c/reactions/r',{uid:'member'});
 }
 const fetcher=async(url,options)=>{
  calls.push({url,method:options.method??'GET'});if(failAt===calls.length){failAt=0;return new Response('',{status:503});}
  const parsed=new URL(url),path=decodeURIComponent(parsed.pathname.split('/documents')[1]??'');
  if(path===':beginTransaction')return Response.json({transaction:'tx'});
  if(path===':rollback')return Response.json({});
  if(path===':runQuery'){
   const query=JSON.parse(options.body).structuredQuery;
   const rows=[...docs.entries()].filter(([p,d])=>p.startsWith('communityInvites450/')&&document(d).communityId===query.where.fieldFilter.value.stringValue).slice(0,query.limit).map(([,document])=>({document}));
   return Response.json(rows);
  }
  if(path===':commit'){
   for(const write of JSON.parse(options.body).writes??[]){const doc=write.update;if(doc){const p=doc.name.slice(database.length);docs.set(p,{...doc,updateTime:'v'+(++version)});}}
   return Response.json({});
  }
  if(path.endsWith(':listCollectionIds')){
   const parent=path.slice(1,-':listCollectionIds'.length),prefix=parent+'/';
   const ids=[...new Set([...docs.keys()].filter(p=>p.startsWith(prefix)&&p.slice(prefix.length).includes('/')).map(p=>p.slice(prefix.length).split('/')[0]))].slice(0,10);
   return Response.json({collectionIds:ids});
  }
  const p=path.slice(1);
  if(options.method==='DELETE'){
   const expected=parsed.searchParams.get('currentDocument.updateTime');
   if(docs.has(p)&&expected&&docs.get(p).updateTime!==expected)return new Response('',{status:412});
   docs.delete(p);return Response.json({});
  }
  if(p.split('/').length%2===1){
   const prefix=p+'/',ids=[...new Set([...docs.keys()].filter(k=>k.startsWith(prefix)).map(k=>k.slice(prefix.length).split('/')[0]))].sort().slice(0,8);
   return Response.json({documents:ids.map(id=>docs.get(prefix+id)??{name:database+prefix+id})});
  }
  return docs.has(p)?Response.json(docs.get(p)):new Response('',{status:404});
 };
 const store=communityDeleteStorage({FIREBASE_PROJECT_ID:'ngelx-44eed'},{fetcher,authorize:async()=>'test-only',now:()=>clock,uuid:()=>String(++version)});
 return {store,docs,calls,set,tick:()=>{clock+=61000;},fail:offset=>{failAt=calls.length+offset;}};
}
test('worker delete route rejects missing authentication and non-POST calls',async()=>{
 assert.equal((await worker.fetch(new Request('https://example.test/community/delete',{method:'POST'}),{})).status,401);
 assert.equal((await worker.fetch(new Request('https://example.test/community/delete'),{})).status,405);
});
test('deletion validation rejects paths, extra fields, anonymous and revoked callers before mutations',async()=>{
 for(const invalid of [{...body,communityId:'../users/u'},{...body,confirmDelete:false},{...body,url:'https://foreign.test'}]){
  let touched=false;const handler=createCommunityDelete556({verify:async()=>identity,rateLimit:async()=>true,store:{claim:()=>{touched=true;}}});
  assert.equal((await handler({},invalid)).status,400);assert.equal(touched,false);
 }
 for(const verify of [async()=>({...identity,firebase:{sign_in_provider:'anonymous'}}),async()=>{throw Error('revoked');}]){
  const handler=createCommunityDelete556({verify,rateLimit:async()=>true,store:{}});assert.ok([401,403].includes((await handler({},body)).status));
 }
});
test('claim requires exact name, current founder and membership',async()=>{
 for(const actor of [{uid:'member'},identity]){
  const f=fixture();if(actor===identity)f.set('communities450/community-556',{name:'PARLAMENT',founderId:'owner',members:['member']});
  assert.equal((await f.store.claim(actor,body)).status,403);assert.ok(f.docs.has('communities450/community-556'));
 }
 const f=fixture();assert.equal((await f.store.claim(identity,{...body,confirmName:'Wrong'})).status,403);
});
test('bounded chunks recursively delete missing ancestors and nested records while preserving unrelated users',async()=>{
 const f=fixture(40);f.set('communityInvites450/owned',{communityId:'community-556'});f.set('communityInvites450/foreign',{communityId:'other'});f.docs.delete('communities450/community-556/posts/p4');
 let complete=false,chunks=0;
 while(!complete&&++chunks<100){
  const claim=await f.store.claim(identity,body);assert.equal(claim.status,202);
  const result=await f.store.advance(claim.job,claim.id);assert.ok(result.requests<=18);complete=result.done;
  await f.store.save(claim.job,claim.id,complete);
 }
 assert.ok(complete);assert.ok(chunks>1);assert.equal([...f.docs.keys()].some(p=>p.startsWith('communities450/community-556')),false);
 assert.ok(f.docs.has('users/unrelated'));assert.equal(f.docs.has('communityInvites450/owned'),false);assert.equal(f.docs.has('communityInvites450/foreign'),true);assert.equal((await f.store.claim(identity,body)).deleted,true);
 assert.equal((await f.store.claim({uid:'member'},body)).status,403);
 assert.equal([...f.docs.keys()].filter(p=>p.startsWith('community_deletions543/')).length,1);
});
test('an active lease cannot be stolen and completed ID cannot delete a recreated community',async()=>{
 const f=fixture(0),a=await f.store.claim(identity,body);
 assert.equal((await f.store.claim(identity,body)).busy,true);
 const result=await f.store.advance(a.job,a.id);await f.store.save(a.job,a.id,result.done);
 f.set('communities450/community-556',{name:'PARLAMENT',founderId:'owner',members:['owner']});
 assert.equal((await f.store.claim(identity,body)).status,403);assert.ok(f.docs.has('communities450/community-556'));
});
test('interrupted first chunk resumes from owner receipt after lease expiry without false success',async()=>{
 const f=fixture(4),claim=await f.store.claim(identity,body);f.fail(3);
 await assert.rejects(f.store.advance(claim.job,claim.id));
 assert.equal((await f.store.claim(identity,body)).busy,true);f.tick();
 let done=false;
 for(let i=0;i<20&&!done;i++){const c=await f.store.claim(identity,body);const r=await f.store.advance(c.job,c.id);done=r.done;await f.store.save(c.job,c.id,done);}
 assert.ok(done);assert.ok(f.docs.has('users/unrelated'));
});
test('queue cannot delete outside the authorized community prefix',async()=>{
 const f=fixture(0),c=await f.store.claim(identity,body);c.job.stackJson=JSON.stringify([{kind:'doc',path:'users/unrelated'}]);
 await assert.rejects(f.store.advance(c.job,c.id));assert.ok(f.docs.has('users/unrelated'));
});
test('handler reports pending until server storage confirms every descendant is gone',async()=>{
 let done=false,stored=false;
 const handler=createCommunityDelete556({verify:async()=>identity,rateLimit:async()=>true,store:{claim:async()=>({status:202,job:{},id:'community-556'}),advance:async()=>({done}),save:async()=>{stored=true;}}});
 let result=await handler({},body);assert.equal(result.status,202);assert.equal(result.body.deleted,false);assert.ok(stored);
 done=true;result=await handler({},body);assert.equal(result.status,200);assert.equal(result.body.deleted,true);
});
