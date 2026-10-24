import test from 'node:test';import assert from 'node:assert/strict';
import {threeMonths,identityPlan,updateIdentity,verificationEmail} from './policy.mjs';
test('three calendar months clamp month ends and preserve UTC time',()=>{
 assert.equal(threeMonths('2026-01-31T23:30:12.345Z').toISOString(),'2026-04-30T23:30:12.345Z');
 assert.equal(threeMonths('2023-11-30T10:00:00Z').toISOString(),'2024-02-29T10:00:00.000Z');
 assert.equal(threeMonths('2026-10-24T23:30:00Z').toISOString(),'2027-01-24T23:30:00.000Z');
});
test('independent clocks, exact boundary, unchanged values, missing legacy timestamp',()=>{
 const p={displayName:'Old Name',username:'oldname',displayNameChangedAt559:new Date('2026-01-31T23:30:00Z')};
 assert.throws(()=>identityPlan(p,{displayName:'New Name'},new Date('2026-04-30T23:29:59Z')),/cooldown/);
 const plan=identityPlan(p,{displayName:'New Name'},new Date('2026-04-30T23:30:00Z'));assert.equal(plan.displayName,'New Name');assert.ok(!Object.hasOwn(plan,'usernameChangedAt559'));
 assert.deepEqual(identityPlan(p,{displayName:' Old Name '},new Date('2026-02-01')),{});
 assert.equal(identityPlan(p,{username:'different'},new Date('2026-02-01')).username,'different');
 assert.throws(()=>identityPlan(p,{username:'admin'},new Date()),/invalid-username/);
 assert.throws(()=>identityPlan(p,{displayNameChangedAt559:0},new Date()),/invalid-request/);
});
function fixture(profile,foreign){
 const writes=[];const ref=(path)=>({path});
 const db={collection:collection=>({doc:id=>ref(collection+'/'+id),where:(field,op,value)=>({limit:n=>({query:true,field,value})})}),runTransaction:async f=>f({get:async r=>r.query?{docs:foreign?[{id:'other'}]:[]}:{exists:r.path==='users/u',data:()=>r.path==='app_config/identity559'?{usernameIndexReady:true}:profile},set:(r,v)=>writes.push([r.path,v]),update:(r,v)=>writes.push([r.path,v])})};return {db,writes};
}
test('name ownership is read before writes, rejects duplicates and retires old handle',async()=>{
 let f=fixture({username:'oldname',usernameLower:'oldname'},true);
 await assert.rejects(updateIdentity({db:f.db,uid:'u',body:{username:'newname'}}),/username-taken/);assert.equal(f.writes.length,0);
 f=fixture({username:'oldname',usernameLower:'oldname'},false);
 await updateIdentity({db:f.db,uid:'u',body:{username:'newname'}});
 assert.equal(f.writes.find(([p])=>p==='login_usernames/oldname')[1].status,'retired');
 assert.equal(f.writes.find(([p])=>p==='users/u')[1].username,'newname');
});
test('email is Turkish, escaped, button-linked, and cannot link an arbitrary host',()=>{
 const link='https://ngelx-44eed.firebaseapp.com/__/auth/action?mode=verifyEmail&oobCode=TEST-ONLY&lang=tr';
 const email=verificationEmail({name:'<img src=x>',link});
 assert.ok(email.html.includes('E-postamı doğrula'));assert.ok(email.html.includes('&lt;img src=x&gt;'));assert.ok(!email.html.includes('<img src=x>'));
 assert.ok(!email.html.includes('Hello'));assert.ok(email.text.includes('NgelX Ekibi'));assert.ok(email.html.includes('href="https://ngelx-44eed.firebaseapp.com/__/auth/action?mode=verifyEmail&amp;'));
 assert.throws(()=>verificationEmail({name:'A',link:'https://evil.test/?mode=verifyEmail&oobCode=X'}));
});
