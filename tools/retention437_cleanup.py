"""Approved retention, bounded pages, transaction rechecks, resumable media intents.

Preview by default. Never delete an R2 object here. Media is removed only by the
existing ownership/reference/ETag-checked cleanup worker; its completed state is
required before a message record can be purged. Drafts and live content survive.
"""
import argparse,datetime as dt,hashlib,json,itertools
UTC=dt.timezone.utc
FINISHED={'accepted','rejected','cancelled','superseded','withdrawn'}
MEDIA=('mediaUrl','videoUrl','audioUrl','fileUrl','thumbnailUrl','posterUrl','coverUrl','imageUrl')

def old(stamp,now,days):
    return isinstance(stamp,dt.datetime) and stamp.tzinfo is not None and now-stamp.astimezone(UTC)>=dt.timedelta(days=days)

def action(path,v,now):
    p=path.split('/')
    if any(v.get(k) for k in ('draft','isDraft','saved','highlighted','archivedAt')):return None
    if len(p)==4 and p[0]=='chats' and p[2]=='messages':
        if not old(v.get('createdAt'),now,14):return None
        manifest=v.get('cleanupMediaUrls')
        media=any(isinstance(v.get(k),str) and v[k].strip() for k in MEDIA) or (isinstance(manifest,list) and any(isinstance(x,str) and x.strip() for x in manifest))
        if v.get('deletedForEveryone') is True:
            if media and v.get('mediaCleanupState') not in ('done','shared-retained'):return 'wait-media'
            return 'delete'
        return 'queue-media' if media else 'delete'
    if len(p)==2 and p[0]=='notifications':
        if v.get('type') in ('follow_request','friend_request','group_join_request'):
            if v.get('status') not in FINISHED:return None
            return 'delete' if old(v.get('updatedAt') or v.get('answeredAt') or v.get('createdAt'),now,90) else None
        if v.get('read') is True and old(v.get('readAt') or v.get('createdAt'),now,30):return 'delete'
        if v.get('type') in ('interaction','like','comment') and isinstance(v.get('sourceId'),str) and v['sourceId'] and '/' not in v['sourceId'] and v.get('targetKind') in (None,'post','video','content'):return 'check-content'
        return None
    if len(p)==4 and p[0] in ('follow_requests','friend_requests') and p[2]=='outgoing':
        # Missing resolution timestamps are not guessed from the request's age.
        return 'delete' if v.get('status') in FINISHED and old(v.get('updatedAt') or v.get('answeredAt') or v.get('cancelledAt'),now,90) else None
    if len(p)==4 and p[0]=='users' and p[2]=='searchHistory':
        return 'delete' if old(v.get('createdAt'),now,30) else None
    return None

def pages(db,scope,limit,apply):
    """Advance each independent scope; old protected rows cannot starve later rows."""
    from firebase_admin import firestore
    from google.cloud.firestore_v1 import FieldPath
    state=db.collection('_retention437_cursors').document(hashlib.sha256(scope.encode()).hexdigest())
    cursor=(state.get().to_dict() or {}).get('lastPath')
    query=db.collection(scope).order_by(FieldPath.document_id()).limit(limit)
    if cursor:query=query.start_after({'__name__':db.document(cursor)})
    docs=list(query.stream(retry=None,timeout=20))
    return docs,state,limit

def run(db,now,apply,limit):
    from firebase_admin import firestore
    stats={'scanned':0,'deleted':0,'queued':0,'waiting':0,'changed':0,'preview':{}}
    def visit(snap):
        stats['scanned']+=1
        candidate=action(snap.reference.path,snap.to_dict() or {},now)
        if candidate is None:return
        stats['preview'][candidate]=stats['preview'].get(candidate,0)+1
        if not apply:return
        @firestore.transactional
        def mutate(tx):
            fresh=snap.reference.get(transaction=tx)
            if not fresh.exists or fresh.update_time!=snap.update_time:return 'changed'
            v=fresh.to_dict() or {};kind=action(fresh.reference.path,v,dt.datetime.now(UTC))
            if kind=='check-content':
                source=db.collection('videos').document(v['sourceId']).get(transaction=tx)
                sv=source.to_dict() or {}
                if source.exists and not any(sv.get(k) is True for k in ('deleted','isDeleted','removed')):return 'changed'
                kind='delete'
            parent=None;clear_preview=False
            if kind in ('delete','queue-media') and fresh.reference.path.startswith('chats/'):
                parent=fresh.reference.parent.parent
                chat=parent.get(transaction=tx)
                latest=list(tx.get(parent.collection('messages').order_by('createdAt',direction=firestore.Query.DESCENDING).limit(1)))
                clear_preview=bool(chat.exists and latest and old((latest[0].to_dict() or {}).get('createdAt'),dt.datetime.now(UTC),14))
            def clear():
                if clear_preview:
                    cv=chat.to_dict() or {}
                    tx.update(parent,{'lastMessage':'','lastMessageType':'','lastMessageClientAt':None,**{k:0 for k in cv if k.startswith('unread_')}})
            if kind=='delete':
                # Chat documents are kept: members, drafts and accepted requests survive.
                tx.delete(fresh.reference);clear();return 'deleted'
            if kind=='queue-media':
                owner=v.get('senderId')
                if not isinstance(owner,str) or not owner:return 'changed'
                tx.update(fresh.reference,{
                    'deletedForEveryone':True,'deletedBy':owner,'deletedAt':firestore.SERVER_TIMESTAMP,
                    'retentionExpired':True,'mediaCleanupState':'pending',
                    'cleanupMediaUrls':[v.get(k,'') for k in MEDIA],
                    'text':'','fileName':'','linkUrl':'','reactions':{},'pinned':False,
                    **{k:'' for k in MEDIA},
                });clear();return 'queued'
            return 'waiting'
        stats[mutate(db.transaction())]+=1
    # Each run has a fixed read bound. Cursors continue later on large databases.
    def scan(scope,count):
        docs,state,size=pages(db,scope,count,apply)
        for snap in docs:visit(snap)
        if apply:state.set({'scope':scope,'lastPath':docs[-1].reference.path if len(docs)==size else None,'updatedAt':firestore.SERVER_TIMESTAMP})
        return docs
    scan('notifications',limit)
    for chat in scan('chats',min(limit,20)):
        scan(chat.reference.path+'/messages',limit)
    for root in ('follow_requests','friend_requests'):
        # Parent request documents can be missing while outgoing children exist.
        # Consume a bounded page after the previous document name, including missing parents.
        cursor=db.collection('_retention437_cursors').document(root)
        previous=(cursor.get().to_dict() or {}).get('lastPath','') or ''
        parents=db.collection(root).list_documents(page_size=20,retry=None,timeout=20)
        chosen=list(itertools.islice((r for r in parents if r.path>previous),20))
        if not chosen:chosen=list(itertools.islice(db.collection(root).list_documents(page_size=20,retry=None,timeout=20),20))
        for parent in chosen:
            scan(parent.path+'/outgoing',limit)
        if apply:cursor.set({'lastPath':chosen[-1].path if len(chosen)==20 else ''})
    for user in scan('users',min(limit,20)):
        scan(user.reference.path+'/searchHistory',limit)
    return stats

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true');parser.add_argument('--limit',type=int,default=25)
    cfg=parser.parse_args()
    if not 1<=cfg.limit<=50:parser.error('limit must be 1–50')
    import firebase_admin
    from firebase_admin import firestore
    firebase_admin.initialize_app();db=firestore.client()
    print(json.dumps(run(db,dt.datetime.now(UTC),cfg.apply,cfg.limit),sort_keys=True))
if __name__=='__main__':main()
