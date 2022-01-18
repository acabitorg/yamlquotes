#!/usr/bin/env python3
# -*- coding: utf8 -*-

# sudo apt install -y geckodriver-firefox
# pip install selenium

import os
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait 
import sys
import time

from auth_selenium import (
    username,
    password
)


xpath_login_button = \
'/html/body/div[1]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div'
xpath_login_button2 = \
'/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a/div'
xpath_login_button3 = \
'/html/body/div/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/a[2]/div'
xpath_username_textfield = \
'/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[5]/label/div/div[2]/div/input'
xpath_next_button = \
'/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[6]/div'
xpath_password_textfield = \
'/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[3]/div/label/div/div[2]/div[1]/input'
xpath_password_login_button = \
'/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div'
xpath_tweet_textfield = \
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div'
xpath_tweet_button = \
'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span'

def send_keys_delay(element, keys, delay):    
    for c in keys:
        element.send_keys(c)
        time.sleep(delay)

def sleep_humanly():
    time.sleep(0.10 + random.random() * 0.25)

def send_keys_humanly(element, keys):
    for c in keys:
        element.send_keys(c)
        sleep_humanly()

def click_humanly(element):
    sleep_humanly()
    element.click()

def wait_until_find_by_xpath(driver, xpath):
    return WebDriverWait(driver, 10).until(
            lambda x: x.find_element_by_xpath(xpath)) 

def twitter_login():
    driver = webdriver.Firefox()
    driver.get('https://twitter.com')
    try:
        element = wait_until_find_by_xpath(driver, xpath_login_button) 
        click_humanly(element)
    except Exception as e:
        try:
            element = wait_until_find_by_xpath(driver, xpath_login_button2)
            click_humanly(element)
        except Exception as e:
            element = wait_until_find_by_xpath(driver, xpath_login_button3)
            click_humanly(element)

    element = wait_until_find_by_xpath(driver, xpath_username_textfield)
    send_keys_humanly(element, username)

    element = wait_until_find_by_xpath(driver, xpath_next_button)
    click_humanly(element)

    element = wait_until_find_by_xpath(driver, xpath_password_textfield)
    send_keys_humanly(element, password)

    element = wait_until_find_by_xpath(driver, xpath_password_login_button)
    click_humanly(element)
    return driver

def tweet(driver, s):
    element = wait_until_find_by_xpath(driver, xpath_tweet_textfield)
    click_humanly(element)
    actions = ActionChains(driver)
    actions.send_keys(s)
    actions.perform()
    element = wait_until_find_by_xpath(driver, xpath_tweet_button)
    click_humanly(element)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('missing argument')
        sys.exit(1)
    elif len(sys.argv) > 2:
        print('unexpected argument')
        sys.exit(1)
    else:
        path = sys.argv[1]
        txt = ''
        with open(path, 'r') as f:
            txt = f.read()
        driver = twitter_login()
        tweet(driver, txt)
