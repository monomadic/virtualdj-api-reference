#!/usr/bin/env python3
"""Query skin class translation-unit provenance from unstripped b9246 STABS.

Reuses the action-module parser, preserving multiple defining modules rather
than assuming a partition. Tier 2 structural leads only; no behavior claims.
Regenerate with --app PATH > tests/skin-modules-9246.json.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import plistlib
import re

from extract_action_modules import STAB, class_module_sets, stabs

ARTIFACT = Path('tests/skin-modules-9246.json')


def build_artifact(app: Path) -> dict:
    binary = app / 'Contents/MacOS/VirtualDJ'
    dump = stabs(binary)
    classes = {k: sorted(v) for k, v in sorted(class_module_sets(dump, 'CSkin').items())}
    if not classes:
        raise SystemExit('No CSkin STABS methods found; use the unstripped b9246 app')
    skin_objects = sorted({os.path.basename(m.group(2)) for line in dump.splitlines()
                           if (m := STAB.search(line)) and m.group(1) == 'N_OSO'
                           and os.path.basename(m.group(2)).startswith('Skin')})
    modules = {obj: sorted(c for c, objects in classes.items() if obj in objects)
               for obj in sorted(set(skin_objects) | {o for objects in classes.values() for o in objects})}
    split = {c: objects for c, objects in classes.items() if len(objects) > 1}
    build = plistlib.loads((app / 'Contents/Info.plist').read_bytes())['CFBundleVersion']
    return {
        'summary': {
            'build': build,
            'architectures_in_dsymutil_dump': sorted(set(re.findall(r"Symbol table for: .* \(([^)]+)\)", dump))),
            'binary_sha256': hashlib.sha256(binary.read_bytes()).hexdigest(),
            'classes': len(classes), 'modules': len(modules),
            'skin_prefix_object_files': len(skin_objects),
            'classes_in_multiple_modules': len(split),
            'evidence_tier': 2,
        },
        'method': 'N_OSO object-file basename and subsequent N_FUN Itanium class name, using extract_action_modules.class_module_sets with prefix CSkin. Architecture slices are unioned; repeated definitions are deduplicated.',
        'limits': [
            'This is a many-to-many relation, not a partition: methods of a class can originate in multiple translation units.',
            'Skin*.o is case-sensitive; the class map also includes matching methods from other object files, including skinEqualizer.o.',
            'Only class-prefixed N_FUN records are attributed. Missing classes or empty modules do not establish absence of implementation.',
            'The reused parser matches _ZN followed directly by a class-name length; const-qualified _ZNK and other mangling forms are outside its traversal.',
            'Historical source provenance does not establish current-build vocabulary or runtime behavior. Test a controlled live skin fixture with independent visual or state readback to establish behavior.',
        ],
        'skin_prefix_object_files': skin_objects,
        'skin_objects_without_cskin_methods': [o for o in skin_objects if not modules[o]],
        'classes_in_multiple_modules': split,
        'classes': classes,
        'modules': modules,
    }


def check(data: dict) -> None:
    classes, modules, summary = data['classes'], data['modules'], data['summary']
    assert classes and summary['build'] and summary['binary_sha256']
    assert summary['classes'] == len(classes)
    assert summary['modules'] == len(modules)
    assert summary['skin_prefix_object_files'] == len(data['skin_prefix_object_files'])
    assert data['classes_in_multiple_modules'] == {c: ms for c, ms in classes.items() if len(ms) > 1}
    assert summary['classes_in_multiple_modules'] == len(data['classes_in_multiple_modules'])
    for cls, objects in classes.items():
        assert cls.startswith('CSkin') and objects == sorted(set(objects))
        assert objects == sorted(m for m, cs in modules.items() if cls in cs)
    for obj, members in modules.items():
        assert members == sorted(c for c, objects in classes.items() if obj in objects)
    assert data['skin_objects_without_cskin_methods'] == [o for o in data['skin_prefix_object_files'] if not modules[o]]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--app', type=Path)
    p.add_argument('--get', help='CSkin class name')
    p.add_argument('--module', help='Object-file name, with optional .o')
    p.add_argument('--check', action='store_true')
    args = p.parse_args()
    data = build_artifact(args.app) if args.app else json.loads(ARTIFACT.read_text())
    check(data)
    if args.check:
        print(f"skin modules check passed on build {data['summary']['build']}")
        return 0
    if args.get:
        result = {'build': data['summary']['build'], 'evidence_tier': 2, 'class': args.get,
                  'modules': data['classes'].get(args.get)}
    elif args.module:
        obj = args.module if args.module.endswith('.o') else args.module + '.o'
        result = {'build': data['summary']['build'], 'evidence_tier': 2, 'module': obj,
                  'classes': data['modules'].get(obj)}
    else:
        result = data if args.app else data['summary']
    print(json.dumps(result, indent=1))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
