#!/usr/bin/env python3
"""Owner-checked retention cleanup. Preview by default; --apply enables deletion.
Requires application default Firebase Admin credentials and R2 credentials.
Never scan/delete arbitrary unreferenced media: only verified content records.
"""
import argparse
import datetime as dt
import os
from urllib.parse import urlparse, unquote
UTC=dt.timezone.utc

def expires_unsaved(data,now):
    expires=data.get('expiresAt')
    return (data.get('type')=='story' and isinstance(expires,dt.datetime)
            and expires.astimezone(UTC)<=now and not data.get('archivedAt')
            and data.get('highlighted') is not True and data.get('saved') is not True)

def own_media_key(raw,uid):
    if not isinstance(raw,str) or not uid:return None
    path=unquote(urlparse(raw).path)
    if not path.startswith('/media/'):return None
    key=path[len('/media/'):]
    parts=key.split('/')
    if len(parts)<3 or parts[0] not in ('stories','videos','photos') or parts[1]!=uid:
        return None
    if any(p in ('','..','.') for p in parts):return None
    return key

def media_urls(data):
    return {v for field in ('mediaUrl','videoUrl','audioUrl','thumbnailUrl','posterUrl','coverUrl')
            if isinstance((v:=data.get(field)),str) and v.strip()}

def main():
    args=argparse.ArgumentParser(description=__doc__)
    args.add_argument('--apply',action='store_true')
    args.add_argument('--limit',type=int,default=100)
    cfg=args.parse_args()
    if cfg.limit<1 or cfg.limit>500:args.error('limit must be 1–500')
    import firebase_admin
    from firebase_admin import firestore
    firebase_admin.initialize_app()
    db=firestore.client()
    now=dt.datetime.now(UTC)
    candidates=[]
    for doc in db.collection('videos').where('type','==','story').stream():
        if expires_unsaved(doc.to_dict(),now):candidates.append(doc)
        if len(candidates)>=cfg.limit:break
    print(f'{len(candidates)} expired, unsaved stories; mode={"apply" if cfg.apply else "preview"}')
    if not cfg.apply:return
    import boto3
    media_origin=os.environ['NGELX_MEDIA_ORIGIN'].rstrip('/')
    bucket=os.environ['NGELX_R2_BUCKET']
    r2=boto3.client('s3',endpoint_url=os.environ['NGELX_R2_ENDPOINT'],
        aws_access_key_id=os.environ['NGELX_R2_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['NGELX_R2_SECRET_ACCESS_KEY'],region_name='auto')
    def purge(ref):
        for collection in ref.collections():
            for child in collection.stream():purge(child.reference)
        ref.delete()
    for candidate in candidates:
        ref=candidate.reference
        # Re-read ownership, expiration, and save flags immediately before cleanup.
        snap=ref.get();data=snap.to_dict() or {}
        if not expires_unsaved(data,dt.datetime.now(UTC)):continue
        uid=data.get('ownerId')
        if not isinstance(uid,str) or not uid:continue
        keys=[]
        safe=True
        for raw in media_urls(data):
            if urlparse(raw).netloc!=urlparse(media_origin).netloc:
                safe=False;break
            key=own_media_key(raw,uid)
            if key is None:safe=False;break
            try:
                metadata=r2.head_object(Bucket=bucket,Key=key).get('Metadata',{})
            except r2.exceptions.ClientError as error:
                if error.response['Error']['Code'] not in ('404','NoSuchKey','NotFound'):raise
                continue
            if metadata.get('uid')!=uid:safe=False;break
            keys.append(key)
        if not safe:
            print(f'SKIP {ref.id}: unverifiable media ownership');continue
        # Atomically move an unchanged expired record into a durable cleanup job.
        # A concurrent save or edit wins the version check and is never deleted.
        job=db.collection('_retention_cleanup_jobs').document(ref.id)
        @firestore.transactional
        def claim(transaction):
            current=ref.get(transaction=transaction)
            if current.update_time!=snap.update_time:return False
            if not expires_unsaved(current.to_dict() or {},dt.datetime.now(UTC)):return False
            transaction.set(job,{'ownerId':uid,'sourcePath':ref.path,'keys':keys,
                                 'createdAt':firestore.SERVER_TIMESTAMP})
            transaction.delete(ref)
            return True
        if not claim(db.transaction()):continue
        print(f'QUEUED {ref.id}')
    # Jobs contain only paths verified before the record was removed. An R2 failure
    # leaves the durable job intact and the following run resumes it.
    for pending in db.collection('_retention_cleanup_jobs').limit(cfg.limit).stream():
        job=pending.to_dict() or {}
        uid=job.get('ownerId');source=job.get('sourcePath','')
        if not isinstance(uid,str) or not source.startswith('videos/') or source.count('/')!=1:
            continue
        keys=job.get('keys',[])
        if not isinstance(keys,list) or any(own_media_key(media_origin+'/media/'+key,uid)!=key for key in keys):
            continue
        for key in keys:
            try:
                metadata=r2.head_object(Bucket=bucket,Key=key).get('Metadata',{})
            except r2.exceptions.ClientError as error:
                if error.response['Error']['Code'] not in ('404','NoSuchKey','NotFound'):raise
                continue
            if metadata.get('uid')!=uid:raise RuntimeError('Cleanup media ownership changed')
            r2.delete_object(Bucket=bucket,Key=key)
        # Refuse to remove a newly restored/recreated record's child collections.
        ref=db.document(source)
        if ref.get().exists:continue
        purge(ref)
        pending.reference.delete()
        print(f'CLEANED {pending.id}')

if __name__=='__main__':main()
