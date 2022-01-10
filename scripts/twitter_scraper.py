#!/usr/bin/env python3
# -*- coding: utf8 -*-

import time
from twython import Twython
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

#scrape twitter quotes into text format then use txt2yamlquotes.py to convert to yamlquotes
#see orig_quotes.txt for expected plaintext format

screen_name = 'AnarchQuotes'
count = 200
max_id = None

#basically this should go back in time, grabbing up to 200 tweets per request.
#max_id ensures we only get tweets older than the ones we already got.
while True:
    quotes_written = [] # prevent duplicates
    print(f'twitter get_user_timeline count={count} max_id={max_id}')
    data = twitter.get_user_timeline(
        screen_name=screen_name, tweet_mode='extended', 
        count=count, exclude_replies=True,
        max_id=max_id)
    for i, tweet in enumerate(data):
        if tweet['id'] == max_id:
            break # if we're getting duplicates, we already got everything there is to get
        max_id = tweet['id']
        full_text = tweet['full_text']
        # with this quotes bot (AnarchQuotes), the first line is always the author
        if full_text.find('\n') != -1:
            text, author = full_text.split('\n', 1)
            author = author.strip()
            text = text.strip()
            if text.find('"') != -1:
                text = text.split('"', 1)[1] #strip leftmost doublequote
            if text.find('"') != -1:
                text = text.rsplit('"', 1)[0] # strip rightmost doublequote
            text = f'“{text}”'
            if text not in quotes_written:
                #print(f"quote {i}:")
                print(f"{text}")
                print(f"\u2013 {author}")
                print("")
                quotes_written.append(text)
        else:
            print(f'Ignoring invalid tweet:\n"{full_text}"')
    time.sleep(1)
