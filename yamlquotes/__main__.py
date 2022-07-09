# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import argparse
import logging.config
import logging
import os
import sys
assert sys.version_info >= (3, 9)
import yaml

with open('logging.yml','rt') as f:
    config=yaml.safe_load(f.read())
    f.close()
logging.config.dictConfig(config)

from .args_apply_filter import FilterArgsApplier
from .args_apply_list import ListArgsApplier
from .args_apply_make import MakeArgsApplier
from .args_apply_save import SaveArgsApplier
from .args_apply_sort import SortArgsApplier
from .args_apply_util import UtilArgsApplier
from .args_apply_validate import ValidateArgsApplier
from .constants import (OUTDIR)
from .load_quotes import load_quotes

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='yamlquotes.py')

#input:
parser.add_argument('-f', '--file', type=str,
                    help='<quotes_filename.yml>', required=True)

#filter modifiers:
parser.add_argument('--include-tags', type=str, \
    help='Only include quotes with the specified tag(s) (command-separated values)')
parser.add_argument('--exclude-tags', type=str, \
    help='Exclude quotes with the specified tag(s) (command-separated values) ' + \
    'Takes precedence over --include-tags')

parser.add_argument('--include-langs', type=str, \
    help='Only include quotes in the specified language(s) (command-separated values)')
parser.add_argument('--exclude-langs', type=str, \
    help='Exclude quotes in the specified language(s) (command-separated values) ' + \
    'Takes precedence over --include-langs')

cw_group = parser.add_mutually_exclusive_group()
cw_group.add_argument('--exclude-cw', type=str, \
    help='Exclude quotes with the specified content-warning(s) (command-separated values)')
cw_group.add_argument('--exclude-any-cw', action='store_true', \
    help='Exclude quotes with any content-warnings')
cw_group.add_argument('--include-cw', type=str, \
    help='Only include quotes with the specified content-warning(s) (command-separated values)')

#sort modifiers:
parser.add_argument('--sort-by-author', action='store_true', \
    help='Sort output by author name, reversed')
parser.add_argument('--sort-randomly', action='store_true', \
    help='Random shuffle')

#operation:
oper_group = parser.add_mutually_exclusive_group(required=True)

oper_group.add_argument('--validate', action='store_true', \
    help='Validate quotes yaml and exit')

oper_group.add_argument('--make-pdf', action='store_true', \
    help='Make pdf from quotes yaml')
oper_group.add_argument('--make-pdf-book', action='store_true', \
    help='Make pdf booklet from quotes yaml using pdfjam/pdfpages')
oper_group.add_argument('--make-png-images', action='store_true', \
    help='Make png images from quotes yaml')
oper_group.add_argument('--make-png-video-frames', action='store_true', \
    help='Make png video frames for ffmpeg from quotes yaml')

oper_group.add_argument('--save', action='store_true', \
    help='Save sorted and/or filtered yaml to \'.saved.yaml\' file')

oper_group.add_argument('--list-tags', action='store_true', \
    help='List all tags in the quotes file')
oper_group.add_argument('--list-cw', action='store_true', \
    help='List all content-warnings in the quotes file')
oper_group.add_argument('--list-langs', action='store_true', \
    help='List all languages in the quotes file')

oper_group.add_argument('--stats', action='store_true', \
    help='Display statistics about the the quotes file')
oper_group.add_argument('--print', action='store_true', \
    help='Print quotes')
oper_group.add_argument('--speak', action='store_true', \
    help='Speak quotes (output to speaker)')
oper_group.add_argument('--speak-wav', action='store_true', \
    help='Speak quotes (output to WAV file(s)')
oper_group.add_argument('--speak-mp3', action='store_true', \
    help='Speak quotes (output to MP3 file(s)')

#operation modifiers:
parser.add_argument('--no-flip', action='store_true', default=False, \
    help='Don\'t flip every other page vertically')
parser.add_argument('--max', nargs='?', const=1, type=int, \
    help='Maximum number of quotes')
parser.add_argument('--max-length', nargs='?', const=180, type=int, \
    help='Maximum length of quote(s) in characters')
parser.add_argument('--short', action='store_true', default=False, \
    help='Text and author only, no context')
parser.add_argument('--hashtags', action='store_true', default=False, \
    help='Add as many hashtags as possible without exceeding max-length')

args = parser.parse_args()

def main():
    data = load_quotes(args.file)

    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)

    app = ValidateArgsApplier(args)
    app.apply(data)

    app = SortArgsApplier(args)
    app.apply(data)

    app = FilterArgsApplier(args)
    app.apply(data)

    app = SaveArgsApplier(args)
    app.apply(data)

    app = UtilArgsApplier(args)
    app.apply(data)
    
    app = MakeArgsApplier(args)
    app.apply(data)
    
    app = ListArgsApplier(args)
    app.apply(data)

if __name__ == '__main__':
    main()
