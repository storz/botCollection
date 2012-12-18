#-*- encoding: utf-8 -*-
require 'rubygems'
require 'twitter'
require 'user_stream'
require 'json'

oauth = JSON.load(open('./config/twitterOAuth.json'))
config = JSON.load(open('./config/packman.json'))

userid = config['screen_name'] #アカウント名(screen_name)を入力
queue = config['queue'] #保持するポストの数を入力
tl = []
posted = []
post = ''

Twitter.configure do |config| #以下の4つに投稿したいアカウントのキー・トークンを入力
  config.consumer_key = oauth['post']['consumer_key']
  config.consumer_secret = oauth['post']['consumer_secret']
  config.oauth_token = oauth['post']['access_token_key']
  config.oauth_token_secret = oauth['post']['access_token_secret']
end

UserStream.configure do |config| #以下の4つにタイムラインを監視したいアカウントのキー・トークンを入力
  config.consumer_key = oauth['observe']['consumer_key']
  config.consumer_secret = oauth['observe']['consumer_secret']
  config.oauth_token = oauth['observe']['access_token_key']
  config.oauth_token_secret = oauth['observe']['access_token_secret']
end

tweets = Twitter.user_timeline(userid) #現在の自分のツイートを取得
for tweet in tweets
  said = tweet.text
  t = said.gsub(/\\u([\da-fA-F]{4})/) {|m| [$1].pack("H*").unpack("n*").pack("U*")}
  posted.push(t)
end

client = UserStream.client
client.user do |status|
  if tl.size == 0 then
    p('start')
  end
  if status.text != nil && /RT|\@/ !~ status.text then #RTと@付きポストのコピペは除外
    if tl.index(status.text) then #キューに保持したTimeLineから探索
      if status.user.screen_name != userid && !posted.index(status.text) then
        body = status.text
        posted.push(body)
        post = body.gsub(/\\u([\da-fA-F]{4})/) {|m| [$1].pack("H*").unpack("n*").pack("U*")}
        Twitter.update(post)
        p('Posted')
      end
    end
  end

  if tl.size == queue then
    tl.shift #キューから一番古いものを取り出す
  end

  tl.push(status.text) #取得したツイートをキューに入れる
end