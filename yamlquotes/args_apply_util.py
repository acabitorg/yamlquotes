# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging

from .helpers import get_defaults
from .repr_quote_plaintext import repr_quote_plaintext

logger = logging.getLogger(__name__)

class UtilArgsApplier():

    def __init__(self, args):
        self.args = args
        self.defaults = {}
        self.quotes = []
        self.quotes_s = []

    def apply(self, data):
        self.defaults = get_defaults(data)
        i = 0
        for qt in data['quotes']:
            s = repr_quote_plaintext(qt, self.defaults, short=self.args.short)
            if self.args.max_length and len(s) >= self.args.max_length:
                continue
            if self.args.hashtags:
                s = self._add_hashtags(qt, s)
            self.quotes.append(qt)
            self.quotes_s.append(s)
            i += 1
            if self.args.max and i >= self.args.max:
                break

        if self.args.stats:
            self.__print_stats() 
        elif self.args.print:
            self.__print_quotes()

    def __print_stats(self):
        count = len(self.quotes)
        print("count={}".format(count))

    def __print_quotes(self):
        for s in self.quotes_s:
            print(s)

    def _add_hashtags(self, qt, s):
        if 'tags' in qt:
            tags = qt['tags']
            for i, t in enumerate(tags):
                s2 = s
                if i == 0:
                    s2 += '\n'
                s2 += f' #{t}'
                if self.args.max_length and len(s2) > self.args.max_length:
                    break
                s = s2
        return s
