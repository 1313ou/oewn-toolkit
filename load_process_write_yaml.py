#!/usr/bin/python3

import argparse
import re
import sys
from oewn_core import wordnet
from oewn_core import wordnet_toyaml

from load_yaml import load


def default_processing(s):
    return s


process = False


def process_definition(definition, processingf):
    if isinstance(definition, str):
        definition = processingf(definition)
    elif isinstance(definition, wordnet.Definition):
        definition.text = processingf(definition.text)
    return definition


def process_example(example, processingf):
    if isinstance(example, str):
        example = processingf(example)
    elif isinstance(example, wordnet.Example):
        example.text = processingf(example.text)
    return example


def members(wn, synset):
    return [wn.id2entry[m].lemma.written_form for m in synset.members]


def save_data(wn, dstdir, processingf):
    synset_yaml = {}
    for synset in wn.synsets:
        s = {}
        if synset.ili and synset.ili != "in":
            s["ili"] = synset.ili
        s["partOfSpeech"] = synset.pos.value
        definitions = [wordnet_yaml.definition_to_yaml(wn, d) for d in synset.definitions]
        if process:
            definitions = [process_definition(d, processingf) for d in definitions]
        s["definition"] = definitions
        if synset.examples:
            examples = [wordnet_yaml.example_to_yaml(wn, x) for x in synset.examples]
            if process:
                examples = [process_example(x, processingf) for x in examples]
            s["example"] = examples
        if synset.usages:
            usages = [wordnet_yaml.usage_to_yaml(wn, x) for x in synset.usages]
            if process:
                usages = [process_example(x, processingf) for x in usages]
            s["usages"] = usages
        if synset.source:
            s["source"] = synset.source
        if synset.wikidata:
            s["wikidata"] = synset.wikidata
        for r in synset.synset_relations:
            if r.rel_type not in wordnet_yaml.ignored_symmetric_synset_rels:
                if r.rel_type.value not in s:
                    s[r.rel_type.value] = [r.target[wordnet_yaml.KEY_PREFIX_LEN:]]
                else:
                    s[r.rel_type.value].append(r.target[wordnet_yaml.KEY_PREFIX_LEN:])
        if synset.lex_name not in synset_yaml:
            synset_yaml[synset.lex_name] = {}
        synset_yaml[synset.lex_name][synset.id[wordnet_yaml.KEY_PREFIX_LEN:]] = s
        s["members"] = members(wn, synset)
        # BUG : these do not preserve order
        # s["members"] = entries_ordered(wn, synset.id)
        # s["members"] = wn.members_by_id(synset.id)


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

    print(f"Saving to {args.repo2}")
    save(wn, args.repo2)
    print(f"Saved to {args.repo2}")


if __name__ == '__main__':
    main()
