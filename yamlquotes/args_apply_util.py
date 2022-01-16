# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging

logger = logging.getLogger(__name__)



class UtilArgsApplier():

    def __init__(self, args):
        self.args = args

    def apply(self, data):
        if self.args.stats:
            self.__print_stats(data) 
        elif self.args.print:
            self.__print_quotes(data)

    def __print_stats(self, data):
        quotes = data['quotes']
        count = len(quotes)
        print("count={}".format(count))

    def __print_quotes(self, data):
        quotes = data['quotes']
        for i, qt in enumerate(quotes):
            print('{}: {}'.format(i+1, qt))
