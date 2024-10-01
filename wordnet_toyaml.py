"""WordNet YAML interface"""
import codecs

import yaml

from wordnet import *


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)


def sense_to_yaml(s, resolver):
    """Converts a single sense to the YAML form"""
    y = {'synset': s.synset, 'id': s.id}
    if s.adjposition:
        y['adjposition'] = s.adjposition
    for r in s.sense_relations:
        if r.rel_type not in ignored_symmetric_sense_rels:
            t = r.rel_type.value
            if t not in y:
                y[t] = []
            if resolver is not None and resolver[r.target] == r.resolved_target.id:
                raise f'Dead link from {s.id} to {r.target}'
            y[t].append(r.target)

    if s.subcat:
        y['subcat'] = s.subcat
    if s.sent:
        y['sent'] = s.sent
    return y


def example_to_yaml(example):
    """Convert an example to YAML"""
    if example.source:
        return {'text': example.text, 'source': example.source}
    else:
        return example.text


def entry_to_yaml(entry, sense_resolver):
    """Convert an entry to YAML"""
    e = {}
    if entry.forms:
        e['form'] = entry.forms
    if entry.pronunciation:
        e['pronunciation'] = []
        for p in entry.pronunciation:
            if p.variety:
                e['pronunciation'].append({'value': p.value, 'variety': p.variety})
            else:
                e['pronunciation'].append({'value': p.value})
    e['sense'] = [sense_to_yaml(s, sense_resolver) for s in entry.senses]
    return e


def save_entries(wn, home, change_list=None):
    entry_yaml = {c: {} for c in char_range('a', 'z')}
    entry_yaml['0'] = {}
    for entry in wn.entries:
        e = entry_to_yaml(entry, wn.sense_resolver)

        first = entry.lemma.lower()
        if first not in char_range('a', 'z'):
            first = '0'
        if entry.lemma not in entry_yaml[first]:
            entry_yaml[first][entry.lemma.written_form] = {}
        if entry.lemma.part_of_speech.value in entry_yaml[first][entry.lemma]:
            print(
                'Duplicate: %s - %s' %
                (entry.lemma.written_form,
                 entry.lemma.part_of_speech.value))
        entry_yaml[first][entry.lemma.written_form][entry.lemma.part_of_speech.value] = e

    for c in char_range('a', 'z'):
        if not change_list or c in change_list.entry_files:
            with codecs.open(f'{home}/entries-%s.yaml' % c, 'w', 'utf-8') as outp:
                outp.write(yaml.dump(entry_yaml[c], default_flow_style=False,
                                     allow_unicode=True))
    if not change_list or '0' in change_list.entry_files:
        with codecs.open(f'{home}/entries-0.yaml', 'w', 'utf-8') as outp:
            outp.write(yaml.dump(entry_yaml['0'], default_flow_style=False, allow_unicode=True))


def save_synsets(wn, home, change_list=None):
    synset_yaml = {}
    for synset in wn.synsets:
        s = {'members': [wn.id2entry[m].lemma.written_form for m in synset.members],
             'partOfSpeech': synset.part_of_speech.value,
             'definition': [d.text for d in synset.definitions]}
        if synset.examples:
            s['example'] = [example_to_yaml(x) for x in synset.examples]
        if synset.usages:
            s['usage'] = synset.usages
        if synset.source:
            s['source'] = synset.source
        if synset.ili and synset.ili != 'in':
            s['ili'] = synset.ili
        for r in synset.synset_relations:
            if r.rel_type not in ignored_symmetric_synset_rels:
                t = r.rel_type.value
                if t not in s:
                    s[t] = [r.target]
                else:
                    s[t].append(r.target)
        if synset.lex_name not in synset_yaml:
            synset_yaml[synset.lex_name] = {}
        synset_yaml[synset.lex_name][synset.id] = s

    for key, synsets in synset_yaml.items():
        if not change_list or key in change_list.lexfiles:
            with codecs.open(f'{home}/%s.yaml' % key, 'w', 'utf-8') as outp:
                outp.write(yaml.dump(synsets, default_flow_style=False, allow_unicode=True))


def save_frames(wn, home):
    with open(f'{home}/frames.yaml', 'w') as outp:
        outp.write(yaml.dump(wn.frames, default_flow_style=False, allow_unicode=True))


def save(wn, home, change_list=None):
    save_entries(wn, home, change_list)
    save_synsets(wn, home, change_list)
    save_frames(wn, home)
