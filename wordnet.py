from enum import Enum


class Lexicon:
    """The Lexicon contains all the synsets and entries"""

    def __init__(self, lid, label, language, email, wnlicense, version, url):
        self.id = lid
        self.label = label
        self.language = language
        self.email = email
        self.license = wnlicense
        self.version = version
        self.url = url
        self.entries = []
        self.synsets = []
        self.frames = []
        self.comments = {}

        self.synset_resolver = {}
        self.sense_resolver = {}
        self.member_resolver = {}

    def __str__(self):
        return "Lexicon with ID %s and %d entries and %d synsets" % (
            self.id, len(self.entries), len(self.synsets))

    def add_entry(self, entry):
        self.entries.append(entry)

    def add_synset(self, synset):
        self.synsets.append(synset)
        self.synset_resolver[synset.id] = synset


class LexicalEntry:
    """The lexical entry consists of a single word"""

    def __init__(self, lemma, pos, discriminant):
        self.lemma = lemma
        self.pos = pos
        self.discriminant = discriminant
        self.forms = []
        self.pronunciation = []
        self.senses = []


class Pronunciation:
    """The pronunciation of a lemma"""

    def __init__(self, value, variety):
        self.value = value
        self.variety = variety


class Sense:
    """The sense links an entry to a synset"""

    def __init__(self, senseid, entry, synsetid, n=-1, adjposition=None):
        self.id = senseid
        self.entry = entry
        self.synsetid = synsetid
        self.n = n
        self.sense_relations = []
        self.adjposition = adjposition
        self.sent = None
        self.frames = None
        self.subcat = None
        self.resolved_synset = None



class Synset:
    """The synset is a collection of synonyms"""

    def __init__(self, synsetid, pos, members, lex_name):
        self.id = synsetid
        self.part_of_speech = pos
        self.members = members
        self.lex_name = lex_name
        self.examples = []
        self.usages = []
        self.definitions = []
        self.ili_definition = None
        self.synset_relations = []
        self.source = None
        self.wikidata = None
        self.ili = None
        self.resolved_members = None


class Definition:
    def __init__(self, text):
        self.text = text


class Example:
    def __init__(self, text, source=None):
        self.text = text
        self.source = source


class Usage:
    def __init__(self, text):
        self.text = text


class SynsetRelation:
    def __init__(self, target, rel_type):
        self.target = target
        self.rel_type = rel_type
        self.resolved_target = None


class SenseRelation:
    def __init__(self, target, rel_type, other_type=None):
        self.target = target
        self.rel_type = rel_type
        self.other_type = other_type
        self.resolved_target = None


class SyntacticBehaviour:
    def __init__(self, bid, subcategorization_frame):
        if not isinstance(subcategorization_frame, str):
            raise "Syntactic Behaviour is not string" + \
                  str(subcategorization_frame)
        self.subcategorization_frame = subcategorization_frame
        self.id = bid


class PartOfSpeech(Enum):
    NOUN = 'n'
    VERB = 'v'
    ADJECTIVE = 'a'
    ADVERB = 'r'
    ADJECTIVE_SATELLITE = 's'
    NAMED_ENTITY = 't'
    CONJUNCTION = 'c'
    ADPOSITION = 'p'
    OTHER = 'x'
    UNKNOWN = 'u'


class SynsetRelType(Enum):
    AGENT = 'agent'
    ALSO = 'also'
    ATTRIBUTE = 'attribute'
    BE_IN_STATE = 'be_in_state'
    CAUSES = 'causes'
    CLASSIFIED_BY = 'classified_by'
    CLASSIFIES = 'classifies'
    CO_AGENT_INSTRUMENT = 'co_agent_instrument'
    CO_AGENT_PATIENT = 'co_agent_patient'
    CO_AGENT_RESULT = 'co_agent_result'
    CO_INSTRUMENT_AGENT = 'co_instrument_agent'
    CO_INSTRUMENT_PATIENT = 'co_instrument_patient'
    CO_INSTRUMENT_RESULT = 'co_instrument_result'
    CO_PATIENT_AGENT = 'co_patient_agent'
    CO_PATIENT_INSTRUMENT = 'co_patient_instrument'
    CO_RESULT_AGENT = 'co_result_agent'
    CO_RESULT_INSTRUMENT = 'co_result_instrument'
    CO_ROLE = 'co_role'
    DIRECTION = 'direction'
    DOMAIN_REGION = 'domain_region'
    DOMAIN_TOPIC = 'domain_topic'
    EXEMPLIFIES = 'exemplifies'
    ENTAILS = 'entails'
    EQ_SYNONYM = 'eq_synonym'
    HAS_DOMAIN_REGION = 'has_domain_region'
    HAS_DOMAIN_TOPIC = 'has_domain_topic'
    IS_EXEMPLIFIED_BY = 'is_exemplified_by'
    HOLO_LOCATION = 'holo_location'
    HOLO_MEMBER = 'holo_member'
    HOLO_PART = 'holo_part'
    HOLO_PORTION = 'holo_portion'
    HOLO_SUBSTANCE = 'holo_substance'
    HOLONYM = 'holonym'
    HYPERNYM = 'hypernym'
    HYPONYM = 'hyponym'
    IN_MANNER = 'in_manner'
    INSTANCE_HYPERNYM = 'instance_hypernym'
    INSTANCE_HYPONYM = 'instance_hyponym'
    INSTRUMENT = 'instrument'
    INVOLVED = 'involved'
    INVOLVED_AGENT = 'involved_agent'
    INVOLVED_DIRECTION = 'involved_direction'
    INVOLVED_INSTRUMENT = 'involved_instrument'
    INVOLVED_LOCATION = 'involved_location'
    INVOLVED_PATIENT = 'involved_patient'
    INVOLVED_RESULT = 'involved_result'
    INVOLVED_SOURCE_DIRECTION = 'involved_source_direction'
    INVOLVED_TARGET_DIRECTION = 'involved_target_direction'
    IS_CAUSED_BY = 'is_caused_by'
    IS_ENTAILED_BY = 'is_entailed_by'
    LOCATION = 'location'
    MANNER_OF = 'manner_of'
    MERO_LOCATION = 'mero_location'
    MERO_MEMBER = 'mero_member'
    MERO_PART = 'mero_part'
    MERO_PORTION = 'mero_portion'
    MERO_SUBSTANCE = 'mero_substance'
    MERONYM = 'meronym'
    SIMILAR = 'similar'
    OTHER = 'other'
    PATIENT = 'patient'
    RESTRICTED_BY = 'restricted_by'
    RESTRICTS = 'restricts'
    RESULT = 'result'
    ROLE = 'role'
    SOURCE_DIRECTION = 'source_direction'
    STATE_OF = 'state_of'
    TARGET_DIRECTION = 'target_direction'
    SUBEVENT = 'subevent'
    IS_SUBEVENT_OF = 'is_subevent_of'
    ANTONYM = 'antonym'


class SenseRelType(Enum):
    ANTONYM = 'antonym'
    ALSO = 'also'
    PARTICIPLE = 'participle'
    PERTAINYM = 'pertainym'
    DERIVATION = 'derivation'
    DOMAIN_TOPIC = 'domain_topic'
    HAS_DOMAIN_TOPIC = 'has_domain_topic'
    DOMAIN_REGION = 'domain_region'
    HAS_DOMAIN_REGION = 'has_domain_region'
    EXEMPLIFIES = 'exemplifies'
    IS_EXEMPLIFIED_BY = 'is_exemplified_by'
    SIMILAR = 'similar'
    OTHER = 'other'


class OtherSenseRelType(Enum):
    AGENT = 'agent'
    MATERIAL = 'material'
    EVENT = 'event'
    INSTRUMENT = 'instrument'
    LOCATION = 'location'
    BY_MEANS_OF = 'by_means_of'
    UNDERGOER = 'undergoer'
    PROPERTY = 'property'
    RESULT = 'result'
    STATE = 'state'
    USES = 'uses'
    DESTINATION = 'destination'
    BODY_PART = 'body_part'
    VEHICLE = 'vehicle'


inverse_synset_rels = {
    SynsetRelType.HYPERNYM: SynsetRelType.HYPONYM,
    SynsetRelType.HYPONYM: SynsetRelType.HYPERNYM,
    SynsetRelType.INSTANCE_HYPERNYM: SynsetRelType.INSTANCE_HYPONYM,
    SynsetRelType.INSTANCE_HYPONYM: SynsetRelType.INSTANCE_HYPERNYM,
    SynsetRelType.MERONYM: SynsetRelType.HOLONYM,
    SynsetRelType.HOLONYM: SynsetRelType.MERONYM,
    SynsetRelType.MERO_LOCATION: SynsetRelType.HOLO_LOCATION,
    SynsetRelType.HOLO_LOCATION: SynsetRelType.MERO_LOCATION,
    SynsetRelType.MERO_MEMBER: SynsetRelType.HOLO_MEMBER,
    SynsetRelType.HOLO_MEMBER: SynsetRelType.MERO_MEMBER,
    SynsetRelType.MERO_PART: SynsetRelType.HOLO_PART,
    SynsetRelType.HOLO_PART: SynsetRelType.MERO_PART,
    SynsetRelType.MERO_PORTION: SynsetRelType.HOLO_PORTION,
    SynsetRelType.HOLO_PORTION: SynsetRelType.MERO_PORTION,
    SynsetRelType.MERO_SUBSTANCE: SynsetRelType.HOLO_SUBSTANCE,
    SynsetRelType.HOLO_SUBSTANCE: SynsetRelType.MERO_SUBSTANCE,
    SynsetRelType.BE_IN_STATE: SynsetRelType.STATE_OF,
    SynsetRelType.STATE_OF: SynsetRelType.BE_IN_STATE,
    SynsetRelType.CAUSES: SynsetRelType.IS_CAUSED_BY,
    SynsetRelType.IS_CAUSED_BY: SynsetRelType.CAUSES,
    SynsetRelType.SUBEVENT: SynsetRelType.IS_SUBEVENT_OF,
    SynsetRelType.IS_SUBEVENT_OF: SynsetRelType.SUBEVENT,
    SynsetRelType.MANNER_OF: SynsetRelType.IN_MANNER,
    SynsetRelType.IN_MANNER: SynsetRelType.MANNER_OF,
    SynsetRelType.RESTRICTS: SynsetRelType.RESTRICTED_BY,
    SynsetRelType.RESTRICTED_BY: SynsetRelType.RESTRICTS,
    SynsetRelType.CLASSIFIES: SynsetRelType.CLASSIFIED_BY,
    SynsetRelType.CLASSIFIED_BY: SynsetRelType.CLASSIFIES,
    SynsetRelType.ENTAILS: SynsetRelType.IS_ENTAILED_BY,
    SynsetRelType.IS_ENTAILED_BY: SynsetRelType.ENTAILS,
    SynsetRelType.DOMAIN_REGION: SynsetRelType.HAS_DOMAIN_REGION,
    SynsetRelType.HAS_DOMAIN_REGION: SynsetRelType.DOMAIN_REGION,
    SynsetRelType.DOMAIN_TOPIC: SynsetRelType.HAS_DOMAIN_TOPIC,
    SynsetRelType.HAS_DOMAIN_TOPIC: SynsetRelType.DOMAIN_TOPIC,
    SynsetRelType.EXEMPLIFIES: SynsetRelType.IS_EXEMPLIFIED_BY,
    SynsetRelType.IS_EXEMPLIFIED_BY: SynsetRelType.EXEMPLIFIES,
    SynsetRelType.ROLE: SynsetRelType.INVOLVED,
    SynsetRelType.INVOLVED: SynsetRelType.ROLE,
    SynsetRelType.AGENT: SynsetRelType.INVOLVED_AGENT,
    SynsetRelType.INVOLVED_AGENT: SynsetRelType.AGENT,
    SynsetRelType.PATIENT: SynsetRelType.INVOLVED_PATIENT,
    SynsetRelType.INVOLVED_PATIENT: SynsetRelType.PATIENT,
    SynsetRelType.RESULT: SynsetRelType.INVOLVED_RESULT,
    SynsetRelType.INVOLVED_RESULT: SynsetRelType.RESULT,
    SynsetRelType.INSTRUMENT: SynsetRelType.INVOLVED_INSTRUMENT,
    SynsetRelType.INVOLVED_INSTRUMENT: SynsetRelType.INSTRUMENT,
    SynsetRelType.LOCATION: SynsetRelType.INVOLVED_LOCATION,
    SynsetRelType.INVOLVED_LOCATION: SynsetRelType.LOCATION,
    SynsetRelType.DIRECTION: SynsetRelType.INVOLVED_DIRECTION,
    SynsetRelType.INVOLVED_DIRECTION: SynsetRelType.DIRECTION,
    SynsetRelType.TARGET_DIRECTION: SynsetRelType.INVOLVED_TARGET_DIRECTION,
    SynsetRelType.INVOLVED_TARGET_DIRECTION: SynsetRelType.TARGET_DIRECTION,
    SynsetRelType.SOURCE_DIRECTION: SynsetRelType.INVOLVED_SOURCE_DIRECTION,
    SynsetRelType.INVOLVED_SOURCE_DIRECTION: SynsetRelType.SOURCE_DIRECTION,
    SynsetRelType.CO_AGENT_PATIENT: SynsetRelType.CO_PATIENT_AGENT,
    SynsetRelType.CO_PATIENT_AGENT: SynsetRelType.CO_AGENT_PATIENT,
    SynsetRelType.CO_AGENT_INSTRUMENT: SynsetRelType.CO_INSTRUMENT_AGENT,
    SynsetRelType.CO_INSTRUMENT_AGENT: SynsetRelType.CO_AGENT_INSTRUMENT,
    SynsetRelType.CO_AGENT_RESULT: SynsetRelType.CO_RESULT_AGENT,
    SynsetRelType.CO_RESULT_AGENT: SynsetRelType.CO_AGENT_RESULT,
    SynsetRelType.CO_PATIENT_INSTRUMENT: SynsetRelType.CO_INSTRUMENT_PATIENT,
    SynsetRelType.CO_INSTRUMENT_PATIENT: SynsetRelType.CO_PATIENT_INSTRUMENT,
    SynsetRelType.CO_RESULT_INSTRUMENT: SynsetRelType.CO_INSTRUMENT_RESULT,
    SynsetRelType.CO_INSTRUMENT_RESULT: SynsetRelType.CO_RESULT_INSTRUMENT,
    SynsetRelType.ANTONYM: SynsetRelType.ANTONYM,
    SynsetRelType.EQ_SYNONYM: SynsetRelType.EQ_SYNONYM,
    SynsetRelType.SIMILAR: SynsetRelType.SIMILAR,
    #        SynsetRelType.ALSO: SynsetRelType.ALSO,
    SynsetRelType.ATTRIBUTE: SynsetRelType.ATTRIBUTE,
    SynsetRelType.CO_ROLE: SynsetRelType.CO_ROLE
}

inverse_sense_rels = {
    SenseRelType.DOMAIN_REGION: SenseRelType.HAS_DOMAIN_REGION,
    SenseRelType.HAS_DOMAIN_REGION: SenseRelType.DOMAIN_REGION,
    SenseRelType.DOMAIN_TOPIC: SenseRelType.HAS_DOMAIN_TOPIC,
    SenseRelType.HAS_DOMAIN_TOPIC: SenseRelType.DOMAIN_TOPIC,
    SenseRelType.EXEMPLIFIES: SenseRelType.IS_EXEMPLIFIED_BY,
    SenseRelType.IS_EXEMPLIFIED_BY: SenseRelType.EXEMPLIFIES,
    SenseRelType.ANTONYM: SenseRelType.ANTONYM,
    SenseRelType.SIMILAR: SenseRelType.SIMILAR,
    SenseRelType.ALSO: SenseRelType.ALSO,
    SenseRelType.DERIVATION: SenseRelType.DERIVATION,
}

ignored_symmetric_synset_rels = {
    SynsetRelType.HYPONYM, SynsetRelType.INSTANCE_HYPONYM, SynsetRelType.HOLONYM,
    SynsetRelType.HOLO_LOCATION, SynsetRelType.HOLO_MEMBER, SynsetRelType.HOLO_PART,
    SynsetRelType.HOLO_PORTION, SynsetRelType.HOLO_SUBSTANCE, SynsetRelType.STATE_OF,
    SynsetRelType.IS_CAUSED_BY, SynsetRelType.IS_SUBEVENT_OF, SynsetRelType.IN_MANNER,
    SynsetRelType.RESTRICTED_BY, SynsetRelType.CLASSIFIED_BY, SynsetRelType.IS_ENTAILED_BY,
    SynsetRelType.HAS_DOMAIN_REGION, SynsetRelType.HAS_DOMAIN_TOPIC,
    SynsetRelType.IS_EXEMPLIFIED_BY, SynsetRelType.INVOLVED, SynsetRelType.INVOLVED_AGENT,
    SynsetRelType.INVOLVED_PATIENT, SynsetRelType.INVOLVED_RESULT,
    SynsetRelType.INVOLVED_INSTRUMENT, SynsetRelType.INVOLVED_LOCATION,
    SynsetRelType.INVOLVED_DIRECTION, SynsetRelType.INVOLVED_TARGET_DIRECTION,
    SynsetRelType.INVOLVED_SOURCE_DIRECTION, SynsetRelType.CO_PATIENT_AGENT,
    SynsetRelType.CO_INSTRUMENT_AGENT, SynsetRelType.CO_RESULT_AGENT,
    SynsetRelType.CO_INSTRUMENT_PATIENT, SynsetRelType.CO_INSTRUMENT_RESULT}

ignored_symmetric_sense_rels = {
    SenseRelType.HAS_DOMAIN_REGION, SenseRelType.HAS_DOMAIN_TOPIC,
    SenseRelType.IS_EXEMPLIFIED_BY}

if __name__ == "__main__":
    pass
