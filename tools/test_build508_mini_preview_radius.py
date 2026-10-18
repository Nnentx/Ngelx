#!/usr/bin/env python3
"""Before the Build469 mini-preview transform, verify both UI generations."""
import importlib.util
from pathlib import Path
import re

spec = importlib.util.spec_from_file_location(
    'build469_mini', 'tools/apply_build469_live_mini_call.py'
)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
source = Path('app/lib/build445_inbox_model.dart').read_text(encoding='utf-8')
assert mod.TAG not in source, 'Preflight must run before Build469 patch'
start = source.index(mod.START)
stop = source.index(mod.END, start)
overlay = source[start:stop]
pattern = re.compile(
    r'CircleAvatar\(radius:(?:20|28),[^\n]*?detail\.video\?Icons\.videocam:Icons\.call[^\n]*?\),'
)
anchors = pattern.findall(overlay)
assert len(anchors) == 1, f'Unexpected Build445 mini avatar anchor count: {len(anchors)}'
anchor = anchors[0]
for radius in (20, 28):
    variant = re.sub(r'radius:(?:20|28)', f'radius:{radius}', anchor, count=1)
    fixture = source.replace(anchor, variant, 1)
    transformed = mod.transform(fixture)
    assert mod.TAG in transformed
    assert f'else CircleAvatar(radius:{radius},' in transformed
    assert 'if(detail.video)_ngelx469Preview(room,detail.photo)' in transformed
    assert 'onEnd:()=>ngelx445EndBackground(name)' in transformed
    assert 'FirebaseAuth.instance.currentUser?.uid!=detail.uid' in transformed
    assert mod.transform(transformed) == transformed, 'Patch must be idempotent'
print('Build508 preflight PASS: Build469 video preview supports radius 20/28 and preserves call guards')
