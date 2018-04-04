import numpy as np



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



X = np.array([1, 2])
X.shape

W = np.array([[1, 3, 5], [2, 4, 6]])
W.shape

Y = np.dot(X, W)
print (Y)