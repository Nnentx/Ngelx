// Each seat receives every face once per six accepted rolls. Cryptographic
// sampling without replacement bounds droughts equally for humans and bots.
// Remaining faces are server-private and must never appear in API responses.
function index(limit){
 const ceiling=Math.floor(4294967296/limit)*limit;
 let n;do{n=crypto.getRandomValues(new Uint32Array(1))[0];}while(n>=ceiling);
 return n%limit;
}
export function balancedRoll592(room,seat){
 room.diceBags592??={};
 let bag=room.diceBags592[seat];
 if(!Array.isArray(bag)||!bag.length)bag=[1,2,3,4,5,6];
 const choice=index(bag.length),face=bag.splice(choice,1)[0];
 room.diceBags592[seat]=bag;
 return face;
}
export function publicRoom592(room){
 const {diceBags592,...visible}=room;
 return visible;
}
export function startFull592(room,now){
 if(room.status==='waiting'&&room.capacity===4&&room.players.filter(p=>!p.left).length===4){
  room.status='playing';room.deadline=now+15000;room.autoNextAt=now+2600;
  room.autoStarted592=true;
 }
 return room;
}
