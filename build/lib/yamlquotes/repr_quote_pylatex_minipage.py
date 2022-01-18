# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import os
from pylatex import (LineBreak, MiniPage)
from pylatex.utils import italic, NoEscape

from .constants import EM_DASH
from .helpers import (format_text, get_lang)

logger = logging.getLogger(__name__)

def mp_append_t(mp, qt, defaults):
    mp.append(format_text(qt['t'], get_lang(qt, defaults)))
    mp.append(LineBreak())
    mp.append(NoEscape(r'\vspace{1mm}'))

def mp_append_txr(mp, qt, defaults):
    if 'txr' in qt:
        #translation quotation marks always conform to default language
        mp.append(format_text(qt['txr'], defaults['l']))
        mp.append(LineBreak())

def mp_append_a(mp, qt, defaults):
    mp.append(EM_DASH + qt['a'])

def mp_append_ac(mp, qt, defaults):
    if 'ac' in qt:
        mp.append(NoEscape(', \\textit{{{}}}'.format(qt['ac'].rstrip())))   

def mp_append_c(mp, qt, defaults):
    if 'c' in qt:
        mp.append(NoEscape(', \\textit{{{}}}'.format(qt['c'].rstrip())))    

def mp_append_d(mp, qt, defaults):
    if 'd' in qt:
        field_d = str(qt['d'])
        mp.append(', ' + field_d)

def mp_append_g(mp, qt, defaults):
    if 'g' in qt:
        field_g = qt['g']
        mp.append(', ' + field_g)

def repr_quote_pylatex_minipage(qt, defaults):
    mp = MiniPage(align='l')
    mp_append_t(mp, qt, defaults)
    mp_append_txr(mp, qt, defaults)
    mp_append_a(mp, qt, defaults)
    mp_append_ac(mp, qt, defaults)
    mp_append_c(mp, qt, defaults)
    mp_append_d(mp, qt, defaults)
    mp_append_g(mp, qt, defaults)
    return mp
