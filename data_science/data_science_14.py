from collections import Counter
from data_science_04 import  vector_subtract
from data_science_05 import mean, correlation, standard_deviation, de_mean#平均・共分散・標準偏差・偏差
from data_science_08 import minimize_stochastic
import math, random

#data_science_05の外れ値を除いたデータを利用
num_friends_good = [49,41,40,25,21,21,19,19,18,18,16,15,15,15,15,14,14,13,13,13,13,12,12,
					11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,9,9,9,9,9,9,9,9,9,9,9,
					9,9,9,9,9,9,9,8,8,8,8,8,8,8,8,8,8,8,8,8,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,
					6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,5,5,5,5,5,5,5,5,5,5,5,5,
					5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,
					3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,
					1,1,1,1,1,1,1,1,1,1,1,1,1]

daily_minutes_good = [68.77,51.25,52.08,38.36,44.54,57.13,51.4,41.42,31.22,34.76,54.01,38.79,
					  47.59,49.1,27.66,41.03,36.73,48.65,28.12,46.62,35.57,32.98,35,26.07,
					  23.77,39.73,40.57,31.65,31.21,36.32,20.45,21.93,26.02,27.34,23.49,46.94,
					  30.5,33.8,24.23,21.4,27.94,32.24,40.57,25.07,19.42,22.39,18.42,46.96,
					  23.72,26.41,26.97,36.76,40.32,35.02,29.47,30.2,31,38.11,38.18,36.31,
					  21.03,30.86,36.07,28.66,29.08,37.28,15.28,24.17,22.31,30.17,25.53,19.85,
					  35.37,44.6,17.23,13.47,26.33,35.02,32.09,24.81,19.33,28.77,24.26,31.98,
					  25.73,24.86,16.28,34.51,15.23,39.72,40.8,26.06,35.76,34.76,16.13,44.04,
					  18.03,19.65,32.62,35.59,39.43,14.18,35.24,40.13,41.82,35.45,36.07,43.67,
					  24.61,20.9,21.9,18.79,27.61,27.21,26.61,29.77,20.59,27.53,13.82,33.2,25,
					  33.1,36.65,18.63,14.87,22.2,36.81,25.53,24.62,26.25,18.21,28.08,19.42,
					  29.79,32.8,35.99,28.32,27.79,35.88,29.06,36.28,14.1,36.63,37.49,26.9,18.58,
					  38.48,24.48,18.95,33.55,14.24,29.04,32.51,25.63,22.22,19,32.73,15.16,13.9,
					  27.2,32.01,29.27,33,13.74,20.42,27.32,18.23,35.35,28.48,9.08,24.62,20.12,
					  35.26,19.92,31.02,16.49,12.16,30.7,31.22,34.65,13.13,27.51,33.2,31.57,14.1,
					  33.42,17.44,10.12,24.42,9.82,23.39,30.93,15.03,21.67,31.09,33.29,22.61,26.89,
					  23.48,8.38,27.81,32.35,23.84]



#単純な線形回帰

#y=βx+αと仮定した時
def predict(alpha, beta, x_i):
	return beta * x_i + alpha

#αとβを仮定して、実際との差を求める
def error(alpha, beta, x_i, y_i):
	return y_i - predict(alpha, beta, x_i)

#どれだけ誤差があるかを知りたいので、プラマイで相殺されるのを防ぐために、二乗する
def sum_of_squared_errors(alpha, beta, x, y):
	return sum(error(alpha, beta, x_i, y_i) ** 2 for x_i, y_i in zip(x, y))

#最小二乗法：sum_of_squared_errorsを最小化するαとβを求める
#ここでは微分を利用
def least_squared_fit(x, y):
	beta = correlation(x, y) * standard_deviation(y) / standard_deviation(x)
	alpha = mean(y) - beta * mean(x)

	return alpha, beta

alpha, beta = least_squared_fit(num_friends_good, daily_minutes_good)#α=22.95 β=0.903
#つまりn人の知り合いのいるユーザーは毎日22.95+n*0.903分間サイトを使うことがわかる


#決定係数R^2：どの程度データに当てはまるかを把握するための指標
def total_sum_of_squares(y):#平均との差の二乗の和
	return sum(v ** 2 for v in de_mean(y))

def r_squared(alpha, beta, x, y):#モデルから得られたyの結果は(1-得られなかったyの割合)に等しい
	return 1.0 - (sum_of_squared_errors(alpha, beta, x, y) / total_sum_of_squares(y))

r_squared(alpha, beta, num_friends_good, daily_minutes_good)#0.329
#R^2は大きいほど良いモデルと言える　今回は悪くはないが、改良が必要



#勾配下降法
#θ=[α, β]とする
def squared_error(x_i, y_i, theta):
	alpha, beta = theta
	return error(alpha, beta, x_i, y_i) ** 2

def squared_error_gradient(x_i, y_i, theta):
	alpha, beta = theta
	return [-2 * error(alpha, beta, x_i, y_i),#αの偏導関数
			-2 * error(alpha, beta, x_i, y_i) * x_i]#βの偏導関数

random.seed(0)
thera = [random.random(), random.random()]
alpha, beta = minimize_stochastic(squared_error, squared_error_gradient, num_friends_good, daily_minutes_good, theta, 0.0001)

print(alpha, beta)
#α=22.93 β=0.905

#最尤推定において重要


