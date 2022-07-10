# -*- coding: utf8 -*-

# Copyright 2021 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import logging
import os
import torch

from .helpers import get_defaults
from .repr_quote_plaintext import repr_quote_plaintext

logger = logging.getLogger(__name__)

class UtilArgsApplier():

    def __init__(self, args):
        self.args = args
        self.defaults = {}
        self.quotes = []
        self.quotes_s = []
        self.device = torch.device('cuda')
        torch.set_num_threads(4)
        local_file = 'model-en.pt'
        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file('https://models.silero.ai/models/tts/en/v3_en.pt', local_file)
        self.model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        self.model.to(self.device)

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
        ofname = str(i).zfill(6)
        sample_rate = 48000
        speaker='en_0'
        audio_paths = self.model.save_wav(text=s,
                            speaker=speaker,
                            sample_rate=sample_rate)
        logger.info('i=%d, model.save_wav complete', i)
        if outfmt == 'wav':
            os.rename('test.wav', f'{ofname}.wav')
        elif outfmt == 'mp3':
            cmd = f"ffmpeg -i test.wav -ar 44100 -ac 2 -ab 192k -f mp3 {ofname}.mp3"
            logger.info('i=%d, outfmt=%s, cmd:=%s', i, outfmt, cmd)
            os.system(cmd)
            os.remove('test.wav')
        else:
            logger.error('invalid outfmt')

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
