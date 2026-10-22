import {accessToken,document} from '../../call-push/src/google.mjs';
import {activeRoom} from '../../../server/livekit443/room-policy.mjs';
const bytes=new TextEncoder();
export function storage(env,fetcher=fetch,now=()=>Date.now(),authorize=()=>accessToken(env)){
  if(env.FIREBASE_PROJECT_ID!=='ngelx-44eed')throw Error('Wrong project');
  const database=`projects/${env.FIREBASE_PROJECT_ID}/databases/(default)`;
  const root=`https://firestore.googleapis.com/v1/${database}/documents`;
  const path=(live,uid)=>'live_streams/'+encodeURIComponent(live)+(uid?'/guest_requests/'+encodeURIComponent(uid):'');
  async function api(url,options={}){
    const r=await fetcher(url,{...options,headers:{authorization:'Bearer '+await authorize(),
      'content-type':'application/json'},signal:AbortSignal.timeout(8000)});
    if(r.status===404)return null;
    if(r.status===409||r.status===412)throw Object.assign(Error('conflict'),{retry:true});
    if(!r.ok)throw Error('Firestore operation failed');
    return r.json();
  }
  const get=async(p,transaction)=>document(await api(root+'/'+p+(transaction?'?transaction='+encodeURIComponent(transaction):'')));
  const post=(url,body)=>api(url,{method:'POST',body:JSON.stringify(body)});
  async function transact(action){
    for(let attempt=0;attempt<3;attempt++){
      const begin=await post(root+':beginTransaction',{});
      if(!begin?.transaction)throw Error('Transaction unavailable');
      try{
        const writes=await action(p=>get(p,begin.transaction));
        await post(root+':commit',{transaction:begin.transaction,writes});return;
      }catch(error){
        try{await post(root+':rollback',{transaction:begin.transaction});}catch{}
        if(!error.retry||attempt===2)throw error;
      }
    }
  }
  const ref=p=>database+'/documents/'+decodeURIComponent(p);
  return {
    getRoom:live=>get(path(live)),
    async getGuest(live,uid){
      const guest=await get(path(live,uid));
      if(guest?.status!=='accepted')return guest;
      const rows=await post(root+'/live_streams/'+encodeURIComponent(live)+':runQuery',{
        structuredQuery:{from:[{collectionId:'guest_requests'}],where:{fieldFilter:{field:{fieldPath:'status'},op:'EQUAL',value:{stringValue:'accepted'}}},
          orderBy:[{field:{fieldPath:'__name__'},direction:'ASCENDING'}],limit:11}});
      if(!Array.isArray(rows))throw Error('Invalid capacity response');
      const ids=rows.filter(r=>r.document).slice(0,10).map(r=>r.document.name.split('/').at(-1));
      return {...guest,guestCapacityAllowed:ids.includes(uid)};
    },
    async rateLimit(scope,max=20){
      const digest=await crypto.subtle.digest('SHA-256',bytes.encode(scope));
      const id=Array.from(new Uint8Array(digest),b=>b.toString(16).padStart(2,'0')).join('');
      const p='_livekit_rate_limits/free_'+id;
      let allowed=false;
      await transact(async read=>{
        const current=await read(p),window=Math.floor(now()/60000);
        const count=current?.window===window?current.count:0;
        allowed=count<max;
        if(!allowed)return [];
        return [{update:{name:ref(p),fields:{window:{integerValue:String(window)},count:{integerValue:String(count+1)},
          expiresAt:{timestampValue:new Date(now()+3600000).toISOString()}}}}];
      });
      return allowed;
    },
    async saveAction({liveId,guestUid,ownerUid,roomName,action}){
      await transact(async read=>{
        const room=await read(path(liveId)),guest=await read(path(liveId,guestUid));
        if(room?.ownerId!==ownerUid||room.roomName!==roomName||!activeRoom(room,now())||
          guest?.hostUid!==ownerUid||guest.guestUid!==guestUid||guest.status!=='accepted')throw Error('Moderation state changed');
        if(!['mute','unmute','kick'].includes(action))throw Error('Invalid action');
        const writes=[{transform:{document:ref(path(liveId)),fieldTransforms:[{
          fieldPath:'guestAudioMutedUids',
          [action==='mute'?'appendMissingElements':'removeAllFromArray']:{values:[{stringValue:guestUid}]},
        }]}}];
        if(action==='kick')writes.push({update:{name:ref(path(liveId,guestUid)),fields:{status:{stringValue:'rejected'}}},
          updateMask:{fieldPaths:['status']},updateTransforms:[{fieldPath:'updatedAt',setToServerValue:'REQUEST_TIME'}]});
        return writes;
      });
    },
  };
}
