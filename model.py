import json
'''
Explaination about data structure
Dictionary
|   |
|   Entry
|   |   |
|   |   Sense
|   |       |
|   |       Block
|   |
|   Entry
|   |
|   Entry
|
Dictionary
'''

class Base(object):
    def show(self):
        print(json.dumps(self, default=lambda o: o.__dict__))


class Ref(Base):
    def __init__(self, text, extra):
        self.text = text
        self.extra = extra

    def to_s(self):
        return "%s (%s)" % (self.text, self.extra) if self.extra is not '' else self.text


class Block(Base):
    def __init__(self, info, definition):
        self.info = info
        self.definition = definition
        self.examples = []
        self.synonyms = []
        self.opposites = []
        self.compares = []

    def add_example(self, example):
        self.examples.append(example)

    def add_synonyms(self, synonyms):
        self.synonyms = self.synonyms + synonyms

    def add_opposites(self, opposites):
        self.opposites = self.opposites + opposites

    def add_compares(self, compares):
        self.compares = self.compares + compares


class Phrase(Block): pass


class Sense(Base):
    def __init__(self, text):
        self.text = text
        self.blocks = []
        self.phrases = []

    def add_block(self, block):
        self.blocks.append(block)

    def add_phrase(self, phrase):
        self.phrases.append(phrase)


class Entry(Base):
    def __init__(self, head):
        self.head = head
        self.senses = []
        self.related_words = []

    def add_sense(self, sense):
        self.senses.append(sense)

    def add_related_words(self, words):
        self.related_words = self.related_words + words

    class Head(Base):
        def __init__(self, word, extra, pronun, pronun_audio_url):
            self.word = word
            self.extra = extra
            self.pronun = pronun
            self.pronun_audio_url = pronun_audio_url


class Dictionary(Base):
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

class Word(Base):
    def __init__(self):
        self.word = ''
        self.pronunciation = ''
        self.part_of_speech = ''
        self.label = ''
        self.definition = ''
        self.vietnamese = ''
        self.examples = ''
        self.synonyms = ''
        self.opposites = ''
        self.compares = ''
        self.word_family = ''
        self.pronun_audio_url = ''

    def generate_line(self):
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            self.word,
            self.pronunciation,
            self.part_of_speech,
            self.label,
            self.definition,
            self.vietnamese,
            self.examples,
            self.synonyms,
            self.opposites,
            self.compares,
            self.word_family,
            self.pronun_audio_url
            )

