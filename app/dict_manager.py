import calendar
import time
import requests, os
import random
from parser import Parser
from writer import Writer
from reader import Reader
from model import Word

class DictManager:
    BASE_URL = "http://dictionary.cambridge.org"
    ENG_ENG = "dictionary/english"
    ENG_VNE = "dictionary/english-vietnamese"
    OUTPUT = 'output'

    @classmethod
    def process(cls, input_filename):
        print("DictManager.process")
        start_time = time.time()
        global output_dir
        output_dir = "%s/%s" % (DictManager.OUTPUT, int(time.time()))

        os.mkdir(output_dir)
        output_filename = "%s/output.txt" % output_dir
        print("Input: %s " % input_filename)
        print("Output: %s" % output_filename)

        input_words = Reader.read("%s" % (input_filename))

        num_words = 0
        mid = 1
        for input_word in input_words:
            print(input_word)
            d = DictManager(mid, input_word)
            d.request()
            lines = []

            for word in d.words:
                lines.append(word.generate_line())

            if len(lines) > 0:
                Writer.append(output_filename, lines)
            else:
                print("Seem invalid word: '%s'" % input_word)

            num_words = num_words + len(lines)

            mid = mid + 1
            print("Sleeping 0.5s")
            print("")
            time.sleep(0.5)

        end_time = time.time()
        print("Num words: %s" % num_words)
        print("Elapsed time: %s" % (end_time - start_time))
        print("End")

    def __init__(self, mid, word):
        self.mid = mid
        self.word = word
        self.dictionary = None
        self.words = []

        # For downloading sound
        self.sound_dict = {}
        pass

    def request(self):
        page = requests.get("%s/%s/%s" % (self.BASE_URL, self.ENG_ENG, self.word))
        self.__parse(page.content)
        self.__generate_words()

        self.__download_sounds()

    def __download_sounds(self):
        i = 1
        for key, value in self.sound_dict.items():
            # Key, value
            r = requests.get(key)
            sound_name = key.split("/")[-1]
            filename = "%s/%s-%s-%s-%s" %(output_dir, self.mid, value, i, sound_name)
            print(filename)
            with open(filename, "wb") as f:
                f.write(r.content)

            i = i + 1

    def __parse(self, content):
        self.dictionary = Parser.parse(content)

    def __generate_words(self):
        if self.dictionary is None:
            return

        for entry in self.dictionary.entries:
            for sense in entry.senses:
                for block in sense.blocks:
                    word = Word()
                    # Word
                    word.word = entry.head.word

                    # Pronunciation
                    word.pronunciation = entry.head.pronun

                    #print("block.info: '%s'" % block.info)
                    #print("entry.head.extra: '%s'" % entry.head.extra)
                    # Label
                    word.label = block.info.strip()

                    # Type
                    if sense.text.strip() == '':
                        word.part_of_speech = entry.head.extra.strip()
                    else:
                        word.part_of_speech = sense.text.replace(word.word, "").strip()

                    # Definition
                    word.definition = block.definition.strip()
                    if word.definition[-1] == ':':
                        word.definition = word.definition[:-1]

                    # Definition
                    word.vietnamese = ''

                    # Examples
                    for i, ex in enumerate(block.examples[0:5]):
                        word.examples = "%s (%s) %s" % (word.examples.strip(), i + 1, ex.strip())

                    # Synonyms
                    word.synonyms = ", ".join([synonym.to_s() for synonym in block.synonyms])

                    # Opposites
                    word.opposites = ", ".join([opposite.to_s() for opposite in block.opposites])

                    # Compares
                    word.compares = ", ".join([compare.to_s() for compare in block.compares])

                    # Word family
                    word.word_family = ", ".join([related_word.to_s() for related_word in entry.related_words])

                    word.pronun_audio_url = entry.head.pronun_audio_url

                    self.sound_dict["%s%s" % (DictManager.BASE_URL, word.pronun_audio_url)] = word.word

                    self.words.append(word)

