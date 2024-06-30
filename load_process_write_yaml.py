#!/usr/bin/python3

import argparse
import re
import sys
import oewnio
import wordnet

import wordnet_yaml


quotes2_open = '“'
quotes2_close = '”'
grave_accent = '`'
acute_accent = '´'
full_width_apostrophe = '＇'
apostrophe = "'"


def default_processing(s):
    return s


def revert_to_grave_acute(s):
    s = re.sub(quotes2_open, grave_accent, s)
    s = re.sub(quotes2_close, acute_accent, s)
    s = re.sub(full_width_apostrophe, apostrophe, s)
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
        s["partOfSpeech"] = synset.part_of_speech.value
        definitions = [wordnet_yaml.definition_to_yaml(wn, d) for d in synset.definitions]
        if process:
            definitions = [process_definition(d, processingf) for d in definitions]
        s["definition"] = definitions
        if synset.examples:
            examples = [wordnet_yaml.example_to_yaml(wn, x) for x in synset.examples]
            if process:
                examples = [process_example(x, processingf) for x in examples]
            s["example"] = examples
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
        # BUG : these do not order preserving
        # s["members"] = entries_ordered(wn, synset.id)
        # s["members"] = wn.members_by_id(synset.id)
    for key, synsets in synset_yaml.items():
        with wordnet_yaml.codecs.open("%s/src/yaml/%s.yaml" % (dstdir, key), "w", "utf-8") as os:
            os.write(wordnet_yaml.yaml.dump(synsets, default_flow_style=False, allow_unicode=True))


def get_processing(name):
    return globals()[name] if name else default_processing


def main():
    parser = argparse.ArgumentParser(description="load from yaml and write")
    parser.add_argument('repo', type=str, help='repository home')
    parser.add_argument('--processing', type=str, help='processing function to apply')
    args = parser.parse_args()
    processingf = get_processing(args.processing)
    if processingf:
        print(processingf, file=sys.stderr)

    wn = oewnio.load(args.repo)
    save_data(wn, args.repo, processingf)


if __name__ == '__main__':
    main()
