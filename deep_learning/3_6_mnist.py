from os import path, pardir
from PIL import Image
import mnist #mnist.pyをインポート
import numpy as np
import pickle


def sigmoid(x):
	return 1 / (1 + np.exp(-x))
#3_4_neural_networkをインポート(-.,が含まれる場合も利用可)↓↓↓↓
#module = __import__("3_4_neural_network")

def softmax(a):
	c = np.max(a)#cには最も大きい項を用いるのが一般的
	exp_a = np.exp(a - c)
	sum_exp_a = np.sum(exp_a)
	y = exp_a / sum_exp_a

	return y





def img_show(img):
    pil_img = Image.fromarray(np.uint8(img))
    pil_img.show()

(x_train, t_train), (x_test, t_test) = mnist.load_mnist(flatten=True, normalize=False)
#[訓練画像, 訓練ラベル], [テスト画像, テストラベル]


img = x_train[0]
label = t_train[0]
print(label)  # 5

print(img.shape)  # (784,)
img = img.reshape(28, 28)  # 形状を元の画像サイズに変形
print(img.shape)  # (28, 28)

img_show(img)


def get_data():
	(x_train,  t_train), (x_test, t_test) = \
		mnist.load_mnist(normalize=True, flatten=True, one_hot_label=False)
	return x_test, t_test
'''
normalize:0.0~1.0に正規化(データをある決まった範囲に変換処理)するか
flatten:一次元配列に変換するか
one_hot_label:one-hotにするか
'''


def init_network():
	with open("sample_weight.pkl", "rb") as f:
		network = pickle.load(f)
	return network
'''
plt.imread()画像を読み込む
plt.imshow()画像表示
'''

def predict(network, x):
	W1, W2, W3 = network["W1"], network["W2"], network["W3"]
	b1, b2, b3 = network["b1"], network["b2"], network["b3"]

	a1 = np.dot(x, W1) + b1
	z1 = sigmoid(a1)
	a2 = np.dot(z1, W2) + b2
	z2 = sigmoid(a2)
	a3 = np.dot(z2, W3) + b3
	y = softmax(a3)

	return(y)
'''
[0.0, 0.3, 0.7, ...]と出力されたとする
前から順に読み込んだ画像がそれぞれ0,1,2,...である確率である
'''

x, t = get_data()
network = init_network()

#バッチ処理
batch_size = 100
#正解ラベルと比較して精度を求める
accuracy_cnt = 0

for i in range(0, len(x), batch_size):
	x_batch = x[i:i + batch_size]
	y_batch = predict(network, x_batch)
	p = np.argmax(y_batch, axis = 1)#argmaxは最大値のインデックスを返す・
	accuracy_cnt += np.sum(p == t[i:i + batch_size])#np.sumはTrueとFalseを0と1に変換して合計
'''
x[i:i+n]はiからi+n番目までのデータを取り出す　この場合はx[1:100], x[100:200]
axis=1は軸　この場合は1次元目の要素ごとに取り出している
'''
print("Accuracy:" + str(float(accuracy_cnt) / len(x)))
print(p)#インデックスで表示されるのに注意





#形状の確認
x , _ = get_data()
network = init_network()
W1, W2, W3 = network['W1'], network['W2'], network['W3']
print(x.shape)    #(10000, 784)
print(x[0].shape) #(784,)
print(W1.shape)   #(784, 50)
print(W2.shape)   #(50, 100)
print(W3.shape)   #(100, 10)

