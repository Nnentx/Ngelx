import {verificationEmail561} from './template.mjs';

// Dependencies are supplied by the existing Firebase adapter. Recipient and
// one-time action link are always obtained server-side, never from the client.
export function createVerificationHandler561({verifyToken,rateLimit,getUser,generateLink,send}){
  return async({token,body})=>{
    if(!token)return {status:401,body:{error:'unauthenticated'}};
    let claims;
    try{claims=await verifyToken(token);}catch{return {status:401,body:{error:'unauthenticated'}};}
    if(!claims?.uid||claims.firebase?.sign_in_provider==='anonymous')return {status:403,body:{error:'account-required'}};
    if(!body||typeof body!=='object'||Array.isArray(body)||Object.keys(body).length)return {status:400,body:{error:'invalid-request'}};
    try{
      if(!await rateLimit(claims.uid))return {status:429,body:{error:'rate-limit'}};
      const user=await getUser(claims.uid);
      if(user.disabled||!user.email)return {status:403,body:{error:'account-unavailable'}};
      if(user.emailVerified)return {status:200,body:{verified:true}};
      const link=await generateLink(user.email);
      const template=verificationEmail561({name:user.displayName,link});
      await send({to:user.email,...template});
      return {status:200,body:{sent:true}};
    }catch{return {status:503,body:{error:'unavailable'}};}
  };
}
