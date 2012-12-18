botCorrection
=============

概要
-----

1. simplebot.py
  tweetlist.txtからランダムに一つ投稿するだけの単純なbotです。

2. markov.py
  特定のユーザーのツイートからマルコフ連鎖によりtweetlist.txtを生成します。1.と組み合わせて使います。

3. packman.rb
  タイムラインをUserstreamで監視し、コピペツイートが行われた場合に自分も同じ内容をツイートします。こいつだけRubyです。

4. checkakucom.py
  価格.comの値段をチェックし、価格変動をツイートします。


使い方
---

configディレクトリ内の設定ファイルを書き換えます。<br>
まず、twitterOAuth.jsonに、投稿したいユーザー・監視したいユーザーそれぞれのapplication key、access token等を入力してください。<br>

1. simplebot.py
  特に設定は必要ありません。cronで回すだけです。

2. markov.py
  markov.jsonにappid(Yahoo!WebAPIのアプリケーションID)と、markovchain(マルコフ連鎖数)、get(種となる取得ツイート数)、size(生成する文章の個数)を入力してください。これもcronで回すと発言に新鮮味が増します。

3. packman.rb
  packman.jsonにscreen_name(監視するユーザー、即ち自分自身のscreen_name)とqueue(コピペ検知をする最新ツイート件数)を入力してください。起動している間ずっと監視を続けます。

4. checkakucom.py
  checkakucom.jsonにitem(監視したい商品のID http://kakaku.com/item/***/ の***部分)を入力してください。複数入力可です。cromで回してください。[商品ID].txtが出力されます。


必要ライブラリ
---

1. simplebot.py: tweepy
2. markov.py: tweepy
3. packman.rb: twitter, userstream
4. checkakucom.py: tweepy, lxml
