#!/usr/bin/env python3
"""Build484: post-patch legacy founder client authorization repair.

Runs AFTER Build456/Build481 generated source transforms. It intentionally
does not touch the pre-Build456 input or production security rules.
"""
from pathlib import Path

FILE = Path("app/lib/community450.dart")
MARK = "// Build484: legacy communities can have a verified founder"
OLD = """bool _communityAdmin450(Map<String, dynamic> v) =>
    _communityUid450.isNotEmpty &&
    (v['founderId'] == _communityUid450 ||
        List<String>.from(v['admins'] ?? []).contains(_communityUid450));"""
NEW = """// Build484: legacy communities can have a verified founder who is not in
// admins. The shared helper also requires verified community membership.
bool _communityAdmin450(Map<String, dynamic> v) =>
    ngelx484CommunityManager(v, _communityUid450);"""

def transform(src: str) -> str:
    if MARK in src:
        if "ngelx484CommunityManager(v, _communityUid450)" not in src:
            raise RuntimeError("Build484 marker present without role guard")
        return src
    if src.count(OLD) != 1:
        raise RuntimeError("Unexpected existing community manager helper; do not overwrite")
    return src.replace(OLD, NEW, 1)

def main():
    original = FILE.read_text(encoding="utf-8")
    updated = transform(original)
    if updated != original:
        FILE.write_text(updated, encoding="utf-8")
    if transform(updated) != updated:
        raise RuntimeError("Build484 transform must be idempotent")
    print("Build484 legacy founder client permissions patched; no Firebase deploy")

if __name__ == "__main__":
    main()
