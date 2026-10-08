#!/usr/bin/python3

import argparse
import os
from oewn_core import wordnet_fromyaml
from oewn_core.wordnet import Example

import process
from process import *

processing_result = False


def process_text(input_text, rowid, processingf):
    r = processingf(input_text)
    if r:
        if processing_result:
            print(f"{rowid}\t{input_text}\t{r}")
        else:
            print(f"{rowid}\t{input_text}")
        return 1
    return 0


def load(repo):
    current_dir = os.getcwd()
    os.chdir(repo)
    wn = wordnet_fromyaml.load('.')
    os.chdir(current_dir)
    return wn


def get_processing(name):
    return globals()[name] if name else process.default_process


def main():
    parser = argparse.ArgumentParser(description="load from yaml")
    parser.add_argument('repo', type=str, help='repository home')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    processing = get_processing(args.processing)
    print(processing, file=sys.stderr)

    wn = load(args.repo)
    print('loaded', file=sys.stderr)

    for synset in wn.synsets:
        for definition in synset.definitions:
            process_text(definition, f"{synset.id}\tdef", processing)
        for example in synset.examples:
            e = example.text if example is Example else example
            process_text(e, f"{synset.id}\tsam", processing)
    print('processed', file=sys.stderr)


if __name__ == '__main__':
    main()
