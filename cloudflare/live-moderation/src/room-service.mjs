const bytes=new TextEncoder();
const b64=value=>btoa(String.fromCharCode(...new Uint8Array(value))).replace(/=/g,'').replace(/\+/g,'-').replace(/\//g,'_');
export async function adminToken(env,room,now=Date.now()){
  if(!env.LIVEKIT_API_KEY||!env.LIVEKIT_API_SECRET||!room)throw Error('LiveKit administration not configured');
  const seconds=Math.floor(now/1000);
  const unsigned=b64(bytes.encode(JSON.stringify({alg:'HS256',typ:'JWT'})))+'.'+
    b64(bytes.encode(JSON.stringify({iss:env.LIVEKIT_API_KEY,iat:seconds,nbf:seconds-5,
      exp:seconds+120,video:{roomAdmin:true,room}})));
  const key=await crypto.subtle.importKey('raw',bytes.encode(env.LIVEKIT_API_SECRET),
    {name:'HMAC',hash:'SHA-256'},false,['sign']);
  return unsigned+'.'+b64(await crypto.subtle.sign('HMAC',key,bytes.encode(unsigned)));
}
export function roomService(env,fetcher=fetch){
  const url=new URL(env.LIVEKIT_SERVER_URL);
  if(!['https:','wss:'].includes(url.protocol)||url.username||url.password||url.search||url.hash||url.pathname!=='/')throw Error('Invalid LiveKit service URL');
  url.protocol='https:';
  async function call(method,room,fields={}){
    const response=await fetcher(new URL('/twirp/livekit.RoomService/'+method,url),{
      method:'POST',headers:{authorization:'Bearer '+await adminToken(env,room),'content-type':'application/json'},
      body:JSON.stringify({room,...fields}),signal:AbortSignal.timeout(8000)});
    if(!response.ok)throw Error('LiveKit administration failed');
    return response.json();
  }
  return {
    async listParticipants(room){
      const result=await call('ListParticipants',room);
      if(!Array.isArray(result.participants??[]))throw Error('Invalid room response');
      return (result.participants??[]).map(p=>({...p,tracks:(p.tracks??[]).map(t=>({...t,
        type:t.type==='AUDIO'?0:t.type==='VIDEO'?1:t.type}))}));
    },
    updateParticipant:(room,identity,options)=>call('UpdateParticipant',room,{identity,...options}),
    mutePublishedTrack:(room,identity,trackSid,muted)=>call('MutePublishedTrack',room,{identity,trackSid,muted}),
    removeParticipant:(room,identity)=>call('RemoveParticipant',room,{identity}),
  };
}
