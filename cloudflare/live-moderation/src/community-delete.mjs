import {accessToken,document} from '../../call-push/src/google.mjs';
import {validateDelete543} from '../../../server/community543/delete-policy.mjs';
const encode=path=>path.split('/').map(encodeURIComponent).join('/');
const fields=value=>Object.fromEntries(Object.entries(value).map(([key,v])=>[key,typeof v==='boolean'?{booleanValue:v}:typeof v==='number'?{integerValue:String(v)}:{stringValue:String(v)}]));
export function communityDeleteStorage(env,{fetcher=fetch,authorize=()=>accessToken(env),now=()=>Date.now(),uuid=()=>crypto.randomUUID()}={}){
 if(env.FIREBASE_PROJECT_ID!=='ngelx-44eed')throw Error('Wrong project');
 const database=`projects/${env.FIREBASE_PROJECT_ID}/databases/(default)`,base=`https://firestore.googleapis.com/v1/${database}/documents`;
 const name=p=>database+'/documents/'+p;
 async function api(path,options={}){
  const response=await fetcher(base+path,{...options,headers:{authorization:'Bearer '+await authorize(),'content-type':'application/json'},signal:AbortSignal.timeout(8000)});
  if(response.status===404)return null;
  if(!response.ok)throw Object.assign(Error('datastore_unavailable'),{conflict:response.status===409||response.status===412});
  return response.status===204?{}:response.json();
 }
 const post=(path,body)=>api(path,{method:'POST',body:JSON.stringify(body)});
 const get=async(path,tx)=>document(await api('/'+encode(path)+(tx?'?transaction='+encodeURIComponent(tx):'')));
 const jobPath=id=>'community_deletions543/'+id;
 async function transaction(action){
  for(let attempt=0;attempt<3;attempt++){
   const begin=await post(':beginTransaction',{});if(!begin?.transaction)throw Error('transaction_unavailable');
   try{const result=await action(begin.transaction);await post(':commit',{transaction:begin.transaction,writes:result.writes});return result.value;}
   catch(error){try{await post(':rollback',{transaction:begin.transaction});}catch{}if(!error.conflict||attempt===2)throw error;}
  }
 }
 return {
  async claim(identity,body){return transaction(async tx=>{
   const id=body.communityId,root='communities450/'+id;
   const community=await get(root,tx),receipt=await get(jobPath(id),tx);
   const owns=receipt?.ownerUid===identity.uid&&receipt.name===body.confirmName;
   if(receipt&&!owns)return {writes:[],value:{status:403}};
   if(receipt?.rootDeleted&&community||receipt?.state==='done'&&community)return {writes:[],value:{status:403}};
   if(receipt?.state==='done')return {writes:[],value:{status:200,deleted:true}};
   if(community&&!validateDelete543(identity,community,body)||!community&&!owns)return {writes:[],value:{status:403}};
   if(receipt?.leaseUntil>now())return {writes:[],value:{status:202,busy:true}};
   const job={ownerUid:identity.uid,name:body.confirmName,state:'deleting',stackJson:receipt?.stackJson??JSON.stringify([{kind:'invites',path:root},{kind:'doc',path:root}]),rootDeleted:receipt?.rootDeleted??false,
    rootVersion:community?._updateTime??receipt?.rootVersion??'',leaseId:uuid(),leaseUntil:now()+60000,requestedAt:receipt?.requestedAt??now()};
   return {writes:[{update:{name:name(jobPath(id)),fields:fields(job)}}],value:{status:202,job,id}};
  });},
  async advance(job,id,{budget=18,deadline=now()+15000}={}){
   const root='communities450/'+id,stack=JSON.parse(job.stackJson);let requests=0;
   const valid=path=>typeof path==='string'&&(path===root||path.startsWith(root+'/'))&&path.split('/').every(x=>x&&x!=='.'&&x!=='..');
   // Remove the visible root with a version precondition first. This immediately
   // denies new member writes through existing root-membership security rules.
   // An immutable owner receipt retains the only authority for resumptions.
   if(!job.rootDeleted){
    await api('/'+encode(root)+(job.rootVersion?'?currentDocument.updateTime='+encodeURIComponent(job.rootVersion):''),{method:'DELETE'});requests++;job.rootDeleted=true;
   }
   while(stack.length&&requests+2<=budget&&now()<deadline){
    const task=stack.at(-1);if(!valid(task.path)||!['doc','collection','invites'].includes(task.kind))throw Error('invalid_delete_scope');
    if(task.kind==='invites'){
     if(task.path!==root)throw Error('invalid_invite_scope');
     const limit=Math.min(8,budget-requests-1);
     const rows=await post(':runQuery',{structuredQuery:{from:[{collectionId:'communityInvites450'}],where:{fieldFilter:{field:{fieldPath:'communityId'},op:'EQUAL',value:{stringValue:id}}},limit}});requests++;
     if(!Array.isArray(rows))throw Error('invalid_invite_response');
     const invites=rows.filter(row=>row.document).map(row=>row.document);
     if(invites.length>limit)throw Error('invalid_invite_count');
     if(!invites.length)stack.pop();
     for(const invite of invites){
      const prefix=name('communityInvites450')+'/';
      if(!invite.name?.startsWith(prefix)||invite.name.slice(prefix.length).includes('/')||document(invite)?.communityId!==id||!invite.updateTime)throw Error('invalid_invite_scope');
      await api('/'+encode(invite.name.slice((database+'/documents/').length))+'?currentDocument.updateTime='+encodeURIComponent(invite.updateTime),{method:'DELETE'});requests++;
     }
    }else if(task.kind==='doc'){
     const result=await post('/'+encode(task.path)+':listCollectionIds',{pageSize:10});requests++;
     const ids=result?.collectionIds??[];if(!Array.isArray(ids)||ids.some(id=>typeof id!=='string'||!id||id.includes('/')))throw Error('invalid_collection');
     if(ids.length){
      // Retain the parent frame and revisit after its first collections drain.
      for(const collection of ids)stack.push({kind:'collection',path:task.path+'/'+collection});
     }else{
      await api('/'+encode(task.path),{method:'DELETE'});requests++;stack.pop();
     }
    }else{
     const result=await api('/'+encode(task.path)+'?pageSize=8&showMissing=true');requests++;
     const docs=result?.documents??[];if(!Array.isArray(docs))throw Error('invalid_documents');
     if(!docs.length){stack.pop();continue;}
     for(const doc of docs){
      const prefix=name(task.path)+'/';if(typeof doc.name!=='string'||!doc.name.startsWith(prefix)||doc.name.slice(prefix.length).includes('/'))throw Error('invalid_document_scope');
      stack.push({kind:'doc',path:doc.name.slice((database+'/documents/').length)});
     }
    }
    if(stack.length>500||JSON.stringify(stack).length>65536)throw Error('delete_scope_too_deep');
   }
   job.stackJson=JSON.stringify(stack);return {done:stack.length===0,requests};
  },
  async save(job,id,done){return transaction(async tx=>{
   const current=await get(jobPath(id),tx);
   if(current?.ownerUid!==job.ownerUid||current.leaseId!==job.leaseId)throw Error('lost_delete_lease');
   const next={...job,state:done?'done':'deleting',leaseUntil:0,leaseId:'',updatedAt:now()};
   return {writes:[{update:{name:name(jobPath(id)),fields:fields(next)}}],value:true};
  });},
 };
}
export function createCommunityDelete556({verify,rateLimit,store}){
 return async(request,body)=>{
  if(!body||typeof body!=='object'||Array.isArray(body)||Object.keys(body).some(k=>!['communityId','confirmName','confirmDelete'].includes(k))||body.confirmDelete!==true||!/^[-_A-Za-z0-9]{1,128}$/.test(body.communityId??'')||typeof body.confirmName!=='string'||!body.confirmName.length||body.confirmName.length>60)return {status:400,body:{error:'invalid_request'}};
  let identity;try{identity=await verify(request);}catch{return {status:401,body:{error:'unauthenticated'}};}
  if(!identity?.uid||identity.firebase?.sign_in_provider==='anonymous')return {status:403,body:{error:'forbidden'}};
  let lease;
  try{
   if(!await rateLimit(identity.uid))return {status:429,body:{error:'rate_limited'}};
   lease=await store.claim(identity,body);
   if(lease.status===403)return {status:403,body:{error:'forbidden'}};
   if(lease.deleted)return {status:200,body:{deleted:true}};
   if(lease.busy)return {status:202,body:{deleted:false,pending:true}};
   const progress=await store.advance(lease.job,lease.id);await store.save(lease.job,lease.id,progress.done);
   return {status:progress.done?200:202,body:{deleted:progress.done,pending:!progress.done}};
  }catch{
   // Replaying an earlier queue is safe: missing documents and empty subtrees
   // are idempotent. Do not release a failed lease with a partially trusted queue.
   return {status:503,body:{error:'temporarily_unavailable'}};
  }
 };
}
