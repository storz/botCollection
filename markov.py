#!/usr/local/bin python
# -*- coding: utf-8 -*-

from urllib import urlopen
from xml.etree.ElementTree import ElementTree
from xml.dom import minidom
import tweepy
import random
import re
import json
from collections import defaultdict

token = json.loads(open('./config/twitterOAuth.json', 'r').read())
config = json.loads(open('./config/markov.json', 'r').read())

wordlists = []
table = {}
sentence = []

def cut(word):
    wlist = []
    source = u'http://jlp.yahooapis.jp/MAService/V1/parse?appid='+config["appid"]+u'&results=ma&response=surface&sentence='+word
    xml = minidom.parse(file=urlopen(source.encode('utf-8')))
    elm = xml.getElementsByTagName('surface')
    for i, w in enumerate(elm):
        wlist.append(w.childNodes[0].data)

    return wlist

def markov1(wordlist):
    w1 = ""
    for word in wordlist:
        if w1:
            if w1 not in table:
                table[w1] = []
            table[w1].append(word)
        w1 = word

def generate1(head):
    count = 0
    sentence = head
    w1 = head
    while len(sentence) < 140:
        if w1 in table:
            tmp = random.choice(table[w1])
            sentence += tmp
            w1 = tmp
        else:
            return sentence
            break

    return sentence

def markov2(wordlist):
    w1 = ""
    w2 = ""
    for word in wordlist:
        if w1 and w2:
            if (w1, w2) not in table:
                table[(w1, w2)] = []
            table[(w1, w2)].append(word)
        w1, w2 = w2, word

def generate2(head1,head2):
    count = 0
    sentence = head1+head2
    w1, w2 = head1, head2
    while len(sentence) < 140:
        if (w1, w2) in table:
            tmp = random.choice(table[(w1, w2)])
            sentence += tmp
            w1, w2 = w2, tmp
        else:
            return sentence
            break
        
    return sentence

def markov3(wordlist):
    w1 = ""
    w2 = ""
    w3 = ""
    for word in wordlist:
        if w1 and w2 and w3:
            if (w1, w2, w3) not in table:
                table[(w1, w2, w3)] = []
            table[(w1, w2, w3)].append(word)
        w1, w2, w3 = w2, w3, word

def generate3(head1, head2, head3):
    count = 0
    sentence = head1+head2+head3
    w1, w2, w3 = head1, head2, head3
    while len(sentence) < 140:
        if (w1, w2, w3) in table:
            tmp = random.choice(table[(w1, w2, w3)])
            sentence += tmp
            w1, w2, w3 = w2, w3, tmp
        else:
            return sentence
            break
        
    return sentence

def markov4(wordlist):
    w1 = ""
    w2 = ""
    w3 = ""
    w4 = ""
    for word in wordlist:
        if w1 and w2 and w3 and w4:
            if (w1, w2, w3, w4) not in table:
                table[(w1, w2, w3, w4)] = []
            table[(w1, w2, w3, w4)].append(word)
        w1, w2, w3, w4 = w2, w3, w4, word

def generate4(head1, head2, head3, head4):
    count = 0
    sentence = head1+head2+head3+head4
    w1, w2, w3, w4 = head1, head2, head3, head4
    while len(sentence) < 140:
        if (w1, w2, w3, w4) in table:
            tmp = random.choice(table[(w1, w2, w3, w4)])
            sentence += tmp
            w1, w2, w3, w4 = w2, w3, w4, tmp
        else:
            return sentence
            break
        
    return sentence

def get_oauth(token):
    auth = tweepy.auth.OAuthHandler(token['consumer_key'], token['consumer_secret'])
    auth.set_access_token(token['access_token_key'], token['access_token_secret'])
    return auth

if __name__ == '__main__':
    save = open("tweetlist.txt", "w")
    auth = get_oauth(token['observe'])
    api = tweepy.API(auth_handler=auth)
    for p in tweepy.Cursor(api.user_timeline).items(config["get"]):
        body = p.text
        result = cut(body)
        if len(result) > 1:
            wordlists.append(result)

    for wordlist in wordlists:
        if config["markovchain"] == 1:
            markov1(wordlist)
        elif config["markovchain"] == 2:
            markov2(wordlist)
        elif config["markovchain"] == 3:
            markov3(wordlist)
        elif config["markovchain"] == 4:
            markov4(wordlist)

    for i in range(config["size"]):
        h = random.choice(wordlists)
        #sentence = generate1(h[0])
        if config["markovchain"] == 1:
            sentence = generate1(h[0])
        elif config["markovchain"] == 2:
            sentence = generate2(h[0],h[1])
        elif config["markovchain"] == 3:
            sentence = generate3(h[0],h[1],h[2])
        elif config["markovchain"] == 4:
            sentence = generate4(h[0],h[1],h[2],h[3])
        
        save.write(sentence.encode('utf-8')+"\n")
        i += 1

    save.close()