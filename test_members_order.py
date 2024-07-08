#!/usr/bin/python3

import argparse
import sys

import oewnio


def lemma2senseorder(wn, l, synset_id):
    for e2 in wn.entry_by_lemma(l):
        for sense in wn.entry_by_id(e2).senses:
            if sense.synset == synset_id:
                sk = sense.id
                num = sk[-4:-2]
                num2 = sk[-2:]
                print(f"object:{l}, sensekey:{sk}, sensenum:{num}, sensenum2:{num2}")
                return num
    return "99"


def entries_ordered(wn, synset_id):
    """Get the lemmas for entries ordered correctly"""
    e = wn.members_by_id(synset_id)
    e.sort(key=lambda l: lemma2senseorder(wn, l, synset_id))
    return e


def members(wn, synset):
    return [wn.id2entry[m].lemma.written_form for m in synset.members]


def test_members(wn, synsetid):
    print("ORDER PRESERVING")
    synset = wn.id2synset[synsetid]
    # BUG members = entries_ordered(wn, synset.id)
    members2 = members(wn, synset)
    for l in members2:
        print(l)


def test_members_orig(wn, synsetid):
    print("WITH ENTRIES ORDERED")
    synset = wn.id2synset[synsetid]
    # BUG
    members2 = entries_ordered(wn, synset.id)
    for l in members2:
        print(l)


def test_xml(wn, synsetid):
    print("XML")
    synset = wn.id2synset[synsetid]
    synset.to_xml(sys.stdout, [])


def main():
    parser = argparse.ArgumentParser(description="load from yaml and write")
    parser.add_argument('repo', type=str, help='repository home')
    args = parser.parse_args()

    # wn = load(args.repo)
    wn = oewnio.load_pickle(args.repo)

    # save(wn)
    test_members(wn, 'oewn-07299259-n')
    test_members_orig(wn, 'oewn-07299259-n')
    test_xml(wn, 'oewn-07299259-n')


if __name__ == '__main__':
    main()
