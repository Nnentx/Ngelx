export const turnWindow583=15000;
export const autoStep583=2600;
export class LudoError extends Error{constructor(code,status=400){super(code);this.status=status;}}
const fail=(code,status)=>{throw new LudoError(code,status)};
export const powerTiles570=new Map([[2,'control'],[10,'shield'],[18,'double'],[28,'control'],[36,'shield'],[44,'double']]);
export const safe=new Set([0,8,13,21,26,34,39,47]);
export const sameTeam=(r,a,b)=>r.team&&a%2===b%2;
export function createRoom({uid,name,photo='',capacity=2,team=false,mode='classic',id},now){
 if(![2,4].includes(capacity)||!['classic','power'].includes(mode)||team&&capacity!==4)fail('invalid_settings');
 return {id,owner:uid,capacity,team,mode,status:'waiting',powerTiles:Object.fromEntries(powerTiles570),bonusTiles:[4,17,30,43],players:[{uid,name:name.slice(0,40),photo:String(photo).slice(0,2048),seat:0,left:false}],tokens:[[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]],power:[{double:1,control:1,shield:1},{double:1,control:1,shield:1},{double:1,control:1,shield:1},{double:1,control:1,shield:1}],shields:{},autoSeats:{},turn:0,dice:null,sixes:0,revision:0,deadline:now+turnWindow583,expiresAt:now+6*3600000,last:{},chat:[],winner:null};
}
const active=r=>r.players.filter(p=>!p.left&&!r.tokens[p.seat].every(x=>x===56));
function next(r,now){const seats=active(r).map(p=>p.seat).sort();r.turn=seats.find(x=>x>r.turn)??seats[0]??0;r.dice=null;r.doubled=false;r.sixes=0;r.openingRolls=0;r.deadline=now+turnWindow583;if(r.shields[r.turn])delete r.shields[r.turn];}
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
   if(r.status==='playing'&&now>=r.deadline)return automatic(r,now,roll,true);
   if(r.status==='playing'&&r.autoSeats?.[r.turn]&&now>=(r.autoNextAt??0))return automatic(r,now,roll,false);
   return r;
  }
  if(typeof b.requestId!=='string'||!/^[a-zA-Z0-9_-]{8,100}$/.test(b.requestId))fail('invalid_request');
  if(r.last[uid]===b.requestId)return r;
  if(b.revision!==r.revision&&b.action!=='leave')fail('state_changed',409);
  if(b.action==='leave'){
   player.left=true;if(r.autoSeats)delete r.autoSeats[player.seat];
   if(r.status==='waiting'){if(uid===r.owner)r.status='closed';else r.players=r.players.filter(p=>p.uid!==uid);}
   else if(r.status==='playing'){
    const survivors=r.players.filter(p=>!p.left);
    if(survivors.length<=1||r.team&&survivors.every(p=>p.seat%2===survivors[0].seat%2)){r.status='finished';r.endReason='abandoned';r.winner=survivors[0]?(r.team?survivors[0].seat%2:survivors[0].seat):null;}
    else if(r.turn===player.seat)next(r,now);
   }
  }else if(b.action==='auto'){
   if(typeof b.enabled!=='boolean')fail('invalid_settings');
   r.autoSeats??={};
   if(b.enabled)r.autoSeats[player.seat]=true;
   else{
    delete r.autoSeats[player.seat];
    // Reclaim a full move window when cancelling timed-out Auto.
    if(r.status==='playing'&&r.turn===player.seat)r.deadline=now+turnWindow583;
   }
  }else if(b.action==='chat'){
   const text=String(b.text??'').trim();if(!text||text.length>180)fail('invalid_message');
   if(now-(r.lastChat?.[uid]??0)<1500)fail('slow_down',429);
   r.chat=[...r.chat,{uid,name:player.name,text,at:now}].slice(-15);r.lastChat={...r.lastChat,[uid]:now};
  }else if(b.action==='start'){
   if(uid!==r.owner)fail('host_only',403);
   const joined=r.players.filter(p=>!p.left);
   if(r.status!=='waiting'||joined.length<2||r.team&&joined.length!==4||r.matchmaking&&joined.length!==r.capacity)fail('waiting_for_players',409);
   r.status='playing';r.deadline=now+turnWindow583;
  }else{
   if(r.status!=='playing')fail('not_playing',409);
   if(now>=r.deadline)return automatic(r,now,roll,true);
   if(r.turn!==player.seat)fail('not_your_turn',403);
   // Any real manual move exits Auto, without disabling server-generated moves.
   if(r.autoSeats?.[player.seat]&&!b.requestId.startsWith('automatic569_'))delete r.autoSeats[player.seat];
   if(b.action==='roll'){
    if(r.dice!==null)fail('move_first',409);
    r.deadline=now+turnWindow583;r.dice=roll();if(!Number.isInteger(r.dice)||r.dice<1||r.dice>6)fail('invalid_dice');
    r.lastRoll={seat:r.turn,value:r.dice,revision:r.revision+1};r.sixes=r.dice===6?r.sixes+1:0;
    if(r.sixes===3)next(r,now);else if(!legal(r,r.turn).length){if(r.tokens[r.turn].every(x=>x===-1)&&(r.openingRolls??0)<2){r.openingRolls=(r.openingRolls??0)+1;r.dice=null;}else next(r,now);}
   }else if(b.action==='power'){
    if(r.mode!=='power')fail('classic_mode');const p=r.power[r.turn];
    if(!['double','control','shield'].includes(b.kind)||p[b.kind]<=0)fail('power_used');
    if(b.kind==='control'){
     if(r.dice!==null||!Number.isInteger(b.number)||b.number<1||b.number>6)fail('invalid_power');
     r.deadline=now+turnWindow583;r.dice=b.number;r.lastRoll={seat:r.turn,value:r.dice,revision:r.revision+1};r.sixes=r.dice===6?r.sixes+1:0;if(r.sixes===3)next(r,now);else if(!legal(r,r.turn).length){if(r.tokens[r.turn].every(x=>x===-1)&&(r.openingRolls??0)<2){r.openingRolls=(r.openingRolls??0)+1;r.dice=null;}else next(r,now);}
    }else if(b.kind==='double'){
     if(r.dice===null||r.doubled)fail('roll_first');r.doubled=true;
     if(!legal(r,r.turn).length)fail('no_move');
    }else r.shields[r.turn]=true;
    p[b.kind]--;
   }else if(b.action==='move'){
    if(!Number.isInteger(b.token)||!legal(r,r.turn).includes(b.token))fail('invalid_move');
    const seat=r.turn,old=r.tokens[seat][b.token],position=old===-1?0:old+r.dice*(r.doubled?2:1);r.tokens[seat][b.token]=position;r.openingRolls=0;
    // +1 is a collectible extra turn. Its position must be changed by the server,
    // not picked independently on each client.
    const globalCell=position<51?(seat*13+position)%52:-1;
    const bonusTiles=r.bonusTiles??[4,17,30,43];
    const gainedBonus=r.mode==='power'&&bonusTiles.includes(globalCell);
    if(gainedBonus){
      const occupied=new Set();
      for(const player of r.players)if(!player.left)for(const progress of r.tokens[player.seat])
        if(progress>=0&&progress<51)occupied.add((player.seat*13+progress)%52);
      const powers=r.powerTiles??Object.fromEntries(powerTiles570);
      const options=Array.from({length:52},(_,i)=>i).filter(i=>
        i!==globalCell&&!safe.has(i)&&!bonusTiles.includes(i)&&!occupied.has(i)&&!Object.hasOwn(powers,i));
      const index=bonusTiles.indexOf(globalCell);
      if(options.length){
        const choice=options[crypto.getRandomValues(new Uint32Array(1))[0]%options.length];
        bonusTiles[index]=choice;
      }else{
        bonusTiles.splice(index,1); // No free slot: consumed until a free slot exists
      }
      r.bonusTiles=bonusTiles;
      r.bonusPickup={seat,at:now,cell:globalCell};
    }
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
    if((!r.team&&won)||teamWon){r.status='finished';r.endReason='completed';r.winner=r.team?seat%2:seat;}
    else if(won||(!captured&&position!==56&&r.dice!==6&&!gainedBonus))next(r,now);
    else{r.dice=null;r.doubled=false;r.deadline=now+turnWindow583;}
   }else fail('invalid_action');
  }
  r.last[uid]=b.requestId;
 }
 if(['roll','move','start','auto'].includes(b.action))r.autoNextAt=now+autoStep583;
 r.revision++;return r;
}

// Server-owned timeout and Auto logic. One action per sync avoids invisible chains.
function autoChoice575(room){
 const choices=legal(room,room.turn);
 if(!choices.length)return null;
 const seat=room.turn,steps=room.dice*(room.doubled?2:1);
 const players=room.players.filter(p=>!p.left&&p.seat!==seat&&!sameTeam(room,seat,p.seat));
 const tokens=room.tokens[seat];
 function score(token){
  const start=tokens[token],position=start<0?0:start+steps;
  let points=position===56?270:(position>=51?90:0)+(start<0?35:0)+position*.6;
  if(position>=51)return points;
  const cell=(seat*13+position)%52;
  if(safe.has(cell)||room.shields?.[seat])points+=27;
  for(const p of players)for(const progress of room.tokens[p.seat]){
   if(progress<0||progress>=51)continue;
   const other=(p.seat*13+progress)%52;
   if(other===cell&&!safe.has(cell)&&!room.shields?.[p.seat])points+=170;
   const distance=(cell-other+52)%52;
   if(!safe.has(cell)&&distance>0&&distance<=6)points-=23;
  }
  if(room.mode==='power'&&room.powerTiles?.[cell])points+=28;
  if(room.mode==='power'&&room.bonusTiles?.includes(cell))points+=60;
  return points;
 }
 return choices.map(token=>({token,points:score(token)})).sort((a,b)=>b.points-a.points||a.token-b.token)[0].token;
}
function automatic(room,now,roll,activate=true){
 const player=room.players.find(p=>p.seat===room.turn&&!p.left);
 if(!player)return room;
 const ready=structuredClone(room);
 ready.deadline=now+turnWindow583;
 if(activate&&!player.bot){ready.autoSeats??={};ready.autoSeats[ready.turn]=true;}
 // A stale dice value without a legal move should never deadlock the room.
 if(ready.dice!==null&&!legal(ready,ready.turn).length){next(ready,now);ready.autoNextAt=now+autoStep583;ready.revision++;return ready;}
 const token=ready.dice===null?null:autoChoice575(ready);
 return act(ready,player.uid,{action:token===null?'roll':'move',...(token===null?{}:{token}),revision:ready.revision,requestId:'automatic569_'+ready.revision},now,roll);
}
