// Minimal operator client for Build575 Ludo reports.
// No token is persisted, printed, or passed on the command line.
// Run only by an operator whose verified Firebase UID is in LUDO_MODERATOR_UIDS.
import {pathToFileURL} from 'node:url';

const help=[
 'Usage:',
 '  LUDO_REVIEW_ENDPOINT_URL=https://<verified-worker>/ludo LUDO_MODERATOR_ID_TOKEN=<firebase-id-token> node tools/ludo575_moderator_cli.mjs list [YYYY-MM-DD] [page]',
 '  LUDO_REVIEW_ENDPOINT_URL=https://<verified-worker>/ludo LUDO_MODERATOR_ID_TOKEN=<firebase-id-token> node tools/ludo575_moderator_cli.mjs resolve report575_<64-hex> reviewed|dismissed|actioned',
 'Do not store or paste identity tokens in logs, tickets, chat, or arguments.',
].join('\n');

export async function runModeratorCommand575(args,{
 env=process.env,fetcher=fetch,now=()=>Date.now()
}={}){
 const endpoint=env.LUDO_REVIEW_ENDPOINT_URL,token=env.LUDO_MODERATOR_ID_TOKEN;
 if(!endpoint||!token||typeof token!=='string'||token.length<20)
  throw Error('Moderator endpoint and signed-in Firebase ID token must be provided through private environment variables');
 let url;
 try{url=new URL(endpoint);}catch{throw Error('Moderator endpoint URL is invalid');}
 if(url.protocol!=='https:'||url.username||url.password||url.search||url.hash||url.pathname!=='/ludo')
  throw Error('Moderator endpoint must be an HTTPS /ludo API without embedded credentials or parameters');
 const [command,value,argument,...extra]=args;
 if(extra.length||!['list','resolve'].includes(command))throw Error(help);
 let body;
 if(command==='list'){
  const day=value??new Date(now()).toISOString().slice(0,10);
  const page=argument===undefined?0:Number(argument);
  if(!/^\d{4}-\d{2}-\d{2}$/.test(day)||!Number.isSafeInteger(page)||page<0||page>49)
   throw Error('Invalid day or page');
  body={action:'moderation_queue',day,page};
 }else{
  if(typeof value!=='string'||!/^report575_[a-f0-9]{64}$/.test(value)||
   !['reviewed','dismissed','actioned'].includes(argument))throw Error(help);
  body={action:'moderation_resolve',reportId:value,decision:argument};
 }
 // No implicit retries on moderation decisions. A human can query the report
 // again if a request is interrupted before submitting a second decision.
 let response;
 try{
  response=await fetcher(url.toString(),{
   method:'POST',
   headers:{authorization:'Bearer '+token,'content-type':'application/json','cache-control':'no-store'},
   body:JSON.stringify(body),signal:AbortSignal.timeout(12000),
  });
 }catch{
  throw Error('Could not reach moderation service; review report status before retrying');
 }
 if(!response.ok){
  if(response.status===401||response.status===403)throw Error('Operator is not authorized by Firebase and the Worker moderator allowlist');
  if(response.status===404)throw Error('Moderation endpoint or report not found');
  throw Error('Moderation service returned '+response.status);
 }
 const result=await response.json();
 if(!result||typeof result.room!=='object'||result.room===null)
  throw Error('Unexpected moderator API response');
 return result.room;
}

if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 runModeratorCommand575(process.argv.slice(2)).then(x=>{
  process.stdout.write(JSON.stringify(x,null,2)+'\n');
 }).catch(e=>{
  // Never print the potentially sensitive HTTP request or Firebase ID token.
  process.stderr.write('Moderator action failed: '+e.message+'\n');
  process.exitCode=1;
 });
}
