import numpy as np
import matplotlib.pylab as plt


#ステップ関数:一定値を超えると1を返す
def step_function(x):
	return np.array(x > 0, dtype=np.int)

x = np.arange(-5.0, 5.0, 0.1)#-0.5から0.5まで0.1ずつ
y = step_function(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()



#シグモイド関数:
def sigmoid(x):
	return 1 / (1 + np.exp(-x))

x = np.arange(-5.0, 5.0, 0.1)
y = sigmoid(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()



#ReLU関数:0を超えるとその値を返す
def relu(x):
	return np.maximum(0, x)

x = np.arange(-5.0, 5.0, 0.5)
y = relu(x)
plt.plot(x, y)
plt.ylim(-0.1, 5.1)
plt.show()


