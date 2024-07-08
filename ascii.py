#!/usr/bin/python3

import argparse
import sys
import unicodedata

qd1 = "“"
qd2 = "”"
qs1 = "‘"
qs2 = "’"
aa = "`"
ag = "´"
ed = "—"
el = "…"

wellknown = (qs1, qs2, qd1, qd2, aa, ag, ed, el)


def code(char):
    return hex(ord(char))


def category(char):
    return unicodedata.category(char)


def is_ascii(char):
    return ord(char) <= 127


def is_ascii2(char):
    return char.isascii()


def is_ascii3(char):
    # Ll (Lowercase letter),
    # Lu (Uppercase letter),
    # Nd (Decimal number)
    # Po (Punctuation, other)
    return unicodedata.category(char) in ['Ll', 'Lu', 'Nd', 'Po']


def is_ascii4(char):
    """Checks if a character is ASCII (Python 2 compatible)."""
    try:
        char.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False


def process_line(line):
    count = 0
    for c in line:
        if not is_ascii(c) and c not in wellknown:
            # if c == ag:
            count += 1
            print(f"{c}\t{code(c)}\t{category(c)}\t{line}", file=sys.stderr)
    return count


def read_file(file):
    scanned = 0
    file_count = 0
    with open(file) as fp:
        for line in fp:
            file_count += process_line(line.strip())
            scanned += 1
    print(f"{file} {scanned} lines scanned, {file_count} not ascii")  # , file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="scans files")
    parser.add_argument('files', nargs='+', type=str, help='file')
    args = parser.parse_args()
    for f in args.files:
        read_file(f)


def main0():
    for c in (q1, q2, aa, ag):
        print(f"{c} {is_ascii(c)}")
        print(f"{c} {is_ascii2(c)}")
        print(f"{c} {is_ascii3(c)}")
        print(f"{c} {is_ascii4(c)}")
        print()


if __name__ == '__main__':
    main()
