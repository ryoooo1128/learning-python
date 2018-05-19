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
	assignments = map(clusterer.classify, inputs)

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

