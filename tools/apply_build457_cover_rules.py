"""Build457 narrow legacy-founder cover fallback, emulator-only by default.

The normal communityValid450(v) rule requires founderId in admins. Legacy
documents missing that invariant cannot pass the normal update rule even
after adding a founder OR. Add an independent *cover-only* allow update.
Never bypass authentication, immutable fields, or field-type constraints.
"""
from pathlib import Path

SOURCE=Path('firestore.rules')
OLD="""        );
      allow delete: if false;
      match /requests/{uid} {"""

NEW="""        );
      // Build457 legacy founder cover-only repair (does NOT grant admin rights).
      // Normal validated updates already work for founders listed in admins.
      allow update: if communitySigned450()
        && request.auth.uid == resource.data.founderId
        && request.auth.uid in resource.data.members
        && !(request.auth.uid in resource.data.get('admins',[]))
        && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['coverUrl','coverAlignment'])
        && request.resource.data.coverUrl is string
        && request.resource.data.coverUrl.size() <= 2048
        && request.resource.data.get('coverAlignment',0) is number
        && request.resource.data.get('coverAlignment',0) >= -1
        && request.resource.data.get('coverAlignment',0) <= 1;
      allow delete: if false;
      match /requests/{uid} {"""

def transform(source):
    if '// Build457 legacy founder cover-only repair' in source:
        return source
    start=source.find("match /communities450/{cid} {")
    if start<0:
        raise ValueError("Build450 community match is missing")
    region=source[start:]
    if region.count(OLD)!=1:
        raise ValueError(f"Community root update boundary mismatched: {region.count(OLD)}")
    return source[:start]+region.replace(OLD,NEW,1)

def main():
    before=SOURCE.read_text()
    after=transform(before)
    if after!=before: SOURCE.write_text(after)
    print('Build457: narrow legacy-founder cover-only rule installed for emulator')

if __name__=='__main__':
    main()
