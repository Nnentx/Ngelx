import {normalizeUsername} from '../auth/username-ownership.mjs';
export function threeMonths(value){
 const date=new Date(value);if(!Number.isFinite(+date))throw Error('invalid-date');
 const month=date.getUTCMonth()+3;
 const last=new Date(Date.UTC(date.getUTCFullYear(),month+1,0)).getUTCDate();
 const result=new Date(+date);result.setUTCDate(1);result.setUTCMonth(month);result.setUTCDate(Math.min(date.getUTCDate(),last));return result;
}
export function identityPlan(profile,body,now){
 if(!body||typeof body!=='object'||Array.isArray(body)||Object.keys(body).some(k=>!['displayName','username'].includes(k)))throw Error('invalid-request');
 const patch={};
 for(const field of ['displayName','username']){
  if(!Object.hasOwn(body,field))continue;
  if(typeof body[field]!=='string')throw Error('invalid-request');
  const value=body[field].trim(),previous=String(profile[field]??'').trim();
  if(value===previous)continue;
  if(field==='displayName'&&(value.length<2||value.length>60||/[\x00-\x1f\x7f]/.test(value)))throw Error('invalid-name');
  if(field==='username')patch.usernameLower=normalizeUsername(value);
  const raw=profile[field+'ChangedAt559'];
  if(raw!=null){const stamp=raw?.toDate?raw.toDate():new Date(raw);if(!Number.isFinite(+stamp)||+now<+threeMonths(stamp))throw Error('cooldown');}
  patch[field]=value;patch[field+'ChangedAt559']=new Date(now);
 }
 return patch;
}
export async function updateIdentity({db,uid,body,now=new Date()}){
 if(typeof uid!=='string'||!uid||uid.includes('/'))throw Error('unauthenticated');
 return db.runTransaction(async tx=>{
  const ref=db.collection('users').doc(uid),snap=await tx.get(ref);
  if(!snap.exists)throw Error('profile-required');
  const profile=snap.data(),patch=identityPlan(profile,body,now);
  if(!Object.keys(patch).length)return {changed:false};
  let target,oldRef;
  if(patch.usernameLower){
   const readiness=await tx.get(db.collection('app_config').doc('identity559'));
   if(readiness.data()?.usernameIndexReady!==true)throw Error('username-index-not-ready');
   target=db.collection('login_usernames').doc(patch.usernameLower);
   const record=await tx.get(target);
   if(record.exists&&(record.data()?.uid!==uid||record.data()?.status!=='active'))throw Error('username-taken');
   // Revalidate both modern and legacy exact names; ownership index serializes new claims.
   const modern=await tx.get(db.collection('users').where('usernameLower','==',patch.usernameLower).limit(2));
   const legacy=await tx.get(db.collection('users').where('username','==',patch.username).limit(2));
   if([...modern.docs,...legacy.docs].some(d=>d.id!==uid))throw Error('username-taken');
   const old=profile.usernameLower;
   if(typeof old==='string'&&old!==patch.usernameLower&&/^[a-z0-9._]{3,20}$/.test(old)){
    oldRef=db.collection('login_usernames').doc(old);
    const prior=await tx.get(oldRef);
    if(prior.exists&&(prior.data()?.uid!==uid||prior.data()?.status!=='active'))throw Error('ownership-conflict');
   }
  }
  if(target)tx.set(target,{uid,status:'active',version:1});
  if(oldRef)tx.set(oldRef,{uid,status:'retired',version:1});
  tx.update(ref,{...patch,updatedAt:new Date(now)});
  return {changed:true};
 });
}
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function verificationEmail({name,link}){
 const url=new URL(link);
 if(url.protocol!=='https:'||url.host!=='ngelx-44eed.firebaseapp.com'||url.pathname!=='/__/auth/action'||url.searchParams.get('mode')!=='verifyEmail'||!url.searchParams.get('oobCode'))throw Error('invalid-action-link');
 const safe=escape(link),hello=name?`Merhaba ${escape(name)},`:'Merhaba,';
 const text=`${name?'Merhaba '+name+',':'Merhaba,'}\n\nNgelX hesabını etkinleştirmek için e-posta adresini doğrula:\n${link}\n\nBu işlemi sen başlatmadıysan bu e-postayı yok sayabilirsin. Bağlantı geçersizse uygulamadan yeni bir doğrulama e-postası iste.\n\nNgelX Ekibi\nBu otomatik e-postaya verilen yanıtlar takip edilmez.`;
 return {subject:'NgelX — E-posta adresini doğrula',text,html:`<!doctype html><html lang="tr"><head><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0;background:#f7f4ff;font:16px Arial,sans-serif;color:#252033"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:32px 16px"><table role="presentation" width="100%" style="max-width:520px;background:white;border-radius:24px" cellpadding="28"><tr><td><div style="font-size:32px;font-weight:bold;color:#783ff0">NgelX</div><h1 style="font-size:26px">E-postanı doğrula</h1><p>${hello}</p><p>NgelX hesabını etkinleştirmek için aşağıdaki düğmeye dokun.</p><table role="presentation" cellpadding="0"><tr><td bgcolor="#783ff0" style="border-radius:14px"><a href="${safe}" style="display:inline-block;padding:18px 26px;color:white;text-decoration:none;font-size:18px;font-weight:bold">E-postamı doğrula</a></td></tr></table><p style="font-size:14px;color:#655e75">Düğme açılmıyorsa <a href="${safe}">bu bağlantıya dokun</a>. Bağlantı geçersizse veya süresi dolduysa NgelX uygulamasından yeniden gönder.</p><p>Bu işlemi sen başlatmadıysan bu e-postayı yok sayabilirsin.</p><p><strong>NgelX Ekibi</strong></p><p style="font-size:12px;color:#777">Bu otomatik e-postaya verilen yanıtlar takip edilmez.</p></td></tr></table></td></tr></table></body></html>`};
}
