// Pure policy boundary. No Firebase service credentials or mutable roles from clients.
export function validateDelete543(identity,community,body){
 if(!identity?.uid||identity.firebase?.sign_in_provider==='anonymous')return false;
 if(body?.confirmDelete!==true||typeof body.communityId!=='string'||!/^[-_A-Za-z0-9]{1,128}$/.test(body.communityId))return false;
 return community?.founderId===identity.uid&&Array.isArray(community.members)&&community.members.includes(identity.uid)
  &&typeof community.name==='string'&&community.name.length>0&&body.confirmName===community.name;
}
export function createCommunityDelete543({verify,lookup,begin,erase,finish,rateLimit}){
 for(const fn of [verify,lookup,begin,erase,finish,rateLimit])if(typeof fn!=='function')throw new Error('missing_dependency');
 return async function handle({method,authorization,body}){
  const result=(status,data)=>({status,body:data});
  if(method!=='POST')return result(405,{error:'method_not_allowed'});
  if(!body||Object.keys(body).some(k=>!['communityId','confirmName','confirmDelete'].includes(k)))return result(400,{error:'invalid_request'});
  const token=/^Bearer (\S+)$/.exec(authorization??'')?.[1];
  if(!token)return result(401,{error:'unauthenticated'});
  let identity;
  try{identity=await verify(token);}catch{return result(401,{error:'unauthenticated'});}
  if(!identity?.uid||identity.firebase?.sign_in_provider==='anonymous')return result(403,{error:'forbidden'});
  if(!/^[-_A-Za-z0-9]{1,128}$/.test(body.communityId??''))return result(400,{error:'invalid_request'});
  try{
   if(!await rateLimit(identity.uid))return result(429,{error:'rate_limited'});
   const current=await lookup(body.communityId);
   if(!current.community){
    const owned=current.job?.ownerUid===identity.uid&&body.confirmDelete===true&&body.confirmName===current.job.name;
    if(owned&&current.job.state==='done')return result(200,{deleted:true});
    // A failed recursive delete may have removed the root before its children.
    // Only the immutable server job's original owner can resume that exact ID.
    if(owned&&current.job.state==='deleting'){
     await erase(body.communityId,identity.uid);await finish(body.communityId,identity.uid);return result(200,{deleted:true});
    }
    return result(403,{error:'forbidden'});
   }
   if(!validateDelete543(identity,current.community,body))return result(403,{error:'forbidden'});
   // begin rechecks founder, membership and confirmation under a transaction.
   if(!await begin(identity,body))return result(403,{error:'forbidden'});
   await erase(body.communityId,identity.uid);
   await finish(body.communityId,identity.uid);
   return result(200,{deleted:true});
  }catch{return result(503,{error:'temporarily_unavailable'});}
 };
}
