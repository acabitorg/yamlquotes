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
        self.models = {}
        lang_model_urls = {
            'eng': 'https://models.silero.ai/models/tts/en/v3_en.pt',
            'deu': 'https://models.silero.ai/models/tts/de/v3_de.pt',
            'fra': 'https://models.silero.ai/models/tts/fr/v3_fr.pt',
            'spa': 'https://models.silero.ai/models/tts/es/v3_es.pt',
            'rus': 'https://models.silero.ai/models/tts/ru/v3_1_ru.pt'
        }
        self.lang_speakers = {
            'eng': 'en_0',
            'deu': 'eva_k',
            'fra': 'fr_0',
            'spa': 'es_0',
            'rus': 'aidar',
        }
        self.random_speaker = True # overrides self.lang_speakers

        for lang, url in lang_model_urls.items():
            local_file = f'model-{lang}.pt'
            if not os.path.isfile(local_file):
                torch.hub.download_url_to_file(url, local_file)
            self.models[lang] = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
            self.models[lang].to(self.device)

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
        for i, qt in enumerate(self.quotes):
            self.__speak_quote(i, qt, outfmt)

    def __speak_quote(self, i, qt, outfmt=None):
        ofname = str(i).zfill(6)
        
        lang = 'eng'
        if 'l' in qt:
            lang = qt['l']
        text = qt['t'] + ', ' + qt['a']
        self.__speak_text(text, lang, '1.wav')

        if 'txr' in qt:
            lang = 'eng'
            text = qt['txr'] + ', ' + qt['a']
            self.__speak_text(text, lang, '2.wav')
            with open('alist', 'w') as f:
                f.write("file '1.wav'\nfile '2.wav'")
            os.system("ffmpeg -f concat -i alist -c copy out.wav")
            os.remove('1.wav')
            os.remove('2.wav')
            os.remove('alist')
        else:
            os.rename('1.wav', 'out.wav')

        if outfmt == 'wav':
            os.rename('out.wav', f'{ofname}.wav')
        elif outfmt == 'mp3':
            cmd = f"ffmpeg -i out.wav -ar 44100 -ac 2 -ab 192k -f mp3 {ofname}.mp3"
            logger.info('i=%d, outfmt=%s, cmd:=%s', i, outfmt, cmd)
            os.system(cmd)
            os.remove('out.wav')
        else:
            logger.error('invalid outfmt')

    def __speak_text(self, text, lang, ofname):
        sample_rate = 48000
        model = self.models['eng']
        speaker = self.lang_speakers['eng']        
        if lang in self.models.keys():
            model = self.models[lang]
        if lang in self.lang_speakers:
            speaker = self.lang_speakers[lang]
        if self.random_speaker:
            speaker = 'random'
        audio_paths = model.save_wav(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate)
        logger.info('model.save_wav complete. audiopaths=%s', repr(audio_paths))
        os.rename('test.wav', ofname)

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
