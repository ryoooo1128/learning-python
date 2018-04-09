import numpy as np


#ソフトマックス計算
a = np.array([0.3, 2.9, 4.0])
exp_a = np.exp(a)
sum_exp_a = np.sum(exp_a)
y = exp_a / sum_exp_a

print(y)


#ソフトマックス関数:数が大きい時にエラーになるのを防ぐ
def softmax(a):
	c = np.max(a)#cには最も大きい項を用いるのが一般的
	exp_a = np.exp(a - c)
	sum_exp_a = np.sum(exp_a)
	y = exp_a / sum_exp_a

	return y

print(softmax(a))#上と一致する

#足すと１になる = 確率と捉えることができる
print(np.sum(softmax(a)))
