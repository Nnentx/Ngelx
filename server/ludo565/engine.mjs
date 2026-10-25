export class LudoError extends Error{constructor(code,status=400){super(code);this.status=status;}}
const fail=(code,status)=>{throw new LudoError(code,status)};
export const powerTiles570=new Map([2,5,10,15,18,23,28,31,36,41,44,49].map((cell,i)=>[cell,['control','double','shield'][i%3]]));
export const safe=new Set([0,8,13,21,26,34,39,47]);
export const sameTeam=(r,a,b)=>r.team&&a%2===b%2;
export function createRoom({uid,name,photo='',capacity=2,team=false,mode='classic',id},now){
 if(![2,4].includes(capacity)||!['classic','power'].includes(mode)||team&&capacity!==4)fail('invalid_settings');
 return {id,owner:uid,capacity,team,mode,status:'waiting',powerTiles:Object.fromEntries(powerTiles570),players:[{uid,name:name.slice(0,40),photo:String(photo).slice(0,2048),seat:0,left:false}],tokens:[[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]],power:[{double:1,control:1,shield:1},{double:1,control:1,shield:1},{double:1,control:1,shield:1},{double:1,control:1,shield:1}],shields:{},turn:0,dice:null,sixes:0,revision:0,deadline:now+10000,expiresAt:now+6*3600000,last:{},chat:[],winner:null};
}
const active=r=>r.players.filter(p=>!p.left&&!r.tokens[p.seat].every(x=>x===56));
function next(r,now){const seats=active(r).map(p=>p.seat).sort();r.turn=seats.find(x=>x>r.turn)??seats[0]??0;r.dice=null;r.doubled=false;r.sixes=0;r.openingRolls=0;r.deadline=now+10000;if(r.shields[r.turn])delete r.shields[r.turn];}
export function legal(r,seat){if(r.dice===null)return [];const distance=r.dice*(r.doubled?2:1);return r.tokens[seat].flatMap((p,i)=>p===56?[]:p===-1?(r.dice===6?[i]:[]):p+distance<=56?[i]:[]);}
export function secureRoll(){let n;do{n=crypto.getRandomValues(new Uint32Array(1))[0];}while(n>=4294967292);return n%6+1;}
export function act(original,uid,b,now,roll=secureRoll){
 const r=structuredClone(original);if(now>r.expiresAt)fail('room_expired',410);
 let player=r.players.find(p=>p.uid===uid);
 if(b.action==='join'){
  if(player){if(player.left)fail('already_left',403);return r;}
  if(r.status!=='waiting'||r.players.length>=r.capacity)fail('room_full',409);
  const seats=r.capacity===2?[0,2]:[0,1,2,3],seat=seats.find(s=>!r.players.some(p=>p.seat===s));
  r.players.push({uid,seat,name:String(b.name??'Oyuncu').slice(0,40),photo:String(b.photo??'').slice(0,2048),left:false});
 }else{
  if(!player||player.left)fail('not_a_player',403);
  if(b.action==='sync'){
   if(r.status==='playing'&&now>=r.deadline)return automatic(r,now,roll);return r;
  }
  if(typeof b.requestId!=='string'||!/^[a-zA-Z0-9_-]{8,100}$/.test(b.requestId))fail('invalid_request');
  if(r.last[uid]===b.requestId)return r;
  if(b.revision!==r.revision)fail('state_changed',409);
  if(b.action==='leave'){
   player.left=true;
   if(r.status==='waiting'){if(uid===r.owner)r.status='closed';else r.players=r.players.filter(p=>p.uid!==uid);}
   else if(r.status==='playing'){
    const survivors=r.players.filter(p=>!p.left);
    if(survivors.length<=1||r.team&&survivors.every(p=>p.seat%2===survivors[0].seat%2)){r.status='finished';r.winner=survivors[0]?(r.team?survivors[0].seat%2:survivors[0].seat):null;}
    else if(r.turn===player.seat)next(r,now);
   }
  }else if(b.action==='chat'){
   const text=String(b.text??'').trim();if(!text||text.length>180)fail('invalid_message');
   if(now-(r.lastChat?.[uid]??0)<1500)fail('slow_down',429);
   r.chat=[...r.chat,{uid,name:player.name,text,at:now}].slice(-15);r.lastChat={...r.lastChat,[uid]:now};
  }else if(b.action==='start'){
   if(uid!==r.owner)fail('host_only',403);if(r.status!=='waiting'||r.players.length!==r.capacity)fail('waiting_for_players',409);
   r.status='playing';r.deadline=now+10000;
  }else{
   if(r.status!=='playing')fail('not_playing',409);
   if(now>=r.deadline)return automatic(r,now,roll);
   if(r.turn!==player.seat)fail('not_your_turn',403);
   if(b.action==='roll'){
    if(r.dice!==null)fail('move_first',409);
    r.deadline=now+10000;r.dice=roll();if(!Number.isInteger(r.dice)||r.dice<1||r.dice>6)fail('invalid_dice');
    r.lastRoll={seat:r.turn,value:r.dice};r.sixes=r.dice===6?r.sixes+1:0;
    if(r.sixes===3)next(r,now);else if(!legal(r,r.turn).length){if(r.tokens[r.turn].every(x=>x===-1)&&(r.openingRolls??0)<2){r.openingRolls=(r.openingRolls??0)+1;r.dice=null;}else next(r,now);}
   }else if(b.action==='power'){
    if(r.mode!=='power')fail('classic_mode');const p=r.power[r.turn];
    if(!['double','control','shield'].includes(b.kind)||p[b.kind]<=0)fail('power_used');
    if(b.kind==='control'){
     if(r.dice!==null||!Number.isInteger(b.number)||b.number<1||b.number>6)fail('invalid_power');
     r.deadline=now+10000;r.dice=b.number;r.lastRoll={seat:r.turn,value:r.dice};r.sixes=r.dice===6?r.sixes+1:0;if(r.sixes===3)next(r,now);else if(!legal(r,r.turn).length){if(r.tokens[r.turn].every(x=>x===-1)&&(r.openingRolls??0)<2){r.openingRolls=(r.openingRolls??0)+1;r.dice=null;}else next(r,now);}
    }else if(b.kind==='double'){
     if(r.dice===null||r.doubled)fail('roll_first');r.doubled=true;
     if(!legal(r,r.turn).length)fail('no_move');
    }else r.shields[r.turn]=true;
    p[b.kind]--;
   }else if(b.action==='move'){
    if(!Number.isInteger(b.token)||!legal(r,r.turn).includes(b.token))fail('invalid_move');
    const seat=r.turn,old=r.tokens[seat][b.token],position=old===-1?0:old+r.dice*(r.doubled?2:1);r.tokens[seat][b.token]=position;r.openingRolls=0;
    let captured=false;
    if(r.mode==='power'&&position<51){
     const global=(seat*13+position)%52,tiles=r.powerTiles??Object.fromEntries(powerTiles570);
     const kind=tiles[global];
     if(kind){
      r.power[seat][kind]=Math.min(9,(r.power[seat][kind]??0)+1);
      delete tiles[global];
      const occupied=new Set();
      for(const p of r.players)if(!p.left)for(const v of r.tokens[p.seat])
       if(v>=0&&v<51)occupied.add((p.seat*13+v)%52);
      const open=Array.from({length:52},(_,i)=>i).filter(cell=>!safe.has(cell)&&cell!==global&&!Object.hasOwn(tiles,cell)&&!occupied.has(cell));
      if(open.length){
       const rnd=crypto.getRandomValues(new Uint32Array(1))[0];
       tiles[open[rnd%open.length]]=kind;
      }
      r.powerTiles=tiles;r.pickup={seat,kind,at:now,cell:global};
     }
    }
    if(position<51){const global=(seat*13+position)%52;
     if(!safe.has(global))for(const p of r.players){if(p.left||p.seat===seat||sameTeam(r,seat,p.seat)||r.shields[p.seat])continue;
      r.tokens[p.seat]=r.tokens[p.seat].map(x=>{if(x>=0&&x<51&&(p.seat*13+x)%52===global){captured=true;return -1;}return x;});
     }
    }
    const won=r.tokens[seat].every(x=>x===56);
    const teamWon=r.team&&[seat%2,seat%2+2].every(s=>r.tokens[s].every(x=>x===56));
    if((!r.team&&won)||teamWon){r.status='finished';r.winner=r.team?seat%2:seat;}
    else if(won||(!captured&&position!==56&&r.dice!==6&&!(r.mode==='power'&&position<51&&[4,17,30,43].includes((seat*13+position)%52))))next(r,now);
    else{r.dice=null;r.doubled=false;r.deadline=now+10000;}
   }else fail('invalid_action');
  }
  r.last[uid]=b.requestId;
 }
 r.revision++;return r;
}

// Expiration uses the same validated actions as a human, including captures and bonuses.
function automatic(room,now,roll){
 const player=room.players.find(p=>p.seat===room.turn&&!p.left);
 if(!player)return room;
 const ready=structuredClone(room);ready.deadline=now+10000;
 const choices=legal(ready,ready.turn);
 return act(ready,player.uid,{action:ready.dice===null?'roll':'move',...(ready.dice===null?{}:{token:choices[0]}),revision:ready.revision,requestId:'automatic569_'+ready.revision},now,roll);
}
