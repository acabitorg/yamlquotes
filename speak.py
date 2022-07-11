#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright 2022 Acabit.org <https://github.com/acabitorg/yamlquotes>
# License: GPLv3 <https://www.gnu.org/licenses/gpl-3.0.html>

import argparse
import logging
import os
import time
import torch

log_level = logging.INFO
log_format = '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.FileHandler("speak.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='yamlquotes.py')

#input:
parser.add_argument('-l', '--lang', type=str,
                    help='<lang>', required=True)
parser.add_argument('-t', '--text', type=str,
                    help='<text>', required=True)
parser.add_argument('-o', '--output-filename', type=str,
                    help='<output-filename>', required=True)

args = parser.parse_args()

class Speaker():
    def __init__(self, device):
        self.device = torch.device(device)
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

    def speak(self, text, lang, ofname):
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
        logger.info('renamed test.wav to %s', ofname)

if __name__ == '__main__':
    speaker = Speaker(device='cpu')
    speaker.speak(args.text, args.lang, args.output_filename)
