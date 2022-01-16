#!/usr/bin/env python3
# -*- coding: utf8 -*-
 
import random
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

from yamlquotes.helpers import get_defaults
from yamlquotes.load_quotes import load_quotes
from yamlquotes.repr_quote_plaintext import repr_quote_plaintext

data = load_quotes('../yamlquotes/data/quotes.yml')
q = random.choice(data['quotes'])
txt = repr_quote_plaintext(q, get_defaults(data))
print(txt)

try:
    twitter.update_status(status=txt)
except TwythonError as e:
    print(e)
