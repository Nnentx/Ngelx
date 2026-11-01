import {accessToken,document} from '../../call-push/src/google.mjs';
const field=v=>v===null?{nullValue:null}:typeof v==='boolean'?{booleanValue:v}:typeof v==='number'?{integerValue:String(v)}:typeof v==='string'?{stringValue:v}:Array.isArray(v)?{arrayValue:{values:v.map(field)}}:{mapValue:{fields:Object.fromEntries(Object.entries(v).map(([k,v])=>[k,field(v)]))}};
export function pkStorage588(env,fetcher=fetch){
  if(env.FIREBASE_PROJECT_ID!=='ngelx-44eed')throw Error('Wrong project');
  const root=`https://firestore.googleapis.com/v1/projects/${env.FIREBASE_PROJECT_ID}/databases/(default)/documents`;
  async function api(path,body){
    const r=await fetcher(root+path,{method:body?'POST':'GET',headers:{authorization:'Bearer '+await accessToken(env),'content-type':'application/json'},...(body?{body:JSON.stringify(body)}:{}),signal:AbortSignal.timeout(8000)});
    if(r.status===404)return null;
    if(!r.ok)throw Object.assign(Error('storage_error'),{retry:r.status===409||r.status===412});
    return r.json();
  }
  return {async transact(action){
    for(let attempt=0;attempt<3;attempt++){
      const {transaction}=await api(':beginTransaction',{});const writes=[];
      try{
        const result=await action({get:async path=>document(await api('/'+path+'?transaction='+encodeURIComponent(transaction))),
          update:(path,values)=>writes.push({update:{name:root.replace('https://firestore.googleapis.com/v1/','')+'/'+path,fields:Object.fromEntries(Object.entries(values).map(([k,v])=>[k,field(v)]))},updateMask:{fieldPaths:Object.keys(values)}})});
        await api(':commit',{transaction,writes});return result;
      }catch(e){try{await api(':rollback',{transaction});}catch{}if(!e.retry||attempt===2)throw e;}
    }
  }};
}
