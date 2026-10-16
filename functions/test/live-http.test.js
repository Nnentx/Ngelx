import test from 'node:test';
import assert from 'node:assert/strict';
import {createLiveHttpServer} from '../live-http.js';
test('HTTP adapter preserves signed webhook bytes, validates API bodies and isolates health',async()=>{
 const calls=[];
 const server=createLiveHttpServer({
  live:async(req,res)=>{calls.push({path:req.path,body:req.body,auth:req.headers.authorization});res.json({ok:true});},
  webhook:async(req,res)=>{calls.push({raw:req.rawBody.toString(),auth:req.headers.authorization});res.sendStatus(200);},
 });
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
 const base=`http://127.0.0.1:${server.address().port}`;
 try {
  assert.equal((await fetch(base+'/health')).status,200);assert.equal(calls.length,0);
  assert.equal((await fetch(base+'/live/start')).status,405);
  assert.equal((await fetch(base+'/other')).status,404);
  assert.equal((await fetch(base+'/live/start',{method:'POST',body:'{}'})).status,415);
  for(const body of ['bad','[]','null']) assert.equal((await fetch(base+'/live/start',{method:'POST',headers:{'Content-Type':'application/json'},body})).status,400);
  assert.equal((await fetch(base+'/live/start',{method:'POST',headers:{'Content-Type':'application/json'},body:'x'.repeat(16385)})).status,413);
  assert.equal(calls.length,0);
  await fetch(base+'/live/start',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer test-token'},body:'{"title":"Test"}'});
  assert.deepEqual(calls[0],{path:'/live/start',body:{title:'Test'},auth:'Bearer test-token'});
  const raw='{ "event" : "participant_joined" }\n';
  await fetch(base+'/webhook',{method:'POST',headers:{Authorization:'test-signature'},body:raw});
  assert.deepEqual(calls[1],{raw,auth:'test-signature'});
 } finally {await new Promise(resolve=>server.close(resolve));}
});
