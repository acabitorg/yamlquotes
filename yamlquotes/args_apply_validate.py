# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import sys

from .validate_quotes import validate_quotes

logger = logging.getLogger(__name__)

class ValidateArgsApplier():

    def __init__(self, args):
        self.args = args

    def apply(self, data):
        if self.args.validate:
            validate_quotes(data)
            print('Valid')
            sys.exit(0)
