import {createRoom,act,LudoError,legal,secureRoll} from '../../../server/ludo565/engine.mjs';
import {accessToken} from '../../call-push/src/google.mjs';
import {chooseBotToken572} from '../../../server/ludo565/strategy572.mjs';
import {ensureStarter575,ludoWallet575,settleMatch575,claimDaily575,claimChest575} from '../../../server/ludo565/rewards575.mjs';
import {sendLudoGift575,ludoGiftCatalog575} from '../../../server/ludo565/gifts575.mjs';
import {ludoBlock575,ludoReport575} from '../../../server/ludo565/safety575.mjs';
import {ludoModeratorQueue575,ludoModeratorResolve575,moderationDay575} from '../../../server/ludo565/moderation575.mjs';
import {createAdSession575,adRewardStatus575} from '../../../server/ludo565/admob575.mjs';
import {invitation580} from '../../../server/ludo565/invites580.mjs';
export function ludoStore565(env,{fetcher=fetch,authorize=()=>accessToken(env)}={}){
 if(env.FIREBASE_PROJECT_ID!=='ngelx-44eed')throw Error('Wrong project');
 const base=`https://firestore.googleapis.com/v1/projects/${env.FIREBASE_PROJECT_ID}/databases/(default)/documents/_ngelx_ludo565/`;
 const safeDocumentId=id=>typeof id==='string'&&/^[a-zA-Z0-9_-]{1,180}$/.test(id);
 const checkDocumentId=id=>{if(!safeDocumentId(id))throw new LudoError('invalid_document_id',400);return id;};
 async function api(id,options={},suffix=''){checkDocumentId(id);const r=await fetcher(base+id+suffix,{...options,headers:{authorization:'Bearer '+await authorize(),'content-type':'application/json'},signal:AbortSignal.timeout(8000)});if(r.status===404){if((options.method??'GET')==='GET')return null;throw new LudoError('state_changed',409);}if(r.status===409||r.status===412)throw new LudoError('state_changed',409);if(!r.ok)throw Error('Datastore unavailable');return r.json();}
 return {
  async get(id){const d=await api(id);return d?{room:JSON.parse(d.fields.state.stringValue),stamp:d.updateTime}:null;},
  async put(id,room,stamp){return api(id,{method:'PATCH',body:JSON.stringify({fields:{state:{stringValue:JSON.stringify(room)}}})},'?'+(stamp?'currentDocument.updateTime='+encodeURIComponent(stamp):'currentDocument.exists=false'));},
  async putMany(changes){
   if(!Array.isArray(changes)||changes.length<2||changes.length>3||new Set(changes.map(x=>x.id)).size!==changes.length)throw new LudoError('invalid_transaction',400);
   const root='projects/'+env.FIREBASE_PROJECT_ID+'/databases/(default)/documents/_ngelx_ludo565/';
   const url='https://firestore.googleapis.com/v1/projects/'+env.FIREBASE_PROJECT_ID+'/databases/(default)/documents:commit';
   for(const x of changes)checkDocumentId(x.id);
   const writes=changes.map(x=>({update:{name:root+x.id,fields:{state:{stringValue:JSON.stringify(x.room)}}},
    currentDocument:x.stamp?{updateTime:x.stamp}:{exists:false}}));
   const response=await fetcher(url,{method:'POST',
    headers:{authorization:'Bearer '+await authorize(),'content-type':'application/json'},
    body:JSON.stringify({writes}),signal:AbortSignal.timeout(8000)});
   if(response.status===409||response.status===412)throw new LudoError('state_changed',409);
   if(!response.ok)throw new Error('Gift transaction unavailable');
   return response.json();
  },
 };
}
export function createLudo565({verify,profile,store,limit=async()=>true,isModerator=async()=>false,adEnabled=false,now=()=>Date.now(),uuid=()=>String(100000+crypto.getRandomValues(new Uint32Array(1))[0]%900000),roll}){
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
   const wallet580=['wallet','create','bot','join','match','start','roll','move','auto','daily_reward','chest_reward','gift','block','rematch','invite_join'].includes(b.action)?await ensureStarter575(store,uid):null;
   const withWallet575=async(room)=>{
    const wallet=room.status==='finished'?await settleMatch575(store,uid,room,now()):
     b.action==='gift'?await ludoWallet575(store,uid):wallet580??await ludoWallet575(store,uid);
    const players=await Promise.all((room.players??[]).map(async p=>{
     if(p.bot)return {...p,level:p.level??1};
     const w=p.uid===uid?wallet:await ludoWallet575(store,p.uid);
     return {...p,level:w.level};
    }));
    const blocked=new Set(wallet.blockedUsers??[]);
    return {...room,...wallet,
     // Hide messages and in-room gift notifications from locally blocked players.
     chat:Array.isArray(room.chat)?room.chat.filter(m=>!blocked.has(m.uid)):room.chat,
     gifts:Array.isArray(room.gifts)?room.gifts.filter(g=>!blocked.has(g.from)):room.gifts,
     players:Array.isArray(room.players)?players:room.players};
   };
   let matchKey;
   if(b.action==='match'&&b.requestId!==undefined){
    if(typeof b.requestId!=='string'||!/^[a-zA-Z0-9_-]{16,100}$/.test(b.requestId))return json({error:'invalid_request'},400);
    const hash=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid+':'+b.requestId));
    matchKey='match568_'+Array.from(new Uint8Array(hash),x=>x.toString(16).padStart(2,'0')).join('');
    const saved=await store.get(matchKey),prior=saved?await store.get(saved.room.id):null;
    if(prior&&prior.room.players.some(p=>p.uid===uid)&&prior.room.expiresAt>now())return json({room:await withWallet575(prior.room)});
   }
   const matched=async(room,status=200)=>{
    if(matchKey){const prior=await store.get(matchKey);if(!prior)try{await store.put(matchKey,{id:room.id,revision:0});}catch(e){if(e.status!==409)throw e;}}
    return json({room:await withWallet575(room)},status);
   };
   let createId;
   if(['create','bot'].includes(b.action)&&b.requestId!==undefined){
    if(typeof b.requestId!=='string'||!/^[a-zA-Z0-9_-]{16,100}$/.test(b.requestId))return json({error:'invalid_request'},400);
    const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(uid+':'+b.requestId));
    createId=String(100000+new DataView(digest).getUint32(0)%900000);
    const prior=await store.get(createId);
    if(prior){if(prior.room.owner!==uid)return json({error:'state_changed'},409);return json({room:await withWallet575(prior.room)});}
   }
   if(!await limit(uid,b.action))return json({error:'slow_down'},429);
   if(['invite_create','invite_status','invite_join'].includes(b.action)){
    const result=await invitation580({body:b,uid,store,now:now(),roll,profile});
    return json({room:result.joinedRoom?await withWallet575(result.joinedRoom):result});
   }
   if(b.action==='moderation_queue'||b.action==='moderation_resolve'){
    // Explicit deployment allowlist, checked AFTER Firebase token verification.
    if(!await isModerator(uid))return json({error:'moderator_only'},403);
    if(b.action==='moderation_queue')
     return json({room:await ludoModeratorQueue575(store,b.day??moderationDay575(now()),now(),b.page??0)});
    return json({room:await ludoModeratorResolve575(store,b.reportId,uid,b.decision,now())});
   }
   if(b.action==='wallet')return json({room:await ludoWallet575(store,uid)});
   if(b.action==='ad_session'){
    if(!adEnabled)return json({error:'ads_not_configured'},503);
    return json({room:await createAdSession575(store,uid,now())});
   }
   if(b.action==='ad_status'){
    if(!adEnabled)return json({error:'ads_not_configured'},503);
    return json({room:await adRewardStatus575(store,uid,b.token,now())});
   }
   if(b.action==='gift_catalog')return json({room:{gifts:ludoGiftCatalog575}});
   if(b.action==='daily_reward'||b.action==='chest_reward'){
    const reward=b.action==='daily_reward'?await claimDaily575(store,uid,now()):await claimChest575(store,uid,now());
    return json({room:reward});
   }
   if(b.action==='match'){
    if(![2,4].includes(b.capacity)||!['classic','power'].includes(b.mode))return json({error:'invalid_settings'},400);
    const key='queue568_'+b.mode+'_'+b.capacity;
    const p=await profile(uid);
    for(let attempt=0;attempt<8;attempt++){
     const slot=await store.get(key),found=slot?await store.get(slot.room.id):null;
     if(found&&found.room.expiresAt>now()&&['waiting','playing'].includes(found.room.status)&&found.room.players.some(p=>p.uid===uid&&!p.left))return await matched(found.room);
     if(found&&found.room.status==='waiting'&&found.room.expiresAt>now()){
      let room=found.room;
      if(room.players.some(p=>p.uid===uid))return await matched(room);
      try{
       room=act(room,uid,{action:'join',name:p?.displayName??p?.username??'Oyuncu',photo:p?.photoUrl??''},now(),roll);
       if(room.players.length===room.capacity){room=act(room,room.owner,{action:'start',revision:room.revision,requestId:'auto_start568'},now(),roll);room.expiresAt=now()+6*3600000;}
       await store.put(room.id,room,found.stamp);return await matched(room);
      }catch(e){if(e.status===409)continue;throw e;}
     }
     const id=uuid();
     if(await store.get(id))continue;
     let room=createRoom({uid,id,name:p?.displayName??p?.username??'Oyuncu',photo:p?.photoUrl??'',capacity:b.capacity,mode:b.mode},now());
     room.matchmaking=true;room.expiresAt=now()+90000;
     try{await store.put(id,room);await store.put(key,{id,revision:(slot?.room.revision??0)+1},slot?.stamp);return await matched(room,201);}
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
     if(createId&&error.status===409){const prior=await store.get(id);if(prior?.room?.owner===uid)return json({room:await withWallet575(prior.room)});}
     throw error;
    }
    return json({room:await withWallet575(room)},201);
   }
   if(!/^(?:[0-9]{6}|[A-F0-9]{16})$/.test(b.id??''))return json({error:'invalid_room'},400);
   const existing=await store.get(b.id);if(!existing)return json({error:'room_not_found'},404);
   if(existing.room.expiresAt<=now())return json({error:'room_expired'},410);
   if(b.action==='block'){
    const action=await ludoBlock575(store,b.id,uid,b.to,b.blocked,now());
    return json({room:action});
   }
   if(b.action==='report'){
    const action=await ludoReport575(store,b.id,uid,b.to,b.reason,now());
    return json({room:action});
   }
   if(b.action==='gift'){
    const result=await sendLudoGift575(store,b.id,uid,b,now());
    const room=await withWallet575({...result.room,
      spectatorCount:result.room.spectatorCount??0,
      giftSent:result.sent,giftAlreadySent:result.alreadySent});
    return json({room});
   }
   if(b.action==='rematch'){
    const original=existing.room;
    if(original.status!=='finished'||original.botGame||!original.players.some(p=>p.uid===uid&&!p.left))return json({error:'not_available'},409);
    const ref='rematch575_'+original.id;
    for(let attempt=0;attempt<6;attempt++){
     let pointer=await store.get(ref);
     let target=pointer?await store.get(pointer.room.id):null;
     if(!target||target.room.expiresAt<=now()){
      const p=await profile(uid),id=uuid();
      if(await store.get(id))continue;
      let room=createRoom({uid,id,name:String(p?.displayName??p?.username??'Oyuncu'),
       photo:String(p?.photoUrl??''),capacity:original.capacity,team:original.team,mode:original.mode},now());
      room.rematchOf=original.id;
      try{
       await store.put(id,room);
       await store.put(ref,{id,revision:(pointer?.room.revision??0)+1},pointer?.stamp);
       target=await store.get(id);
      }catch(e){if(e.status===409)continue;throw e;}
     }
     let room=target.room;
     if(!room.players.some(p=>p.uid===uid)){
      const profileData=await profile(uid);
      try{
       room=act(room,uid,{action:'join',name:String(profileData?.displayName??profileData?.username??'Oyuncu'),
        photo:String(profileData?.photoUrl??'')},now(),roll);
       if(room.players.length===room.capacity){
        room=act(room,room.owner,{action:'start',revision:room.revision,
         requestId:'rematch_start575'},now(),roll);
       }
       await store.put(room.id,room,target.stamp);
      }catch(e){if(e.status===409)continue;throw e;}
     }
     return json({room:await withWallet575(room)});
    }
    return json({error:'state_changed'},409);
   }
   if(b.action==='join'){const p=await profile(uid);b={...b,name:String(p?.displayName??p?.username??'Oyuncu'),photo:String(p?.photoUrl??'')};}
   // Spectators use separate presence documents and never mutate the game revision.
   const presenceId='view570_'+b.id;
   const presence=async(remove=false)=>{
    for(let attempt=0;attempt<4;attempt++){
     const old=await store.get(presenceId),viewers=Object.fromEntries(Object.entries(old?.room?.viewers??{}).filter(([,seen])=>now()-seen<25000));
     if(remove)delete viewers[uid];else if(!existing.room.players.some(p=>p.uid===uid&&!p.left))viewers[uid]=now();
     if(Object.keys(viewers).length>200)throw new LudoError('room_full',409);
     try{await store.put(presenceId,{viewers,revision:(old?.room?.revision??0)+1},old?.stamp);return Object.keys(viewers).length;}catch(e){if(e.status!==409||attempt===3)throw e;}
    }
   };
   const viewerCount=async()=>{const entry=await store.get(presenceId);return Object.values(entry?.room?.viewers??{}).filter(seen=>now()-seen<25000).length;};
   if(['watch','watch_leave'].includes(b.action)){
    const count=await presence(b.action==='watch_leave');return json({room:{...existing.room,spectatorCount:count,viewOnly:true}});
   }
   if(b.action==='sync'&&!existing.room.players.some(p=>p.uid===uid&&!p.left))return json({error:'not_a_player'},403);
   let room=act(existing.room,uid,b,now(),roll);
   // Run one server-authoritative bot action per response, preserving visible turns.
   const bot=room.players.find(p=>p.seat===room.turn&&p.bot&&!p.left);
   if(room.botGame&&room.status==='playing'&&bot&&room.revision===existing.room.revision&&now()>=(room.autoNextAt??0)){
    let move;
    if(room.dice===null)move={action:'roll'};
    else{
     const token=chooseBotToken572(room,bot.seat,room.difficulty,roll??secureRoll);
     move={action:'move',token};
    }
    room=act(room,bot.uid,{...move,revision:room.revision,requestId:'bot568_'+room.revision},now(),roll);
   }
   if(room.revision!==existing.room.revision)await store.put(b.id,room,existing.stamp);
   return json({room:await withWallet575({...room,spectatorCount:await viewerCount()})});
  }catch(e){return json({error:e instanceof LudoError?e.message:'temporarily_unavailable'},e.status??503);}
 };
}
