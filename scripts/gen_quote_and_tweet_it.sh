#!/usr/bin/env bash

while :
do
	cd ..
	python3 -m yamlquotes -f yamlquotes/data/quotes.yml --sort-randomly --print --max 1 --max-length 180 --short > ./scripts/twitter_bot_input.txt
	cd scripts
	DISPLAY=:0 python3 twitter_bot_selenium.py twitter_bot_input.txt
	sleep 14400
done
