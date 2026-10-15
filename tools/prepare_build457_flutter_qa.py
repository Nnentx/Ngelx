#!/usr/bin/env python3
"""Reconstruct the Build457 Flutter source tree in a disposable QA checkout.

This script replays *only* local source-generation scripts and local git
patches listed in the existing Build457 release workflow, in the same order.
It never executes deploy steps, cloud API calls, data migrations, or cleanup.
"""
from pathlib import Path
import os
import re
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
# Build456 applies large diffs to generated community files. For UI-only
# compilation, replay from an untouched release baseline; the hardened
# Firestore rules are tested separately in the emulator job. No deployment.
if os.environ.get("NGELX_QA_BASELINE_COMMUNITY") == "1":
    subprocess.run(
        ["git","fetch","--depth=1","origin","work/build-457-device-recovery"],
        cwd=root,check=True,timeout=60,
    )
    for relative in ("app/lib/community450.dart","firestore.rules"):
        data=subprocess.check_output(["git","show",f"FETCH_HEAD:{relative}"],cwd=root)
        (root/relative).write_bytes(data)
    print("QA: restored untouched Build457 community inputs; UI parts remain under test.",flush=True)

workflow=root/".github/workflows/NgelX-BUILD457-CONSOLIDATED.yml"
content=workflow.read_text(encoding="utf-8")
prefix=content.split("      - name: Test Build457 inbox nickname",1)[0]
commands=[]
for line in prefix.splitlines():
    line=line.strip()
    if line.startswith("run: "):
        line=line[5:]
    script=re.fullmatch(r"python3(?: -u)? (tools/apply_build[0-9][A-Za-z0-9_]*\.py)",line)
    patch=re.fullmatch(r"git apply (tools/build(?:447|448|454|456)\.patch)",line)
    if script:
        commands.append([sys.executable,script.group(1)])
    elif patch:
        commands.append(["git","apply",patch.group(1)])

assert len(commands)>=70, f"Unexpected release source generation count: {len(commands)}"
assert sum(cmd[0]=="git" for cmd in commands)==4, "Expected four local patch application steps"
assert commands[0][1].endswith("apply_build395_final_login_inbox_ui.py")
assert commands[-1][1].endswith("apply_build457_inbox_rows.py")
for index,cmd in enumerate(commands,1):
    print(f"[QA {index}/{len(commands)}] {' '.join(cmd)}",flush=True)
    subprocess.run(cmd,cwd=root,check=True,timeout=180)

main=(root/"app/lib/main.dart").read_text(encoding="utf-8")
required=[
    "part 'community450.dart';",
    "part 'build445_inbox_model.dart';",
    "part 'build455_widgets.dart';",
    "part 'build456_widgets.dart';",
]
missing=[entry for entry in required if entry not in main]
assert not missing, f"Build457 source parts not linked: {missing}"
print("Build457 Flutter QA preparation finished without deploying anything.")
