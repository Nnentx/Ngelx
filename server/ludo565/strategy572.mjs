import {legal,safe,sameTeam,secureRoll} from './engine.mjs';

// A deterministic, inspectable decision scorer. Dice still come from the fair game engine.
export function scoreBotMove572(room,seat,token) {
 const old=room.tokens[seat][token],distance=room.dice*(room.doubled?2:1);
 const position=old<0?0:old+distance;
 if(position>56)return -Infinity;
 let score=position===56?240:(position>=51?55:0)+(old<0?32:0)+position*.55;
 if(position>=51)return score;
 const cell=(seat*13+position)%52,protectedSquare=safe.has(cell)||Boolean(room.shields?.[seat]);
 if(protectedSquare)score+=30;
 const enemies=(room.players??[]).filter(p=>!p.left&&p.seat!==seat&&!sameTeam(room,seat,p.seat));
 let captures=0,threat=0;
 for(const player of enemies) {
  const enemySeat=player.seat;
  for(const progress of room.tokens[enemySeat]) {
   if(progress<0||progress>=51)continue;
   const enemyCell=(enemySeat*13+progress)%52;
   if(enemyCell===cell&&!safe.has(cell)&&!room.shields?.[enemySeat])captures++;
   const reach=(cell-enemyCell+52)%52;
   if(!protectedSquare&&reach>=1&&reach<=6)threat+=1;
  }
 }
 score+=captures*145;
 score-=Math.min(3,threat)*25;
 if(room.mode==='power'){
   const tiles=room.powerTiles??Object.fromEntries([[2,'control'],[5,'double'],[10,'shield'],[15,'control'],[18,'double'],[23,'shield'],[28,'control'],[31,'double'],[36,'shield'],[41,'control'],[44,'double'],[49,'shield']]);
   if(tiles[cell]!==undefined)score+=20;
 }
 // Moving a threatened piece is preferable to abandoning it.
 if(old>=0&&old<51&&!room.shields?.[seat]){
  const origin=(seat*13+old)%52;
  if(!safe.has(origin)){
   const danger=enemies.some(p=>room.tokens[p.seat].some(t=>t>=0&&t<51&&((origin-(p.seat*13+t)%52+52)%52) >=1&&((origin-(p.seat*13+t)%52+52)%52)<=6));
   if(danger&&protectedSquare)score+=24;
  }
 }
 return score;
}
export function chooseBotToken572(room,seat,difficulty='medium',roll=secureRoll){
 const options=legal(room,seat);
 if(!options.length)return null;
 const ranked=options.map(token=>({token,score:scoreBotMove572(room,seat,token)})).sort((a,b)=>b.score-a.score||a.token-b.token);
 if(difficulty==='hard')return ranked[0].token;
 const random=()=>options[(roll()-1)%options.length];
 if(difficulty==='easy')return random();
 return roll()<=4?ranked[0].token:random();
}
