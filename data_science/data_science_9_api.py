from collections import Counter

#API
#JSON: APIを利用するためには、データ間のやりとりがHTTPで行われるため、データを文字列をシリアライズ(直線に)変換するために用いる
import json

#ちょっとお試し
#jsonの辞書の型
serialized = """{ "title" : "Data Science Book",
				  "author" : "Joel Grus",
				  "publivcationYear" : 2014,
				  "topics" : ["data", "science", "data science"] }"""

#jsonの辞書をpythonの辞書に変換
deserialized = json.loads(serialized)
if "data science" in deserialized["topics"]:
	print(deserialized)





#認証のないgithubのapiの事例
import requests, json

endpoint = "https://api.github.com/users/joelgrus/repos"
repos = json.loads(requests.get(endpoint).text)#この時点でpythonの辞書になる

#例えば更新日時
#reposではunicode文字列なので、日付パーサーを使う
from dateutil.parser import parse

dates = [parse(repo["created_at"]) for  repo in repos]
month_counts = Counter(date.month for date in dates)
weekday_counts = Counter(date.weekday for date in dates)

#最後の5つのレポジトリの言語を調べる
last_5_repositories = sorted(repos,
							 key = lambda r: r["created_at"],
							 reverse = True)[:5]

last_5_language = [repo["language"] for repo in last_5_repositories]

print(last_5_language)



#Twitter API
"""
認証
Consumer(API)Key: 
ConsumerSecret: 

AccessToken: 
AccessTokenSecret: 
"""

#Search API：最近の一握りのツイートの結果を返す
from twython import Twython

#twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twython("PHMPYHD8zFgK6jK1jXscgLnFy", "AvefBrRTXShkS83iYgKCdsr2EAghWdK0Sd0yq8CBfVLZe6IHdd")


#”data science”を含むツイートを検索する
for status in twitter.search(q = '"data science"')["statuses"]:
	user = status["user"]["screen_name"].encode('utf-8')
	text = status["text"].encode('utf-8')
	print(user, ":", text)



#Streaming API：より多くのツイートをランダムに検索できる
from twython import TwythonStreamer

#データを大域変数に格納するのは稚拙だが、コードを簡単にできる
tweets = []

#streamとのやりとりを定義するクラス
class MyStreamer(TwythonStreamer):

	#twitterがデータを送った(成功)場合　＊dataは辞書型
	def on_success(self, data):
		if data['lang'] == "en":
			tweets.append(data)
			print("received tweet #", len(tweets))

			#十分なデータを得たら終了
			if  len(tweets) >= 1000:
				self.disconnect()

	def on_error(self, status_code, data):
		print(status_code, data)
		self.disconnect()

#stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream = MyStreamer("PHMPYHD8zFgK6jK1jXscgLnFy", "AvefBrRTXShkS83iYgKCdsr2EAghWdK0Sd0yq8CBfVLZe6IHdd",
					"983868618105536512-sHxOXWeBtKxNfFCsK2nyf25Oyq21qUe", "IcKvQMpi3GhEz9Mrz29QP9xNoRrTmDkBOTachs763xCo5")

#ツイートからキーワード'data'を含むものを収集
stream.statuses.filter(track = "data")

#全てのツイートからランダムに収集
stream.statuses.sample()


#最もよく使われているハッシュタグを調べる
top_hashtags = Counter(hashtag['text'].lower() for tweet in tweets for hashtag in tweet["entities"]["hashtags"])

print(top_hashtags.most_common(5))



