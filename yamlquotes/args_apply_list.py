# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging

logger = logging.getLogger(__name__)

class ListArgsApplier():

    def __init__(self, args):
        self.args = args

    def apply(self, data):
        if self.args.list_cw:
            self.__list_cw(data)
        elif self.args.list_langs:
            self.__list_langs(data)
        elif self.args.list_tags:
            self.__list_tags(data)

    def __get_qt_prop_type(self, prop_name):
        if prop_name == 'cw' or prop_name == 'tags':
            return 'list'
        return 'str'

    def __list_qt_prop_vals(self, data, prop_name):
        vals = set()
        for qt in data['quotes']:
            if prop_name in qt:
                if self.__get_qt_prop_type(prop_name) == 'list':
                    vals.update(qt[prop_name])
                else:
                    vals.add(qt[prop_name])
        logger.debug('\n'.join(vals))

    def __list_cw(self, data):
        self.__list_qt_prop_vals(data, 'cw')

    def __list_langs(self, data):
        self.__list_qt_prop_vals(data, 'l')

    def __list_tags(self, data):
        self.__list_qt_prop_vals(data, 'tags')
