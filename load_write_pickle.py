#!/usr/bin/python3

import argparse
import oewnio


def main():
    parser = argparse.ArgumentParser(description="load from yaml and write")
    parser.add_argument('repo', type=str, help='repository home')
    args = parser.parse_args()
    wn = oewnio.load(args.repo)
    oewnio.save_pickle(wn, args.repo)


if __name__ == '__main__':
    main()
