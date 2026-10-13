import test from 'node:test';
import assert from 'node:assert/strict';
import {giftCost, validRecipient, pkLive, finishPK, requireActive, validId} from '../live-domain.js';
test('gift quantities reject negative, fractional, huge and unknown inputs',()=>{
 for(const [id,n] of [['rose',0],['rose',-1],['rose',1.5],['rose',100],['__proto__',1],['unknown',1]])assert.throws(()=>giftCost(id,n));
 assert.equal(giftCost('rocket',99),49500);
});
test('only current host/guest receive gifts',()=>{
 const stream={ownerId:'host',guestUid:'guest'};
 assert.ok(validRecipient(stream,'host'));assert.ok(validRecipient(stream,'guest'));
 assert.equal(validRecipient(stream,'viewer'),false);assert.equal(validRecipient({ownerId:'host',guestUid:''},''),false);
});
test('PK boundary excludes gifts arriving at and after deadline',()=>{
 const pk={status:'active',endsAtMs:1000};assert.ok(pkLive(pk,999));assert.equal(pkLive(pk,1000),false);
 assert.equal(pkLive({status:'pending',endsAtMs:1000},999),false);
});
test('PK winner and draw use authoritative scores',()=>{
 assert.equal(finishPK({hostScore:10,guestScore:9}).result,'host');
 assert.equal(finishPK({hostScore:8,guestScore:9}).result,'guest');
 assert.equal(finishPK({hostScore:9,guestScore:9}).result,'draw');
});
test('closed streams and invalid document paths are rejected',()=>{
 assert.throws(()=>requireActive(null));assert.throws(()=>requireActive({active:false}));
 assert.throws(()=>validId('../wallet'));assert.throws(()=>validId('a/b'));assert.equal(validId('live-123_abc'),'live-123_abc');
});
