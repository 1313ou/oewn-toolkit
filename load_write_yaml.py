#!/usr/bin/python3

import argparse

import oewnio
import wordnet_yaml


def members(wn, synset):
    return [wn.id2entry[m].lemma.written_form for m in synset.members]


def save_data(wn, dstdir):
    synset_yaml = {}
    for synset in wn.synsets:
        s = {}
        if synset.ili and synset.ili != "in":
            s["ili"] = synset.ili
        s["partOfSpeech"] = synset.part_of_speech.value
        definitions = [wordnet_yaml.definition_to_yaml(wn, d) for d in synset.definitions]
        s["definition"] = definitions
        if synset.examples:
            examples = [wordnet_yaml.example_to_yaml(wn, x) for x in synset.examples]
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
        with wordnet_yaml.codecs.open("%s/src/yaml/%s.yaml" % (dstdir, key), "w", "utf-8") as outp:
            outp.write(wordnet_yaml.yaml.dump(synsets, default_flow_style=False, allow_unicode=True))


def main():
    parser = argparse.ArgumentParser(description="load from yaml and write")
    parser.add_argument('repo', type=str, help='repository home')
    args = parser.parse_args()

    wn = oewnio.load(args.repo)
    save_data(wn, args.repo)


if __name__ == '__main__':
    main()
