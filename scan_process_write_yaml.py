#!/usr/bin/python3

import argparse
import sys
from oewn_core import wordnet
from oewn_core.wordnet_toyaml import save_synsets

from scan_yaml import load


def default_processing(s):
    return s


process = False


def process_definition(definition, processingf):
    return processingf(definition)


def process_example(example, processingf):
    if isinstance(example, str):
        example = processingf(example)
    elif isinstance(example, wordnet.Example):
        example.text = processingf(example.text)
    return example


def process_synsets(wn, dstdir, processingf):
    for synset in wn.synsets:

        definitions = synset.definitions
        if process:
            definitions = [process_definition(d, processingf) for d in definitions]
        synset.definitions = definitions

        if synset.examples:
            examples = synset.examples
            if process:
                examples = [process_example(x, processingf) for x in examples]
            synset.examples = examples

        if synset.usages:
            usages = synset.usages
            if process:
                usages = [process_example(x, processingf) for x in usages]
            synset.usages = usages


def get_processing(name):
    return globals()[name] if name else default_processing


def main():
    parser = argparse.ArgumentParser(description="load from yaml and write")
    parser.add_argument('repo', type=str, help='from-repository home')
    parser.add_argument('repo2', type=str, help='to-repository home')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    processingf = get_processing(args.processing)
    if processingf:
        print(processingf, file=sys.stderr)

    print(f"Loading from {args.repo}")
    wn = load(args.repo)
    print(f"Loaded from {args.repo}")

    process_synsets(wn, processingf)

    print(f"Saving to {args.repo2}")
    save_synsets(wn, args.repo2)
    print(f"Saved to {args.repo2}")


if __name__ == '__main__':
    main()
