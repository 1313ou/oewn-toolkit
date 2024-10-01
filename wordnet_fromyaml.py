"""WordNet YAML interface"""

from glob import glob

import yaml

from wordnet import *


def load_verbframes(home):
    with open(f'{home}/frames.yaml', encoding="utf-8") as inp:
        frames = yaml.load(inp, Loader=yaml.CLoader)
        return [SyntacticBehaviour(k, v) for k, v in frames.items()]


def load_entries(home):
    sense_resolver = {}
    member_resolver = {}
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
                        member_resolver[(lemma, sense.synsetid)] = entry
                    entries.append(entry)
    return entries, sense_resolver, member_resolver


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
    sense_rel_types = [t.value for t in SenseRelType]
    other_rel_types = [t.value for t in OtherSenseRelType]
    for rel, targets in props.items():
        if rel in sense_rel_types:
            for target in targets:
                s.sense_relations.append(SenseRelation(target, SenseRelType(rel)))
        if rel in other_rel_types:
            for target in targets:
                s.sense_relations.append(SenseRelation(target, SenseRelType.OTHER, rel))
    return s


def load_synset(props, synsetid, lex_name):
    ss = Synset(synsetid,
                props["partOfSpeech"],
                props["members"],
                lex_name)
    for defn in props["definition"]:
        ss.definitions.append(Definition(defn))
    for example in props.get("example", []):
        if isinstance(example, str):
            ss.examples.append(Example(example))
        else:
            ss.examples.append(Example(example["text"], example["source"]))
    for usage in props.get("usage", []):
        ss.usages.append(Usage(usage))
    ss.source = props.get("source"),
    ss.wikidata = props.get("wikidata")
    ss.ili = props.get("ili", "in")
    # relations
    synset_rel_types = [t.value for t in SynsetRelType]
    for rel, targets in props.items():
        if rel in synset_rel_types:
            for target in targets:
                ss.synset_relations.append(SynsetRelation(target, SynsetRelType(rel)))
    return ss


def load(home):
    wn = Lexicon("oewn", "English WordNet", "en",
                 "english-wordnet@googlegroups.com",
                 "https://creativecommons.org/licenses/by/4.0",
                 "2024",
                 "https://github.com/globalwordnet/english-wordnet")
    # frames
    wn.frames = load_verbframes(home)

    # lex entries
    wn.entries, wn.sense_resolver, wn.member_resolver = load_entries(home)

    # synsets
    wn.synsets, wn.synset_resolver = load_synsets(home)
    return wn


def resolve(wn):
    # resolve synset reference in sense
    for e in wn.entries:
        for s in e.senses:
            s.resolved_synset = wn.synset_resolver[s.synsetid]

    # resolve member reference in synset
    for ss in wn.synsets:
        ss.resolved_members = [wn.member_resolver[(m, ss.id)] for m in ss.members]

    # resolve target reference in synset relations
    for ss in wn.synsets:
        for r in ss.synset_relations:
            r.resolved_target = wn.synset_resolver[r.target]

    # resolve target reference in sense relations
    for e in wn.entries:
        for s in e.senses:
            for r in s.sense_relations:
                r.resolved_target = wn.sense_resolver[r.target]


def extend(wn):
    pass


def main():
    wn = load("src/yaml")
    resolve(wn)
    print(wn)


if __name__ == '__main__':
    main()
