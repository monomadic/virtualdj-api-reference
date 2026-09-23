#!/usr/bin/env python3
"""Compare condition gates with the visibility fixture's literal controls."""
from pathlib import Path
import runpy

HERE = Path(__file__).resolve().parent
data = runpy.run_path(str(HERE.parent / 'attribute-validity-probe/probe.py'))
runner = data['runner']
base_fixture = data['fixture']
runner.HERE = HERE
runner.NAME = 'ZZ Condition Validity 9644'
runner.INSTALL = Path.home() / 'Library/Application Support/VirtualDJ/Skins' / runner.NAME
runner.STATE = Path('/tmp/vdj-condition-validity-state.json')
runner.JOURNAL = HERE / 'run-9644.jsonl'


def fixture(round_number):
    return base_fixture(round_number).replace(b'ATTRIBUTE CANARY', b'CONDITION CANARY').replace(b'visibility', b'condition')


runner.fixture = fixture
if __name__ == '__main__':
    runner.main()
