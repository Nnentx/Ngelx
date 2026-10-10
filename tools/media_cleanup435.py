"""Resumable story/message cleanup and quarantined orphan R2 cleanup.

All Firestore documents/subcollections are scanned before any object is removed.
Unknown ownership, truncated inventories, read errors, recent objects, shared
references and changed ETags fail closed. Preview is the default.
"""
import argparse,datetime as dt,hashlib,os,re
from urllib.parse import urlparse,unquote
from retention_cleanup import expires_unsaved
UTC=dt.timezone.utc
KINDS={'photos','videos','music','profiles','stories','chats','groups','support','chat-backgrounds','profile-intros','thumbnails','gifs','chat-files','chat-audio'}
ORIGINS={'media.ngelxsocial.com','media2.ngelxsocial.com'}
FIELDS=('mediaUrl','videoUrl','audioUrl','fileUrl','thumbnailUrl','posterUrl','coverUrl','imageUrl')
def key_owner(key):
 if not isinstance(key,str):return None
 parts=key.split('/')
 if len(parts)<3 or parts[0] not in KINDS or any(x in ('','.','..') for x in parts):return None
 return parts[1]
def media_key(raw):
 if not isinstance(raw,str):return None
 u=urlparse(raw)
 if u.scheme!='https' or u.hostname not in ORIGINS or not u.path.startswith('/media/'):return None
 key=unquote(u.path[7:])
 return key if key_owner(key) else None
def collect_keys(value):
 if isinstance(value,str):
  result=set()
  # References may be raw storage paths, nested payload URLs, or URLs inside
  # a message/link. Protect mirrored worker URLs as well as the public origin.
  if key_owner(value):result.add(value)
  for raw in [value,*re.findall(r'https://[^\s<>"\']+',value)]:
   u=urlparse(raw.rstrip('.,;!?)'))
   if u.path.startswith('/media/'):
    key=unquote(u.path[7:])
    if key_owner(key):result.add(key)
  return result
 if isinstance(value,dict):return set().union(*(collect_keys(v) for v in value.values())) if value else set()
 if isinstance(value,(list,tuple)):return set().union(*(collect_keys(v) for v in value)) if value else set()
 return set()
def object_safe(key,meta):
 return bool(key_owner(key) and meta.get('Metadata',{}).get('uid')==key_owner(key))
def orphan_ready(key,head,refs,now,quarantine):
 stamp=head.get('LastModified');etag=head.get('ETag')
 if key in refs or not object_safe(key,head) or not isinstance(stamp,dt.datetime) or not etag:return False
 if now-stamp.astimezone(UTC)<dt.timedelta(days=7):return False
 return bool(quarantine and quarantine.get('etag')==etag and isinstance(quarantine.get('firstSeenAt'),dt.datetime)
             and now-quarantine['firstSeenAt'].astimezone(UTC)>=dt.timedelta(hours=24))
def inventory(db,max_docs=100000):
 result={};count=0
 def walk(collection):
  nonlocal count
  # list_documents includes missing parents that still have subcollections.
  for ref in collection.list_documents():
   snap=ref.get();count+=1
   if count>max_docs:raise RuntimeError('Inventory limit reached; no deletion allowed')
   if snap.exists:result[ref.path]=snap
   for child in ref.collections():walk(child)
 for collection in db.collections():walk(collection)
 return result
def reference_keys(docs,exclude=()):
 result=set()
 for path,snap in docs.items():
  if any(path==p or path.startswith(p+'/') for p in exclude):continue
  if path.startswith(('_media_cleanup435/','_orphan_cleanup435/','_retention_cleanup_jobs/','_live_cleanup_jobs/')):continue
  v=snap.to_dict() or {}
  if '/messages/' in path and v.get('deletedForEveryone') is True:
   # Tombstone manifests are intents, not active references.
   v={k:x for k,x in v.items() if k not in FIELDS and k!='cleanupMediaUrls'}
  result.update(collect_keys(v))
 return result
def job_id(path):return hashlib.sha256(path.encode()).hexdigest()
def remove_media(key,owner,head,reference_scan,delete,source_valid=lambda:True):
 """A failed DELETE raises so its durable job remains for the next run."""
 if key_owner(key)!=owner:return 'blocked'
 first=head(key)
 if first is None:return 'missing'
 if not object_safe(key,first):return 'blocked'
 if key in reference_scan():return 'shared'
 latest=head(key)
 if latest is None:return 'missing'
 if not object_safe(key,latest) or latest.get('ETag')!=first.get('ETag') or not source_valid():return 'blocked'
 if key in reference_scan():return 'shared'
 delete(key)
 return 'deleted'
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--apply',action='store_true');p.add_argument('--limit',type=int,default=100);p.add_argument('--max-docs',type=int,default=100000);cfg=p.parse_args()
 if not 1<=cfg.limit<=500:p.error('limit 1–500')
 import firebase_admin,boto3
 from firebase_admin import firestore
 from botocore.exceptions import ClientError
 firebase_admin.initialize_app();db=firestore.client();now=dt.datetime.now(UTC)
 r2=boto3.client('s3',endpoint_url=os.environ['NGELX_R2_ENDPOINT'],aws_access_key_id=os.environ['NGELX_R2_ACCESS_KEY_ID'],aws_secret_access_key=os.environ['NGELX_R2_SECRET_ACCESS_KEY'],region_name='auto');bucket=os.environ['NGELX_R2_BUCKET']
 def head(key):
  try:return r2.head_object(Bucket=bucket,Key=key)
  except ClientError as e:
   if e.response['Error']['Code'] in ('404','NoSuchKey','NotFound'):return None
   raise
 docs=inventory(db,cfg.max_docs);refs=reference_keys(docs)
 stories=[s for path,s in docs.items() if path.startswith('videos/') and path.count('/')==1 and expires_unsaved(s.to_dict() or {},now)][:cfg.limit]
 messages=[s for path,s in docs.items() if path.startswith('chats/') and path.count('/')==3 and '/messages/' in path and (s.to_dict() or {}).get('deletedForEveryone') is True and (s.to_dict() or {}).get('mediaCleanupState')=='pending'][:cfg.limit]
 print(f'Complete inventory={len(docs)}; expired stories={len(stories)}; message jobs={len(messages)}; apply={cfg.apply}')
 if cfg.apply:
  for snap in stories:
   v=snap.to_dict() or {};owner=v.get('ownerId')
   if not isinstance(owner,str) or not owner:continue
   raw=[v.get(f,'') for f in FIELDS];job=db.collection('_media_cleanup435').document(job_id(snap.reference.path))
   @firestore.transactional
   def claim(tx):
    fresh=snap.reference.get(transaction=tx)
    if fresh.update_time!=snap.update_time or not expires_unsaved(fresh.to_dict() or {},dt.datetime.now(UTC)):return False
    tx.set(job,{'sourcePath':snap.reference.path,'ownerId':owner,'urls':raw,'kind':'story','createdAt':firestore.SERVER_TIMESTAMP,'lastAttemptAt':dt.datetime(1970,1,1,tzinfo=UTC)})
    tx.delete(snap.reference);return True
   claim(db.transaction())
  for snap in messages:
   v=snap.to_dict() or {};job=db.collection('_media_cleanup435').document(job_id(snap.reference.path))
   @firestore.transactional
   def queue(tx):
    fresh=snap.reference.get(transaction=tx);current=fresh.to_dict() or {};existing=job.get(transaction=tx)
    if fresh.update_time!=snap.update_time or current.get('deletedForEveryone') is not True or existing.exists:return
    tx.set(job,{'sourcePath':snap.reference.path,'ownerId':v.get('senderId',''),'urls':v.get('cleanupMediaUrls',[]),'kind':'message','createdAt':firestore.SERVER_TIMESTAMP,'lastAttemptAt':dt.datetime(1970,1,1,tzinfo=UTC)})
   queue(db.transaction())
  # Fresh complete inventory after claims preserves saved/new/shared content.
  docs=inventory(db,cfg.max_docs);refs=reference_keys(docs)
  cleaned=blocked=0
  for pending in db.collection('_media_cleanup435').order_by('lastAttemptAt').limit(cfg.limit).stream():
   j=pending.to_dict() or {};source=j.get('sourcePath','');kind=j.get('kind');owner=j.get('ownerId');raw=j.get('urls',[])
   if not isinstance(raw,list) or not isinstance(owner,str) or not owner:blocked+=1;continue
   valid=(kind=='story' and source.startswith('videos/') and source.count('/')==1) or (kind=='message' and source.startswith('chats/') and source.count('/')==3 and '/messages/' in source)
   if not valid:blocked+=1;continue
   root=db.document(source);fresh=root.get();v=fresh.to_dict() or {}
   if (kind=='story' and fresh.exists) or (kind=='message' and (not fresh.exists or v.get('deletedForEveryone') is not True)):blocked+=1;continue
   unresolved=False;shared=[]
   for url in set(x for x in raw if isinstance(x,str) and x):
    key=media_key(url)
    if not key or key_owner(key)!=owner:unresolved=True;continue
    if key in refs:shared.append(key);continue
    outcome=remove_media(key,owner,head,lambda:reference_keys(inventory(db,cfg.max_docs)),lambda k:r2.delete_object(Bucket=bucket,Key=k),lambda: not root.get().exists if kind=='story' else (root.get().to_dict() or {}).get('deletedForEveryone') is True)
    if outcome=='blocked':unresolved=True
    elif outcome=='shared':shared.append(key)
   if unresolved:
    pending.reference.update({'lastAttemptAt':firestore.SERVER_TIMESTAMP,'status':'ownership-unverified'});blocked+=1;continue
   if kind=='story':
    # Children are removed only while the root is still absent. Recursive Admin
    # deletion also covers comments, likes and user-owned nested history.
    if root.get().exists:blocked+=1;continue
    for c in root.collections():
     for child in c.list_documents():db.recursive_delete(child)
   else:
    @firestore.transactional
    def complete(tx):
     current=root.get(transaction=tx)
     if current.exists and (current.to_dict() or {}).get('deletedForEveryone') is True:
      tx.update(root,{'mediaCleanupState':'shared-retained' if shared else 'done','cleanupMediaUrls':[],'mediaCleanupAt':firestore.SERVER_TIMESTAMP})
    complete(db.transaction())
   pending.reference.delete();cleaned+=1
  print(f'Cleanup completed={cleaned}; ownership/recreated-source blocked={blocked}')
 # Orphans: objects at least 7 days old, verified UID, absent in a full inventory
 # twice at least 24 hours apart. No bucket-wide unreferenced immediate delete.
 docs=inventory(db,cfg.max_docs);refs=reference_keys(docs);seen=deleted=0
 for page in r2.get_paginator('list_objects_v2').paginate(Bucket=bucket):
  for item in page.get('Contents',[]):
   key=item['Key'];stamp=item.get('LastModified')
   if not key_owner(key) or key in refs or not isinstance(stamp,dt.datetime) or now-stamp.astimezone(UTC)<dt.timedelta(days=7):continue
   h=head(key)
   if h is None or not object_safe(key,h):continue
   seen+=1;q=db.collection('_orphan_cleanup435').document(job_id(key));old=q.get().to_dict() or {}
   ready=orphan_ready(key,h,refs,now,old)
   if cfg.apply:
    if ready:
     fresh_refs=reference_keys(inventory(db,cfg.max_docs));h2=head(key)
     if h2 and h2.get('ETag')==h.get('ETag') and orphan_ready(key,h2,fresh_refs,dt.datetime.now(UTC),old):
      r2.delete_object(Bucket=bucket,Key=key);q.delete();deleted+=1
    elif old.get('etag')!=h.get('ETag'):
     q.set({'key':key,'ownerId':key_owner(key),'etag':h.get('ETag'),'firstSeenAt':firestore.SERVER_TIMESTAMP})
   if seen>=cfg.limit:break
  if seen>=cfg.limit:break
 print(f'Orphan candidates={seen}; deleted={deleted}; grace=7days+24hours')
if __name__=='__main__':main()
