#!/usr/bin/env python3
"""Build469 emulator-only rules for legacy founders, strict field-diff bounds.
Review before production rules deployment. Never edit live community records.
"""
from pathlib import Path
RULES=Path('firestore.rules')
TAG='// Build469: legacy verified founder limited-settings compatibility'
def one(s,old,new,label):
    if s.count(old)!=1:raise RuntimeError(f'Build469 community {label}: expected one, got {s.count(old)}')
    return s.replace(old,new,1)
def transform(s):
    if TAG in s:return s
    s=one(s,
      "function communityAdmin450(cid) { return communitySigned450() && request.auth.uid in community450(cid).admins; }",
      """function communityAdmin450(cid) {
      return communitySigned450() &&
        (request.auth.uid == community450(cid).get('founderId', '')
          || request.auth.uid in community450(cid).get('admins', []));
    }""",'founder authorization helper')
    old="""function communityModerator456(cid) { return communitySigned450() &&
      (request.auth.uid in community450(cid).admins || request.auth.uid in community450(cid).get('moderators',[])); }"""
    new="""function communityModerator456(cid) { return communitySigned450() &&
      (request.auth.uid == community450(cid).get('founderId', '')
        || request.auth.uid in community450(cid).get('admins',[])
        || request.auth.uid in community450(cid).get('moderators',[])); }"""
    s=one(s,old,new,'moderation helper')
    start=s.index('    match /communities450/{cid} {')
    end=s.index('      match /requests/{uid} {',start)
    part=s[start:end]
    existing="""      allow delete: if false;"""
    new="""      // Build469: legacy verified founder limited-settings compatibility.
      // Old communities may be missing the founder from the admins list;
      // the old communityValid450 invariant blocks every normal update.
      // This branch may ONLY change bounded, owner-controlled settings.
      allow update: if communitySigned450()
        && resource.data.get('founderId','') == request.auth.uid
        && request.auth.uid in resource.data.get('members',[])
        && request.resource.data.diff(resource.data).affectedKeys().hasOnly([
          'visibility','joinApproval','postApproval','paused',
          'name','description','rules'
        ])
        && request.resource.data.get('visibility','public') in ['public','private']
        && request.resource.data.get('joinApproval',false) is bool
        && request.resource.data.get('postApproval',false) is bool
        && request.resource.data.get('paused',false) is bool
        && request.resource.data.get('name','') is string
        && request.resource.data.get('name','').size() >= 3
        && request.resource.data.get('name','').size() <= 60
        && request.resource.data.get('description','') is string
        && request.resource.data.get('description','').size() <= 240
        && request.resource.data.get('rules','') is string
        && request.resource.data.get('rules','').size() <= 2000;
      allow delete: if false;"""
    part=one(part,existing,new,'founder settings override with zero delete')
    s=s[:start]+part+s[end:]
    if 'allow delete: if false;' not in part or 'hasOnly' not in part:
      raise RuntimeError('refuse unbounded community rights')
    return s
if __name__=='__main__':
    before=RULES.read_text(encoding='utf-8')
    after=transform(before)
    if before!=after:RULES.write_text(after,encoding='utf-8')
    print('Build469: founder-only bounded settings in GENERATED QA rules; NO PRODUCTION DEPLOY')
