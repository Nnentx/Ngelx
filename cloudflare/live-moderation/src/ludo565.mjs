import {createRoom,act,LudoError,legal,secureRoll} from '../../../server/ludo565/engine.mjs';
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
export function createLudo565({verify,profile,store,limit=async()=>true,now=()=>Date.now(),uuid=()=>String(100000+crypto.getRandomValues(new Uint32Array(1))[0]%900000),roll}){
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
   let matchKey;
   if(b.action==='match'&&b.requestId!==undefined){
    if(typeof b.requestId!=='string'||!/^[a-zA-Z0-9_-]{16,100}$/.test(b.requestId))return json({error:'invalid_request'},400);
    const hash=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid+':'+b.requestId));
    matchKey='match568_'+Array.from(new Uint8Array(hash),x=>x.toString(16).padStart(2,'0')).join('');
    const saved=await store.get(matchKey),prior=saved?await store.get(saved.room.id):null;
    if(prior&&prior.room.players.some(p=>p.uid===uid)&&prior.room.expiresAt>now())return json({room:prior.room});
   }
   const matched=async(room,status=200)=>{
    if(matchKey){const prior=await store.get(matchKey);if(!prior)try{await store.put(matchKey,{id:room.id,revision:0});}catch(e){if(e.status!==409)throw e;}}
    return json({room},status);
   };
   let createId;
   if(['create','bot'].includes(b.action)&&b.requestId!==undefined){
    if(typeof b.requestId!=='string'||!/^[a-zA-Z0-9_-]{16,100}$/.test(b.requestId))return json({error:'invalid_request'},400);
    const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid+':'+b.requestId));
    createId=String(100000+new DataView(digest).getUint32(0)%900000);
    const prior=await store.get(createId);
    if(prior){if(prior.room.owner!==uid)return json({error:'state_changed'},409);return json({room:prior.room});}
   }
   if(!await limit(uid,b.action))return json({error:'slow_down'},429);
   if(b.action==='match'){
    if(![2,4].includes(b.capacity)||!['classic','power'].includes(b.mode))return json({error:'invalid_settings'},400);
    const key='queue568_'+b.mode+'_'+b.capacity;
    const p=await profile(uid);
    for(let attempt=0;attempt<8;attempt++){
     const slot=await store.get(key),found=slot?await store.get(slot.room.id):null;
     if(found&&found.room.expiresAt>now()&&['waiting','playing'].includes(found.room.status)&&found.room.players.some(p=>p.uid===uid&&!p.left))return matched(found.room);
     if(found&&found.room.status==='waiting'&&found.room.expiresAt>now()){
      let room=found.room;
      if(room.players.some(p=>p.uid===uid))return matched(room);
      try{
       room=act(room,uid,{action:'join',name:p?.displayName??p?.username??'Oyuncu',photo:p?.photoUrl??''},now(),roll);
       if(room.players.length===room.capacity){room=act(room,room.owner,{action:'start',revision:room.revision,requestId:'auto_start568'},now(),roll);room.expiresAt=now()+6*3600000;}
       await store.put(room.id,room,found.stamp);return matched(room);
      }catch(e){if(e.status===409)continue;throw e;}
     }
     const id=uuid();
     if(await store.get(id))continue;
     let room=createRoom({uid,id,name:p?.displayName??p?.username??'Oyuncu',photo:p?.photoUrl??'',capacity:b.capacity,mode:b.mode},now());
     room.matchmaking=true;room.expiresAt=now()+90000;
     try{await store.put(id,room);await store.put(key,{id,revision:(slot?.room.revision??0)+1},slot?.stamp);return matched(room,201);}
     catch(e){if(e.status===409)continue;throw e;}
    }
    return json({error:'state_changed'},409);
   }
   if(['create','bot'].includes(b.action)){
    const p=await profile(uid),id=createId??uuid();
    let room=createRoom({uid,id,name:String(p?.displayName??p?.username??'Oyuncu'),photo:String(p?.photoUrl??''),capacity:b.capacity,team:b.team===true,mode:b.mode},now());
    if(b.action==='bot'){
     if(!['easy','medium','hard'].includes(b.difficulty??'medium'))return json({error:'invalid_settings'},400);
     room.botGame=true;room.difficulty=b.difficulty??'medium';
     for(let i=1;i<room.capacity;i++){
      const bot='bot568:'+id+':'+i;
      room=act(room,bot,{action:'join',name:'Makine '+i},now(),roll);
      room.players.find(p=>p.uid===bot).bot=true;
     }
     room=act(room,uid,{action:'start',revision:room.revision,requestId:'bot_start568'},now(),roll);
    }
    try{await store.put(id,room);}catch(error){
     if(createId&&error.status===409){const prior=await store.get(id);if(prior?.room?.owner===uid)return json({room:prior.room});}
     throw error;
    }
    return json({room},201);
   }
   if(!/^(?:[0-9]{6}|[A-F0-9]{16})$/.test(b.id??''))return json({error:'invalid_room'},400);
   const existing=await store.get(b.id);if(!existing)return json({error:'room_not_found'},404);
   if(b.action==='join'){const p=await profile(uid);b={...b,name:String(p?.displayName??p?.username??'Oyuncu'),photo:String(p?.photoUrl??'')};}
   let room=act(existing.room,uid,b,now(),roll);
   // Run one server-authoritative bot action per response, preserving visible turns.
   const bot=room.players.find(p=>p.seat===room.turn&&p.bot&&!p.left);
   if(room.botGame&&room.status==='playing'&&bot){
    let move;
    if(room.dice===null)move={action:'roll'};
    else{
     const options=legal(room,bot.seat);
     const ranked=options.map(token=>{
      const next=act(room,bot.uid,{action:'move',token,revision:room.revision,requestId:'score568_'+room.revision},now(),()=>6);
      const captures=room.tokens.flat().filter(x=>x===-1).length<next.tokens.flat().filter(x=>x===-1).length;
      return {token,score:(next.tokens[bot.seat][token]===56?1000:0)+(captures?300:0)+next.tokens[bot.seat][token]};
     }).sort((a,b)=>b.score-a.score);
     const random=()=>options[(roll??secureRoll)()%options.length];
     move={action:'move',token:room.difficulty==='easy'?random():room.difficulty==='hard'?ranked[0].token:((roll??secureRoll)()>3?ranked[0].token:random())};
    }
    room=act(room,bot.uid,{...move,revision:room.revision,requestId:'bot568_'+room.revision},now(),roll);
   }
   if(room.revision!==existing.room.revision)await store.put(b.id,room,existing.stamp);
   return json({room});
  }catch(e){return json({error:e instanceof LudoError?e.message:'temporarily_unavailable'},e.status??503);}
 };
}
