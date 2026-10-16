import {createLiveHttpServer} from './live-http.js';
import {initializeApp, cert} from 'firebase-admin/app';
import {createLiveBackend} from './live-backend.js';

for (const name of ['FIREBASE_SERVICE_ACCOUNT_JSON','LIVEKIT_API_KEY','LIVEKIT_API_SECRET','LIVEKIT_URL']) {
  if (!process.env[name]) throw new Error(`Missing server configuration: ${name}`);
}
const account = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT_JSON);
if (account.project_id !== 'ngelx-44eed') throw new Error('Unexpected Firebase project');
const url = new URL(process.env.LIVEKIT_URL);
if (url.protocol !== 'wss:' || !url.hostname || url.username || url.password) throw new Error('Invalid LiveKit URL');
initializeApp({credential:cert(account),projectId:account.project_id});
const value = name => ({value:()=>process.env[name]});
const backend = createLiveBackend({apiKey:value('LIVEKIT_API_KEY'),apiSecret:value('LIVEKIT_API_SECRET'),liveUrl:value('LIVEKIT_URL')});
let sweepRunning = false;
async function sweep() {
  if (sweepRunning) return;
  sweepRunning = true;
  try { await backend.finishExpiredPK(); }
  catch (_) { console.error('PK deadline sweep failed'); }
  finally { sweepRunning = false; }
}
const server = createLiveHttpServer(backend);
server.listen(Number(process.env.PORT||10000),'0.0.0.0',()=>{
  console.log('NgelX live server ready');
  void sweep();
});
// Render Free may suspend the process. Due PKs settle on wake; no keep-alive traffic.
const timer=setInterval(()=>void sweep(),60000);
timer.unref();
for (const signal of ['SIGTERM','SIGINT']) process.on(signal,()=>{
  clearInterval(timer); server.close(()=>process.exit(0));
  setTimeout(()=>process.exit(0),10000).unref();
});
