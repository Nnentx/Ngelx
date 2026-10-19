#!/usr/bin/env python3
"""Include the Build534 QA helper after the existing Build527 generated part.

app/lib/main.dart is intentionally assembled by the historical Build4xx–527
pipeline and is empty in the GitHub source tree; this transform does not
pretend the generated Flutter application has already been compiled.
"""
from pathlib import Path
MAIN=Path('app/lib/main.dart')
PART="part 'build534_explicit_group_rejoin.dart';"
ANCHOR="part 'build527_group_join_transaction.dart';"

def transform(src: str) -> str:
    if PART in src:
        if src.count(PART)!=1:
            raise RuntimeError('Build534 helper declared multiple times')
        return src
    if src.count(ANCHOR)!=1:
        raise RuntimeError('Build534 needs an assembled Build527 Flutter source')
    return src.replace(ANCHOR,ANCHOR+'\n'+PART,1)

if __name__=='__main__':
    old=MAIN.read_text(encoding='utf-8')
    new=transform(old)
    if new!=old: MAIN.write_text(new,encoding='utf-8')
    print('Build534 assembled Flutter part linked (no production deployment)')
