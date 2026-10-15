import test from 'node:test';
import assert from 'node:assert/strict';
import {serveMediaRequest} from '../src/range_media.js';

const cors=()=>({'access-control-allow-origin':'*'});
const json=(val,status)=>new Response(JSON.stringify(val),{status});
const contentTypeFor=(ext,supplied)=>supplied&&supplied!=='application/octet-stream'
  ?supplied:({mp4:'video/mp4',webp:'image/webp'}[ext]||'application/octet-stream');
function object(range){
 return {size:100,httpEtag:'"v1"',range,
   body:new TextEncoder().encode('0123456789'),
   writeHttpMetadata(headers){headers.set('content-type','application/octet-stream');}};
}
const env=(range)=>({
  async get(key,options){assert.equal(key,'videos/test.mp4');return object(range);},
  async head(key){assert.equal(key,'videos/test.mp4');return object(range);}
});
const url=new URL('https://media.ngelxsocial.com/media/videos/test.mp4');
const deps={cors,json,contentTypeFor};

test('returns HTTP 206 with exact media byte offsets and MP4 type',async()=>{
 const request=new Request(url,{headers:{Range:'bytes=10-19'}});
 const response=await serveMediaRequest(request,url,env({offset:10,length:10}),deps);
 assert.equal(response.status,206);
 assert.equal(response.headers.get('content-range'),'bytes 10-19/100');
 assert.equal(response.headers.get('accept-ranges'),'bytes');
 assert.equal(response.headers.get('content-length'),'10');
 assert.equal(response.headers.get('content-type'),'video/mp4');
});
test('returns HTTP 200 and total length for full media GET',async()=>{
 const response=await serveMediaRequest(new Request(url),url,env(null),deps);
 assert.equal(response.status,200);
 assert.equal(response.headers.get('content-length'),'100');
});
test('HEAD does not fetch body',async()=>{
 let getCalled=false;
 const media={...env(null),async get(){getCalled=true;}};
 const response=await serveMediaRequest(new Request(url,{method:'HEAD'}),url,media,deps);
 assert.equal(response.status,200);
 assert.equal(await response.text(),'');
 assert.equal(getCalled,false);
});
test('invalid or unsatisfiable range does not return false success',async()=>{
 const response=await serveMediaRequest(new Request(url,{headers:{Range:'bytes=200-300'}}),url,env(null),deps);
 assert.equal(response.status,416);
 assert.equal(response.headers.get('content-range'),'bytes */100');
});
test('GET range only reads media',async()=>{
 let get=0,head=0;
 const media={async get(key,opts){get++;assert.ok(opts.range instanceof Headers);return object({offset:20,length:5});},
   async head(){head++;throw Error('no head for range');}};
 const response=await serveMediaRequest(new Request(url,{headers:{Range:'bytes=20-24'}}),url,media,deps);
 assert.equal(response.status,206);assert.equal(get,1);assert.equal(head,0);
});
test('invalid key is rejected',async()=>{
 const req={method:'GET',headers:new Headers()};
 const response=await serveMediaRequest(req,new URL('https://example.com/media/%2E%2E%2Fsecret'),env(null),deps);
 assert.equal(response.status,400);
});
