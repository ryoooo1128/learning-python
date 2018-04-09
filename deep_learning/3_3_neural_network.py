import numpy as np

#多層構造ニューラルネットワーク
A = np.array([1, 2, 3, 4])
print (A)
print(np.ndim(A))#次元数
print(A.shape)   #形(行数, 列数)
print(A.shape[0])#1列目の項数

B = np.array([[1, 2, 3], [4, 5, 6]])
print(B)
print(np.ndim(B))
print(B.shape)

C = np.array([[1, 2], [3, 4]])
D = np.array([[5, 6], [7, 8]])
print(np.dot(C, D))#乗算



X = np.array([1, 2])

W = np.array([[1, 3, 5], [2, 4, 6]])
#X.shape=(1, 2)とW.shape=(2, 3)の間の2項が一致していないと計算できない

Y = np.dot(X, W)
print(Y)