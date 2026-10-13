import {CHUNK,eventFor,eligible,validBody} from './policy.mjs';
const json=(v,status=200)=>new Response(JSON.stringify(v),{status,headers:{'content-type':'application/json','cache-control':'no-store'}});
export function createHandler(io){return async (request)=>{
 const url=new URL(request.url);
 if(url.pathname==='/health'&&request.method==='GET')return json({service:'ngelx-call-push',version:452});
 if(url.pathname!=='/call' || request.method!=='POST')return json({error:'not_found'},404);
 if(Number(request.headers.get('content-length')??0)>2048)return json({error:'too_large'},413);
 try{
  const raw=await request.text();if(raw.length>2048)return json({error:'too_large'},413);
  let body;try{body=JSON.parse(raw);}catch{return json({error:'bad_request'},400);}
  if(!validBody(body))return json({error:'bad_request'},400);
  let uid;try{uid=await io.authenticate(request);}catch{return json({error:'unauthorized'},401);}
  const now=io.now();
  const chat=await io.getChat(body.chatId);
  const event=eventFor(uid,chat,body.roomName,now);
  if(!event)return json({error:'forbidden'},403);
  if(!await io.rateLimit(uid,now))return json({error:'rate_limited'},429);
  const sender=await io.getUser(chat.callStartedBy);
  const actor=uid===chat.callStartedBy?sender:await io.getUser(uid);
  if(!actor||actor.deleted||actor.deactivated||!sender||sender.deleted||sender.deactivated)return json({error:'forbidden'},403);
  if(chat.isGroup!==true)event.title=String(sender.displayName??sender.username??'NgelX araması').slice(0,100);
  let sent=0;const offset=body.offset??0;
  for(const target of event.recipients.slice(offset,offset+CHUNK)){
   const peer=await io.getUser(target);
   if(!eligible({...sender,uid:chat.callStartedBy},peer,target))continue;
   const tokens=await io.tokens(target);
   if(!tokens.length)continue;
   const latest=await io.getChat(body.chatId);
   if(latest?.callRoomName!==chat.callRoomName||latest?.callStatus!==chat.callStatus)break;
   const lease=await io.claim(body.chatId,event.roomName,event.kind,target,now);
   if(!lease)continue;
   try{
    const {recipients,...data}=event;
    for(const token of tokens.slice(0,2)){if(await io.send(token,{...data,recipientUid:target,chatId:body.chatId}))sent++;}
    await io.complete(lease,true);
   }catch(e){await io.complete(lease,false);throw e;}
  }
  return json({sent,nextOffset:offset+CHUNK<event.recipients.length?offset+CHUNK:null});
 }catch{return json({error:'temporarily_unavailable'},503);}
};}
