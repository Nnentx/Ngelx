import test from 'node:test';import assert from 'node:assert/strict';
import {verifyFirebaseIdToken} from '../src/auth.mjs';
const keys=await crypto.subtle.generateKey({name:'RSASSA-PKCS1-v1_5',modulusLength:2048,publicExponent:new Uint8Array([1,0,1]),hash:'SHA-256'},true,['sign','verify']);
const pub=await crypto.subtle.exportKey('jwk',keys.publicKey);pub.kid='unit-key';
const original=globalThis.fetch;globalThis.fetch=async()=>new Response(JSON.stringify({keys:[pub]}),{headers:{'cache-control':'max-age=3600'}});
const b64=x=>Buffer.from(x).toString('base64url');const now=Math.floor(Date.now()/1000);
const base={aud:'ngelx-44eed',iss:'https://securetoken.google.com/ngelx-44eed',sub:'a',iat:now,exp:now+300,firebase:{sign_in_provider:'password'}};
async function request(payload=base){const raw=b64(JSON.stringify({alg:'RS256',kid:'unit-key'}))+'.'+b64(JSON.stringify(payload));const sig=await crypto.subtle.sign('RSASSA-PKCS1-v1_5',keys.privateKey,new TextEncoder().encode(raw));return new Request('https://example.test',{headers:{authorization:'Bearer '+raw+'.'+b64(sig)}});}
test('real RSA signature verifies project-bound Firebase login',async()=>assert.equal((await verifyFirebaseIdToken(await request(),{FIREBASE_PROJECT_ID:'ngelx-44eed'})).sub,'a'));
test('expired, wrong issuer, wrong audience and anonymous tokens rejected',async()=>{for(const change of [{exp:now-1},{aud:'other'},{iss:'https://attacker.test'},{firebase:{sign_in_provider:'anonymous'}}])await assert.rejects(verifyFirebaseIdToken(await request({...base,...change}),{FIREBASE_PROJECT_ID:'ngelx-44eed'}));});
test('tampered signed token and missing authorization rejected',async()=>{const r=await request();const auth=r.headers.get('authorization');const parts=auth.split('.');parts[1]=b64(JSON.stringify({...base,sub:'attacker'}));await assert.rejects(verifyFirebaseIdToken(new Request('https://example.test',{headers:{authorization:parts.join('.')}}),{FIREBASE_PROJECT_ID:'ngelx-44eed'}));await assert.rejects(verifyFirebaseIdToken(new Request('https://example.test'),{FIREBASE_PROJECT_ID:'ngelx-44eed'}));});
test.after(()=>{globalThis.fetch=original;});
