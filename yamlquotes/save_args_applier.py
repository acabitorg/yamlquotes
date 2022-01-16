# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import sys

from .save_quotes import save_quotes

class SaveArgsApplier():

    def __init__(self, args):
        self.args = args

    def apply(self, data):
        if args.save_sorted:
            save_quotes(data, basename)
            sys.exit(0)
