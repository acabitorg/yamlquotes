#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import codecs

class folded_str(str): pass

class literal_str(str): pass

def change_style(style, representer):
    def new_representer(dumper, data):
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar
    return new_representer

import yaml
from yaml.representer import SafeRepresenter

represent_folded_str = change_style('>', SafeRepresenter.represent_str)
represent_literal_str = change_style('|', SafeRepresenter.represent_str)

yaml.add_representer(folded_str, represent_folded_str)
yaml.add_representer(literal_str, represent_literal_str)

def fold_if_necessary(text):
    if text.find(':') != -1:
        return folded_str(text)
    return text

UNICODE=True

def strip_quotes(text):
    text = text.lstrip('\u201C')
    text = text.rstrip('\u201D')
    return text

def strip_guillemets(text):
    text = text.lstrip('\xAB') #open
    text = text.rstrip('\xBB') #close
    return text

def convert_special(text):
    text = text.replace('\u2026', '...')
    text = text.replace('\u2019', "'")
    text = text.replace('\u201C', '"')
    text = text.replace('\u201D', '"')
    text = text.replace('\u2018', "'")
    text = text.replace('\u2019', "'")
    text = text.replace('\u2014', '--') #EM dash
    text = text.replace('\u2013', '--') #EN dash
    text = text.strip('\u200E') #left-to-right mark
    return text

if len(sys.argv) != 3:
    print('Usage: {} <input.txt> <output.yml>'.format(sys.argv[0]))
ifname = sys.argv[1]
ofname = sys.argv[2]
with open(ifname) as f:
    data = {'defaults':{'l':'eng'},'quotes':[]}
    item = {'t': ''}
    for line in f.readlines():
        print(f'line = "{line}"')
        if line.strip() == '':
            if item['t'] != '':
                data['quotes'].append(item)
            item = {'t': ''}
            item['tags'] = ['anarchism', 'politics', 'socialism']
        elif line.startswith('—') or line.startswith('\u2013'):
            author = line[1:].strip()
            print('---Author: \n' + author + '\n')
            item['a'] = convert_special(author)
        else:
            if 'a' in item:
                context = line.strip()
                if len(context) > 0:
                    item['c'] = fold_if_necessary(convert_special(context))
            else:
                text = line.strip()
                if len(text) > 0:
                    if text.startswith('\uFEFF'):
                        continue
                    if text.startswith("DISCLAIMER:"):
                        continue
                    if text.startswith('Q:') or text.startswith('A:'):
                        continue
                    if text.startswith('\xAB'):
                        item['l'] = 'fra'
                        text = strip_guillemets(text)
                    print('---Text: \n' + text + '\n')
                    try:
                        text = strip_quotes(text)
                        text = convert_special(text)
                        if item['t'] != '':
                            item['txr'] = text
                        else:
                            text = text.strip()
                            item['t'] = fold_if_necessary(text)
                    except Exception as e:
                        print(f'Exception {e}')
                        continue
    if UNICODE:
        with codecs.open(ofname, "w", encoding="utf-8") as f:
            f.write(yaml.dump(data, allow_unicode=True))
    else:
        with open(ofname, 'w') as of:
            yaml.dump(data, of, encoding='latin1')
