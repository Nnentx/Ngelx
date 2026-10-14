import {scheduledOutcome} from './policy.mjs';
import {initializeApp,getApps} from 'firebase-admin/app';
import {getFirestore,FieldValue} from 'firebase-admin/firestore';
import {getFunctions} from 'firebase-admin/functions';
import {onDocumentCreated,onDocumentWritten} from 'firebase-functions/v2/firestore';
import {onTaskDispatched} from 'firebase-functions/v2/tasks';
if(!getApps().length)initializeApp();
const region='europe-west1',base={region,memory:'256MiB',timeoutSeconds:60,maxInstances:2,retry:true};
export const queueCommunity456=onDocumentCreated({...base,document:'communities450/{cid}/posts/{pid}'},async e=>{
 const p=e.data?.data();if(p?.status!=='scheduled'||!p.publishAt?.toDate)return;
 await getFunctions().taskQueue(`locations/${region}/functions/publishCommunity456`).enqueue(e.params,{scheduleTime:p.publishAt.toDate(),dispatchDeadlineSeconds:60});
});
export const publishCommunity456=onTaskDispatched({region,memory:'256MiB',timeoutSeconds:60,maxInstances:1,retryConfig:{maxAttempts:5,minBackoffSeconds:60},rateLimits:{maxConcurrentDispatches:1}},async request=>{
 const {cid,pid}=request.data??{};if(!/^[A-Za-z0-9_-]+$/.test(cid??'')||!/^[A-Za-z0-9_-]+$/.test(pid??''))return;
 const db=getFirestore(),root=db.collection('communities450').doc(cid),post=root.collection('posts').doc(pid);
 await db.runTransaction(async tx=>{const [c,p]=await Promise.all([tx.get(root),tx.get(post)]),v=c.data(),item=p.data();const outcome=scheduledOutcome(v,item?{...item,publishAt:item.publishAt?.toMillis?.()}:null,Date.now());if(outcome==='ignore')return;if(outcome==='retry')throw Error('not-due');
 if(outcome==='reject'){tx.update(post,{status:'rejected'});return;}
 tx.update(post,{status:'approved',createdAt:FieldValue.serverTimestamp()});});
});
export const communityCounters456=onDocumentWritten({...base,document:'communities450/{cid}/posts/{pid}/{metric}/{item}'},async e=>{
 if(!['likes','comments','views','shares'].includes(e.params.metric))return;
 const post=getFirestore().collection('communities450').doc(e.params.cid).collection('posts').doc(e.params.pid);if(!(await post.get()).exists)return;
 const count=await post.collection(e.params.metric).count().get();await post.update({[`counts456.${e.params.metric}`]:count.data().count});
});
export const communityCommentNotify456=onDocumentCreated({...base,document:'communities450/{cid}/posts/{pid}/comments/{commentId}'},async e=>{
 const comment=e.data?.data();if(!comment)return;
 const db=getFirestore(),root=db.collection('communities450').doc(e.params.cid),post=root.collection('posts').doc(e.params.pid);
 const [c,p,sender]=await Promise.all([root.get(),post.get(),db.collection('users').doc(comment.uid).get()]);const community=c.data(),author=sender.data();if(!community||p.data()?.status!=='approved'||!author||author.deactivated)return;
 const subscriptions=await post.collection('subscribers456').where('enabled','==',true).limit(500).get();
 for(const sub of subscriptions.docs){const uid=sub.id;if(uid===comment.uid||!community.members?.includes(uid))continue;const user=(await db.collection('users').doc(uid).get()).data();if(!user||user.deactivated||user.notificationsEnabled===false||user.interactionNotifications===false||user.blocked?.includes(comment.uid)||author.blocked?.includes(uid)||user.restrictedUsers?.includes(comment.uid))continue;
 const ref=db.collection('notifications').doc(`community456_${e.params.cid}_${e.params.pid}_${e.params.commentId}_${uid}`);
 try{await ref.create({toUid:uid,fromUid:comment.uid,type:'comment',senderName:String(author.displayName??author.username??'Üye'),photoUrl:String(author.photoUrl??''),text:`${author.displayName??author.username??'Üye'} topluluk gönderisine yorum yaptı`,read:false,createdAt:FieldValue.serverTimestamp(),eventKind:'community_comment456',sourceId:e.params.cid,targetKind:'community'});}catch(error){if(error.code!==6&&error.code!=='already-exists')throw error;}
 }
});
