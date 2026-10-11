import {test} from 'node:test';
import assert from 'node:assert/strict';
import {normalizeUsername,planUsernameMigration} from '../username-ownership.mjs';
test('username policy matches registration length, characters and reserved names',()=>{
  assert.equal(normalizeUsername(' User.Name_1 '),'user.name_1');
  assert.equal(normalizeUsername('a'.repeat(20)),'a'.repeat(20));
  for(const value of ['ab','a'.repeat(21),'user name','ROOT','support','e@example.com','+905551234567'])assert.throws(()=>normalizeUsername(value));
});
test('migration never picks one owner for duplicate usernames',()=>{
  const result=planUsernameMigration([{uid:'b',usernameLower:'same'},{uid:'a',usernameLower:'same'},{uid:'c',usernameLower:'unique'}]);
  assert.deepEqual(result.active,[{username:'unique',uid:'c'}]);
  assert.deepEqual(result.conflicts,[{username:'same',uids:['a','b']}]);
});
test('invalid and reserved legacy names remain unresolved',()=>{
  const result=planUsernameMigration([{uid:'a',usernameLower:'Admin'},{uid:'b',usernameLower:'ab'},{uid:'c',usernameLower:'Valid'}]);
  assert.equal(result.invalid.length,3);assert.equal(result.active.length,0);
});
test('repeated same profile does not create false conflict',()=>{
  assert.deepEqual(planUsernameMigration([{uid:'a',usernameLower:'user'},{uid:'a',usernameLower:'user'}]).active,[{username:'user',uid:'a'}]);
});
