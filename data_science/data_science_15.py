from collections import Counter
from functools import partial
from data_science_04 import dot, vector_add
from data_science_05 import median, standard_deviation
from data_science_06 import normal_cdf
from data_science_08 import minimize_stochastic
from data_science_14 import total_sum_of_squares
import math, random


x = [[1,49,4,0],[1,41,9,0],[1,40,8,0],[1,25,6,0],[1,21,1,0],[1,21,0,0],
	[1,19,3,0],[1,19,0,0],[1,18,9,0],[1,18,8,0],[1,16,4,0],[1,15,3,0],
	[1,15,0,0],[1,15,2,0],[1,15,7,0],[1,14,0,0],[1,14,1,0],[1,13,1,0],
	[1,13,7,0],[1,13,4,0],[1,13,2,0],[1,12,5,0],[1,12,0,0],[1,11,9,0],
	[1,10,9,0],[1,10,1,0],[1,10,1,0],[1,10,7,0],[1,10,9,0],[1,10,1,0],
	[1,10,6,0],[1,10,6,0],[1,10,8,0],[1,10,10,0],[1,10,6,0],[1,10,0,0],
	[1,10,5,0],[1,10,3,0],[1,10,4,0],[1,9,9,0],[1,9,9,0],[1,9,0,0],[1,9,0,0],
	[1,9,6,0],[1,9,10,0],[1,9,8,0],[1,9,5,0],[1,9,2,0],[1,9,9,0],[1,9,10,0],
	[1,9,7,0],[1,9,2,0],[1,9,0,0],[1,9,4,0],[1,9,6,0],[1,9,4,0],[1,9,7,0],
	[1,8,3,0],[1,8,2,0],[1,8,4,0],[1,8,9,0],[1,8,2,0],[1,8,3,0],[1,8,5,0],
	[1,8,8,0],[1,8,0,0],[1,8,9,0],[1,8,10,0],[1,8,5,0],[1,8,5,0],[1,7,5,0],
	[1,7,5,0],[1,7,0,0],[1,7,2,0],[1,7,8,0],[1,7,10,0],[1,7,5,0],[1,7,3,0],
	[1,7,3,0],[1,7,6,0],[1,7,7,0],[1,7,7,0],[1,7,9,0],[1,7,3,0],[1,7,8,0],
	[1,6,4,0],[1,6,6,0],[1,6,4,0],[1,6,9,0],[1,6,0,0],[1,6,1,0],[1,6,4,0],
	[1,6,1,0],[1,6,0,0],[1,6,7,0],[1,6,0,0],[1,6,8,0],[1,6,4,0],[1,6,2,1],
	[1,6,1,1],[1,6,3,1],[1,6,6,1],[1,6,4,1],[1,6,4,1],[1,6,1,1],[1,6,3,1],
	[1,6,4,1],[1,5,1,1],[1,5,9,1],[1,5,4,1],[1,5,6,1],[1,5,4,1],[1,5,4,1],
	[1,5,10,1],[1,5,5,1],[1,5,2,1],[1,5,4,1],[1,5,4,1],[1,5,9,1],[1,5,3,1],
	[1,5,10,1],[1,5,2,1],[1,5,2,1],[1,5,9,1],[1,4,8,1],[1,4,6,1],[1,4,0,1],
	[1,4,10,1],[1,4,5,1],[1,4,10,1],[1,4,9,1],[1,4,1,1],[1,4,4,1],[1,4,4,1],
	[1,4,0,1],[1,4,3,1],[1,4,1,1],[1,4,3,1],[1,4,2,1],[1,4,4,1],[1,4,4,1],
	[1,4,8,1],[1,4,2,1],[1,4,4,1],[1,3,2,1],[1,3,6,1],[1,3,4,1],[1,3,7,1],
	[1,3,4,1],[1,3,1,1],[1,3,10,1],[1,3,3,1],[1,3,4,1],[1,3,7,1],[1,3,5,1],
	[1,3,6,1],[1,3,1,1],[1,3,6,1],[1,3,10,1],[1,3,2,1],[1,3,4,1],[1,3,2,1],
	[1,3,1,1],[1,3,5,1],[1,2,4,1],[1,2,2,1],[1,2,8,1],[1,2,3,1],[1,2,1,1],
	[1,2,9,1],[1,2,10,1],[1,2,9,1],[1,2,4,1],[1,2,5,1],[1,2,0,1],[1,2,9,1],
	[1,2,9,1],[1,2,0,1],[1,2,1,1],[1,2,1,1],[1,2,4,1],[1,1,0,1],[1,1,2,1],
	[1,1,2,1],[1,1,5,1],[1,1,3,1],[1,1,10,1],[1,1,6,1],[1,1,0,1],[1,1,8,1],
	[1,1,6,1],[1,1,4,1],[1,1,9,1],[1,1,9,1],[1,1,4,1],[1,1,2,1],[1,1,9,1],[
	1,1,0,1],[1,1,8,1],[1,1,6,1],[1,1,1,1],[1,1,1,1],[1,1,5,1]]

daily_minutes_good = [68.77,51.25,52.08,38.36,44.54,57.13,51.4,41.42,31.22,
					  34.76,54.01,38.79,47.59,49.1,27.66,41.03,36.73,48.65,
					  28.12,46.62,35.57,32.98,35,26.07,23.77,39.73,40.57,31.65,
					  31.21,36.32,20.45,21.93,26.02,27.34,23.49,46.94,30.5,33.8,
					  24.23,21.4,27.94,32.24,40.57,25.07,19.42,22.39,18.42,46.96,
					  23.72,26.41,26.97,36.76,40.32,35.02,29.47,30.2,31,38.11,38.18,
					  36.31,21.03,30.86,36.07,28.66,29.08,37.28,15.28,24.17,22.31,
					  30.17,25.53,19.85,35.37,44.6,17.23,13.47,26.33,35.02,32.09,
					  4.81,19.33,28.77,24.26,31.98,25.73,24.86,16.28,34.51,15.23,
					  39.72,40.8,26.06,35.76,34.76,16.13,44.04,18.03,19.65,32.62,
					  35.59,39.43,14.18,35.24,40.13,41.82,35.45,36.07,43.67,24.61,
					  20.9,21.9,18.79,27.61,27.21,26.61,29.77,20.59,27.53,13.82,
					  33.2,25,33.1,36.65,18.63,14.87,22.2,36.81,25.53,24.62,26.25,
					  18.21,28.08,19.42,29.79,32.8,35.99,28.32,27.79,35.88,29.06,
					  36.28,14.1,36.63,37.49,26.9,18.58,38.48,24.48,18.95,33.55,
					  14.24,29.04,32.51,25.63,22.22,19,32.73,15.16,13.9,27.2,32.01,
					  29.27,33,13.74,20.42,27.32,18.23,35.35,28.48,9.08,24.62,20.12,
					  35.26,19.92,31.02,16.49,12.16,30.7,31.22,34.65,13.13,27.51,33.2,
					  31.57,14.1,33.42,17.44,10.12,24.42,9.82,23.39,30.93,15.03,21.67,
					  31.09,33.29,22.61,26.89,23.48,8.38,27.81,32.35,23.84]


#重回帰分析

#xが１つの値ではなく、k個のベクトルとする
#beta = [alpha, beta_1, ..., beta_k]
#x_i = [1, x_i1, ..., beta_k]
def predict(x_i, beta):
	return dot(x_i, beta)
"""
この場合xはベクトルを要素とするリストとなる
x = [1:定数項, 49:知り合いの数, 4:1日あたりの労働時間, 0:PhDの有無]
"""


#モデルのあてはめ
def error(x_i, y_i, beta):
	return y_i - predict(x_i, beta)

def squared_error(x_i, y_i, beta):
	return error(x_i, y_i, beta) ** 2

#微分する
#勾配はi番目の誤差頂の相当する
def squared_error_gradient(x_i, y_i, beta):
	return [-2 * x_xj * error(x_i, y_i, beta) for x_ij in x_i]

#確率的勾配法を使って最適なβを求める
def estimate_beta(x, y):
	beta_initial = [random.random() for x_i in x[0]]
	return minimize_stochastic(squared_error, squared_error_gradient, x, y, beta_initial, 0.001)

random.seed(0)
beta = estimate_beta(x, daily_minutes_good)#[30.63, 0.972, -1.868, 0.911]
#サイトの使用時間=30.63+0.972*知り合いの数-1.868*労働時間+0.911*PhD有無

#あてはめの良さの確認
def multiple_r_squared(x, y, beta):
	sum_of_squared_error = sum(error(x_i, y_i, beta) ** 2 for x_i, y_i in zip(x,y))
	return 1.0 - sum_of_squared_error / total_sum_of_squares
#0.68に改善


#回帰係数の標準誤差
def estimate_sample_data(sample):
	x_sample, y_sample = zip(*sample)#これでzipを分解できる
	return estimate_beta(x_sample, y_sample)

random.seed(0)
bootstrap_betas = bootstrap_statistic(zip(x, daily_minutes_good), estimate_sample_beta, 100)
bootstrap_standard_errors = [standard_deviation([beta[i] for beta in bootstrap_betas])]
"""
[1.174, #定数項			実際=1.19
 0.079, #num_friends	実際=0.08
 0.131, #unemployed		実際=0.127
 0.990] #PhDの有無		実際=0.998
"""


#スチューデントt分布:その値になる確率
def p_value(beta_hat_j, sigma_hat_j):
	if beta_hat_j > 0:#係数が正であれば大きな値を得る確率を2倍にする
		return 2 * (1 - normal_cdf(beta_hat_j / sigma_hat_j))
	else:
		return 2 * normal_cdf(beta_hat_j / sigma_hat_j)
"""
p_value(30.63, 1.174)	~0:定数項
p_value(0.972, 0.079)	~0:num_friends
p_value(-1.868, 0.131)	~0:work_hours
p_value(0.911, 0.990)	0.36:PhD
"""



#正則化：係数が増えれば過学習になる可能性が高くなる
#リッジ回帰：beta_iの二乗の和にペナルティを追加
#ここでのαはペナルティ
def ridge_penalty(beta, alpha):
	return alpha * dot(beta[1:], beta[1:])

def squared_error_ridge(x_i, y_i, beta, alpha):#
	return error(x_i, y_i, beta) ** 2 + ridge_penality(beta, alpha)

def ridge_penalty_grandient(beta, alpha):#ペナルティ項の勾配
	return [0] + [2 * alpha * beta_j for beta_j in beta[1:]]

def estimate_beta_ridge(x, y, alpha):
	beta_initial = [random.random() for x_i in x[0]]
	return minimize_stochastic(partial(squared_error_ridge, alpha=alpha), partial(squared_error_ridge, alpha=alpha), x, y, beta_initial, 0.001)

#alpha=0の時：変わらない
random.seed(0)
beta_0 = estimate_beta_ridge(x, daily_minutes_good, alpha = 0)#[30.6, 0.97, -1.87, 0.91]
dot(beta_0[1:], beta_0[1:])#5.26
multiple_r_squared(x, daily_minutes_good, beta_0)#0.680



#事例
#ペナルティーを追加すると、あてはめは悪くなるが、betaが大きくなる
#alpha=0.01の時
random.seed(0)
beta_0_01 = estimate_beta_ridge(x, daily_minutes_good, alpha = 0)#[30.6, 0.97, -1.86, 0.89]
dot(beta_0_01[1:], beta_0_01[1:])#5.19
multiple_r_squared(x, daily_minutes_good, beta_0_01)#0.680


#alpha=0.1の時
random.seed(0)
beta_0_1 = estimate_beta_ridge(x, daily_minutes_good, alpha = 0)#[30.8, 0.95, -1.84, 0.54]
dot(beta_0_1[1:], beta_0_1[1:])#4.60
multiple_r_squared(x, daily_minutes_good, beta_0_1)#0.680


#alpha=1の時：変わらない
random.seed(0)
beta_1 = estimate_beta_ridge(x, daily_minutes_good, alpha = 0)#[30.7, 0.90, -1.69, 0.085]
dot(beta_1[1:], beta_1[1:])#3.69
multiple_r_squared(x, daily_minutes_good, beta_1)#0.676


#alpha=10の時：変わらない
random.seed(0)
beta_0 = estimate_beta_ridge(x, daily_minutes_good, alpha = 0)#[28.3, 0.72, -0.91, -0.017]
dot(beta_0[1:], beta_0[1:])#1.36
multiple_r_squared(x, daily_minutes_good, beta_0)#0.573
#PhDが0となるのは明らかに間違い
#そのためこの手法を用いる前に、データのスケールの変更が必要



#別の手法：Losso回帰：係数をできるだけ0にする効果を持つ
#例
def lasso_penalty(beta, alpha):
	return alpha * sum(abs(beta_i) for beta_i in beta[1:])



#余談：ビートストラップ
#無作為にデータを抽出して、値に信頼性を持たせる
data = get_sample(num_points = n)

def bootstrap_sample(data):#len(data)を無作為に抽出して置き換える
	return [random.choice(data) for _ in data]

def bootstrap_statistic(data, stats_fn, num_samples):
	return [stats_fn(bootstrap_sample(data)) for _ in range(num_samples)]

#２つのデータセットで考えてみる
close_to_100 = [99.5 + random.random() for _ in range(101)]
far_from_100 = [99.5 + random.random() + [random.random() for _ in range(50)] + [200 + random.random() for _ in range(50)]]

bootstrap_statistic(close_to_100, median, 100)
bootstrap_statistic(far_from_100, median, 100)


