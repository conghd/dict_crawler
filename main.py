#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import sys, os
import re, string
from app.dict_manager import DictManager
from lxml import html
import requests

class Main:
    def __init__(self):
        pass

    def process(self, input_filename):
        DictManager.process(input_filename)
        pass

if (len(sys.argv) < 2):
    print("Usage: python main.py [filename-without-extension]")
    print("Example: python main.py u08_1")
    exit(1)

Main().process('%s' % sys.argv[1])
