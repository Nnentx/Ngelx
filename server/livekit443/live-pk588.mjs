const id=v=>typeof v==='string'&&/^[A-Za-z0-9_-]{1,160}$/.test(v);
const time=v=>typeof v==='number'?v:Date.parse(v??'');
const num=v=>Number.isSafeInteger(v)&&v>=0?v:0;
export function pkResult588(session,a,b,statsA={},statsB={},now=Date.now(),cancel=false){
  const end=time(session.endsAt),start=time(session.clientStartedAt??session.startedAt);
  if(!Number.isFinite(end)||!Number.isFinite(start)||end<=start||end-start>190000)throw Error('invalid_session');
  if(cancel&&now<end)return {status:'ended',result588:true,endReason:'cancelled',finalScoreByUid:{},winnerUid:null};
  if(now<end)throw Error('not_finished');
  const score=(room,likes,gifts)=>Math.max(0,num(room.likeCount)-num(likes))+Math.floor(Math.max(0,num(room.giftPoints)-num(gifts))/10);
  const scoreA=score(a,session.startLikeA,session.startGiftA),scoreB=score(b,session.startLikeB,session.startGiftB);
  const au=session.inviterUid,bu=session.inviteeUid;
  const winner=scoreA===scoreB?null:scoreA>scoreB?au:bu;
  return {status:'ended',result588:true,endReason:'time_up',winnerUid:winner,
    finalScoreByUid:{[au]:scoreA,[bu]:scoreB},
    streakByUid:{[au]:winner===null?num(statsA.streak):winner===au?num(statsA.streak)+1:0,
      [bu]:winner===null?num(statsB.streak):winner===bu?num(statsB.streak)+1:0}};
}
export function createPkFinish588({store,now=()=>Date.now()}){
  if(typeof store?.totalsAt!=='function'||typeof store?.transact!=='function')throw Error('Canonical score store required');
  return async(uid,body)=>{
    if(!id(uid)||!id(body?.sessionId)||Object.keys(body).some(k=>!['sessionId','cancel'].includes(k))||
      (body.cancel!==undefined&&typeof body.cancel!=='boolean'))return {status:400,body:{error:'invalid_request'}};
    // Historical snapshots are immutable; reuse them if a transaction retries.
    const snapshots=new Map();
    const totalsAt=(liveId,at)=>{const key=liveId+':'+at;if(!snapshots.has(key))snapshots.set(key,Promise.resolve().then(()=>store.totalsAt(liveId,at)));return snapshots.get(key);};
    try{
      const result=await store.transact(async tx=>{
        const path='calls/'+body.sessionId,session=await tx.get(path);
        if(!session||session.type!=='live_pk'||![session.inviterUid,session.inviteeUid].includes(uid))throw Error('forbidden');
        if(session.result588===true)return session;
        if(session.status!=='active'||!id(session.inviterUid)||!id(session.inviteeUid)||session.inviterUid===session.inviteeUid||
          !id(session.inviterLiveId)||!id(session.inviteeLiveId)||session.inviterLiveId===session.inviteeLiveId)throw Error('invalid_session');
        const [a,b,sa,sb]=await Promise.all([
          tx.get('live_streams/'+session.inviterLiveId),tx.get('live_streams/'+session.inviteeLiveId),
          tx.get('live_pk_stats588/'+session.inviterUid),tx.get('live_pk_stats588/'+session.inviteeUid)]);
        if(!a||!b||a.ownerId!==session.inviterUid||b.ownerId!==session.inviteeUid||a.pkSessionId!==body.sessionId||b.pkSessionId!==body.sessionId)throw Error('invalid_session');
        const timestamp=now(),end=time(session.endsAt),start=time(session.startedAt??session.clientStartedAt);
        if(!Number.isFinite(end)||!Number.isFinite(start)||end<=start||end-start>190000)throw Error('invalid_session');
        const cancelled=body.cancel===true&&timestamp<end;
        if(timestamp<end&&!cancelled)throw Error('not_finished');
        // Old abandoned sessions cannot be reconstructed after Firestore's
        // one-hour historical-read window. Cancel them without changing WIN.
        const expired=timestamp-start>55*60*1000;
        let finalA=a,finalB=b,canonical={...session,startedAt:start,clientStartedAt:start};
        if(!cancelled&&!expired){
          const [startA,startB,endA,endB]=await Promise.all([
            totalsAt(session.inviterLiveId,start),totalsAt(session.inviteeLiveId,start),
            totalsAt(session.inviterLiveId,end),totalsAt(session.inviteeLiveId,end)]);
          finalA=endA;finalB=endB;
          canonical={...canonical,startLikeA:startA.likeCount,startLikeB:startB.likeCount,
            startGiftA:startA.giftPoints,startGiftB:startB.giftPoints};
        }
        const settled=expired?{status:'ended',result588:true,endReason:'cancelled',winnerUid:null,finalScoreByUid:{},detail589:'history_expired'}
          :pkResult588(canonical,finalA,finalB,sa??{},sb??{},timestamp,cancelled);
        const result={...settled,endedAt:new Date(timestamp).toISOString(),endedBy:uid,
          scoreSource589:cancelled||expired?'cancelled':'firestore_read_time',
          scoreStartsAt589:new Date(start).toISOString(),scoreEndsAt589:new Date(end).toISOString()};
        tx.update(path,result);
        for(const [roomId,owner] of [[session.inviterLiveId,session.inviterUid],[session.inviteeLiveId,session.inviteeUid]]){
          const room=roomId===session.inviterLiveId?a:b;
          if(room.pkSessionId===body.sessionId)tx.update('live_streams/'+roomId,{pkActive:false,pkResult588:{sessionId:body.sessionId,...result}});
          if(result.streakByUid)tx.update('live_pk_stats588/'+owner,{streak:result.streakByUid[owner],lastSessionId:body.sessionId,updatedAt:result.endedAt});
        }
        return {...session,...result};
      });
      return {status:200,body:result};
    }catch(e){return {status:e.message==='forbidden'?403:e.message==='not_finished'?409:e.message==='invalid_session'?422:503,body:{error:e.message==='not_finished'?'not_finished':'pk_finish_failed'}};}
  };
}
