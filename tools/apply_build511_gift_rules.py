#!/usr/bin/env python3
"""Staging-only Firestore gift create validation; run after older rules patches."""
from pathlib import Path
FILE=Path('firestore.rules')
MARK='// Build511 QA: bounded immutable virtual gifts, no coin charge'
OLD="""      match /comments/{commentId} {
        allow read: if true;
        allow create: if signedIn() && request.resource.data.userId == request.auth.uid;
        allow update, delete: if signedIn() && (resource.data.userId == request.auth.uid || resource.data.uid == request.auth.uid);
      }
"""
NEW="""      match /comments/{commentId} {
        // Build511 QA: bounded immutable virtual gifts, no coin charge.
        function validVirtualGift511() {
          let g = request.resource.data;
          let qty = g.get('quantity', 0);
          let points = g.get('points', -1);
          let name = g.get('giftName', '');
          return g.keys().hasOnly([
              'uid', 'userId', 'username', 'text', 'kind', 'giftName',
              'giftEmoji', 'quantity', 'points', 'createdAt'
            ])
            && g.get('kind', '') == 'gift'
            && g.get('uid', '') == request.auth.uid
            && g.get('userId', '') == request.auth.uid
            && g.get('username', '') is string
            && g.get('text', '') is string
            && g.get('giftEmoji', '') is string
            && g.get('createdAt', null) == request.time
            && get(/databases/$(database)/documents/live_streams/$(streamId)).data.get('active', false) == true
            && qty is int && qty >= 1 && qty <= 10
            && points is int
            && (
              (name == 'Gül' && points == qty * 1)
              || (name == 'Kalp' && points == qty * 3)
              || (name == 'Yıldız' && points == qty * 5)
              || (name == 'Elmas' && points == qty * 15)
              || (name == 'Kalp Taşı' && points == qty * 15)
              || (name == 'Ayıcık' && points == qty * 25)
              || (name == 'Taç' && points == qty * 25)
              || (name == 'NgelX Roket' && points == qty * 50)
              || (name == 'Galaksi' && points == qty * 100)
            );
        }
        allow read: if true;
        allow create: if signedIn()
          && request.resource.data.userId == request.auth.uid
          && (request.resource.data.get('kind', 'comment') != 'gift'
              || validVirtualGift511());
        // Gifts are append-only; recreating/update/deleting an old gift cannot
        // double count or rewrite a virtual points total.
        allow update: if signedIn()
          && resource.data.get('kind', '') != 'gift'
          && request.resource.data.get('kind', '') != 'gift'
          && (resource.data.userId == request.auth.uid
              || resource.data.uid == request.auth.uid);
        allow delete: if signedIn()
          && resource.data.get('kind', '') != 'gift'
          && (resource.data.userId == request.auth.uid
              || resource.data.uid == request.auth.uid);
      }
"""
def transform(src):
    if MARK in src:return src
    # Transform only the existing live-stream comment rule. Preserve all
    # earlier read/create/moderation rules and AND safety requirements onto
    # each write permission rather than replacing the authorization logic.
    import re
    root=src.find('    match /live_streams/{streamId} {')
    if root<0:raise RuntimeError('Build511 live stream rules missing')
    start=src.find('      match /comments/{commentId} {',root)
    stop=src.find('      match /reactions/{uid} {',start)
    if start<0 or stop<0 or stop<=start:
        raise RuntimeError('Build511 cannot bound exact live comments rule')
    existing=src[start:stop]
    if existing.count('match /')!=1 or 'allow write:' in existing:
        raise RuntimeError('Build511 refuse unknown nested/broad live comment rule')
    if existing.count('allow read: if true;')!=1:
        raise RuntimeError('Build511 unexpected live comment read policy')
    # Require existing identity guard before adding gift validation.
    if existing.count('request.resource.data.userId == request.auth.uid')<1:
        raise RuntimeError('Build511 live comment owner/create guard missing')
    declaration='      match /comments/{commentId} {'
    prefix=NEW[NEW.index(declaration)+len(declaration):NEW.index('        allow read: if true;')]
    position=existing.index(declaration)+len(declaration)
    existing=existing[:position]+prefix+existing[position:]
    pattern=re.compile(r'(?m)^([ \t]*)allow[ \t]+(create|update,[ \t]*delete|update|delete):[ \t]*if[ \t]*(.*?);',re.DOTALL)
    found=[]
    def protect(m):
        indent,action,auth=m.group(1),m.group(2).replace(' ',''),m.group(3).strip()
        found.append(action)
        # Parenthesize original authorization: no existing permission is
        # weakened, including any earlier added host/moderation checks.
        if action=='create':
            return (indent+"allow create: if ("+auth+")"
              + " && (request.resource.data.get('kind', 'comment') != 'gift'"
              + " || validVirtualGift511());")
        old="resource.data.get('kind', '') != 'gift'"
        incoming="request.resource.data.get('kind', '') != 'gift'"
        if action=='update':
            return indent+"allow update: if ("+auth+") && "+old+" && "+incoming+";"
        if action=='delete':
            return indent+"allow delete: if ("+auth+") && "+old+";"
        if action=='update,delete':
            return (indent+"allow update: if ("+auth+") && "+old+" && "+incoming+";\n"
              +indent+"allow delete: if ("+auth+") && "+old+";")
        raise RuntimeError('Build511 unexpected permission '+action)
    transformed=pattern.sub(protect,existing)
    if found.count('create')!=1 or not any('update' in v for v in found):
        raise RuntimeError('Build511 missing unique create or prior update permission: '+str(found))
    if transformed.count('|| validVirtualGift511()')!=1:
        raise RuntimeError('Build511 gift validation insertion failed')
    return src[:start]+transformed+src[stop:]
if __name__=='__main__':
    original=FILE.read_text(encoding='utf-8')
    transformed=transform(original)
    if original!=transformed:FILE.write_text(transformed,encoding='utf-8')
    print('Build511 virtual-gift immutable create rules added to staging QA')
