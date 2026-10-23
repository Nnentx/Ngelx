// Redeploy only the owner's already-running service. No new subscription,
// paid resource, credential creation or plan change is requested here.
const token=process.env.CLOUDFLARE_API_TOKEN,account=process.env.CLOUDFLARE_ACCOUNT_ID;
if(!token||!account)throw Error('Existing deployment connection is missing');
const headers={authorization:'Bearer '+token};
const base='https://api.cloudflare.com/client/v4/accounts/'+encodeURIComponent(account)+'/';
const sub=await fetch(base+'workers/subdomain',{headers,signal:AbortSignal.timeout(10000)});
const domain=await sub.json();if(!sub.ok||domain.result?.subdomain!=='alihancaglar76')throw Error('Existing account could not be verified');
const script=await fetch(base+'workers/scripts/ngelx-live-moderation/settings',{headers,signal:AbortSignal.timeout(10000)});
if(!script.ok)throw Error('Existing worker could not be verified; no deployment permitted');
const health=await fetch('https://ngelx-live-moderation.alihancaglar76.workers.dev/health',{signal:AbortSignal.timeout(10000)});
const data=await health.json();if(!health.ok||data.service!=='ngelx-live-moderation'||data.ok!==true)throw Error('Existing worker is not configured');
console.log('Verified owner account and healthy existing worker. Existing secrets retained; billing unchanged.');
