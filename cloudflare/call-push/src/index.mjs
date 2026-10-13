import {createHandler} from './handler.mjs';
import {verifyFirebaseIdToken} from './auth.mjs';
import {googleIo} from './google.mjs';
export default {async fetch(request,env){const io=googleIo(env);return createHandler({...io,now:()=>Date.now(),authenticate:async r=>{const claims=await verifyFirebaseIdToken(r,env);await io.checkAuth(claims);return claims.sub;}})(request);}};
