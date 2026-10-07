#!/usr/bin/python3

import argparse
import sys
import unicodedata

from ascii import wellknown, is_ascii, is_ascii2, is_ascii3, is_ascii4


def main():
    for c in wellknown:
        print(f"{c} {is_ascii(c)}")
        print(f"{c} {is_ascii2(c)}")
        print(f"{c} {is_ascii3(c)}")
        print(f"{c} {is_ascii4(c)}")
        print()


if __name__ == '__main__':
    main()
