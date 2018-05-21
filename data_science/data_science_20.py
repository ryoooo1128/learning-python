import math, random, re
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
import requests


#自然言語処理

#ワードクラウド
data = [ ("big data", 100, 15), ("Hadoop", 95, 25), ("Python", 75, 50),
         ("R", 50, 40), ("machine learning", 80, 20), ("statistics", 20, 60),
         ("data science", 60, 70), ("analytics", 90, 3),
         ("team player", 85, 85), ("dynamic", 2, 90), ("synergies", 70, 0),
         ("actionable insights", 40, 30), ("think out of the box", 45, 10),
         ("self-starter", 30, 50), ("customer focus", 65, 15),
         ("thought leadership", 35, 35)]

def plot_resume(plt):
	def text_size(total):
		return 8 + total / 200 * 20

	for word, job_popularity, resume_popularity in data:
		plt.text(job_popularity, resume_popularity, word, ha = 'center', va = 'center', size = size_text(job_popularity + resume_popularity))

	plt.xlabel('Popularity on Job Posting')
	plt.ylabel('Popularity on Resumes')
	plt.axis([0, 100, 0, 100])
	plt.xticks()
	plt.yticks()

	plt.show()



#n-gramモデル

#ヘルパー関数１：アポストロフィを通常のものに戻す
def fix_unicode(text):
	return text.replace(u"\u2019", "'")

#ヘルパー関数２：テキストがどこで終わるかわかるようにする　単語とピリオドの列に分割する
url = "http://radar.oreilly.com/2010/06/what-is-data-science.html"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html5lib')

content = soup.find("div", "entry-content")
regex = r"[\w'] + [\.]"#単語またはピリオドにマッチする正規表現

document = []

for paragraph in content("p"):
	words = re.findall(regex, fix_unicode(paragraph.text))
	document.extend(words)

#bi-gramモデル
bigrams = zip(document, document[1:])
transitions = defaultdict(list)
for prev, current in bigrams:
	transitions[prev].append(current)

def generate_using_bigrams():
	current = "."
	result = []

	while True:
		next_word_candidates = transitions[current]#bi-gramsでcurrentの次に来る単語
		current = random.choice(next_word_candidates)#無作為に１つ選ぶ
		result.append(current)#結果のリストに追加
		if current == ".":#.だったら終了
			return " ".join(result)


#tri-gramモデル；２つ先まで見るため、ましになる
trigrams = zip(document, document[1:], document[2:])
trigram_transitions = defaultdict(list)
starts = []

for prev, current, next in trigrams:
	if prev == ".":#直前が.ならそこが文章の始まり
		starts.append(current)

	trigram_transitions[(prev, current)].append(next)

def generate_using_trigrams():
	current = random.choice(starts)
	prev == "."

	result = [current]
	while True:
		next_word_candidates = trigram_transitions[(prev, current)]
		next_word = random.choice(next_word_candidates)

		prev, current = current, next_word
		result.append(current)

		if current == ".":
			return " ".join (result)


#文法
grammar = {
        "_S"  : ["_NP _VP"],
        "_NP" : ["_N",
                 "_A _NP _P _A _N"],
        "_VP" : ["_V",
                 "_V _NP"],
        "_N"  : ["data science", "Python", "regression"],
        "_A"  : ["big", "linear", "logistic"],
        "_P"  : ["about", "near"],
        "_V"  : ["learns", "trains", "tests", "is"]
    }

def is_terminal(token):
	return token[0] != "_"

def expand(grammer, tokens):
	for i, token in enumerate(tokes):
		#終端記号の場合は次に進む
		if is_terminal(token): continue

		#終端記号を見つけたので無作為に生成ルールのいずれかと置き換える
		replacement = random.choice(grammer[token])

		if is_terminal(replacement):
			tokens[i] = replacement
		else:
			tokens = tokens[:i] + replacement.split() + tokens[(i + 1):]

		#新しいトークンのリストにexpandを適用する
		return expand(grammer, tokens)

	return tokens

def generate_sentence(grammer):
	return expand(grammer, ["_S"])



#余談：ギブスサンプリング：標本の生成が難しい条件付き分布の一部が既知である多次元分布に対して標本を生成する方法

#サイコロを２つ投げる
def roll_a_die():
	return random.choice([1, 2, 3, 4, 5, 6])
def direct_sample():
	d1 = roll_a_die()
	d2 = roll_a_die()
	return d1, d1 + d2#それぞれx, yとする
#この時のyの条件付き分布はx+1, x+2, x+3, x+4, x+5, x+6のいずれかになり単純
def random_y_given_x(x):
	return x + roll_a_die()


#より複雑な場合
def random_x_given_y(y):
	if y <= 7:#yが7以下であれば最初の目は1, 2, ...(y-1)のいずれかである
		return random.randrange(1, y)
	else:#yが7以上であれば最初の目は(y-6), (y-5), ...6のいずれかである
		return random.randrange(y - 6, 7)

def gibbs_sample(num_iters = 100):
	x, y = 1, 2#はじまりの値は適当
	for _ in range(num_iters):
		x = random_x_given_y(y)
		y = random_y_given_x(x)
	return x, y

def compare_distributions(num_samples = 1000):
	counts = defaultdict(lambda: [0, 0])
	for _ in range(num_samples):
		counts[gibbs_sample()][0] += 1
		counts[direct_sample()][1] += 1

	return counts



#トピックモデリング
def sample_from(weignts):
	total = sum(weights)
	rnd = total * random.random()
	for i, w in enumerate(weights):
		rnd -= w#weight[0]+...+weight[i] >= rndとなる
		if rnd <= 0: return i#最小のiを返す


documents = [
    ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
    ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
    ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
    ["R", "Python", "statistics", "regression", "probability"],
    ["machine learning", "regression", "decision trees", "libsvm"],
    ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
    ["statistics", "probability", "mathematics", "theory"],
    ["machine learning", "scikit-learn", "Mahout", "neural networks"],
    ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
    ["Hadoop", "Java", "MapReduce", "Big Data"],
    ["statistics", "R", "statsmodels"],
    ["C++", "deep learning", "artificial intelligence", "probability"],
    ["pandas", "R", "Python"],
    ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
    ["libsvm", "regression", "support vector machines"]
]

#k=4のトピックを探す

#文書ごとのカウンターをリスト
document_topic_counts = [Counter() for _ in documents]
#トピックごとのカウンターをリスト
topic_word_counts = [Counter() for _ in range(K)]
#トピックごとの総数リスト
topic_counts = [0 for _ in range(K)]
#ドキュメントごとの総数のリスト
document_lengths = map(len, document)
#ユニークな単語の数
district_words = set(word for document in documents for word in document)
W = len(district_words)
#文書の数
D = len(documents)

#documents[3]の中でトピック1に関連づいた単語の数が次の式でわかる
ducument_topic_counts[3][1]
#トピック2に関連づいたnlpの数
document[2]['nlp']



#条件付き確率を求めていく

#document[d]の中でtopicに割り当てられた単語の割合(スムージング項が含まれる)
def p_topic_given_document(topic, d, alpha = 0.1):
	return ((document_topic_counts[d][topic] + alpha) / (document_lengths[d] + K * alpha))

#topicに割り当てられた単語の割合
def p_word_given_topic(word, topic, beta = 0.1):
	return ((topic_word_counts[topic][word] + beta / (topic_counts[topic] + W * beta)))

#与えられt文章とその中の単語に対するk番目のトピックの重みを返す
def topic_weight(d, word, k):
	return p_word_given_topic(word, k) * p_topic_given_document(k, d)

def choose_new_topic(d, word):
	return sample_from([topic_weight(d, word, k) for k in range(k)])



random.seed(0)
document_topics = [[random.randrange(K) for word in document] for document in documnets]

for d in range(D):
	for word, topic in zip(documents[d], document_topics[d]):
		document_topic_counts[d][topic] += 1
		topic_word_counts[topic][word] += 1
		topic_counts[topic] += 1

for iter in range(1000):
	for d in range(D):
		for i, (word, topic) in enumerate(zip(documents[d], document_topics[d])):

			#重みに影響を与えないために、まず単語とトピックを除外する
			document_topic_counts[d][topic] -= 1
			topic_word_counts[topic][word] -= 1
			topic_counts[topic] -= 1
			document_lengths[d] -= 1

			#重みに従い新しいトピックを割り当てる
			new_topic = choose_new_topic(d, word)
			document_topics[d][i] = new_topic

			#新しいトピックでカウンターを更新する
			document_topic_counts[d][new_topic] += 1
			topic_word_counts[new_topic][word] += 1
			topic_counts[new_topic] += 1
			document_lengths[d] += 1

for k, word_counts in enumerate(topic_word_counts):
	for word, count in word_counts.common():
		if count > 0: print(k, word, count)


topic_names = ["Big Data and programming language",
			   "Python and statistics",
			   "databases",
			   "machine learning"]

for document, topic_count in zip(documents, document_topic_counts):
	print(document)
	for topic, count in topic_counts.most_common():
		if count > 0:
			print(topic_names[topic], count)

"""
['Hadoop', 'Big Data', 'HBase', 'Java', 'Spark', 'Storm', 'Cassandra']
Big Data and programming language 4 databeses 3
['NoSOL', 'MongoDB', 'Cassandra', 'HBase', 'Postgres']
databases 5
['Python', 'sckit-learn', 'scipy', 'numpy', 'statsmodels', 'pandas']
Python and statistics 5 machine learning
"""
