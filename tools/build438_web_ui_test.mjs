import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
const root=path.resolve('web');
const server=http.createServer(async(req,res)=>{
  const file=path.resolve(root,'.'+new URL(req.url,'http://localhost').pathname);
  if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
  try{const data=await fs.readFile(file);res.setHeader('Content-Type',file.endsWith('.mjs')?'text/javascript':file.endsWith('.css')?'text/css':'text/html');res.end(data);}catch(_){res.writeHead(404).end();}
});
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
const origin='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({headless:true});
// Only fake SDK modules are served. No real accounts or backend requests are used.
const mocks={
  'firebase-app.js':`export const initializeApp=()=>({});`,
  'firebase-auth.js':`const auth={currentUser:null};export const getAuth=()=>auth;export const inMemoryPersistence={};export async function setPersistence(){} export async function signInWithEmailAndPassword(_,email){auth.currentUser={uid:'browser438',email};return {user:auth.currentUser};} export async function signOut(){auth.currentUser=null;} export async function sendPasswordResetEmail(){}`,
  'firebase-firestore.js':`export const getFirestore=()=>({});export class Timestamp{constructor(ms){this.ms=ms;}static fromMillis(ms){return new Timestamp(ms);}toDate(){return new Date(this.ms);}}export const serverTimestamp=()=>new Timestamp(Date.now());export const collection=(_,p)=>({path:p});export const doc=(db,...parts)=>({path:parts.length?parts.join('/'):db.path+'/browser-request',id:parts.at(-1)||'browser-request'});const data=new Map([['users/browser438',{displayName:'Test',deactivated:false}]]);window.__writes=[];export async function runTransaction(_,fn){return fn({get:async ref=>({exists:()=>data.has(ref.path),data:()=>data.get(ref.path)}),set:(ref,value)=>{data.set(ref.path,value);window.__writes.push({path:ref.path,value});}});}export async function setDoc(ref,value){window.__writes.push({path:ref.path,value});}`,
};
try{
  for(const width of [360,1280]){
    const context=await browser.newContext({viewport:{width,height:900}});
    await context.route('https://www.gstatic.com/firebasejs/**',route=>{
      const key=new URL(route.request().url()).pathname.split('/').at(-1);
      return route.fulfill({contentType:'text/javascript',body:mocks[key]||''});
    });
    for(const file of ['delete-account.html','support.html']){
      const page=await context.newPage();
      await page.goto(origin+'/'+file);
      await page.waitForFunction(()=>!document.getElementById('login').disabled);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
      await page.fill('#email','browser@example.test');await page.fill('#password','fake-test-password');
      await page.click('#login');await page.waitForSelector('#action-section',{state:'visible'});
      assert.equal(await page.inputValue('#password'),'');
      if(file.startsWith('delete')){
        await page.click('#submit');
        assert.equal(await page.evaluate(()=>window.__writes.length),0,'Confirmation checkbox must prevent accidental deletion');
        await page.check('#confirm');
      }else{await page.fill('#description','Tarayıcı formu için yeterli test açıklaması.');}
      await page.click('#submit');
      await page.waitForSelector('#status.success');
      const writes=await page.evaluate(()=>window.__writes);
      assert.equal(JSON.stringify(writes).includes('fake-test-password'),false);
      assert.equal(writes.length,file.startsWith('delete')?2:1);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
      if(file.startsWith('delete'))assert.equal(await page.locator('#action-form').isHidden(),true);
      await page.close();
    }
    await context.close();
  }
  const context=await browser.newContext();
  await context.route('https://www.gstatic.com/firebasejs/**',route=>route.abort());
  const page=await context.newPage();await page.goto(origin+'/support.html');await page.waitForSelector('#status.error');
  assert.equal(await page.locator('#login').isDisabled(),true,'SDK failure must not leave a working-looking submit button');
  await context.close();
  console.log('Web UI passed: mobile/desktop overflow, explicit deletion confirmation, password clearing, success states and SDK failure handling.');
}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
