const account=process.env.CLOUDFLARE_ACCOUNT_ID,token=process.env.CLOUDFLARE_API_TOKEN;
if(!account||!token)throw Error('Existing Cloudflare deployment identity missing');
const base=`https://api.cloudflare.com/client/v4/accounts/${account}/workers/domains`;
async function api(url,options={}){const r=await fetch(url,{...options,headers:{authorization:'Bearer '+token,'content-type':'application/json'},signal:AbortSignal.timeout(20000)});const d=await r.json();if(!r.ok||!d.success)throw Error('Custom game domain operation HTTP '+r.status);return d.result;}
const domains=await api(base),hostname='oyun.ngelxsocial.com',service='ngelx-live-moderation';
const prior=domains.find(d=>d.hostname===hostname);
if(prior&&prior.service!==service)throw Error('Existing domain belongs to another service; unchanged');
if(!prior){
 const zone=domains.find(d=>['media.ngelxsocial.com','media2.ngelxsocial.com'].includes(d.hostname))?.zone_id;
 if(!zone)throw Error('Existing owned media domain zone not found; no DNS changed');
 await api(base,{method:'PUT',body:JSON.stringify({hostname,service,environment:'production',zone_id:zone})});
}
console.log('Game domain attached to the existing worker; existing media and website domains unchanged.');
