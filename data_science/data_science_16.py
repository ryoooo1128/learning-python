from collections import Counter
from functools import partial, reduce
from data_science_04 import dot, vector_add
from data_science_08 import maximize_stochastic, maximize_batch
from data_science_10 import rescale
from data_science_11 import train_test_split
from data_science_15 import estimate_beta, predict
import math, random
import matplotlib as plt


#ロジスティック回帰

#data=([勤続年数, 給与, 有料のアカウントの有無], ...)
data = [(0.7,48000,1),(1.9,48000,0),(2.5,60000,1),(4.2,63000,0),(6,76000,0),
		(6.5,69000,0),(7.5,76000,0),(8.1,88000,0),(8.7,83000,1),(10,83000,1),
		(0.8,43000,0),(1.8,60000,0),(10,79000,1),(6.1,76000,0),(1.4,50000,0),
		(9.1,92000,0),(5.8,75000,0),(5.2,69000,0),(1,56000,0),(6,67000,0),
		(4.9,74000,0),(6.4,63000,1),(6.2,82000,0),(3.3,58000,0),(9.3,90000,1),
		(5.5,57000,1),(9.1,102000,0),(2.4,54000,0),(8.2,65000,1),(5.3,82000,0),
		(9.8,107000,0),(1.8,64000,0),(0.6,46000,1),(0.8,48000,0),(8.6,84000,1),
		(0.6,45000,0),(0.5,30000,1),(7.3,89000,0),(2.5,48000,1),(5.6,76000,0),
		(7.4,77000,0),(2.7,56000,0),(0.7,48000,0),(1.2,42000,0),(0.2,32000,1),
		(4.7,56000,1),(2.8,44000,1),(7.6,78000,0),(1.1,63000,0),(8,79000,1),
		(2.7,56000,0),(6,52000,1),(4.6,56000,0),(2.5,51000,0),(5.7,71000,0),
		(2.9,65000,0),(1.1,33000,1),(3,62000,0),(4,71000,0),(2.4,61000,0),
		(7.5,75000,0),(9.7,81000,1),(3.2,62000,0),(7.9,88000,0),(4.7,44000,1),
		(2.5,55000,0),(1.6,41000,0),(6.7,64000,1),(6.9,66000,1),(7.9,78000,1),
		(8.1,102000,0),(5.3,48000,1),(8.5,66000,1),(0.2,56000,0),(6,69000,0),
		(7.5,77000,0),(8,86000,0),(4.4,68000,0),(4.9,75000,0),(1.5,60000,0),
		(2.2,50000,0),(3.4,49000,1),(4.2,70000,0),(7.7,98000,0),(8.2,85000,0),
		(5.4,88000,0),(0.1,46000,0),(1.5,37000,0),(6.3,86000,0),(3.7,57000,0),
		(8.4,85000,0),(2,42000,0),(5.8,69000,1),(2.7,64000,0),(3.1,63000,0),
		(1.9,48000,0),(10,72000,1),(0.2,45000,0),(8.6,95000,0),(1.5,64000,0),
		(9.8,95000,0),(5.3,65000,0),(7.5,80000,0),(9.9,91000,0),(9.7,50000,1),
		(2.8,68000,0),(3.6,58000,0),(3.9,74000,0),(4.4,76000,0),(2.5,49000,0),
		(7.2,81000,0),(5.2,60000,1),(2.4,62000,0),(8.9,94000,0),(2.4,63000,0),
		(6.8,69000,1),(6.5,77000,0),(7,86000,0),(9.4,94000,0),(7.8,72000,1),
		(0.2,53000,0),(10,97000,0),(5.5,65000,0),(7.7,71000,1),(8.1,66000,1),
		(9.8,91000,0),(8,84000,0),(2.7,55000,0),(2.8,62000,0),(9.4,79000,0),
		(2.5,57000,0),(7.4,70000,1),(2.1,47000,0),(5.3,62000,1),(6.3,79000,0),
		(6.8,58000,1),(5.7,80000,0),(2.2,61000,0),(4.8,62000,0),(3.7,64000,0),
		(4.1,85000,0),(2.3,51000,0),(3.5,58000,0),(0.9,43000,0),(0.9,54000,0),
		(4.5,74000,0),(6.5,55000,1),(4.1,41000,1),(7.1,73000,0),(1.1,66000,0),
		(9.1,81000,1),(8,69000,1),(7.3,72000,1),(3.3,50000,0),(3.9,58000,0),
		(2.6,49000,0),(1.6,78000,0),(0.7,56000,0),(2.1,36000,1),(7.5,90000,0),
		(4.8,59000,1),(8.9,95000,0),(6.2,72000,0),(6.3,63000,0),(9.1,100000,0),
		(7.3,61000,1),(5.6,74000,0),(0.5,66000,0),(1.1,59000,0),(5.1,61000,0),
		(6.2,70000,0),(6.6,56000,1),(6.3,76000,0),(6.5,78000,0),(5.1,59000,0),
		(9.5,74000,1),(4.5,64000,0),(2,54000,0),(1,52000,0),(4,69000,0),(6.5,76000,0),
		(3,60000,0),(4.5,63000,0),(7.8,70000,0),(3.9,60000,1),(0.8,51000,0),(4.2,78000,0),
		(1.1,54000,0),(6.2,60000,0),(2.9,59000,0),(2.1,52000,0),(8.2,87000,0),(4.8,73000,0),
		(2.2,42000,1),(9.1,98000,0),(6.5,84000,0),(6.9,73000,0),(5.1,72000,0),(9.1,69000,1),
		(9.8,79000,1),]	

#有料アカウントの有無を予測する

#データを適切な形にする
x = [[1] + row[:2] for row in data]#x = [1, 勤続年数, 給与]
y = [row[2] for row in data]#yは有料アカウントの有無

#線形回帰を利用してみる
rescaled_x = rescale(x)
beta = estimate_beta(rescaled_x, y)#[0.26, 0.43, -0.43]
predictions = [predict(x_i, beta) for x_i in rescaled_x]
#予測が非常に大きくなったり、マイナスになることがわかる
#勤続年数は有料アカウントの有無に影響を与えており、かつ有料アカウントの有無は最大で1。つまりβの予測には偏りがある


#ロジスティック回帰
def logistic(x):
	return 1.0 / (1 + math.exp(-x))

def logistic_prime(x):
	return logistic(x) * (1 - logistic(x))

#対数尤度を最大化することで、尤度も同時に最大化する
def logistic_log_likelihood_i(x_i, y_i, beta):
	if y_i == 1:
		return math.log(logistic(dot(x_i, beta)))
	else:
		return math.log(1 - logistic(dot(x_i, beta)))

#全体の対数尤度は、個々の尤度の和になる
def logistic_log_likelihood(x, y, beta):
	return sum(logistic_log_likelihood_i(x_i, y_i, beta) for x_i, y_i in zip(x, y))


#微分する
#iはデータポイントのインデックス、jは導関数のインデックス
def logistic_log_partial_ij(x_i, y_i, beta, j):
	return (y_i - logistic(dot(x_i, y_i, beta))) * x_i[j]

def logistic_log_gradient(x_i, y_i, beta):
	return [logistic_log_partial_ij(x_i, y_i, beta, j) for j, _ in enumerate(beta)]

def logistic_log_gradient(x, y, beta):
	return reduce(vector_add, [logistic_log_gradient_i(x_i, y_i, beta) for x_i, y_i in zip(x, y)])



#モデルのあてはめ
#データを分ける
random.seed(0)
x_train, x_test, y_train, y_test = train_test_split(rescaled_x, y, 0.33)

#対数尤度を最大化する
fn = partial(logistic_log_likelihood, x_train, y_train)
gradiet_fn = partial(logistic_log_gradient, x_train, y_train)

#開始地点を無作為に指定
beta_0 = [random.random() for _ in range(3)]

#勾配加工法により最大化する
beta_hat = maximize_batch(fn, gradiet_fn, beta_0)

#もしくは確率的勾配降下法
beta_hat = maximize_stochastic(logistic_log_likelihood_i, logistic_log_gradient_i, x_train, y_train, beta_0)
"""
beta_hat = [-1.90, 4.05, -3.87]
スケールを変更前に戻す
beta_hat_unscaled = [7.61, 1.42, -0.000249]
"""


#モデルのあてはめの良さ
true_positives = false_positives = true_negatives = false_negatives = 0

for x_i, y_i in zip(x_test, y_test):
	predict = logistic(dot(beta_hat, x_i))

	if y_i == 1 and predict >= 0.5:	#真陽性：有料アカウントを有料アカウントと予測
		true_positives += 1
	elif y_i == 1:					#偽陰性：有料アカウントを無料と予測した
		false_negatives += 1
	elif predict >=0.5:				#偽陽性：無料アカウントを有料と判断した
		false_positives += 1
	else:							#無料アカウントを無料と判断した
		true_negatives += 1

precision = true_positives / (true_positives + false_positives)
recall = true_positives / (true_positives + false_negatives)




class plot():
	predictions = [predict(x_i, beta) for x_i in rescaled_x]
	plt.scatter(prediction, y)
	plt.xlabel("predicted")
	plt.ylabel("actual")
	plt.title("Simple Regression Predicted vs. Actual")
	plt.show()

	predictions = [logistic(dot(beta_hat, x_i)) for x_i in x_test]
	plt.scatter(predictions, y_test)
	plt.xlabel("predicted probability")
	plt.ylabel("actual outcome")
	plt.title("Logistc Regression Predicted vs. Actual")
	plt.show()

