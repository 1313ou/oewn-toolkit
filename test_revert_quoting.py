#!/usr/bin/python3

import load_write_yaml

ss = [
    'blabla “Achilles＇ heel” blabla',
    'blabla “Achilles＇ heel” blabla',
    '“Achilles＇ heel”',
    '“＇”',
    '“”',
    '',
    ]

for s in ss:
    r = load_write_yaml.revert_to_grave_acute(s)
    print(s)
    print(r)
    print()