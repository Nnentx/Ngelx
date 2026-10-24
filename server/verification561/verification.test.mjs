import test from 'node:test';
import assert from 'node:assert/strict';
import {verificationEmail561} from './template.mjs';
import {createVerificationHandler561} from './handler.mjs';
const link='https://ngelx-44eed.firebaseapp.com/__/auth/action?mode=verifyEmail&oobCode=synthetic-test-only';
test('HTML and plain text preserve the real action; hostile names cannot inject markup',()=>{
 const m=verificationEmail561({name:'<img src=x onerror=alert(1)>',link});
 assert.match(m.html,/&lt;img/);assert.doesNotMatch(m.html,/<img src=x/);
 assert.match(m.html,/E-postamı Doğrula/);assert.match(m.html,/cid:ngelx-verification-envelope/);
 assert.match(m.html,/lang=tr/);assert.match(m.text,/synthetic-test-only/);
 assert.equal(m.attachments[0].content_id,'ngelx-verification-envelope');
 assert.equal(Buffer.from(m.attachments[0].content,'base64').subarray(1,4).toString(),'PNG');
});
test('arbitrary links and wrong actions are rejected',()=>{
 for(const value of ['https://evil.example/__/auth/action?mode=verifyEmail&oobCode=x',link.replace('verifyEmail','resetPassword'),link.replace('https:','http:'),link.replace('oobCode=synthetic-test-only','x=1'),link.replace('firebaseapp.com','firebaseapp.com.evil.example')]){
  assert.throws(()=>verificationEmail561({name:'A',link:value}));
 }
});
function fixture(overrides={}){
 const calls=[];
 const handler=createVerificationHandler561({verifyToken:async token=>({uid:'user',firebase:{sign_in_provider:'password'}}),rateLimit:async()=>true,getUser:async()=>({email:'actual@example.test',displayName:'Şevket'}),generateLink:async email=>{calls.push(['link',email]);return link;},send:async mail=>{calls.push(['mail',mail]);},...overrides});
 return {handler,calls};
}
test('recipient is resolved from Auth and a fresh action link is sent once',async()=>{
 const {handler,calls}=fixture();const response=await handler({token:'valid',body:{}});
 assert.equal(response.status,200);assert.deepEqual(response.body,{sent:true});
 assert.equal(calls[0][1],'actual@example.test');assert.equal(calls[1][1].to,'actual@example.test');
 assert.equal(calls.length,2);
});
test('client cannot choose a recipient or verification link',async()=>{
 const {handler,calls}=fixture();
 for(const body of [{email:'other@example.test'},{link},{name:'injected'},[],null])assert.equal((await handler({token:'valid',body})).status,400);
 assert.equal(calls.length,0);
});
test('unauthenticated, revoked, anonymous and disabled accounts send nothing',async()=>{
 const cases=[{token:undefined,override:{}},{token:'revoked',override:{verifyToken:async()=>{throw Error('revoked');}}},{token:'guest',override:{verifyToken:async()=>({uid:'guest',firebase:{sign_in_provider:'anonymous'}})}},{token:'disabled',override:{getUser:async()=>({disabled:true,email:'a@example.test'})}}];
 for(const c of cases){const {handler,calls}=fixture(c.override);assert.ok([401,403].includes((await handler({token:c.token,body:{}})).status));assert.equal(calls.length,0);}
});
test('already verified and rate-limited users do not receive extra mail',async()=>{
 for(const override of [{rateLimit:async()=>false},{getUser:async()=>({email:'a@example.test',emailVerified:true})}]){
  const {handler,calls}=fixture(override);await handler({token:'valid',body:{}});assert.equal(calls.length,0);
 }
});
test('delivery errors are reported without leaking action tokens',async()=>{
 const {handler}=fixture({send:async()=>{throw Error('synthetic-test-only');}});
 const response=await handler({token:'valid',body:{}});assert.equal(response.status,503);assert.doesNotMatch(JSON.stringify(response),/synthetic-test-only/);
});
