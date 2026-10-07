#!/usr/bin/python3

from process import revert_to_grave_acute

ss = [
    'blabla “Achilles＇ heel” blabla',
    'blabla “Achilles＇ heel” blabla',
    '“Achilles＇ heel”',
    '“＇”',
    '“”',
    '',
    ]

for s in ss:
    r = revert_to_grave_acute(s)
    print(s)
    print(r)
    print()