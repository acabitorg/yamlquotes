#!/usr/bin/env bash

cd ..
python3 -m yamlquotes -f yamlquotes/data/quotes.yml --sort-randomly --print --max 1 > ./scripts/twitter_bot_input.txt
cd scripts
./twitter_bot_selenium.py twitter_bot_input.txt
