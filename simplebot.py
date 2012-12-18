#!/usr/local/bin python
# -*- coding: utf-8 -*-

import tweepy
import random
import json

token = json.loads(open('./config/twitterOAuth.json', 'r').read())

def get_oauth(token):
    auth = tweepy.auth.OAuthHandler(token['consumer_key'], token['consumer_secret'])
    auth.set_access_token(token['access_token_key'], token['access_token_secret'])
    return auth

if __name__ == '__main__':
    auth = get_oauth(token['observe'])
    api = tweepy.API(auth_handler=auth)
    txt = open("tweetlist.txt", "rt").read()
    lines = txt.split('\n')
    say = random.choice(lines)
    api.update_status(say)