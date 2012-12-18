#!/usr/local/bin python
# -*- coding: utf-8 -*-

import urllib2
import lxml.html
import json
from tweepy.auth import OAuthHandler
from tweepy.api import API

token = json.loads(open('./config/twitterOAuth.json', 'r').read())
config = json.loads(open('./config/checkakucom.json', 'r').read())

def check_price(item):
    url = u'http://kakaku.com/item/'
    html = urllib2.urlopen(url+item+u'/pricehistory/').read()
    dom = lxml.html.fromstring(html)
    name = dom.xpath('//h1/a')[0].text_content()
    name = name.replace(u' の価格推移グラフ', '')
    now_price = dom.xpath('//td/strong')[31].text_content()
    try:
        load = open(item+'.txt', 'r')
        old_price = load.read()
        load.close()
    except:
        result = name+u'の記録を開始しました。現在の値段は'+now_price+u'です '+url+item
    else:
        compare = dom.xpath('//td[@nowrap]')[31].text_content()
        if now_price == old_price.decode('utf-8'):
            result = name+u'の現在の値段は'+now_price+u'で、値段に変動はありません '+url+item
            #result = ''
        else:
            if int(compare.replace(',','')) > 0:
                result = name+u'現在の値段は'+now_price+u'で、前回の変動から'+compare+u'円上昇しました '+url+item
            elif int(compare.replace(',','')) < 0:
                result = name+u'現在の値段は'+now_price+u'で、前回の変動から'+compare+u'円下降しました '+url+item


    save = open(item+'.txt', 'w')
    save.write(now_price.encode('utf-8'))
    return result

def get_oauth(token):
    auth = OAuthHandler(token['consumer_key'], token['consumer_secret'])
    auth.set_access_token(token['access_token_key'], token['access_token_secret'])
    return auth

if __name__ == '__main__':
    for i in config['item']:
        detail = check_price(i)
        if not detail == '':
            auth = get_oauth(token['post'])
            api = API(auth_handler=auth)
            api.update_status(detail)
            #print detail.encode('utf-8')