# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import yaml
from yaml.representer import SafeRepresenter

logger = logging.getLogger(__name__)

class folded_str(str): pass

class literal_str(str): pass

def change_style(style, representer):
    def new_representer(dumper, data):
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar
    return new_representer

represent_folded_str = change_style('>', SafeRepresenter.represent_str)
represent_literal_str = change_style('|', SafeRepresenter.represent_str)

yaml.add_representer(folded_str, represent_folded_str)
yaml.add_representer(literal_str, represent_literal_str)

def fold_if_necessary(text):
    if text.find(':') != -1:
        return folded_str(text)
    return text

def save_quotes(data, basename):
    ofname = '{}.saved.yml'.format(basename)
    for qt in data['quotes']:
        if 't' in qt:
            qt['t'] = fold_if_necessary(qt['t'])
        if 'c' in qt:
            qt['c'] = fold_if_necessary(qt['c'])
        if 'cw' in qt:
            qt['cw'] = sorted(qt['cw'])
        if 'tags' in qt:
            qt['tags'] = sorted(qt['tags'])
    with codecs.open(ofname, "w", encoding="utf-8") as f:
        f.write(yaml.dump(data, allow_unicode=True))
