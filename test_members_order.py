#!/usr/bin/python3

import argparse

import oewnio


def lemma2senseorder(wn, l, synset_id):
    for e2 in wn.entry_by_lemma(l):
        for sense in wn.entry_by_id(e2).senses:
            if sense.synset == synset_id:
                sk = sense.id
                num = sk[-4:-2]
                print(l, sk, num)
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
    synset = wn.id2synset[synsetid]
    # BUG members = entries_ordered(wn, synset.id)
    lemmas = members(wn, synset)
    for l in lemmas:
        print(l)


def test_xml(wn, synsetid):
    synset = wn.id2synset[synsetid]
    with open("test-%s.xml" % synsetid, "w") as out:
        synset.to_xml(out, [])


def main():
    parser = argparse.ArgumentParser(description="load from yaml and write")
    parser.add_argument('repo', type=str, help='repository home')
    args = parser.parse_args()

    # wn = load(args.repo)
    wn = oewnio.load_pickle(args.repo)

    # save(wn)
    test_xml(wn, 'oewn-07299259-n')
    test_members(wn, 'oewn-07299259-n')


if __name__ == '__main__':
    main()
