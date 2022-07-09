# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import os

from .helpers import get_defaults
from .repr_quote_plaintext import repr_quote_plaintext

logger = logging.getLogger(__name__)

class UtilArgsApplier():

    def __init__(self, args):
        self.args = args
        self.defaults = {}
        self.quotes = []
        self.quotes_s = []
        self.espeak_args = '-v en -a 100 -p 0 -s 120'

    def apply(self, data):
        self.defaults = get_defaults(data)
        i = 0
        for qt in data['quotes']:
            s = repr_quote_plaintext(qt, self.defaults, short=self.args.short)
            if self.args.max_length and len(s) >= self.args.max_length:
                continue
            if self.args.hashtags:
                s = self._add_hashtags(qt, s)
            self.quotes.append(qt)
            self.quotes_s.append(s)
            i += 1
            if self.args.max and i >= self.args.max:
                break

        if self.args.stats:
            self.__print_stats() 
        elif self.args.print:
            self.__print_quotes()
        elif self.args.speak:
            self.__speak_quotes()
        elif self.args.speak_wav:
            self.__speak_quotes(outfmt="wav")
        elif self.args.speak_mp3:
            self.__speak_quotes(outfmt="mp3")

    def __print_stats(self):
        count = len(self.quotes)
        print("count={}".format(count))

    def __print_quotes(self):
        for s in self.quotes_s:
            print(s)

    def __speak_quotes(self, outfmt=None):
        for i, s in enumerate(self.quotes_s):
            self.__speak_quote(i, s, outfmt)

    def __speak_quote(self, i, s, outfmt=None):
        with open('/tmp/tmp.txt', 'w') as f:
            f.write(s)
        ofname = str(i).zfill(6)
        cmd = f'espeak {self.espeak_args} -f /tmp/tmp.txt'
        if outfmt == 'wav':
            cmd += f' --stdout > {ofname}.wav'
        elif outfmt == 'mp3':
            cmd += f' --stdout | ffmpeg -i - -ar 44100 -ac 2 -ab 192k -f mp3 {ofname}.mp3'
        logger.info('i: %d outfmt: %s cmd: %s', i, outfmt, cmd)
        os.system(cmd)

    def _add_hashtags(self, qt, s):
        if 'tags' in qt:
            tags = qt['tags']
            for i, t in enumerate(tags):
                s2 = s
                if i == 0:
                    s2 += '\n'
                s2 += f' #{t}'
                if self.args.max_length and len(s2) > self.args.max_length:
                    break
                s = s2
        return s
