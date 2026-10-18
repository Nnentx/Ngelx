#!/usr/bin/env python3
"""Extract the exact pure Build485 kick/rejoin policy functions for unit testing.

The production build uses part-of main.dart after historical source generation.
Here we test its unchanged decision logic without pretending the ungenerated
QA repository main.dart already imports every production part.
"""
from pathlib import Path

SOURCE=Path("app/lib/build446_call_lifecycle.dart")
DEST=Path("app/lib/build485_kick_policy_test_api.dart")

def main():
    src=SOURCE.read_text(encoding="utf-8")
    start=src.index("int ngelx485KickEpoch(")
    end=src.index("class _Call446 {",start)
    code=src[start:end]
    for marker in ("int ngelx485KickEpoch(","bool ngelx485FreshKick(","Map<String,dynamic> ngelx485NextKickEpochs("):
        if code.count(marker)!=1:raise RuntimeError("Build485 logic absent or duplicated "+marker)
    DEST.write_text("// GENERATED TEST-ONLY. Extracted from production Build485 part.\n"+code,encoding="utf-8")
    print("Build495: extracted exact Build485 event counter and replay-safe kick policy")


if __name__=="__main__":main()
