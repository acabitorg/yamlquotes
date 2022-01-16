# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import argparse
import codecs
import logging.config
import logging
import math
import os
import sys
assert sys.version_info >= (3, 9)
import yaml
from yaml.representer import SafeRepresenter

with open('logging.yml','rt') as f:
    config=yaml.safe_load(f.read())
    f.close()
logging.config.dictConfig(config)

from .constants import (OUTDIR)
from .filter_args_applier import FilterArgsApplier
from .list_args_applier import ListArgsApplier
from .load_quotes import load_quotes
from .make_args_applier import MakeArgsApplier
from .save_args_applier import SaveArgsApplier
from .sort_args_applier import SortArgsApplier
from .util_args_applier import UtilArgsApplier
from .validate_args_applier import ValidateArgsApplier

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

oper_group.add_argument('--save-sorted', action='store_true', \
    help='Save sorted yaml to \'_sorted.yaml\' file')

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

#operation modifiers:
parser.add_argument('--no-flip', action='store_true', default=False, \
    help='Don\'t flip every other page vertically')

args = parser.parse_args()

def main():
    data = load_quotes(args.file)

    if not os.path.exists(OUTDIR):
        os.mkdir(OUTDIR)

    app = ValidateArgsApplier(args)
    app.apply(data)

    app = SortArgsApplier(args)
    app.apply(data)

    app = SaveArgsApplier(args)
    app.apply(data)

    app = FilterArgsApplier(args)
    app.apply(data)

    app = UtilArgsApplier(args)
    app.apply(data)
    
    app = MakeArgsApplier(args)
    app.apply(data)
    
    app = ListArgsApplier(args)
    app.apply(data)

if __name__ == '__main__':
    main()
