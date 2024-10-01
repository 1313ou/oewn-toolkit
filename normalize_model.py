#!/usr/bin/python3

import argparse
import oewnio


def normalize(repo):
    wn = oewnio.load(repo)
    oewnio.save(wn, repo)


def main():
    parser = argparse.ArgumentParser(description="load from yaml and write")
    parser.add_argument('repo', type=str, help='repository home')
    args = parser.parse_args()
    normalize(args.repo)


if __name__ == '__main__':
    main()
