import math, random, re, datetime
from collections import defaultdict, Counter
from functools import partial
from naive_bayes import tokenize


#MapReduce

#map関数を使わない単語カウント
def word_count_old(documents):
	return Counter(word for document in documents for word in tokenize(document))

def wc_mapper(document):#各単語ごとに(word, 1)を出力する
	for word in document:
		yield (word, 1)

def wc_reducer(word, counts):#単語の数を合計する
	yield (word, sum(counts))

def word_count(documents):#入力した単語をMapReduceを使って数える
	#グループ分けした結果を格納する場所
	collector = defaultdict(list)

	for document in ducuments:
		for word, count in wc_mapper(document):
			collector[word].append(count)

	return [output, for word, count in collector.items() for output in wc_reducer(word, count)]

"""
data = ["data science", "big data", "science fiction"]
wc_mapper(data) = collector = { "data":[1, 1], "science":[1, 1], "big":[1], "fiction":[1] }
wc_reducer(collector) = [("data", 2), ("science", 2), ("big", 1), ("fiction", 1)]
"""


def map_reduce(inputs, mapper, reducer):
	#mapperとreducerを使って、inputに対してMapReduceを行う
	collerctor = defaultdict(list)

	for input in inputs:
		for key, value in mapper(input):
			collector[key].append(value)

	return [output for key, values in collector.items() for output in reducer(key, values)]

word_counts = map_reduce(documents, wc_mapper, wc_reducer)


def recuce_values_using(aggregation_fn, key, values):#キーバリューにaggregation_fnを適用してreduceする
	yield (key, aggregation_fn(values))

def values_reducer(aggregation_fn):
	return partial(reduce_values_using, aggregation_fn)


sum_reducer = values_reducer(sum)
max_reducer = values_reducer(max)
min_reducer = values_reducer(min)
count_distinct_reducer = values_reducer(lambda values: len(set(values)))


#事例：近況更新の分析
"""
データの例
{ "id" : 1,
  "user name" : "joelgrus",
  "text" : "Is anyone interested in a data science book?",
  "created_at" : datetime.datetime(2013, 12, 21, 11, 47, 0),
  "liked_by" : ["data_guy", "data_gal", "mike"] }
"""
def data_science_day_mapper(status_update):
	if "data science" in status_update["text"].lower:
		day_of_week = status_update["created_at"].weekday()
		yield (day_of_week, 1)

data_sciennce_days = map_reduce(status_updates, data_science_day_mapper, sum_reducer)

def words_per_user_mapper(status_update):
	user = status_update["username"]
	for word in tokenize(status_update["text"]):
		yield(user, (word, 1))

def most_popular_word_reducer(user, words_and_count):#(単語,単語数)のデータを与えると頻出単語を返す
	word_counts = Counter()

	for word, count in words_and_count:
		word_counts[word] += count

	word, count = word_counts.most.common(1)[0]

	yield (user, (word, count))


user_words = map_reduce(status_updates, words_per_user_mapper, most_popular_word_reducer)


#近況にリンクしているユニークなユーザー数を数える
def liker_mapper(status_update):
	user = status_update["username"]
	for liker in status_update["liked_by"]:
		yield (user, liker)

distinct_likers_per_user = map_reduce(status_updates, liker_mapper, count_distinct_reducer)



#事例：行列操作
def matrix_multiply_mapper(m, element):
	"""
	m = (Aの列, Bの行)
	element = (行列名, i, j, 値)
	"""
	name, i, j, value = element

	if name == "A":#A_ijは各C_ik, k=1..mのそれぞれに対する合計のj番目要素
		for k in range(m):#他のC_ikと共にグループ化する
			yield ((k, j), (j, value))

	else:#B_ijは各C_kjそれぞれに対する合計のj番目要素
		for k in range(m):#他のC_kj要素と共にグループ化する
			yield((k, j), (i, value))

def matrix_multiply_reducer(m, key, indexed_values):
	results_by_index = defaultdict(list)
	for index, value in indexed_values:
		results_by_index[index].append(value)

	sum_product = sum(results[0] * results[1] for results in results_by_index.values() if len(results) == 2)

	if sum_product != 0.0:
		yield (key, sum_product)

"""
２つの行列を想定
A = [[3, 2, 0],
	 [0, 0, 0]]

B = [[4, -1, 0],
	 [10, 0, 0],
	 [0, 0, 0]]
"""
entries = [("A", 0, 0, 3), ("A", 0, 1, 2),
		   ("B", 0, 0, 4), ("B", 0, 1, -1), ("B", 1, 0, 10)]
mapper = partial(matrix_multiply_mapper, 3)
reducer = partial(matrix_multiply_reducer, 3)

map_reduce(entries, mapper, reducer)#[((0, 1), -3), ((0, 0), 32)]

