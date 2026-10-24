import {test} from 'node:test';import assert from 'node:assert/strict';
import {createWorker,smallBody} from './index.mjs';
const env={FIREBASE_PROJECT_ID:'ngelx-44eed',EMAIL_FROM:'NgelX <noreply@ngelxsocial.com>',RESEND_API_KEY:'synthetic',GOOGLE_SERVICE_ACCOUNT:'synthetic'};
const req=(body={})=>new Request('https://unit.invalid/verify-email',{method:'POST',headers:{authorization:'Bearer synthetic','content-type':'application/json'},body:JSON.stringify(body)});
function fixture(user={localId:'u',email:'actual@example.invalid',displayName:'<Test>',validSince:'1'}){let sent=[];const worker=createWorker({verify:async()=>({sub:'u',auth_time:10,firebase:{sign_in_provider:'password'}}),quota:async()=>true,api:async(e,url,body)=>url.endsWith('accounts:lookup')?{users:[user]}:{oobLink:'https://ngelx-44eed.firebaseapp.com/__/auth/action?mode=verifyEmail&oobCode=SYNTHETIC'},sendFetch:async(url,options)=>{sent.push(JSON.parse(options.body));return new Response('{}');}});return {worker,sent};}
test('sends approved template to account email only',async()=>{const {worker,sent}=fixture();assert.equal((await worker.fetch(req(),env)).status,200);assert.deepEqual(sent[0].to,['actual@example.invalid']);assert.match(sent[0].html,/&lt;Test&gt;/);assert.equal(sent[0].attachments.length,1);});
test('rejects recipient override without delivery',async()=>{const {worker,sent}=fixture();assert.equal((await worker.fetch(req({to:'other@example.invalid'}),env)).status,400);assert.equal(sent.length,0);});
test('revoked login cannot send',async()=>{const {worker,sent}=fixture({localId:'u',email:'actual@example.invalid',validSince:'20'});assert.equal((await worker.fetch(req(),env)).status,401);assert.equal(sent.length,0);});
test('verified account does not send',async()=>{const {worker,sent}=fixture({localId:'u',email:'actual@example.invalid',emailVerified:true});assert.equal((await worker.fetch(req(),env)).status,200);assert.equal(sent.length,0);});
test('body size is bounded',async()=>{await assert.rejects(smallBody(req({x:'x'.repeat(3000)})));});
test('missing secret fails closed',async()=>{const {worker}=fixture();assert.equal((await worker.fetch(req(),{})).status,503);});
