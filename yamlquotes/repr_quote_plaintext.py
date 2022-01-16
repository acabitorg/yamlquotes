# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import os

from .constants import EM_DASH
from .helpers import (format_text, get_lang)
from .image_utils import ImageText

logger = logging.getLogger(__name__)

def get_t(qt, defaults):
    txt = ''
    txt += format_text(qt['t'], get_lang(qt, defaults))
    txt += '\n'
    return txt 

def get_txr(qt, defaults):
    txt = ''
    if 'txr' in qt:
        #translation quotation marks always conform to default language
        txt += format_text(qt['txr'], defaults['l'])
        txt += '\n'
    return txt

def get_a(qt, defaults):
    return EM_DASH + qt['a']

def get_ac(qt, defaults):
    txt = ''
    if 'ac' in qt:
        txt += ', {}'.format(qt['ac'].rstrip())
    return txt

def get_d(qt, defaults):
    txt = ''
    if 'd' in qt:
        field_d = str(qt['d'])
        txt += ', ' + field_d
    return txt

def get_c(qt, defaults):
    txt = ''
    if 'c' in qt:
        txt += ', {}'.format(qt['c'].rstrip())
    return txt

def get_g(qt, defaults):
    txt = ''
    if 'g' in qt:
        field_g = qt['g']
        txt += ', ' + field_g
    return txt

def repr_quote_plaintext(qt, defaults):
    txt = ''
    txt += get_t(qt, defaults)
    txt += get_txr(qt, defaults)
    txt += get_a(qt, defaults)
    txt += get_ac(qt, defaults)
    txt += get_c(qt, defaults)
    txt += get_d(qt, defaults)
    txt += get_g(qt, defaults)
    return txt
