#データの操作
import math, random, csv
import matplotlib.pyplot as plt
import dateutil.parser
from collections import Counter, defaultdict
from functools import partial, reduce

from data_science_04 import shape, get_row, get_column, make_matrix, vector_mean, vector_sum, dot, magnitude, vector_subtract, scalar_multiply
from data_science_05 import correlation, standard_deviation, mean
from data_science_06 import inverse_normal_cdf
from data_science_08 import maximize_batch, maximize_stochastic


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
	return { field_name : try_parse_field(field_name, value, parser_dict) for field_name, value in input_dict.items()}



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
by_symbol = defaultdict(list)#：by_symbol = {a:[], b:[], ...}
for row in data:
	by_symbol[row["symbol"]].append(row)
#銘柄ごとに、辞書内包を使って最高値をもとめる
max_price_by_symbol = { symbol : max(row["cloosing_price"]
									 for row in grouped_rows)
						for symbol, grouped_rows in by_symbol.items}

def picker(field_name):#辞書から列を取り出す
	return lambda row: row[field_name]


def pluck(field_name, rows):
	return map(picker(field_name), rows)#mapは関数とシーケンス(値)を引数にとる


def group_by(grouper, rows, value_transform = None):
	grouped = defaultdict(list)
	for row in rows:
		grouped[grouper(row)].append(row)

		if value_transform is None:
			return grouped
		else:
			return { key : value_transform(rows)
					 for key, rows in grouped.items()}

max_price_by_symbol = group_by(picker("symbol"), data, lambda rows: max(pluck("cloosing_price", rows)))




#価格が最も動いた日を調べる
#1.値を利用して、日付順に並べる　2.前日と当日をzipで組み合わせる　3.動いた差をリストにする
def percent_price_change(yesterday, today):
	return today["cloosing_price"] / yesterday["cloosing_price"] - 1

def day_over_day_change(grouped_rows):
	offerd = sorted(grouped_rows, key = picker("data"))
	return [{ "symbol" : today["symbol"],
			  "date" : today["date"]
			  "change" : percent_price_change(yesterday, today) }
			  for yesterday, today in zip(ordered, ordered[1:])]

#key:銘柄 value:前日比の辞書
change_by_symbol = group_by(picker("symbol"), data, day_over_day_change)
#全ての前日比の辞書をリストに格納
all_changes = [change for changes in change_by_symbol.values() for change in changes]

#最高値と最低値を求める
max(all_changes, key = picker("change"))
min(all_changes, key = picker("change"))



def combine_pct_changes(pct_changes1, pct_changes2):
	return (1 + pct_changes1) * (1 + pct_changes2) - 1

def overall_change(changes):
	return reduce(combine_pct_changes, pluck("change", changes))

overall_change_by_month = group_by(lambda row: row['date'].month, all_changes, overall_change)



#スケールの変更

#単位が異なる場合は比較できない
#それぞれの単位で平均0標準偏差1にデータを変更する

def scale(data_matrix):#各列の平均と偏差を返す
	num_rows, num_cols = shape(data_matrix)
	means = [mean(get_column(data_matrix, j))
			 for j in range(num_cols)]
	stdevs = [standard_deviation(get_column(data_matrix, j))
			  for j in range(num_rows)]

	return means, stdevs


def rescale(data_matrix):#平均0標準偏差1に入力データのスケールを修正
	means, stdevs = scale(data_matrix)
	def rescaled(i, j):
		if stdevs[j] > 0:
			return (data_matrix[i][j] - means[j]) / means[j]
		else:#偏差が０のものは変更しない
			return data_matrix[i][j]
	num_rows, num_cols = shape(data_matrix)

	return make_matrix(num_rows, num_cols, rescaled)








X = [[20.9666776351559,-13.1138080189357],
    [22.7719907680008,-19.8890894944696],
    [25.6687103160153,-11.9956004517219],
    [18.0019794950564,-18.1989191165133],
    [21.3967402102156,-10.8893126308196],
    [0.443696899177716,-19.7221132386308],
    [29.9198322142127,-14.0958668502427],
    [19.0805843080126,-13.7888747608312],
    [16.4685063521314,-11.2612927034291],
    [21.4597664701884,-12.4740034586705],
    [3.87655283720532,-17.575162461771],
    [34.5713920556787,-10.705185165378],
    [13.3732115747722,-16.7270274494424],
    [20.7281704141919,-8.81165591556553],
    [24.839851437942,-12.1240962157419],
    [20.3019544741252,-12.8725060780898],
    [21.9021426929599,-17.3225432396452],
    [23.2285885715486,-12.2676568419045],
    [28.5749111681851,-13.2616470619453],
    [29.2957424128701,-14.6299928678996],
    [15.2495527798625,-18.4649714274207],
    [26.5567257400476,-9.19794350561966],
    [30.1934232346361,-12.6272709845971],
    [36.8267446011057,-7.25409849336718],
    [32.157416823084,-10.4729534347553],
    [5.85964365291694,-22.6573731626132],
    [25.7426190674693,-14.8055803854566],
    [16.237602636139,-16.5920595763719],
    [14.7408608850568,-20.0537715298403],
    [6.85907008242544,-18.3965586884781],
    [26.5918329233128,-8.92664811750842],
    [-11.2216019958228,-27.0519081982856],
    [8.93593745011035,-20.8261235122575],
    [24.4481258671796,-18.0324012215159],
    [2.82048515404903,-22.4208457598703],
    [30.8803004755948,-11.455358009593],
    [15.4586738236098,-11.1242825084309],
    [28.5332537090494,-14.7898744423126],
    [40.4830293441052,-2.41946428697183],
    [15.7563759125684,-13.5771266003795],
    [19.3635588851727,-20.6224770470434],
    [13.4212840786467,-19.0238227375766],
    [7.77570680426702,-16.6385739839089],
    [21.4865983854408,-15.290799330002],
    [12.6392705930724,-23.6433305964301],
    [12.4746151388128,-17.9720169566614],
    [23.4572410437998,-14.602080545086],
    [13.6878189833565,-18.9687408182414],
    [15.4077465943441,-14.5352487124086],
    [20.3356581548895,-10.0883159703702],
    [20.7093833689359,-12.6939091236766],
    [11.1032293684441,-14.1383848928755],
    [17.5048321498308,-9.2338593361801],
    [16.3303688220188,-15.1054735529158],
    [26.6929062710726,-13.306030567991],
    [34.4985678099711,-9.86199941278607],
    [39.1374291499406,-10.5621430853401],
    [21.9088956482146,-9.95198845621849],
    [22.2367457578087,-17.2200123442707],
    [10.0032784145577,-19.3557700653426],
    [14.045833906665,-15.871937521131],
    [15.5640911917607,-18.3396956121887],
    [24.4771926581586,-14.8715313479137],
    [26.533415556629,-14.693883922494],
    [12.8722580202544,-21.2750596021509],
    [24.4768291376862,-15.9592080959207],
    [18.2230748567433,-14.6541444069985],
    [4.1902148367447,-20.6144032528762],
    [12.4332594022086,-16.6079789231489],
    [20.5483758651873,-18.8512560786321],
    [17.8180560451358,-12.5451990696752],
    [11.0071081078049,-20.3938092335862],
    [8.30560561422449,-22.9503944138682],
    [33.9857852657284,-4.8371294974382],
    [17.4376502239652,-14.5095976075022],
    [29.0379635148943,-14.8461553663227],
    [29.1344666599319,-7.70862921632672],
    [32.9730697624544,-15.5839178785654],
    [13.4211493998212,-20.150199857584],
    [11.380538260355,-12.8619410359766],
    [28.672631499186,-8.51866271785711],
    [16.4296061111902,-23.3326051279759],
    [25.7168371582585,-13.8899296143829],
    [13.3185154732595,-17.8959160024249],
    [3.60832478605376,-25.4023343597712],
    [39.5445949652652,-11.466377647931],
    [25.1693484426101,-12.2752652925707],
    [25.2884257196471,-7.06710309184533],
    [6.77665715793125,-22.3947299635571],
    [20.1844223778907,-16.0427471125407],
    [25.5506805272535,-9.33856532270204],
    [25.1495682602477,-7.17350567090738],
    [15.6978431006492,-17.5979197162642],
    [37.42780451491,-10.843637288504],
    [22.974620174842,-10.6171162611686],
    [34.6327117468934,-9.26182440487384],
    [34.7042513789061,-6.9630753351114],
    [15.6563953929008,-17.2196961218915],
    [25.2049825789225,-14.1592086208169]]
#次元削除

def de_mean_matrix(A):#まず各次元の平均を0に変換
	nr, nc = shape(A)
	column_means, _ = scale(A)
	return make_matrix(nr, nc, lambda i, j: A[i][j] - column_means[j])

def direction(w):
	mag = magnitude(w)
	return [w_i / mag for w_i in w]

def directional_variance_i(x_i, w):
	return dot(x_i, direction(w) ** 2)

def directional_variance(X, w):
	return sum(directional_variance_i(x_i, w) for x_i in X)

def directional_variance_gradient_i(x_i, w):
	projection_length = dot(x_i, direction(w))
	return [2 * projection_length * x_ij for x_ij in x_i]

def direction_variance_gradient(X, w):
	return vector_sum(directional_variance_gradient_i(x_i, w) for x_i in X)

def first_principal_component(X):
	guess = [1 for _ in X[0]]
	unscaled_maximazer = maximize_batch(partial(directional_variance, X),
										partial(directional_variance_gradient, X),
										guess)

	return derection(unscaled_maximazer)

def first_principal_component_sgd(X):
	guess = [1 for _ in X[0]]
	unscaled_maximazer  = maximize_stochastic(lambda x, _, w: directional_variance_i(x, w),
											  lambda x, _, w: directional_variance_gradient_i(x, w),
											  X,
											  [None for _ in X],
											  guess)
	return deirection(unscaled_maximazer)

def project(v, w):
	projection_length = dot(v, w)
	return scalar_multiply(projection_length, w)

def remove_projection_from_vector(v, w):
	return vector_subtract(v, project(v, w))

def remove_projection(X, w):
	return [remove_projection_from_vector(x_i, w) for x_i in X]

def principal_componert_analysis(X, num_component):
	components = []
	for _ in range(components):
		component = first_principal_component(X)
		components.append(component)
		X = remove_projection(X, component)

	return components

def transform_vector(v, components):
	return [dot(v, w) for w in components]

def transform(X, components):
	return [transform_vector(x_i, components) for x_i in X]



