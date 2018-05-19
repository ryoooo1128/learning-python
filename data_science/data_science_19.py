from data_science_04 import squared_distance, vector_mean, distance
import math, random
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


#クラスタリング

#k平均法：クラスタの数をk個用意しておいて、距離の二乗を最小化する
class kMeans:
	def __init__(self, k):
		self.k = k#クラスタの数
		self.means = None#クラスタの中心

	def classify(self, input):#最も近いクラスタのインデックスを返す
		return min(range(self.k), key = lambda i: squared_distance(input, self.means[i]))

	def train(self, inputs):
		#k個の無作為の点をクラスタの最初の点として選択する
		self.means = random.sample(inputs, self.k)
		assignments = None


		while True:
			#新しい割り当てを探す
			new_assignments = map(self.classify, inputs)

			#割り当てが変化しなかったら終了
			if assignments == new_assignments:
				return

			#新しい割り当てが見つかったら採用する
			assignments = new_assignments

			#新しい割り当てを使って中心を再計算する
			for i in range(self.k):
				#クラスタiに属する値を全て抽出する
				i_points = [p for p in zip(inputs, assignments) if a == i]

				#0で除算を行わないようにi_pointsが空でないことを確認
				if i_points:
					self.means[i] = vector_mean(i_points)



#事例：オフラインミーティング
inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],
		  [-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],
		  [-25,-9],[-18,-3]]

#k=3を想定
random.seed(0)
clusterer = kMeans(3)
clusterer.train(inputs)
print(clusterer.means)
#[-44, 5], [-16, -10], [18, 20]を中心とするクラスタが見つかる

#k=2を想定
random.seed(0)
clusterer = kMeans(2)
clusterer.train(inputs)
print(clusterer.means)
#[18, 20], [-26, -5]




#kの選択
#誤差の二乗をの和をグラフで描き、線が折れているところを見る
def squared_clustering_errors(inputs, k):
	clusterer = kMeans(k)
	clusterer.train(inputs)
	means = clusterer.means
	assignments = list(map(clusterer.classify, inputs))

	return sum(squared_distance(inputs, means[cluseter]) for input, cluster in zip(inputs, assignments))


#1からlen(inputs)までのクラスタ分けした結果のグラフを描く
ks = range(1, len(inputs) + 1)
errors = [squared_clustering_errors(inputs, k) for k in ks]

plt.plot(ks, errors)
plt.xticks(ks)
plt.xlabel("k")
plt.ylabel("total squared error")
plt.title("Total Errors vs. # of Clusters")

plt.show()



#事例：色のクラスタリング

#まずイメージを読み込む
path_to_png_file = ""
img = maping.imread(path_to_png_file)

top_row = row[0]
top_left_pixel = top_row[0]
red, green, blue  = top_left_pixel#データは[赤, 緑, 青]になってるとする

pixels = [pixel for row in img for pixel in row]

clusterer = kMeans(5)
cluserer.train(pixels)

def recolor(pixel):
	cluster = clusterer.classify(pixel)#ピクセルが分類されたクラスタのインデックス
	return clusterer.means[cluster]#クラスタの平均値

#ピクセルの行の色を再設定する　イメージの行を順を処理する
new_img = [[recolor(pixel) for pixel in row] for row in img]

plt.imshow(new_img)
plt.axis('off')
plt.show()



#凝縮型階層的クラスタリング：クラスタをさらにクラスタリングする
#２つのクラスタを仮定する
leaf1 = ([10, 20],)#値が１つのタプルを作るときは最後にカンマが必要
leaf2 = ([30, -15])

#(結合順, クラスタ)
merged = (1, [leaf1, leaf2])

#クラスタの長さが1なら末端クラスタ
def is_leaf(cluster):
	return len(cluster) == 1

#結合クラスタならその２つの子クラスタを返す
#末端クラスタなら例外を投げる発生をさせる
def get_children(cluster):
	if is_leaf(cluster):
		raise TypeError("a leaf cluster has no children")
	else:
		return cluster[1]

#末端クラスタの場合クラスタ内の値を返す
#そうでなければ下位にある全ての末端クラスタの値を返す
def get_values(cluster):
	if is_leaf(cluster):
		return cluster#末端クラスタなので値を１つ持つタプル
	else:
		return [value for child in get_children(cluster) for value in get_values(child)]

#cluster1とcluster2の距離を求めて、パラメーターdistance_aggを適用する
#様々な方法があるが、ここではmin最小値を利用する
def cluster_distance(cluster1, cluster2, distance_agg = min):
	return distance_agg([distance(input1, input2) for input1 in get_values(cluster1) for input2 in get_values(cluster2)])

#結合順の値を使って結合の順番を辿る　小さければ小さいほど後に結合したことになる
#そのため分離するときは小さいものから行う
def get_merge_order(cluster):
	#末端クラスタは結合されたものではないので、無限大が返るようにしておく
	if is_leaf(cluster):
		return float('inf')
	else:
		return cluster[0]#結合順は2値のタプルの第一要素


def bottom_up_cluster(inputs, distance_agg = min):
	#全ての入力を値が１つの末端クラスタにする
	cluster = [(input, ) for input in inputs]

	#１つ以上のクラスタが残っている限り続ける
	while len(cluster) > 1:
		#２つの近傍クラスタを選択
		c1, c2 = min([cluster1, cluster2 for cluster1 in enumerate(clusters) for cluster2 in clusters[:i]], key = lambda (x, y): cluster_distance(x, y, distance_agg))
		#それらをクラスタから取り除く
		clusters = [c for c in clusters if c != c1 and c != c2]
		#結合順を残りのクラスタ数にして2つのクラスタを結合する
		merge_cluster = (len(clusters), [c1, c2])
		#結合したクラスタをリストに加える
		clusters.append(merge_cluster)

	return clusters[0]


#使ってみる
base_cluster = bottom_up_cluster(inputs)
"""
結果
(0, [(1, [(3, [(14, [(18[([19, 28], ),
						 ([21, 27], )]),
					 ([20, 23], )]),
			   ([26, 13], )]),
		  (16, [([11, 15], ),
		  		([13, 13], )])]),
	 (2, [(4, [(5, [(9, [(11, [([-49, 0], ),
	 						   ([-46, 5], )]),
	 					  ([-41, 8], )]),
	 				([-49, 15], )]),
	 		   ([-34, -1], )]),
	 	  (6, [(7, [(8, [(10, [([-22, -16], ), 
	 	  					   ([-19, -11], )]),
	 	  				 ([-25, -9], )]),
					(13, [(15, [(17, [([-11, -6], ),
									  ([-12, -8], )]),
								([-14, -5], )]),
						  ([-18, -3], )])]),
					(12, [([-13, -19], ),
						  ([-9, -16],)])])])])          
"""
"""
クラスタ0：クラスタ1とクラスタ2の結合
クラスタ1：クラスタ3とクラスタ16の結合
クラスタ16：リーフクラスタ[11,15]と[13,13]の結合
...と解釈できる
"""

#可視化してみる
def generate_cluster(base_cluster, num_cluster):
	#元のクラスタをリストにしてから開始する
	clusters = [base_cluster]

	#指定した数のクラスタになるまで繰り返す
	while len(cluster) < num_cluster:
		#最後に行われた結合を探す
		next_cluster = min(clusters, key = get_merge_order)
		#クラスタのリストから取り除く
		clusters = [c for c in clusters if c != next_cluster]
		#分解したクラスタをリストに追加する
		clusters.extend(get_children(next_cluster))

	return clusters


#例えば３つのクラスタが必要な場合
three_clusters = [get_values(cluster) for cluster in generate_cluster(base_cluster, 3)]


#グラフ化もしてみる
for i, cluster, marker, color in zip([1, 2, 3], three_clusters, ['D', 'o', '*'], ['r', 'g', 'b']):
	xs, ys = zip(*cluster)
	plt.scatter(xs, ys, color = color, marker = marker)

	#クラスタの平均を表示する
	x, y = vector_mean(cluster)
	plt.plot(x, y, marker ='$' + str(i) + '$', color = 'black')

plt.title("User Locations -- 3 Bottom-Up Cluster, Min")
plt.xlabel("blocks east of city center")
plt.ylabel("blocks eorth of city center")
plt.show()


