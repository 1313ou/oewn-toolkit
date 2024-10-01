from wordnet import *


class WordNetContentHandler(ContentHandler):
    def __init__(self):
        ContentHandler.__init__(self)
        self.lexicon = None
        self.entry = None
        self.sense = None
        self.defn = None
        self.ili_defn = None
        self.example = None
        self.example_source = None
        self.usage = None
        self.synset = None
        self.pron = None
        self.pron_var = None

    def startElement(self, name, attrs):
        if name == "Lexicon":
            self.lexicon = Lexicon(
                attrs["id"],
                attrs["label"],
                attrs["language"],
                attrs["email"],
                attrs["license"],
                attrs["version"],
                attrs["url"])
        elif name == "LexicalEntry":
            self.entry = LexicalEntry(attrs["id"])
        elif name == "Lemma":
            self.entry.set_lemma(
                Lemma(
                    attrs["writtenForm"],
                    PartOfSpeech(
                        attrs["partOfSpeech"])))
        elif name == "Form":
            self.entry.add_form(Form(attrs["writtenForm"]))
        elif name == "Sense":
            if "n" in attrs:
                n = int(attrs["n"])
            else:
                n = -1
            self.sense = Sense(attrs["id"], attrs["synset"], attrs.get(
                "dc:identifier") or "", n, attrs.get("adjposition"))
        elif name == "Synset":
            self.synset = Synset(attrs["id"], attrs["ili"],
                                 PartOfSpeech(attrs["partOfSpeech"]),
                                 attrs.get("lexfile", attrs.get("dc:subject", "")),
                                 attrs.get("dc:source", ""))
            self.synset.members = attrs.get("members", "").split(" ")
        elif name == "Definition":
            self.defn = ""
        elif name == "ILIDefinition":
            self.ili_defn = ""
        elif name == "Example":
            self.example = ""
            self.example_source = attrs.get("dc:source")
        elif name == "Usage":
            self.example = ""
        elif name == "SynsetRelation":
            self.synset.add_synset_relation(
                SynsetRelation(attrs["target"],
                               SynsetRelType(attrs["relType"])))
        elif name == "SenseRelation":
            self.sense.add_sense_relation(
                SenseRelation(attrs["target"],
                              SenseRelType(attrs["relType"]),
                              attrs.get("dc:type")))
        elif name == "SyntacticBehaviour":
            pass
            # self.entry.add_syntactic_behaviour(
            #    SyntacticBehaviour(
            #        attrs["subcategorizationFrame"],
            #        attrs["senses"].split(" ")))
        elif name == "Pronunciation":
            self.pron = ""
            self.pron_var = attrs.get("variety")
        elif name == "LexicalResource":
            pass
        else:
            raise ValueError("Unexpected Tag: " + name)

    def endElement(self, name):
        if name == "LexicalEntry":
            self.lexicon.add_entry(self.entry)
            self.entry = None
        elif name == "Sense":
            self.entry.add_sense(self.sense)
            self.sense = None
        elif name == "Synset":
            self.lexicon.add_synset(self.synset)
            self.synset = None
        elif name == "Definition":
            self.synset.add_definition(Definition(self.defn))
            self.defn = None
        elif name == "ILIDefinition":
            self.synset.add_definition(Definition(self.ili_defn), True)
            self.ili_defn = None
        elif name == "Example":
            self.synset.add_example(Example(self.example, self.example_source))
            self.example = None
        elif name == "Usage":
            self.synset.add_usage(Usage(self.usage))
            self.usage = None
        elif name == "Pronunciation":
            self.entry.pronunciation.append(Pronunciation(self.pron, self.pron_var))
            self.pron = None

    def characters(self, content):
        if self.defn is not None:
            self.defn += content
        elif self.ili_defn is not None:
            self.ili_defn += content
        elif self.example is not None:
            self.example += content
        elif self.usage is not None:
            self.usage += content
        elif self.pron is not None:
            self.pron += content
        elif content.strip() == '':
            pass
        else:
            print(content)
            raise ValueError("Text content not expected")


def escape_xml_lit(lit):
    return (lit.replace("&", "&amp;").replace("'", "&apos;").
            replace("\"", "&quot;").replace("<", "&lt;").replace(">", "&gt;"))


def extract_comments(wordnet_file, lexicon):
    with codecs.open(wordnet_file, "r", encoding="utf-8") as source:
        sen_rel_comment = re.compile(
            ".*<SenseRelation .* target=\"(.*)\".*/> <!-- (.*) -->")
        syn_rel_comment = re.compile(
            ".*<SynsetRelation .* target=\"(.*)\".*/> <!-- (.*) -->")
        comment = re.compile(".*<!-- (.*) -->.*")
        synset = re.compile(".*<Synset id=\"(\\S*)\".*")
        c = None
        for line in source.readlines():
            m = sen_rel_comment.match(line)
            if m:
                lexicon.comments[m.group(1)] = m.group(2)
            else:
                m = syn_rel_comment.match(line)
                if m:
                    lexicon.comments[m.group(1)] = m.group(2)
                else:
                    m = comment.match(line)
                    if m:
                        c = m.group(1)
                    else:
                        m = synset.match(line)
                        if m and c:
                            lexicon.comments[m.group(1)] = c
                            c = None


def parse_wordnet(wordnet_file):
    with codecs.open(wordnet_file, "r", encoding="utf-8") as source:
        handler = WordNetContentHandler()
        parse(source, handler)
    extract_comments(wordnet_file, handler.lexicon)
    return handler.lexicon


if __name__ == "__main__":
    wordnet = parse_wordnet(sys.argv[1])
    xml_file = open("wn31-test.xml", "w")
    wordnet.to_xml(xml_file, True)
