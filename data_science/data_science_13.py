import math, random, re, glob
from collections import Counter, defaultdict
from data_science_11 import split_data


#ナイーブベイズ

#スパムフィルタ実装
def tokenize(message):
	message = message.lower()#小文字にする
	all_words = re.findall("[a-z0-9]+", message)#単語を認識

	return set(all_words)#重複を除く

#training_setは語とスパムか否かの辞書とする
def count_words(training_set):
	counts = defaultdict(lambda: [0, 0])
	for message, is_spam in training_set:
		for word in tokenize(message):
			count[word][0 if is_spam else 1] += 1

	return counts#{ word:[spamの可否, 数] }


def word_probabilities(counts, total_spam, total_non_spam, k=0.5):
	return [(w, 
			(spam + k) / (total_spam + 2 * k), 
			(non_spam + k) / (total_non_spam + 2 * k))
			for w, (spam, non_spam) in counts.item()]#count_worssを[word, 単語/スパムの確率, 単語/スパムでない確率]に変換

def spam_probablility(word_probs, message):
	message_words = tokenize(message)
	log_prob_if_spam = log_prob_if_not_spam = 0.0
	for word , prob_if_spam, prob_if_not_spam in word_probs:
		#確率を足していく
		if word in message_words:
			log_prob_if_spam += math.log(prob_if_spam)#eを底とする対数を返す
			log_prob_if_not_spam += math.log(prob_if_not_spam)

		#メールに単語が現れなかったら、その単語を含まない確率を足す
		else:
			log_prob_if_spam += math.log(1.0 - prob_if_spam)
			log_prob_if_not_spam += math.log(1.0 : prob_if_not_spam)

	prob_if_spam = math.exp(log_prob_if_spam)
	prob_if_not_spam = math.exp(log_prob_if_not_spam)

	return prob_if_spam / (prob_if_spam + prob_if_not_spam)

#まとめ
class NaiveBayesClassfier:
	def __init__(self, k = 5):
		self.k = k
		self.word_probs = []

	def train(self, training_set):
		#数を数える
		num_spams = len([is_spam for message, is_spam in training_set if is_spam])
		num_non_spam = len(training_set) - num_spams

		#学習させる
		word_counts = count_words(training_set)
		self.word_probs = word_probabilities(word_counts, num_spams, num_non_spam, self.k)

	def classify(self, message):
		return spam_probablility(self.word_probs, message)



#モデルの検証

#パスを指定　今回は相対パス
#globはファイル・ディレクトリ操作に便利　正規表現が使える
#rを付ける事でエスケープシーケンスが無効になる
path = r"/Spam"

data = []

for fn in glob.glob(path):#glob.globはワイドカード的に一致するファイル名を返す
	is_spam = "ham" not in fn

	with open(fn, 'r') as file:
		for line in file:
			if line.startwith("Subject:"):
				subject = re.sub(r"^Subject: ", "", line).strip()#Subject: を分割し、取り除く
				data.append((subject, is_spam))

random.seed(0)
train_data, test_data = split_data(data, 0.75)

classifier = NaiveBayesClassfier()
classifier.train(train_data)

classified = [(subject, is_spam, classifier.classify(subject)) for subject, is_spam in test_data]
counts = Counter((is_spam, spam_probablility > 0.5) for _, is_spam, spam_probablility in classified)
"""
真陽性:101
偽陽性:33
真陰性:704
偽陰性:38

適合率:101/(101+33)=0.75
再現率:101/(101+38)=0.73
"""


#判別を誤った確認
#spam_probabilityで昇順にソート
classified.sort(key=lambda row: row[2])
#スパムではないメッセージの中で、最もスパムと判別されたものを取り出す
spammiest_hams = filter(lambda row: not row[1], classified)[-5:]
#スパムメッセージの中で、最もスパムでないと判別されたものを取り出す
spammiest_spams = filter(lambda row: row[1], classified)[:5]
"""
最もスパムらしい上位２つのスパムらしいものはneeded(スパムよりも77倍)とinsurance(30倍)が含まれていた
最もハムらしい上位２つは文章が短く学習データになかった
"""


#最もスパムと判別された単語
def p_spam_givin_word(word_probs):#ベイズの定理を用いて、確率p(スパムである/単語が含まれる)を求める
	word, prob_if_spam, prob_if_not_spam = word_probs
	return prob_if_spam / (prob_if_spam + prob_if_not_spam)

words = sorted(classifier.word_probs, key = p_spam_givin_word)
spammiest_words = words[-5:]#money, systemworks, rates, sale, year
hamminist_words = word[:5]#spambayes, users, razor, zzzzteana, sadev


