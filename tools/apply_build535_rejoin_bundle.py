#!/usr/bin/env python3
"""Build535 staged integration entry after the Build527 Flutter source patch.

Run ONLY after the existing generated Flutter app has reached Build527+.
The Build534 part and Build535 actual call-screen preflight are then installed
idempotently as one unit. No APK build, Firebase deploy or code signing here.
"""
from pathlib import Path
import importlib.util

MAIN=Path('app/lib/main.dart')

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Unable to load {name}')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

build534=load('tools/apply_build534_explicit_rejoin.py','build534')
build535=load('tools/apply_build535_consented_group_rejoin.py','build535')

def transform(src):
    if "part 'build527_group_join_transaction.dart';" not in src:
        raise RuntimeError('Generate Build527 before applying Build535')
    src=build534.transform(src)
    return build535.transform(src)

if __name__=='__main__':
    src=MAIN.read_text(encoding='utf-8')
    transformed=transform(src)
    if transformed!=src:
        MAIN.write_text(transformed,encoding='utf-8')
    print('Build535: integrated Build534 part and token-before-consent guard into staged Flutter source')
