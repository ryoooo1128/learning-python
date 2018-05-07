import math, random
import matplotlib.pyplot as plt
from collections import Counter
from data_science_04 import distance
from data_science_05 import mean
from __plot_state_borders import plot_state_borders


#k近傍方

#多数決をする
def raw_major_vote(labels):
	votes = Counter(labels)
	winner, _ = votes.most_common(1)[0]

	return winner

#同数になった場合に多数決が１つになるまでkを少なくする
#ラベルは近いものから遠いものにソートされている前提
def majority_vote(labels):
	vote_counts = Counter(labels)
	winner, winner_count = vote_counts.most_common(1)[0]
	num_winners = len([count
					   for count in vote_counts.value()
					   if count == winner_count])
	if num_winners == 1:
		return winner#多数決が１つになったら結果とする
	else:
		return raw_major_vote(labels[:-1])#最も遠いものを除いて再度実行

#分類器を生成
#ラベル付きデータは(point, label)のペアになっている
def knn_classfy(k, labeled_points, new_point):#k近傍法
	by_distance = sorted(labeled_points, key = lambda point, _: distance(point, new_point))#データポイントから近い順にソート
	k_nearest_labels = [label for _, label in by_distance[:k]]#近い順にk個取り出す
	return majority_vote(k_nearest_labels)#多数決を行う



#事例

#([緯度, 経度], 言語)
cities = [(-86.75,33.5666666666667,'Python'),
		　(-88.25,30.6833333333333,'Python'),
		　(-112.016666666667,33.4333333333333,'Java'),
		　(-110.933333333333,32.1166666666667,'Java'),
		　(-92.2333333333333,34.7333333333333,'R'),
		　(-121.95,37.7,'R'),
		　(-118.15,33.8166666666667,'Python'),
		　(-118.233333333333,34.05,'Java'),
		　(-122.316666666667,37.8166666666667,'R'),
		　(-117.6,34.05,'Python'),
		　(-116.533333333333,33.8166666666667,'Python'),
		　(-121.5,38.5166666666667,'R'),
		　(-117.166666666667,32.7333333333333,'R'),
		　(-122.383333333333,37.6166666666667,'R'),
		　(-121.933333333333,37.3666666666667,'R'),
		　(-122.016666666667,36.9833333333333,'Python'),
		　(-104.716666666667,38.8166666666667,'Python'),
		　(-104.866666666667,39.75,'Python'),
		　(-72.65,41.7333333333333,'R'),
		　(-75.6,39.6666666666667,'Python'),
		　(-77.0333333333333,38.85,'Python'),
		　(-80.2666666666667,25.8,'Java'),
		　(-81.3833333333333,28.55,'Java'),
		　(-82.5333333333333,27.9666666666667,'Java'),
		　(-84.4333333333333,33.65,'Python'),
		　(-116.216666666667,43.5666666666667,'Python'),
		　(-87.75,41.7833333333333,'Java'),
		　(-86.2833333333333,39.7333333333333,'Java'),
		　(-93.65,41.5333333333333,'Java'),
		　(-97.4166666666667,37.65,'Java'),
		　(-85.7333333333333,38.1833333333333,'Python'),
		　(-90.25,29.9833333333333,'Java'),
		　(-70.3166666666667,43.65,'R'),
		　(-76.6666666666667,39.1833333333333,'R'),
		　(-71.0333333333333,42.3666666666667,'R'),
		　(-72.5333333333333,42.2,'R'),
		　(-83.0166666666667,42.4166666666667,'Python'),
		　(-84.6,42.7833333333333,'Python'),
		　(-93.2166666666667,44.8833333333333,'Python'),
		　(-90.0833333333333,32.3166666666667,'Java'),
		　(-94.5833333333333,39.1166666666667,'Java'),
		　(-90.3833333333333,38.75,'Python'),
		　(-108.533333333333,45.8,'Python'),
		　(-95.9,41.3,'Python'),
		　(-115.166666666667,36.0833333333333,'Java'),
		　(-71.4333333333333,42.9333333333333,'R'),
		　(-74.1666666666667,40.7,'R'),
		　(-106.616666666667,35.05,'Python'),
		　(-78.7333333333333,42.9333333333333,'R'),
		　(-73.9666666666667,40.7833333333333,'R'),
		　(-80.9333333333333,35.2166666666667,'Python'),
		　(-78.7833333333333,35.8666666666667,'Python'),
		　(-100.75,46.7666666666667,'Java'),
		　(-84.5166666666667,39.15,'Java'),
		　(-81.85,41.4,'Java'),
		　(-82.8833333333333,40,'Java'),
		　(-97.6,35.4,'Python'),
		　(-122.666666666667,45.5333333333333,'Python'),
		　(-75.25,39.8833333333333,'Python'),
		　(-80.2166666666667,40.5,'Python'),
		　(-71.4333333333333,41.7333333333333,'R'),
		　(-81.1166666666667,33.95,'R'),
		　(-96.7333333333333,43.5666666666667,'Python'),
		　(-90,35.05,'R'),
		　(-86.6833333333333,36.1166666666667,'R'),
		　(-97.7,30.3,'Python'),(-96.85,32.85,'Java'),
		　(-95.35,29.9666666666667,'Java'),
		　(-98.4666666666667,29.5333333333333,'Java'),
		　(-111.966666666667,40.7666666666667,'Python'),
		　(-73.15,44.4666666666667,'R'),
		　(-77.3333333333333,37.5,'Python'),
		　(-122.3,47.5333333333333,'Python'),
		　(-89.3333333333333,43.1333333333333,'R'),
		　(-104.816666666667,41.15,'Java')]



def plot_cities():
	#緯度と経度の辞書を作成
	plots = {"java" : ([], []), "Python" : ([], []), "R" : ([], [])}
	#マーカーの色と形を指定
	makers = { "Java" : "o", "Python" : "s", "R" : "^"}
	colors = { "Java" : "r", "Python" : "b", "R" : "g"}

	for (longitude, latitude), language in cities:
		plots[language][0].append(longitude)
		plots[language][1].append(latitude)

	#各言語ごとに散布図を作る
	for language, (x, y) in plots.item():
		plt.scatter(x, y, color = colors[language], maker = makers[language], label = language, zorder = 10)

	plot_state_borders(plt)
	plt.legend(loc=0)
	plt.axis([-130, -60, 20, 55])
	plt.title("Favorite Programming Language")

	plt.show()


#図から場所が近ければ、同じ言語が選択されているように見える
#よって、近傍値によって予測

#異なるkの値を試す
#ポイントをそれぞれk近傍法で求めて、正解と比較する
for k in [1, 3, 5, 7]:
	num_correct = 0

	for city in cities:
		location, actual_language = city
		other_cities = [other_city for other_city in cities if other_city != city]

		preditced_language = knn_classfy(k, other_cities, location)

		if preditced_language == actual_language:
			num_correct =+ 1

	print(k, "neighbor[s]:", num_correct, "correct out of", len(cities))
"""
1 neighbor[s]:40 correct out of 75
3 neighbor[s]:44 correct out of 75
5 neighbor[s]:41 correct out of 75
7 neighbor[s]:35 correct out of 75
よって３近傍法が最も正確で59％の正解率
"""

#全体を格子状に分割する
plots = {"java" : ([], []), "Python" : ([], []), "R" : ([], [])}
for longitudein in range(-130:-60):
	for latitude in range(20:55):
		preditced_language = knn_classfy(k, cities, [longitudein, latitude])
		plots[preditced_language][0].append(longitudein)
		plots[preditced_language][1].append(latitude)



#多次元の場合の近傍法
def random_point(dim):
	return random.random() for _ in range(dim)

def random_distance(dim, num_pairs):
	return [distance(random_point(dim), random_point(dim)) for _ in range(num_pairs)]


dimensions = range(1, 101)
avg_distances = []
min_distances = []


#1から100の各次元で10000個の距離を計算し、平均距離と最低距離を求める
random.seed(0)
for dim in dimensions:
	distances = random_distances(dim, 10000)
	avg_distances.append(mean(distances))
	min_distances.append(min(distances))

#最低値と平均との比
#高次元になればなった分だけ平均距離は伸び、その差は縮まる
min_avg_ratio = [min_dist / avg_dist for min_dist, avg_dist in zip(min_distances, avg_distances)]

