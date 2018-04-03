import numpy as np


a = np.array([0.3, 2.9, 4.0])

exp_a = np.exp(a)

sum_exp_a = np.sum(exp_a)

y = exp_a / sum_exp_a
print(y)





def spftmax(a):
	c = np.max(a)
	exp_a = np.exp(a - c)
	sum_exp_a = np.sum(exp_a)
	y = exp_a / sum_exp_a

	return y

print(y)

print np.sum(y)