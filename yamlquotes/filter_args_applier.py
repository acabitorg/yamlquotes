# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

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
        if args.include_cw != None:
            self.include_cw += args.include_cw.split(',')
        if args.exclude_tags != None:
            self.exclude_tags += args.exclude_tags.split(',')
        if args.include_tags != None:
            self.include_tags += args.include_tags.split(',')
        if args.exclude_langs != None:
            self.exclude_langs += args.exclude_langs.split(',')
        if args.include_langs != None:
            self.include_langs += args.include_langs.split(',')

        if set(self.include_tags) & set(self.exclude_tags):
            logger.error('--include-tags and --exclude-tags must\'t overlap, ya doofus')
            print_usage()
            sys.exit(1)

        if set(self.include_langs) & set(self.exclude_langs):
            logger.error('--include-langs and --exclude-langs must\'t overlap, ya ding dong')
            print_usage()
            sys.exit(1)

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
        elif prop_name == 'langs':
            return self.exclude_langs
        elif prop_name == 'tags':
            return self.exclude_tags
        sys.exit(1)

    def __get_include_list(self, prop_name):
        if prop_name == 'cw':
            return self.include_cw
        elif prop_name == 'langs':
            return self.include_langs
        elif prop_name == 'tags':
            return self.include_tags
        sys.exit(1)

    def __apply_exclude_filter(self, data, prop_name):
        quotes = []
        exclude_list = self.__get_exclude_list(prop_name)
        for qt in data['quotes']:
            if prop_name in qt and \
            set(qt[prop_name]) & set(exclude_list):
                continue
            quotes.append(qt)
        data['quotes'] = quotes

    def __apply_include_filter(self, data, prop_name):
        quotes = []
        include_list = self.__get_include_list(prop_name)
        for qt in data['quotes']:
            if len(include_list) > 0:
                if prop_name in qt:
                    if not set(qt[prop_name]) & \
                    set(include_list):
                        continue
                else:
                    continue
            quotes.append(qt)
        data['quotes'] = quotes

    def __apply_exclude_cw_filters(self, data):
        self.__apply_exclude_filter(data, 'cw')

    def __apply_exclude_tag_filters(self, data):
        self.__apply_exclude_filter(data, 'tags')

    def __apply_exclude_lang_filters(self, data):
        self.__apply_exclude_filter(data, 'langs')


    def __apply_include_cw_filters(self, data):
        self.__apply_include_filter(data, 'cw')

    def __apply_include_lang_filters(self, data):
        self.__apply_include_filter(data, 'langs')

    def __apply_include_tag_filters(self, data):
        self.__apply_include_filter(data, 'tags')
