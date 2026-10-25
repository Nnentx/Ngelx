import {createRoom,act,LudoError} from '../../../server/ludo565/engine.mjs';
import {accessToken} from '../../call-push/src/google.mjs';
export function ludoStore565(env,{fetcher=fetch,authorize=()=>accessToken(env)}={}){
 if(env.FIREBASE_PROJECT_ID!=='ngelx-44eed')throw Error('Wrong project');
 const base=`https://firestore.googleapis.com/v1/projects/${env.FIREBASE_PROJECT_ID}/databases/(default)/documents/_ngelx_ludo565/`;
 async function api(id,options={}){const r=await fetcher(base+id,{...options,headers:{authorization:'Bearer '+await authorize(),'content-type':'application/json'},signal:AbortSignal.timeout(8000)});if(r.status===404)return null;if(r.status===409||r.status===412)throw new LudoError('state_changed',409);if(!r.ok)throw Error('Datastore unavailable');return r.json();}
 return {
  async get(id){const d=await api(id);return d?{room:JSON.parse(d.fields.state.stringValue),stamp:d.updateTime}:null;},
  async put(id,room,stamp){return api(id+'?'+(stamp?'currentDocument.updateTime='+encodeURIComponent(stamp):'currentDocument.exists=false'),{method:'PATCH',body:JSON.stringify({fields:{state:{stringValue:JSON.stringify(room)}}})});},
 };
}
export function createLudo565({verify,profile,store,limit=async()=>true,now=()=>Date.now(),uuid=()=>crypto.randomUUID().replaceAll('-','').slice(0,16).toUpperCase(),roll}){
 return async function(request){
  const json=(data,status=200)=>Response.json(data,{status,headers:{'cache-control':'no-store'}});
  if(request.method!=='POST')return json({error:'method_not_allowed'},405);
  if(!/^Bearer [^\s]+$/.test(request.headers.get('authorization')??''))return json({error:'unauthorized'},401);
  if(!request.headers.get('content-type')?.startsWith('application/json'))return json({error:'invalid_request'},400);
  try{
   const reader=request.body?.getReader();if(!reader)return json({error:'invalid_request'},400);let size=0,chunks=[];
   while(true){const {value,done}=await reader.read();if(done)break;size+=value.length;if(size>4096){await reader.cancel();return json({error:'invalid_request'},400);}chunks.push(value);}
   const data=new Uint8Array(size);let at=0;for(const c of chunks){data.set(c,at);at+=c.length;}
   let b;try{b=JSON.parse(new TextDecoder().decode(data));}catch{return json({error:'invalid_request'},400);}
   if(!b||typeof b!=='object'||Array.isArray(b))return json({error:'invalid_request'},400);
   let user;try{user=await verify(request);}catch{return json({error:'unauthorized'},401);}
   const uid=user.sub;if(!uid)return json({error:'unauthorized'},401);
   let createId;
   if(b.action==='create'&&b.requestId!==undefined){
    if(typeof b.requestId!=='string'||!/^[a-zA-Z0-9_-]{16,100}$/.test(b.requestId))return json({error:'invalid_request'},400);
    const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid+':'+b.requestId));
    createId=Array.from(new Uint8Array(digest),x=>x.toString(16).padStart(2,'0')).join('').slice(0,16).toUpperCase();
    const prior=await store.get(createId);
    if(prior){if(prior.room.owner!==uid)return json({error:'state_changed'},409);return json({room:prior.room});}
   }
   if(!await limit(uid,b.action))return json({error:'slow_down'},429);
   if(b.action==='create'){
    const p=await profile(uid),id=createId??uuid();
    const room=createRoom({uid,id,name:String(p?.displayName??p?.username??'Oyuncu'),photo:String(p?.photoUrl??''),capacity:b.capacity,team:b.team===true,mode:b.mode},now());
    try{await store.put(id,room);}catch(error){
     if(createId&&error.status===409){const prior=await store.get(id);if(prior?.room?.owner===uid)return json({room:prior.room});}
     throw error;
    }
    return json({room},201);
   }
   if(!/^[A-F0-9]{16}$/.test(b.id??''))return json({error:'invalid_room'},400);
   const existing=await store.get(b.id);if(!existing)return json({error:'room_not_found'},404);
   if(b.action==='join'){const p=await profile(uid);b={...b,name:String(p?.displayName??p?.username??'Oyuncu'),photo:String(p?.photoUrl??'')};}
   const room=act(existing.room,uid,b,now(),roll);
   if(room.revision!==existing.room.revision)await store.put(b.id,room,existing.stamp);
   return json({room});
  }catch(e){return json({error:e instanceof LudoError?e.message:'temporarily_unavailable'},e.status??503);}
 };
}
