"""Live history cleanup: explicit-ended only; preview default; owner media validation."""
import argparse,datetime as dt,os
from urllib.parse import urlparse
from retention_cleanup import own_media_key,media_urls
UTC=dt.timezone.utc

def eligible(v,now):
    # A crash or missing heartbeat is not proof the live session has ended.
    if v.get('active') is True or v.get('status') not in ('ended','stopped','finished'):return False
    if not v.get('ownerId'):return False
    if v.get('deleting') is True:return True
    saved=v.get('saved') is True or v.get('highlighted') is True or bool(v.get('archivedAt'))
    if not saved:return True
    stamp=v.get('endedAt') or v.get('startedAt')
    return isinstance(stamp,dt.datetime) and now-stamp.astimezone(UTC)>=dt.timedelta(days=30)

def urls(v):
    result=media_urls(v)
    if isinstance(v.get('recordingUrl'),str) and v['recordingUrl'].strip():result.add(v['recordingUrl'])
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--limit',type=int,default=100);cfg=p.parse_args()
    if not 1<=cfg.limit<=500:p.error('limit1–500')
    import firebase_admin
    from firebase_admin import firestore
    firebase_admin.initialize_app();db=firestore.client();now=dt.datetime.now(UTC)
    candidates=[]
    for d in db.collection('live_streams').stream():
        if eligible(d.to_dict() or {},now):candidates.append(d)
        if len(candidates)>=cfg.limit:break
    print(f'Live history candidates={len(candidates)}; apply={cfg.apply}')
    if not cfg.apply:return
    # Media-free live records require no R2 credentials. Existing deployments do
    # not record video automatically; arbitrary cover URLs are never deleted.
    r2=None;origin=os.environ.get('NGELX_MEDIA_ORIGIN','').rstrip('/');bucket=os.environ.get('NGELX_R2_BUCKET','')
    def verify(raw,uid):
        nonlocal r2
        key=own_media_key(raw,uid)
        if not origin or urlparse(raw).netloc!=urlparse(origin).netloc or key is None:return None
        if r2 is None:
            import boto3
            if not all(os.environ.get(k) for k in ['NGELX_R2_ENDPOINT','NGELX_R2_ACCESS_KEY_ID','NGELX_R2_SECRET_ACCESS_KEY']):return None
            r2=boto3.client('s3',endpoint_url=os.environ['NGELX_R2_ENDPOINT'],aws_access_key_id=os.environ['NGELX_R2_ACCESS_KEY_ID'],aws_secret_access_key=os.environ['NGELX_R2_SECRET_ACCESS_KEY'],region_name='auto')
        try:meta=r2.head_object(Bucket=bucket,Key=key).get('Metadata',{})
        except r2.exceptions.ClientError as e:
            if e.response['Error']['Code'] in ('404','NoSuchKey','NotFound'):return key
            raise
        return key if meta.get('uid')==uid else None
    queued=skipped=cleaned=0
    for d in candidates:
        current=d.reference.get();v=current.to_dict() or {};uid=v.get('ownerId')
        if not eligible(v,dt.datetime.now(UTC)):continue
        media=urls(v)
        def shared(raw):
            for coll,fields in {'users':['photoUrl','coverUrl','introVideoUrl'],'videos':['mediaUrl','videoUrl','thumbnailUrl','posterUrl'],'live_streams':['mediaUrl','videoUrl','recordingUrl','thumbnailUrl','posterUrl','coverUrl']}.items():
                for field in fields:
                    if any(coll!='live_streams' or other.id!=d.id for other in db.collection(coll).where(field,'==',raw).limit(2).stream()):return True
            return False
        keys=[verify(raw,uid) for raw in media if not shared(raw)]
        if any(k is None for k in keys):skipped+=1;continue
        # A durable job atomically owns the exact unchanged record before deletion.
        job=db.collection('_live_cleanup_jobs').document(d.id)
        @firestore.transactional
        def claim(tx):
            fresh=d.reference.get(transaction=tx)
            if fresh.update_time!=current.update_time or not eligible(fresh.to_dict() or {},dt.datetime.now(UTC)):return False
            tx.set(job,{'sourcePath':d.reference.path,'ownerId':uid,'keys':keys,'createdAt':firestore.SERVER_TIMESTAMP})
            tx.delete(d.reference);return True
        if claim(db.transaction()):queued+=1
    def purge(ref):
        for c in ref.collections():
            for child in c.stream():purge(child.reference)
        ref.delete()
    for pending in db.collection('_live_cleanup_jobs').limit(cfg.limit).stream():
        v=pending.to_dict() or {};source=v.get('sourcePath','');uid=v.get('ownerId');keys=v.get('keys',[])
        if not source.startswith('live_streams/') or source.count('/')!=1 or not isinstance(keys,list):continue
        if any(own_media_key(origin+'/media/'+k,uid)!=k for k in keys):continue
        ref=db.document(source)
        if ref.get().exists:continue
        for k in keys:
            if verify(origin+'/media/'+k,uid)!=k:raise RuntimeError('Job media ownership cannot be verified')
            r2.delete_object(Bucket=bucket,Key=k)
        purge(ref);pending.reference.delete();cleaned+=1
    print(f'Live cleanup queued={queued}; cleaned={cleaned}; unverifiable skipped={skipped}')
if __name__=='__main__':main()
