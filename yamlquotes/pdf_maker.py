# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import os
from pylatex import (Document, LineBreak, NoEscape, Section)

from .constants import OUTDIR
from .helpers import get_defaults
from .repr_quote_pylatex_minipage import repr_quote_pylatex_minipage

logger = logging.getLogger(__name__)

def append_mp(mp, doc):
    mp.append(LineBreak())
    mp.append(NoEscape(r'\vspace{1mm}'))
    doc.append(mp)
    doc.append(LineBreak())
    doc.append(NoEscape(r'\vspace{1mm}'))

def fill_document(data, doc): 
    with doc.create(Section('Selected Quotes')):
        for qt in data['quotes']:
            mp = repr_quote_pylatex_minipage(qt, get_defaults(data))
            append_mp(mp, doc);

def convert_pdf_to_booklet_pdfjam(name, no_flip):
    infile = os.path.join(OUTDIR, "{}.pdf".format(name))
    suffix = 'book'
    pdfjam_args = '--booklet true '
    if no_flip:
        pdfjam_args = '--no-twoside '
        suffix += '-noflip'
    else:
        suffix += '-flip'
    cmd = "pdfjam --landscape --outfile {} --suffix {} " \
        .format(OUTDIR, suffix) + \
        "--paper letter --no-tidy --nup 2x1 --scale 1.0 {} {}" \
        .format(pdfjam_args, infile)
    logger.debug('cmd: %s', cmd)
    if os.system(cmd) != 0:
        sys.exit(1)

def make_pdf(data, name):
    """Note that a 1in margin translates to a 0.5in margin in the 2-up booklet"""
    logger.debug(f'make_pdf name={name}')
    geometry_options = {
        'tmargin': '0.75in',
        'bmargin': '0.75in',
        'lmargin': '0.75in',
        'rmargin': '0.75in',
        'paperheight': '8.5in',
        'paperwidth': '5.5in'
    }
    default_filepath = os.path.join(OUTDIR, name)
    logger.debug(f'default_filepath={default_filepath}')
    doc = Document(default_filepath, geometry_options=geometry_options, font_size='large')

    fill_document(data, doc)
    doc.generate_pdf(clean_tex=False)
    doc.generate_tex()

def make_pdf_book(data, name, no_flip):
    logger.debug(f'make_pdf_book name={name}')
    make_pdf(data, name)
    convert_pdf_to_booklet_pdfjam(name, no_flip)
