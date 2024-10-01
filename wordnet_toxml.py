# TO XML export


def lexicon_to_xml(lexicon, xml_file, part=True):
    xml_file.write("""<?xml version="1.0" encoding="UTF-8"?>\n""")
    if part:
        xml_file.write(
            """<!DOCTYPE LexicalResource SYSTEM "http://globalwordnet.github.io/schemas/WN-LMF-relaxed-1.1.dtd">\n""")
    else:
        xml_file.write(
            """<!DOCTYPE LexicalResource SYSTEM "http://globalwordnet.github.io/schemas/WN-LMF-1.1.dtd">\n""")
    xml_file.write(
        """<LexicalResource xmlns:dc="https://globalwordnet.github.io/schemas/dc/">
<Lexicon id="%s"
       label="%s"
       language="%s"
       email="%s"
       license="%s"
       version="%s"
       url="%s">
""" %
        (lexicon.id,
         lexicon.label,
         lexicon.language,
         lexicon.email,
         lexicon.license,
         lexicon.version,
         lexicon.url))

    for entry in lexicon.entries:
        entry.to_xml(xml_file, lexicon.comments)
    for synset in lexicon.synsets:
        synset.to_xml(xml_file, lexicon.comments)
    for synbeh in lexicon.frames:
        synbeh.to_xml(xml_file)
    xml_file.write("""  </Lexicon>
</LexicalResource>\n""")


def entry_to_xml(entry, xml_file, comments):
    xml_file.write("""    <LexicalEntry id="%s">""" % entry.id)
    if entry.pronunciation:
        xml_file.write("""
      <Lemma writtenForm="%s" partOfSpeech="%s">
""" % (escape_xml_lit(entry.lemma.written_form),
       entry.lemma.part_of_speech.value if entry.lemma.part_of_speech.value != "s" else "a"))
        for pron in entry.pronunciation:
            pron.to_xml(xml_file)
        xml_file.write("""      </Lemma>
""")
    else:
        xml_file.write("""
      <Lemma writtenForm="%s" partOfSpeech="%s"/>
""" % (escape_xml_lit(entry.lemma.written_form), entry.lemma.part_of_speech.value))
    for form in entry.forms:
        form.to_xml(xml_file)
    for sense in entry.senses:
        sense.to_xml(xml_file, comments)
    xml_file.write("""    </LexicalEntry>
""")


def form_to_xml(form, xml_file):
    xml_file.write("""      <Form writtenForm="%s"/>
""" % escape_xml_lit(form.written_form))


def pronunciation_to_xml(pronunciation, xml_file):
    if pronunciation.variety:
        xml_file.write("""        <Pronunciation variety="%s">%s</Pronunciation>
""" % (pronunciation.variety, escape_xml_lit(pronunciation.value)))
    else:
        xml_file.write("""        <Pronunciation>%s</Pronunciation>
""" % (escape_xml_lit(pronunciation.value)))


def sense_to_xml(sense, xml_file, comments):
    if sense.adjposition:
        n_str = " adjposition=\"%s\"" % sense.adjposition
    else:
        n_str = ""
    if sense.n >= 0:
        n_str = "%s n=\"%d\"" % (n_str, sense.n)
    if sense.sense_key:
        sk_str = " dc:identifier=\"%s\"" % escape_xml_lit(sense.sense_key)
    else:
        sk_str = ""
    if sense.subcat:
        subcat_str = " subcat=\"%s\"" % " ".join(sense.subcat)
    else:
        subcat_str = ""
    if len(sense.sense_relations) > 0:
        xml_file.write("""      <Sense id="%s"%s%s synset="%s"%s>
""" % (sense.id, n_str, subcat_str, sense.synset, sk_str))
        for rel in sense.sense_relations:
            rel.to_xml(xml_file, comments)
        xml_file.write("""        </Sense>
""")
    else:
        xml_file.write("""      <Sense id="%s"%s%s synset="%s"%s/>
""" % (sense.id, n_str, subcat_str, sense.synset, sk_str))


def synset_to_xml(synset, xml_file, comments):
    if synset.id in comments:
        xml_file.write("""    <!-- %s -->
""" % comments[synset.id])
    source_tag = ""
    if synset.source:
        source_tag = " dc:source=\"%s\"" % synset.source
    xml_file.write(
        """    <Synset id="%s" ili="%s" members="%s" partOfSpeech="%s" lexfile="%s"%s>
""" %
        (synset.id,
         synset.ili,
         " ".join(synset.members),
         synset.part_of_speech.value,
         synset.lex_name,
         source_tag))
    for defn in synset.definitions:
        defn.to_xml(xml_file)
    if synset.ili_definition:
        synset.ili_definition.to_xml(xml_file, True)
    for rel in synset.synset_relations:
        rel.to_xml(xml_file, comments)
    for ex in synset.examples:
        ex.to_xml(xml_file)
    for us in synset.usages:
        us.to_xml(xml_file)
    xml_file.write("""    </Synset>
""")


def definition_to_xml(definition, xml_file, is_ili=False):
    if is_ili:
        xml_file.write("""      <ILIDefinition>%s</ILIDefinition>
""" % escape_xml_lit(definition.text))
    else:
        xml_file.write("""      <Definition>%s</Definition>
""" % escape_xml_lit(definition.text))


def example_to_xml(example, xml_file):
    if example.source:
        xml_file.write("""      <Example dc:source=\"%s\">%s</Example>
""" % (escape_xml_lit(example.source), escape_xml_lit(example.text)))
    else:
        xml_file.write("""      <Example>%s</Example>
""" % escape_xml_lit(example.text))


def usage_to_xml(usage, xml_file):
    xml_file.write("""      <Usage>%s</Usage>
""" % escape_xml_lit(usage.text))


def synset_relation_to_xml(synset_relation, xml_file, comments):
    xml_file.write("""      <SynsetRelation relType="%s" target="%s"/>""" %
                   (synset_relation.rel_type.value, synset_relation.target))
    if synset_relation.target in comments:
        xml_file.write(""" <!-- %s -->
""" % comments[synset_relation.target])
    else:
        xml_file.write("\n")


def sense_relation_to_xml(sense_relation, xml_file, comments):
    if sense_relation.other_type:
        xml_file.write(
            """        <SenseRelation relType="other" target="%s" dc:type="%s"/>""" %
            (sense_relation.target, sense_relation.other_type))
    else:
        xml_file.write(
            """        <SenseRelation relType="%s" target="%s"/>""" %
            (sense_relation.rel_type.value, sense_relation.target))
    if sense_relation.target in comments:
        xml_file.write(""" <!-- %s -->
""" % comments[sense_relation.target])
    else:
        xml_file.write("\n")


def syntactic_behaviour_to_xml(syntactic_behaviour, xml_file):
    xml_file.write(
        """  <SyntacticBehaviour id="%s" subcategorizationFrame="%s"/>
""" %
        (syntactic_behaviour.id, escape_xml_lit(
            syntactic_behaviour.subcategorization_frame)))


def escape_xml_lit(lit):
    return (lit.replace("&", "&amp;").replace("'", "&apos;").
            replace("\"", "&quot;").replace("<", "&lt;").replace(">", "&gt;"))


def escape_lemma(lemma):
    """Format the lemma so it is valid XML id"""

    def elc(c):
        if ('A' <= c <= 'Z') or ('a' <= c <= 'z') or (
                '0' <= c <= '9') or c == '.':
            return c
        elif c == ' ':
            return '_'
        elif c == '(':
            return '-lb-'
        elif c == ')':
            return '-rb-'
        elif c == '\'':
            return '-ap-'
        elif c == '/':
            return '-sl-'
        elif c == '-':
            return '-'
        elif c == ',':
            return '-cm-'
        elif c == '!':
            return '-ex-'
        elif c == '+':
            return '-pl-'
        else:
            return '-%04x-' % ord(c)

    return "".join(elc(c) for c in lemma)
