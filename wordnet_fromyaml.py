"""WordNet YAML interface"""

from glob import glob

import yaml

from wordnet import *


def load_verbframes(home):
    with open(f'{home}/frames.yaml', encoding="utf-8") as inp:
        frames = yaml.load(inp, Loader=yaml.CLoader)
        return [SyntacticBehaviour(k, v) for k, v in frames.items()]


def load_entries(home):
    entry_resolver = {}
    sense_resolver = {}
    entries = []
    for f in glob(f'{home}/entries-*.yaml'):
        with open(f, encoding="utf-8") as inp:
            y = yaml.load(inp, Loader=yaml.CLoader)
            for lemma, poses_discriminants in y.items():
                for pos_discriminant, props in poses_discriminants.items():
                    pos = pos_discriminant[:1]
                    discriminant = pos_discriminant[1:]
                    entry = LexicalEntry(lemma, pos, discriminant)
                    if "form" in props:
                        entry.form = props['form']
                    if "pronunciation" in props:
                        entry.pronunciation = [Pronunciation(p["value"], p.get("variety")) for p in
                                               props["pronunciation"]]
                    for n, sense_props in enumerate(props["sense"]):
                        sense = load_sense(sense_props, entry, n)
                        entry.senses.append(sense)
                        sense_resolver[sense.id] = sense
                    entries.append(entry)
                    entry_resolver[(lemma, pos, discriminant)] = entry
    return entries, entry_resolver, sense_resolver


def load_synsets(home):
    resolver = {}
    synsets = []
    noun_files = glob(f'{home}/noun*.yaml')
    verb_files = glob(f'{home}/verb*.yaml')
    adj_files = glob(f'{home}/adj*.yaml')
    adv_files = glob(f'{home}/adv*.yaml')
    for f in noun_files + verb_files + adj_files + adv_files:
        lex_name = f[9:-5]
        with open(f, encoding="utf-8") as inp:
            y = yaml.load(inp, Loader=yaml.CLoader)
            for synsetid, props in y.items():
                synset = load_synset(props, synsetid, lex_name)
                synsets.append(synset)
                resolver[synsetid] = synset
    return synsets, resolver


def load_sense(props, entry, n):
    s = Sense(props["id"], entry, props["synset"], n, props.get("adjposition"))
    if "sent" in props:
        s.sent = props["sent"]
    if "subcat" in props:
        s.subcat = props["subcat"]
    # relations
    for rel, targets in props.items():
        if rel in SenseRelType._value2member_map_:
            for target in targets:
                s.add_sense_relation(SenseRelation(target, SenseRelType(rel)))
        if rel in OtherSenseRelType._value2member_map_:
            for target in targets:
                s.add_sense_relation(SenseRelation(target, SenseRelType.OTHER, rel))
    return s


def load_synset(props, synsetid, lex_name):
    ss = Synset(synsetid,
                props["members"],
                props["partOfSpeech"],
                lex_name)
    for defn in props["definition"]:
        ss.add_definition(Definition(defn))
    for example in props.get("example", []):
        if isinstance(example, str):
            ss.add_example(Example(example))
        else:
            ss.add_example(Example(example["text"], example["source"]))
    for usage in props.get("usage", []):
        ss.add_usage(Usage(usage))
    ss.source = props.get("source"),
    ss.wikidata = props.get("wikidata")
    ss.ili = props.get("ili", "in")
    # relations
    for rel, targets in props.items():
        if rel in SynsetRelType._value2member_map_:
            for target in targets:
                ss.add_synset_relation(SynsetRelation(target, SynsetRelType(rel)))
    return ss


def resolve_synset_members(wn, ss):
    ss.resolved_members = [wn.synset_resolver[(l, ss.pos)] for l in ss.members]


def load(home):
    wn = Lexicon("oewn", "English WordNet", "en",
                 "english-wordnet@googlegroups.com",
                 "https://creativecommons.org/licenses/by/4.0",
                 "2024",
                 "https://github.com/globalwordnet/english-wordnet")
    # frames
    wn.frames = load_verbframes(home)

    # lex entries
    wn.entries, wn.entry_resolver, wn.sense_resolver = load_entries(home)

    # synsets
    wn.synsets, wn.synset_resolver = load_synsets(home)

    # resolve synset reference in sense
    for e in wn.entries:
        for s in e.senses:
            s.resolved_synset = wn.synset_resolver[s.synsetid]
    return wn


def main():
    wn = load("src/yaml")
    print(wn)

if __name__ == '__main__':
    main()
