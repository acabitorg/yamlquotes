# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
from os.path import (splitext, basename)

from .constants import EM_DASH

logger = logging.getLogger(__name__)

def get_basename(args):
	return splitext(basename(args.file))[0]

def get_defaults(data):
    defaults = {'l':'eng'}
    if 'defaults' in data:
        defaults = data['defaults']
    return defaults

def get_qt_beg(l):
    if l == 'fra':
        return '«\u00A0'
    else:
        return '“'

def get_qt_end(l):
    if l == 'fra':
        return '\u00A0»'
    else:
        return '”'

def expand_markup(t):
    return t.replace('--', EM_DASH)

def format_text(t, l):
    return get_qt_beg(l) + expand_markup(t.rstrip()) + get_qt_end(l)

def get_lang(qt, defaults):
    l = defaults['l']
    if 'l' in qt:
        l = qt['l']    
    return l
