import numpy as np

#パーセプトロン
x = np.array([0, 1])
w = np.array ([0.5, 0.5])
b = -0.7
print(w * x)

print(np.sum(w * x))
print(np.sum(w * x) + b)



#AND:2入力1出力
def AND(x1, x2):
	x = np.array([x1, x2])   #入力
	w = np.array([0.5, 0.5]) #重み
	b = -0.7                 #バイアス
	tmp = np.sum(x * w) + b
	if tmp <= 0:
		return 0
	else :
		return 1

#NAND:ANDの逆
def NAND(x1, x2):
	x = np.array([x1, x2])
	w = np.array([-0.5, -0.5])#重みとバイアスが異なる
	b = 0.7
	tmp = np.sum(w * x) + b
	if tmp <= 0:
		return 0
	else:
		return 1

#OR
def OR(x1, x2):
	x = np.array([x1, x2])   
	w = np.array([0.5, 0.5]) 
	b = 0.2                 
	tmp = np.sum(x * w) + b
	if tmp <= 0:
		return 0
	else :
		return 1

#XOR:多層構造なら可　次へ








#なんでもないこと・感じたままのこと
print "Hello world, a wonderful world.\nIm so glad to be here. (27/3/2018)"