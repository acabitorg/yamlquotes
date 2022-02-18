# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import re
import sys

from .constants import EM_DASH

logger = logging.getLogger(__name__)

ERR_MSG_INVALID = 'One or more validation errors occurred'

def validate_whitespace(qt, prop_name):
    '''Obviously we can and do trim trailing whitespace but the purpose of 
    erroring on trailing whitespace is to reduce unneccessary chars in the 
    yaml, keeping it consistent and making diffing easier.
    Note: This doesn't seem to be working as expected. Probably depends
    on which YAML string format is used.
    '''
    if prop_name in qt:
        val = qt[prop_name].rstrip('\r').rstrip('\n')
        if val.endswith(' '):
            logger.error(
                'Trailing whitespace in quote property \'%s\':\n"%s"', 
                prop_name, val)
            return False
    return True

def assert_property_type_list(qt, prop_name):
    if prop_name in qt:
        if type(qt[prop_name]) != list:
            logger.error(
                "Expected list type for quote property '{}'\n{}"
                .format(prop_name, qt))
            return False
    return True  

def assert_em_dash_escaped(qt, prop_name):
    if prop_name in qt:
        val = qt[prop_name]
        if val.find(EM_DASH) != -1:
            logger.error(
                "Quote property {} contains unescaped EM dash, must escape with '--'\n{}"
                .format(prop_name, qt))
            return False
    return True

def _get_dumb_quotes_err(qt, prop_name, quote_type):
    return "Quote property {}: contains dumb/straight {} quotes;" \
        .format(prop_name, quote_type) + \
        " use ‘ ’ for nested quotes.\n" + \
        "{}: {}".format(prop_name, qt[prop_name])

def assert_no_dumb_quotes(qt, prop_name):
    if prop_name in qt:
        val = qt[prop_name]
        if val.find('"') != -1:
            logger.error(_get_dumb_quotes_err(qt, prop_name, 'double'))
            return False
        elif re.search(r"[^\w]'\w.*\w'[^\w]", val):
            logger.error(_get_dumb_quotes_err(qt, prop_name, 'single'))
            return False
    return True

def _get_prohibited_dash_style_err(qt, prop_name, prohibited_pattern):
    return "Quote property {} contains prohibited dash style '{}';" \
        .format(prop_name, prohibited_pattern) + \
        " use '--' (with no leading or trailing space) instead\n" + \
        "{}: {}".format(prop_name, qt[prop_name])  

def assert_dash_style(qt, prop_name):
    """enforce consistent hyphenation style"""
    if prop_name in qt:
        val = qt[prop_name]
        prohibited_dash_patterns = [' - ', '- ', ' -']
        for prohibited_pattern in prohibited_dash_patterns:
            if val.find(prohibited_pattern) != -1:
                logger.error(_get_prohibited_dash_style_err(qt, prop_name, prohibited_pattern))
                return False
    return True


def validate_quote(qt):
    valid = True
    required = ['t', 'a']
    for r in required:
        if not r in qt:
            logger.error('Missing required field %s:', r)
            valid = False
    valid &= validate_whitespace(qt, 't')
    valid &= validate_whitespace(qt, 'txr')
    valid &= assert_em_dash_escaped(qt, 't')
    valid &= assert_em_dash_escaped(qt, 'txr')
    valid &= assert_no_dumb_quotes(qt, 't')
    valid &= assert_no_dumb_quotes(qt, 'txr')
    valid &= assert_dash_style(qt, 't')
    valid &= assert_dash_style(qt, 'txr')
    valid &= assert_property_type_list(qt, 'tags')
    valid &= assert_property_type_list(qt, 'cw')
    return valid

def validate_quotes(data):
    for qt in data['quotes']:
        if not validate_quote(qt):
            logger.error(ERR_MSG_INVALID)
            sys.exit(1)
