# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import sys

from .save_quotes import save_quotes
from .helpers import get_basename

logger = logging.getLogger(__name__)

class SaveArgsApplier():

    def __init__(self, args):
        self.args = args

    def apply(self, data):
        if self.args.save:
            save_quotes(data, get_basename(self.args))
            sys.exit(0)
