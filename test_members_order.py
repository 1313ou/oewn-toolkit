#!/usr/bin/python3

import argparse
import sys

from oewn_core.deserialize import load_pickle
from oewn_xml.wordnet_toxml import synset_to_xml


def lemma2senseorder(wn, l, synset_id):
    for e2 in wn.entries_resolver_by_lemma[l]:
        for sense in e2.senses:
            if sense.synsetid == synset_id:
                sk = sense.id
                num = sk[-4:-2]
                num2 = sk[-2:]
                print(f"sense of '{l}', sensekey:{sk}, sensenum:{num}, sensenum2:{"" if num2 == '::' else num2}")
                return num
    return "99"


def entries_ordered(wn, synset_id):
    """Get the lemmas for entries ordered correctly"""
    e = [l for l, s in wn.member_resolver if s == synset_id]
    e.sort(key=lambda l: lemma2senseorder(wn, l, synset_id))
    return e


def members(wn, synset):
    return [wn.entry_resolver[(m, "n", None)].lemma for m in synset.members]


def test_members(wn, synsetid):
    print("ORDER PRESERVING")
    synset = wn.synset_resolver[synsetid]
    # BUG members = entries_ordered(wn, synset.id)
    members2 = members(wn, synset)
    for l in members2:
        print(l)


def test_members_orig(wn, synsetid):
    print("WITH ENTRIES ORDERED")
    synset = wn.synset_resolver[synsetid]
    # BUG
    members2 = entries_ordered(wn, synset.id)
    for l in members2:
        print(l)


def test_xml(wn, synsetid):
    print("XML")
    synset = wn.synset_resolver[synsetid]
    synset_to_xml(synset, wn.member_resolver, sys.stdout, [])


def main():
    parser = argparse.ArgumentParser(description="load from yaml and write")
    parser.add_argument('repo', type=str, help='repository home')
    args = parser.parse_args()

    # wn = load(args.repo)
    wn = load_pickle(args.repo)

    # save(wn)
    test_members(wn, '07299259-n')
    test_members_orig(wn, '07299259-n')
    test_xml(wn, '07299259-n')


if __name__ == '__main__':
    main()
