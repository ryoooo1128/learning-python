#データの操作
import math, random
from __probability import inverse_normal_cdf
import matplotlib.pyplot as plt
from collections import Counter

#一次元データの操作
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

#グラフにするデータセット
random.seed(0)#ランダム生成器を初期化

uniform = [200 * random.random() - 100 for _ in range(10000)]

normal = [57 * inverse_normal_cdf(random.random()) for _ in range(10000)]

plot_histogram(uniform, 10, "Uniform Histogram")
plot_histogram(normal, 10, "Normal Histogram")


