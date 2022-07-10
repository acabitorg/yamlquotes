# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import sys
from argparse import ArgumentError
import logging

log_level = logging.INFO
log_format = '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler("yamlquotes.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FilterArgsApplier():

    def __init__(self, args):
        self.args = args
        self.exclude_cw = []
        self.include_cw = []
        self.exclude_tags = [] 
        self.include_tags = []
        self.exclude_langs = []
        self.include_langs = []

        if args.exclude_cw != None:
            self.exclude_cw += args.exclude_cw.split(',')
            logging.info("exclude_cw=[%s]", ','.join(self.exclude_cw))
        if args.include_cw != None:
            self.include_cw += args.include_cw.split(',')
            logging.info("include_cw=[%s]", ','.join(self.include_cw))
        if args.exclude_tags != None:
            self.exclude_tags += args.exclude_tags.split(',')
            logging.info("exclude_tags=[%s]", ','.join(self.exclude_tags))
        if args.include_tags != None:
            self.include_tags += args.include_tags.split(',')
            logging.info("include_tags=[%s]", ','.join(self.include_tags))
        if args.exclude_langs != None:
            self.exclude_langs += args.exclude_langs.split(',')
            logging.info("exclude_langs=[%s]", ','.join(self.exclude_langs))
        if args.include_langs != None:
            self.include_langs += args.include_langs.split(',')
            logging.info("include_langs=[%s]", ','.join(self.include_langs))

        if set(self.include_tags) & set(self.exclude_tags):
            logger.error('--include-tags and --exclude-tags must\'t overlap, ya doofus')
            raise ArgumentError

        if set(self.include_langs) & set(self.exclude_langs):
            logger.error('--include-langs and --exclude-langs must\'t overlap, ya ding dong')
            raise ArgumentError

    def apply(self, data):
        self.__apply_exclude_cw_filters(data)
        self.__apply_include_cw_filters(data)
        self.__apply_exclude_any_cw_filter(data)
        self.__apply_exclude_tag_filters(data)
        self.__apply_include_tag_filters(data)
        self.__apply_exclude_lang_filters(data)
        self.__apply_include_lang_filters(data)

    def __apply_exclude_any_cw_filter(self, data):
        if not self.args.exclude_any_cw:
            return
        data['quotes'] = \
            [qt for qt in data['quotes'] if 'cw' not in 'qt']

    def __get_exclude_list(self, prop_name):
        if prop_name == 'cw':
            return self.exclude_cw
        elif prop_name == 'l':
            return self.exclude_langs
        elif prop_name == 'tags':
            return self.exclude_tags
        else:
            raise ArgumentError

    def __get_include_list(self, prop_name):
        if prop_name == 'cw':
            return self.include_cw
        elif prop_name == 'l':
            return self.include_langs
        elif prop_name == 'tags':
            return self.include_tags
        else:
            raise ArgumentError

    def __apply_exclude_filter(self, data, prop_name):
        quotes = []
        exclude_list = self.__get_exclude_list(prop_name)
        if len(exclude_list) == 0:
            return
        for qt in data['quotes']:
            if prop_name in qt and qt[prop_name] in exclude_list:
                #logger.info("Skipping excluded quote: %s", qt)
                continue
            quotes.append(qt)
        data['quotes'] = quotes

    def __apply_include_filter(self, data, prop_name):
        quotes = []
        include_list = self.__get_include_list(prop_name)
        if len(include_list) == 0:
            return
        for qt in data['quotes']:
            if prop_name not in qt:
                continue
            elif not qt[prop_name] in include_list:
                #logger.info("Skipping non-included quote because prop_name \"%s\" value \"%s\" not in include list: %s", prop_name, qt[prop_name], qt)
                continue
            quotes.append(qt)
        data['quotes'] = quotes

    def __apply_exclude_cw_filters(self, data):
        self.__apply_exclude_filter(data, 'cw')

    def __apply_exclude_tag_filters(self, data):
        self.__apply_exclude_filter(data, 'tags')

    def __apply_exclude_lang_filters(self, data):
        self.__apply_exclude_filter(data, 'l')


    def __apply_include_cw_filters(self, data):
        self.__apply_include_filter(data, 'cw')

    def __apply_include_lang_filters(self, data):
        self.__apply_include_filter(data, 'l')

    def __apply_include_tag_filters(self, data):
        self.__apply_include_filter(data, 'tags')
