#!/usr/bin/env python3
# -*- coding: utf8 -*-
 
import time
from twython import Twython, TwythonError
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

screen_name = 'acabit.org'

from yamlquotes import (load_quotes, repr_quote_plaintext)

data = load_quotes.load_quotes('../yamlquotes/data/quotes.yml')


#for i, q in enumerate(data['quotes']):
#    print('{} {}'.format(i, q['t']))

try:
    twitter.update_status(status='Test 42')
except TwythonError as e:
    print(e)
