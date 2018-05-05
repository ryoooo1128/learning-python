#データの操作
import math, random, csv
import matplotlib.pyplot as plt
import dateutil.parser
from collections import Counter, defaultdict
from functools import partial, reduce

from data_science_04 import shape, get_row, get_column, make_matrix, vector_mean, vector_sum, dot, magnitude, vector_subtract, scalar_multiply
from data_science_05 import correlation, standard_deviation, mean
from data_science_06 import inverse_normal_cdf
from data_science_08 import maximize_batch


#一次元データの
#様々な数値を出した時に良い理解ができなかった時に、ヒストグラムを使う
def bucketize(point, bucket_size):#バケツ(範囲)にpointが入るか入らないかの試行
	return bucket_size * math.floor(point / bucket_size)#floor(x): x以下の最大の整数

def make_histogram(points, bucket_size):#バケツにいくつ入ったか数える
	return Counter(bucketize(point, bucket_size) for point in points)

def plot_histogram(points, bucket_size, title = ""):
	histogram = make_histogram(points, bucket_size)
	plt.bar(histogram.keys(), histogram.values(), width = bucket_size)
	plt.title(title)
	plt.show()



#求めた数値が役に立たない事例
#どちらのデータもおよそ平均0・標準偏差58だが、全く異なる
def compare_two_distributions():
	random.seed(0)#ランダム生成器を初期化

	uniform = [200 * random.random() - 100 for _ in range(10000)]

	normal = [57 * inverse_normal_cdf(random.random()) for _ in range(10000)]

	plot_histogram(uniform, 10, "Uniform Histogram")
	plot_histogram(normal, 10, "Normal Histogram")



#二次元データ
def random_normal():
	#標準誠意分布に従う無作為の数を返す
	return inverse_normal_cdf(random.random())

xs = [random_normal() for _ in range (1000)]
ys1 = [x + random_normal() / 2 for x in xs]
ys2 = [-x + random_normal() / 2 for x in xs]

#ys1, ys2をヒストグラムで表すと、平均と標準偏差が同じなため、ほとんど同じになる
#結合分布で表すと全く異なる
def scatter():
	plt.scatter(xs, ys1, marker = ".", color = "black", label = "ys1")
	plt.scatter(xs, ys2, marker = ".", color = "grey", label = "ys2")
	plt.xlabel("xs")
	plt.ylabel("ys")
	plt.legend(loc = 9)
	plt.title("Very Different Joint Distributions")
	plt.show()

#相関係数でもわかる
print(correlation(xs, ys1))#0.9
print(correlation(xs, ys2))#-0.9




#多次元データ
#相関行列：i次元目とj次元目の相関係数を行列で表したもの
def correlation_matrix(data):
	_, num_columns = shape(data)#num_columnはdataの横(行)の長さ

	def matrix_entry(i, j):
		return correlation(get_column(data, i), get_column(data,j))#ger_columnはi,j列目のデータを取得する

	return make_matrix(num_columns, num_columns, matrix_entry)


#散布図行列：次元数が多くない場合に有効
def make_scatterplot_matrix():

	#まずランダムデータを作る
	num_points = 100

	def random_row():
		row = [None, None, None, None]
		row[0] = random_normal
		row[1] = -5 * row[0] + random_normal()
		row[2] = row[0] + row[1] + 5 * random_normal()
		row[3] = 6 if row[2] > -2 else 0
		return row
	random.seed(0)
	data = [random_row() for _ in range(num_points)]


	 #ここからプロットする
	_, num_columns = shape(data)
	fig, ax = plt.subplot(num_columns, num_columns)#subplot: 別々にプロットした図を１つに表す

	for i in range(num_columns):
	 	for j in range(num_columns):

	 		#x軸のcolumn_j, y軸のcolumn_iの位置に散布図を描画する
	 		if i != j: ax[i][j].scatter(get_column(data, j), get_column(data, i))

	 		#i == jであれば列名を描画する　annotate: グラフにテキストを追加(テキスト, 座標, )
		 	else : ax[i][j].annotate("series" + str(i), (0.5, 0.5), xycoords = "axes fracton", ha = "center", va = "center")

		 	#１番端以外は軸ラベル(メモリ)を表示しない
		 	if i < num_columns - 1: ax[i][j].xaxis.set_visible(False)
		 	if i > 0: ax[i][j].yaxis.set_visible(False)

	#左上と右下はテキストのためメモリが間違っているため、訂正
	ax[-1][-1].set_xlim(ax[0][-1].get_xlim())
	ax[0][0].set_ylim(ax[0][1].get_ylim())

	plt.show()





#データの整理と変換
#csv.readerを用いる時にラップしておくことで、エラーを減らす
def parse_row(input_row, parsers):#複数のパーサーのリストから入力の列ごとに適切なものを利用する Noneはリストに何もしない意
	return [parser(value) if parser is not None else value for value, parser in zip(input_row, parsers)]

def parse_rows_with(reader, parsers):#readerをラップして入力の隠れるにパーサを適用
	for row in readers:
		yield parse_row(row, parsers)

#ヘルパー関数：誤ったデータがある場合にerrorではなく、Noneが返るようにする
def try_or_none(f):
	def f_or_none(x):
		try: return f(x)
		except: return None
	return f_or_none

#try_or_noneを使えるようにparse_rowを再定義
def parse_row(input_row, parsers):
	return [try_or_none(parser)(value) if parser is not None else value for value, parser in zip(input_row, parsers)]

#事例
data =[]

with open("__comma_delimited_stock_price.csv") as f:
	reader = csv.reader(f)
	for line in parse_rows_with(reader, [dateutil.parser.parse, None, float]):
		data.append(line)

for row in data:
	if any(x is None for x in row):
		print(row)



#csv.DictReaderのヘルパー関数
def try_parse_field(field_name, parser_dict):
	parser = parser_dict.get(field_name)#対応する値がなければNoneが返る
	if parser is not None:
		return try_or_none(parser)(value)
	else:
		return value

def parse_dict(input_dict, parser_dict):
	return { field_name : try_parse_field(field_name, value, parser_dict) for field_name, value in input_dict.iteritems()}



#以下のような辞書を扱うことを考える
#AAPLの終値の最高値を求める
"""
data = [{'cloosing_price' : 102.06
		 'date' : datetime.datetime(2014, 8, 29, 0, 0)
		 'symbol' : 'AAPL'
		 #...
		 }]
"""
max_aapl_price = max(row["cloosing_price"] for row in data if row["symbol"] == "AAPL")

#各銘柄に適用することを考える
#銘柄ごとにグループ化する
by_symbol = defaultdict(list)#：by_symbol = []
for row in data:
	by_symbol[row["symbol"]].append(row)
#銘柄ごとに、辞書内包を使って最高値をもとめる
max_price_by_symbol = { symbol : max(row["cloosing_price"]
									 for row in grouped_rows)
						for symbol, grouped_rows in by_symbol.iteritems}








