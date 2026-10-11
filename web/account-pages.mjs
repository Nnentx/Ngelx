import {initializeApp} from 'https://www.gstatic.com/firebasejs/12.4.0/firebase-app.js';
import {getAuth,setPersistence,inMemoryPersistence,signInWithEmailAndPassword,signOut,sendPasswordResetEmail} from 'https://www.gstatic.com/firebasejs/12.4.0/firebase-auth.js';
import * as sdk from 'https://www.gstatic.com/firebasejs/12.4.0/firebase-firestore.js';
import {requestAccountDeletion,supportPayload} from './account-actions.mjs';
const app=initializeApp({apiKey:'AIzaSyAUH9L6aihwx2tzwpGXupYg4J6wBRiQ_sw',authDomain:'ngelx-44eed.firebaseapp.com',projectId:'ngelx-44eed'});
const auth=getAuth(app),db=sdk.getFirestore(app);
auth.languageCode='tr';
const $=id=>document.getElementById(id), page=document.querySelector('main').dataset.page;
let busy=false,finished=false;
function show(message,type=''){ $('status').hidden=false; $('status').textContent=message; $('status').className='status '+type; }
function state(){for(const id of ['login','reset','submit','logout'])$(id).disabled=busy||finished;}
function error(e){
  const code=e?.code||'';
  if(['auth/invalid-credential','auth/wrong-password','auth/user-not-found'].includes(code))return 'E-posta veya şifre yanlış.';
  if(code==='auth/too-many-requests')return 'Çok fazla deneme yapıldı. Bir süre sonra tekrar dene.';
  if(code==='auth/network-request-failed'||code==='unavailable')return 'Sunucuya ulaşılamadı. İnternet bağlantını kontrol et.';
  if(code==='permission-denied')return 'İşlem izni reddedildi. Talep kaydedilmedi.';
  if(code==='resource-exhausted')return 'Sunucu işlem sınırına ulaştı. Daha sonra tekrar dene.';
  if(e?.message==='profile-unavailable')return 'Bu hesabın profil kaydı bulunamadı. Uygulama içinden destek al.';
  return 'İşlem tamamlanamadı. Bağlantını kontrol edip tekrar dene.';
}
async function perform(fn){
  if(busy||finished)return;
  busy=true;state();
  // A timeout cannot cancel an in-flight write; keep the form locked until it settles.
  const notice=setTimeout(()=>{if(!finished)show('Sunucudan onay bekleniyor. İşlem tamamlanmadan başarı bildirilmeyecek.');},15000);
  try{await fn();}catch(e){show(error(e),'error');}finally{clearTimeout(notice);busy=false;state();}
}
$('login-form').addEventListener('submit',e=>{e.preventDefault();perform(async()=>{
  await setPersistence(auth,inMemoryPersistence);
  const result=await signInWithEmailAndPassword(auth,$('email').value.trim(),$('password').value);
  $('password').value='';$('account').textContent='Giriş yapılan hesap: '+result.user.email;
  $('login-section').hidden=true;$('action-section').hidden=false;$('status').hidden=true;
});});
$('reset').addEventListener('click',()=>perform(async()=>{
  if(!$('email').reportValidity())return;
  await sendPasswordResetEmail(auth,$('email').value.trim());
  show('Bu e-posta ile kayıtlı bir hesap varsa şifre yenileme bağlantısı gönderilir. E-posta kutunu kontrol et.','success');
}));
$('logout').addEventListener('click',()=>perform(async()=>{
  await signOut(auth);$('action-section').hidden=true;$('login-section').hidden=false;$('status').hidden=true;$('password').value='';
}));
$('action-form').addEventListener('submit',e=>{e.preventDefault();perform(async()=>{
  const user=auth.currentUser;if(!user)throw new Error('sign-in-required');
  if(page==='delete'){
    const result=await requestAccountDeletion(db,sdk,user.uid);
    finished=true;$('action-form').hidden=true;
    show((result.alreadyScheduled?'Hesabın için zaten bir silme talebi var.':'Silme talebin kaydedildi. Hesabın devre dışı bırakıldı.')+' Kalıcı silme için planlanan tarih: '+result.executeAfter.toLocaleDateString('tr-TR')+'. Bu tarihe kadar uygulamadan hesabını geri açabilirsin.','success');
    try{await signOut(auth);}catch(_){/* Request is already committed; do not misreport failure. */}
  }else{
    const request=sdk.doc(sdk.collection(db,'support_requests'));
    await sdk.setDoc(request,supportPayload(user,$('category').value,$('description').value,sdk));
    $('description').value='';show('Destek talebin kaydedildi. Talep numarası: '+request.id,'success');
  }
});});

state();
