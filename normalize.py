#!/usr/bin/python3

import argparse

from glob import glob
import yaml


def normalize(repo):
    for f in glob(f"{repo}/src/yaml/*.yaml"):
        data = yaml.load(open(f), Loader=yaml.CLoader)
        with open(f, "w") as out:
            out.write(yaml.dump(data, default_flow_style=False, allow_unicode=True))


def main():
    parser = argparse.ArgumentParser(description="load from yaml and write")
    parser.add_argument('repo', type=str, help='repository home')
    args = parser.parse_args()
    normalize(args.repo)


if __name__ == '__main__':
    main()
