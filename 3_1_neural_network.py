import numpy as np
import matplotlib.pylab as plt

def step_function(x):
	return np.array(x > 0, dtype=np.int)

x = np.arange(-5.0, 5.0, 0.1)
y = step_function(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()


def sigmoid(x):
	return 1 / (1 + np.exp(-x))

x = np.arange(-5.0, 5.0, 0.1)
y = sigmoid(x)
plt.plot(x, y)
plt.ylim(-0.1, 1.1)
plt.show()


def relu(x):
	return np.maximum(0, x)

x = np.arange(-5.0, 5.0, 0.5)
y = relu(x)
plt.plot(x, y)
plt.ylim(-0.1, 5.1)
plt.show()


A = np.array([1, 2, 3, 4])
print (A)
print np.ndim(A)
print A.shape
print A.shape[0]

B = np.array([[1, 2, 3], [4, 5, 6]])
print (B)
print np.ndim(B)
print B.shape

C = np.array([[1, 2], [3, 4]])
D = np.array([[5, 6], [7, 8]])
print np.dot(C, D)
