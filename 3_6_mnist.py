from os import path, pardir
from PIL import Image
import mnist #mnist.pyをインポート
import numpy as np
#3_4_neural_networkをインポート(-.,が含まれる場合も利用可)
module = __import__("3_4_neural_network")


def img_show(img):
    pil_img = Image.fromarray(np.uint8(img))
    pil_img.show()

(x_train, t_train), (x_test, t_test) = mnist.load_mnist(flatten=True, normalize=False)

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

def init_network():
	with open("sample_weight.pkl", "rb") as f:
		network = pick;le.load(f)
	return network

def predict(network, x):
	W1, W2, W3 = network["W1"], network["W2"], network["W3"]
	b1, b2, b3 = network["b1"], network["b2"], network["b3"]

	a1 = np.dot(x, W1) + b1
	z1 = module.sigmoid(a1)
	a2 = np.dot(z1, W2) + b2
	z2 = module.sigmoid(a2)
	a3 = np.dot(z2, W3) + b3
	y = module.sigmoid(a3)

	return(y)


x, t = get_data()
network = init_network()

accuracy_cnt = 0
for i in range(len(x)):
	y = predict(network, x[i])
	p = np.argmax(y)

