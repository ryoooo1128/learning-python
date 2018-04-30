import matplotlib.pyplot as plt
import numpy as np
import math
from collections import Counter

#統計


#データ
num_friends = [100,49,41,40,25,21,21,19,19,18,18,16,15,15,15,15,
14,14,13,13,13,13,12,12,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,
9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,
7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,
1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

daily_minutes = [1,68.77,51.25,52.08,38.36,44.54,57.13,51.4,41.42,31.22,34.76,
54.01,38.79,47.59,49.1,27.66,41.03,36.73,48.65,28.12,46.62,35.57,32.98,35,26.07,
23.77,39.73,40.57,31.65,31.21,36.32,20.45,21.93,26.02,27.34,23.49,46.94,30.5,33.8,
24.23,21.4,27.94,32.24,40.57,25.07,19.42,22.39,18.42,46.96,23.72,26.41,26.97,36.76,
40.32,35.02,29.47,30.2,31,38.11,38.18,36.31,21.03,30.86,36.07,28.66,29.08,37.28,15.28,
24.17,22.31,30.17,25.53,19.85,35.37,44.6,17.23,13.47,26.33,35.02,32.09,24.81,19.33,
28.77,24.26,31.98,25.73,24.86,16.28,34.51,15.23,39.72,40.8,26.06,35.76,34.76,16.13,
44.04,18.03,19.65,32.62,35.59,39.43,14.18,35.24,40.13,41.82,35.45,36.07,43.67,24.61,
20.9,21.9,18.79,27.61,27.21,26.61,29.77,20.59,27.53,13.82,33.2,25,33.1,36.65,18.63,
14.87,22.2,36.81,25.53,24.62,26.25,18.21,28.08,19.42,29.79,32.8,35.99,28.32,27.79,
35.88,29.06,36.28,14.1,36.63,37.49,26.9,18.58,38.48,24.48,18.95,33.55,14.24,29.04,
32.51,25.63,22.22,19,32.73,15.16,13.9,27.2,32.01,29.27,33,13.74,20.42,27.32,18.23,
35.35,28.48,9.08,24.62,20.12,35.26,19.92,31.02,16.49,12.16,30.7,31.22,34.65,13.13,
27.51,33.2,31.57,14.1,33.42,17.44,10.12,24.42,9.82,23.39,30.93,15.03,21.67,31.09,
33.29,22.61,26.89,23.48,8.38,27.81,32.35,23.84]


num_friends_array = np.array(num_friends)
daily_minutes_array = np.array(daily_minutes)


#おまけ
#ヒストグラム
def make_friend_counts_histogram(plt):
	friends_counts = Counter(num_friends)
	xs = range(101) #xの範囲を指定
	ys = [friends_counts[x] for x in xs]
	plt.bar(xs, ys)
	plt.axis([0,101,0,25])
	plt.title('Histogram of Friends Counts')
	plt.xlabel('# of friends')
	plt.ylabel('# of people')
	plt.show()


#散布図
plt.scatter(num_friends, daily_minutes)
plt.show()

#データ数
num_points = len(num_friends)	#204


#最大値/最小値
largest_value = max(num_friends)	#100
smallest_value = min(num_friends)	#1


#ソートを利用した方法
sorted_value = sorted(num_friends)
smallest_value = sorted_value[0]	#1
second_smallest_value = sorted_value[1]	#1
second_largest_value = sorted_value[-2]	#49


#平均値
def mean(x):
	return sum(x) / len(x)

#中央値
def median(v):
	n = len(v)
	sorted_v = sorted(v)
	midpoint = n // 2

	if n % 2 == 1:
		return sorted_v[midpoint]
	else:
		lo = sorted_v[midpoint - 1]
		hi = sorted_v[midpoint]
		return (lo + hi) / 2


#分位数
def quantile(x, p):
	p_index = int(p * len(x))
	return sorted(x)[p_index]
"""
quantile(num_friends, 0.25)	#3
quantile(num_friends, 0.75)	#9
"""

#最頻値・モード
def mode(x):
	counts = Counter(x)
	return counts.most_common(1)

'''
collectionsのCounterの中にある。
何番目かも指定可能。
ただし最頻値が複数ある場合はif文で補う。
statisticsのmode()で一発。
ただし最頻値が一つの場合に限る。
'''



#最頻値・複数ver
def mode_by_myself(x):
	counts = Counter(x)                                        #{6:22, 1:22, 4:20, ...}
	times_list = counts.values()                               #(22, 22, 20, ...)
	times_count = Counter(times_list)                          #(1:7, 2:5, 4:2, 15:2, 22:2, ...)
	max_times = max(counts.values())                           #22
	max_times_times = times_count[max_times]                   #2
	max_times_times_list = counts.most_common(max_times_times) #[(6, 22), (1, 22)]
	max_times_times_dict = dict(max_times_times_list)          #{6:22, 1:22}
	answer = max_times_times_dict.keys()                       #[6, 1]

	return answer



#相関
#散らばり
def data_range(x):
	return max(x) - min(x)

#偏差:平均との差
def de_mean(x):
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

#分散:偏差の二乗の平均
def variance(x):
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)

#標準偏差:基本的には分散の平方根
def standard_deviation(x):
    return math.sqrt(variance(x))


def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)

#共分散:数値が大きいほど相関がある。マイナスは逆相関
def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)

#相関係数:共分散を標準偏差で割る。数値が大きいほど相関がある。マイナスは逆相関
def correlation(x, y):
    stdev_x = standard_deviation(x)
    stdev_y = standard_deviation(y)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(x, y) / stdev_x / stdev_y
    else: # if no variation, correlation is zero





#相関(numpyバージョン)

#分散
def variance_np(x_array):
	return np.var(x_array)

#偏差
def de_mean_np(x_i, x_array):
	mean = np.mean(x_array)
	return x - mean

#偏差値
def standard_score_np(x_array):
	return de_mean(x_array) / np.std(x_array) * 10 + 50

#標準偏差
def standard_deviation_np(x_array):
	return np.std(x_array)

#共分散
def covariance_np(x_array, y_array):
	covariance_array = np.cov(x_array, y_array)
	'''np.cov = [xの分散, 共分散 ]
				[共分散 , yの分散]'''
	return covariance_array[0][1]

#相関係数
def correlation_np(x_array, y_array):
	correlation_array = np.corrcoef(num_friends_array, daily_minutes_array)
	'''np.corroef = [1, 相関係数]
					[相関係数, 1]'''
	return correlation_array[0][1]

