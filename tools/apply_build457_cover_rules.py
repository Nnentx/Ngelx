"""Build457 emulator-only founder cover access fix.

Apply AFTER Build456 patch, before Firestore rules emulator tests. This
does not deploy production rules or modify user/community documents.
"""
from pathlib import Path
SOURCE=Path('firestore.rules')

OLD="""          (request.auth.uid in resource.data.admins
            && (request.resource.data.admins == resource.data.admins || request.auth.uid == resource.data.founderId))
"""
NEW=OLD+"""          || (request.auth.uid == resource.data.founderId
            && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['coverUrl','coverAlignment']))
"""

def transform(source):
    if "founderId\n            && request.resource.data.diff(resource.data).affectedKeys().hasOnly(['coverUrl','coverAlignment'])" in source:
        return source
    if source.count(OLD)!=1:
        raise ValueError('Build457 founder cover rule anchor missing or duplicated')
    return source.replace(OLD,NEW,1)

def main():
    before=SOURCE.read_text()
    after=transform(before)
    if after!=before: SOURCE.write_text(after)
    print('Build457: legacy founder cover-only update permission guarded (emulator source)')

if __name__=='__main__':
    main()
