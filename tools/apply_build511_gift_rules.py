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
    if src.count(OLD)!=1:
        raise RuntimeError('Build511 rules expected one live_streams/comments match')
    return src.replace(OLD,NEW,1)
if __name__=='__main__':
    original=FILE.read_text(encoding='utf-8')
    transformed=transform(original)
    if original!=transformed:FILE.write_text(transformed,encoding='utf-8')
    print('Build511 virtual-gift immutable create rules added to staging QA')
