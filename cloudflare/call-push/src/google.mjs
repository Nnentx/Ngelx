const bytes=new TextEncoder();let cachedToken=null,keyPromise=null;
const b64=x=>btoa(String.fromCharCode(...new Uint8Array(x))).replace(/=/g,'').replace(/\+/g,'-').replace(/\//g,'_');
export async function accessToken(env){
 const now=Math.floor(Date.now()/1000);if(cachedToken&&cachedToken.until>now+90)return cachedToken.token;
 const account=JSON.parse(env.GOOGLE_SERVICE_ACCOUNT);
 if(account.project_id!==env.FIREBASE_PROJECT_ID||!account.client_email.endsWith('.iam.gserviceaccount.com'))throw Error('Invalid service account');
 if(!keyPromise){const pem=account.private_key.replace(/-----[^-]+-----/g,'').replace(/\s/g,'');const key=Uint8Array.from(atob(pem),c=>c.charCodeAt(0));keyPromise=crypto.subtle.importKey('pkcs8',key,{name:'RSASSA-PKCS1-v1_5',hash:'SHA-256'},false,['sign']);}
 const header=b64(bytes.encode(JSON.stringify({alg:'RS256',typ:'JWT'})));
 const payload=b64(bytes.encode(JSON.stringify({iss:account.client_email,scope:'https://www.googleapis.com/auth/cloud-platform https://www.googleapis.com/auth/firebase.messaging',aud:'https://oauth2.googleapis.com/token',iat:now,exp:now+3600})));
 const unsigned=header+'.'+payload;const signature=await crypto.subtle.sign('RSASSA-PKCS1-v1_5',await keyPromise,bytes.encode(unsigned));
 const r=await fetch('https://oauth2.googleapis.com/token',{method:'POST',body:new URLSearchParams({grant_type:'urn:ietf:params:oauth:grant-type:jwt-bearer',assertion:unsigned+'.'+b64(signature)}),signal:AbortSignal.timeout(8000)});
 if(!r.ok)throw Error('Server authorization unavailable');const v=await r.json();cachedToken={token:v.access_token,until:now+Math.min(v.expires_in??3600,3600)};return cachedToken.token;
}
export const decode=v=>v?.stringValue??(v?.integerValue!==undefined?Number(v.integerValue):v?.doubleValue??v?.booleanValue??(v?.timestampValue?Date.parse(v.timestampValue):v?.arrayValue? (v.arrayValue.values??[]).map(decode):v?.mapValue?Object.fromEntries(Object.entries(v.mapValue.fields??{}).map(([k,x])=>[k,decode(x)])):null));
export const document=v=>v?{...Object.fromEntries(Object.entries(v.fields??{}).map(([k,x])=>[k,decode(x)])),_updateTime:v.updateTime}:null;
const fields=v=>Object.fromEntries(Object.entries(v).map(([k,x])=>[k,typeof x==='number'?{integerValue:String(x)}:{stringValue:String(x)}]));
export function googleIo(env){
 const base=`https://firestore.googleapis.com/v1/projects/${env.FIREBASE_PROJECT_ID}/databases/(default)/documents`;
 async function api(url,options={}){const r=await fetch(url,{...options,headers:{authorization:'Bearer '+await accessToken(env),'content-type':'application/json',...options.headers},signal:AbortSignal.timeout(8000)});if(r.status===404)return null;if(r.status===409||r.status===412)return false;if(!r.ok)throw Error('Datastore unavailable');return r.json();}
 const get=async path=>document(await api(base+'/'+path));
 const put=async(path,data,old)=>api(base+'/'+path+'?'+(old?'currentDocument.updateTime='+encodeURIComponent(old):'currentDocument.exists=false'),{method:'PATCH',body:JSON.stringify({fields:fields(data)})});
 async function key(value){return b64(await crypto.subtle.digest('SHA-256',bytes.encode(value)));}
 return {
  getChat:id=>get('chats/'+encodeURIComponent(id)),getUser:id=>get('users/'+encodeURIComponent(id)),
  async checkAuth(claims){const r=await api(`https://identitytoolkit.googleapis.com/v1/projects/${env.FIREBASE_PROJECT_ID}/accounts:lookup`,{method:'POST',body:JSON.stringify({localId:[claims.sub]})});const u=r?.users?.[0];if(!u||u.disabled||Number(u.validSince??0)>claims.iat)throw Error('Revoked login');},
  async tokens(uid){const r=await api(base+'/_call_devices/'+encodeURIComponent(uid)+'/tokens?pageSize=2&orderBy=updatedAt%20desc');return [...new Set((r?.documents??[]).map(x=>document(x)?.token).filter(x=>typeof x==='string'&&x.length>20&&x.length<4096))];},
  async rateLimit(uid,now){const path='_call_push_rate452/'+encodeURIComponent(uid);const old=await get(path);const window=Math.floor(now/60000);const count=old?.window===window?old.count??0:0;if(count>=40)return false;return !!await put(path,{window,count:count+1},old?._updateTime);},
  async claim(chat,room,kind,uid,now){const path='_call_push452/'+await key(chat+':'+kind+':'+uid);const old=await get(path);if(old?.room===room&&(old.state==='sent'||now-(old.claimedAt??0)<15000))return null;const v=await put(path,{room,state:'pending',claimedAt:now},old?._updateTime);return v?{path,room,claimedAt:now,updateTime:v.updateTime}:null;},
  async complete(lease,ok){await put(lease.path,{room:lease.room,state:ok?'sent':'retry',claimedAt:lease.claimedAt},lease.updateTime);},
  async send(token,data){const r=await fetch(`https://fcm.googleapis.com/v1/projects/${env.FIREBASE_PROJECT_ID}/messages:send`,{method:'POST',headers:{authorization:'Bearer '+await accessToken(env),'content-type':'application/json'},body:JSON.stringify({message:{token,data,android:{priority:'HIGH',ttl:Math.max(1,Math.ceil((Number(data.expiresAt)-Date.now())/1000))+'s',collapse_key:data.roomName.slice(0,64)}}}),signal:AbortSignal.timeout(8000)});if(r.ok)return true;const error=await r.json();if(error?.error?.details?.some(x=>x.errorCode==='UNREGISTERED'))return false;throw Error('Push unavailable');},
 };
}
