import {readFileSync} from 'node:fs';

const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export function verificationEmail561({name,link}){
  const action=new URL(link);
  if(action.protocol!=='https:'||action.host!=='ngelx-44eed.firebaseapp.com'||action.username||action.password||action.pathname!=='/__/auth/action'||action.searchParams.get('mode')!=='verifyEmail'||!action.searchParams.get('oobCode'))throw Error('invalid-action-link');
  action.searchParams.set('lang','tr');
  const safe=escape(action.toString());
  const hello=name?`Merhaba ${escape(name)},`:'Merhaba,';
  return {
    subject:'NgelX — E-posta adresini doğrula',
    text:`${name?'Merhaba '+name+',':'Merhaba,'}\n\nNgel’e hoş geldin!\nHesabını kullanmaya başlamak için e-posta adresini doğrula:\n${action}\n\nBu işlemi sen başlatmadıysan bu e-postayı yok sayabilirsin.\n\nSevgiler, Ngel Ekibi`,
    html:`<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#eeebff;font-family:Arial,Helvetica,sans-serif;color:#141132">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eeebff"><tr><td align="center" style="padding:26px 12px">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background:#ffffff;border-radius:26px"><tr><td align="center" style="padding:30px 22px">
<div style="font-size:52px;line-height:1.1;font-weight:900;letter-spacing:-2px;color:#7c5cff">Ngel</div>
<p style="font-size:11px;letter-spacing:4px;color:#827ab1;margin:20px 0 12px">HESAP DOĞRULAMA</p>
<img src="cid:ngelx-verification-envelope" alt="Mor-mavi zarf ve doğrulama kalkanı" width="310" style="display:block;width:100%;max-width:310px;height:auto;border:0;margin:0 auto">
<h1 style="font-size:30px;line-height:1.2;margin:8px 0 20px;color:#140d36">Ngel’e hoş geldin!</h1>
<p style="font-size:21px;line-height:1.4;margin:0 0 10px;color:#28283c">${hello}</p>
<p style="font-size:17px;line-height:1.6;color:#5d587d;margin:0 0 25px">Hesabını kullanmaya başlamak için<br>e-posta adresini doğrula.</p>
<table role="presentation" cellpadding="0" cellspacing="0" width="100%"><tr><td align="center" bgcolor="#8651ed" style="border-radius:32px;background:#8651ed;background-image:linear-gradient(100deg,#b039f9,#398dff)">
<a href="${safe}" style="display:block;padding:19px 12px;border-radius:32px;color:#ffffff;text-decoration:none;font-size:20px;font-weight:700;line-height:1.3">✓&nbsp; E-postamı Doğrula</a>
</td></tr></table>
<p style="font-size:13px;line-height:1.6;color:#837aaa;margin:22px 0">Bu işlemi sen başlatmadıysan bu e-postayı yok sayabilirsin.</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td height="1" style="background:#e7e0fb;font-size:1px;line-height:1px">&nbsp;</td></tr></table>
<p style="font-size:14px;line-height:1.5;color:#706991;margin:20px 0 0">Sevgiler,<br><strong>Ngel Ekibi</strong></p>
</td></tr></table></td></tr></table></body></html>`,
    attachments:[{filename:'verification-envelope.png',content:readFileSync(new URL('./verification-envelope.png',import.meta.url)).toString('base64'),content_id:'ngelx-verification-envelope'}],
  };
}
