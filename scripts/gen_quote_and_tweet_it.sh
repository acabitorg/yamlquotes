#!/usr/bin/env bash

cd $YAMLQUOTES_HOME
python3 -m yamlquotes -f yamlquotes/data/quotes.yml --sort-randomly --print --max 1 > ./scripts/twitter_bot_input.txt
cd scripts
DISPLAY=:0 python3 twitter_bot_selenium.py twitter_bot_input.txt
