import re, string
from lxml import html
from model import *

class Parser:
    @classmethod
    def parse(cls, content):
        #print("Parser.parse()")
        doc = html.fromstring(content)

        elements = doc.xpath("//div[@class='page']/div[@class='pr dictionary'][1]")
        #print(len(elements))

        dict_node = elements[0] if (len(elements) > 0) else None
        #print(dict_node)

        dictionary = None if dict_node is None else Parser().parse_dict(dict_node)
        if dictionary is not None:
            pass
            #dictionary.show()

        return dictionary

    def __init__(self):
        pass

    def parse_dict(self, dict_node):
        #print("parse_dict()")
        dictionary = Dictionary()
        entry_nodes = dict_node.xpath("div[@class='link']/div/div/div/div/div[@class='pr entry-body__el']")
        #print("num entries: %s" % len(entry_nodes))
        if entry_nodes is None:
            return dictionary

        for entry_node in entry_nodes:
            entry = self.parse_entry(entry_node)
            dictionary.add_entry(entry)
        # FOR TESTING
        #dictionary.add_entry(self.parse_entry(entry_nodes[0]))

        # Return
        return dictionary


    def parse_entry(self, entry_node):
        #print("parse_entry")
        head_node = entry_node.xpath("div[@class='pos-header dpos-h']")[0]
        entry = Entry(self.parse_entry_head(head_node))

        body_nodes = entry_node.xpath("div[@class='pos-body']/div")
        #print("num body nodes: %s" % len(body_nodes))
        for body_node in body_nodes:
            html_class = body_node.get("class")
            if "dsense" in html_class:
                #print("dsense")
                sense = self.parse_sense(body_node)
                entry.add_sense(sense)
            elif "grammar" in html_class:
                pass
            elif "idioms" in html_class:
                pass
            elif "related_word" in html_class:
                related_words = self.parse_related_words(body_node)
                entry.add_related_words(related_words)
            else:
                pass

        # Return
        return entry

    def parse_entry_head(self, node):
        # word, extra, pronun, pronun_audio_url
        elements = node.xpath("div[@class='di-title']")
        word = self.get_text(elements[0]) if (len(elements) > 0) else ''

        elements = node.xpath("div[@class='posgram dpos-g hdib lmr-5']")
        posgram_info = self.get_text(elements[0]) if (len(elements) > 0) else ''

        elements = node.xpath("span[@class='lab dlab']")
        lab_info = self.get_text(elements[0]) if (len(elements) > 0) else ''
        extra = "%s %s" % (posgram_info, lab_info)

        elements = node.xpath("span[@class='uk dpron-i ']//source[@type='audio/mpeg']")
        pronun_audio_url = elements[0].get("src") if (len(elements) > 0) else ''
        #print("pronun_audio_url : %s " % extra)

        elements = node.xpath("span[@class='uk dpron-i ']//span[@class='pron dpron']")
        pronun = self.get_text(elements[0]) if (len(elements) > 0) else ''
        #print("pronun: %s " % extra)

        head = Entry.Head(word, extra, pronun, pronun_audio_url)
        #head.show()

        return head


    def parse_sense(self, node):
        # head, blocks, phrases
        elements = node.xpath("h3[@class='dsense_h']")
        text = self.get_text(elements[0]) if (len(elements) > 0) else ''

        sense = Sense(text)

        #block_nodes = node.xpath("div[@class='sense-body dsense_b']/div[@class='def-block ddef_block ']")
        elements = node.xpath("div[@class='sense-body dsense_b']/div")
        #print("num blocks: %s" % len(block_nodes))
        for element in elements:
            html_class = element.get('class')
            if 'def-block ddef_block' in html_class:
                block = self.parse_block(element)
                sense.add_block(block)
            elif 'phrase-block dphrase-block' in html_class:
                # sense.add_phrase_block(phrase_block)
                pass
            else:
                pass

        #sense.show()
        return sense

    def parse_block(self, node):
        # Info
        elements = node.xpath(".//div[@class='ddef_h']/span[@class='def-info ddef-info']/span")
        info = ''
        for element in elements:
            html_class = element.get('class')
            if html_class is None:
                continue

            if 'gram dgram' in html_class or 'var dvar' in html_class or 'lab dlab' in html_class or 'epp-xref dxref' in html_class:
                info = "%s %s" % (info, self.get_text(element))
                #print("info: %s" % info)

        # Definition
        elements = node.xpath(".//div[@class='ddef_h']/div[@class='def ddef_d db']")
        definition = self.get_text(elements[0]) if (len(elements) > 0) else ''
        #print("definition: %s" % definition)

        block = Block(info, definition)
        # Examples
        elements = node.xpath(".//div[@class='def-body ddef_b']/div")
        for element in elements:
            html_class = element.get('class')
            if 'examp' in html_class:
                block.add_example(self.get_text(element))
            elif 'synonym' in html_class:
                #print(self.parse_ref(element))
                block.add_synonyms(self.parse_ref(element))
            elif 'opposite' in html_class:
                block.add_opposites(self.parse_ref(element))
            elif 'compare' in html_class:
                block.add_compares(self.parse_ref(element))
            else:
                pass


        # block.show()
        return block

    # Parse references
    def parse_ref(self, node):
        #print("parse_ref")
        refs = []
        elements = node.xpath("div[@class='lcs lmt-10 lmb-20']/div")
        for element in elements:
            text_nodes = element.xpath("a")
            text = self.get_text(text_nodes[0]) if len(text_nodes) > 0 else ''

            extra_nodes = element.xpath("span/span")
            extra = self.get_text(extra_nodes[0]) if len(extra_nodes) > 0 else ''

            refs.append(Ref(text, extra))

        return refs

    def parse_related_words(self, node):
        related_words = []
        elements = node.xpath("div[@class='hax lp-10 lb lb-cm lbt0']/div/div")
        for element in elements:
            text_nodes = element.xpath("a/span")
            text = self.get_text(text_nodes[0]) if len(text_nodes) > 0 else ''
            extra = self.get_text(text_nodes[1]) if len(text_nodes) > 1 else ''

            related_words.append(Ref(text, extra))

        return related_words

    def parse_phrase(self, phrase):
        pass

    def get_text(self, element):
        return '' if element is None else re.sub(r"\s+", " ", element.text_content().strip())

