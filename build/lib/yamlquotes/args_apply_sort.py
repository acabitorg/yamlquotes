# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import random

logger = logging.getLogger(__name__)

def qt_key_rauthor(qt):
    """Key function to sort by author name reversed
    E.g. 'Dwight D. Eisenhower'.split()[::-1]
    ['Eisenhower', 'D.', 'Dwight']
    """
    return qt['a'].split()[::-1]

class SortArgsApplier():

    def __init__(self, args):
        self.args = args
        if self.args.sort_by_author and self.args.sort_randomly:
            logger.error("You think you're funny don't you? Well I don't")
            sys.exit(1)

    def apply(self, data):
        if self.args.sort_by_author:
            data['quotes'] = sorted(data['quotes'], key=qt_key_rauthor)
        elif self.args.sort_randomly:
            random.shuffle(data['quotes'])
