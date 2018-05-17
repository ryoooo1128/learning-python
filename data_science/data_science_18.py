from collections import Counter
from functools import partial
from data_science_04 import dot
import math, random
import matplotlib
import matplotlib.pyplot as plt


#ニューラルネットワーク
#deep_learningでより詳しく

#パーセプトロン
def step_function(x):
	return 1 if x >= 0 else 0

def perceptron_output(weights, x):
	calculation = dot(weights, x) + bias
	return step_function(calculation)

#ANDゲート
weights = [2, 2]
bias = -3
#ORゲート
weights = [2, 2]
bias = -1
#NOTゲート
weights = [-2]
bias = 1

and_gate = min
or_gate = max
xor_gate = lambda x, y: 0 if x == y else 1


#フィードファワードニューラルネットワーク
#シグモイド関数
def sigmoid(t):
	return 1 / (1 + math.exp(-t))

def neuron_output(weights, inputs):
	return sigmoid(dot(weights, inputs))

def feed_forward(nueral_network, input_vector):
	output = []

	#ニューロン層を１つずつ計算する
	for layer in nueral_network:
		input_with_bias = input_vector + [1]#バイアスを加える
		output = [nueral_output(neuron, input_with_bias) for nueron in layer]#出力を計算する
		outputs.append(output)#出力を記憶する

	#このニューロン層の出力を、次のニュートン層の入力にする
	input_vector = output

	return output

xor_network = [#隠れ層
			   [20, 20, -30],#ANDニューロン
			   [20, 20, -10],#ORニューロン
			  [[-60, 60, -30]]]#２番目の入力と１番目の入力のNOTとを、ANDするニューロン

for x in [0, 1]:
	for y in [0, 1]:
		print(x, y, feed_forward(xor_network, [x, y])[-1])

"""
0 0 [9.38314668300676e-14]
0 1 [0.9999999999999059]
1 0 [0.9999999999999059]
1 1 [9.383146683006828e-14]
"""


#逆伝播誤差法(バックプロパゲーション)
def backpropagate(network, input_vector, targets):
	hidden_outputs, outputs = feed_forward(network, input_vector)

	#output * (1 - output)はシグモイド関数の導関数
	output_deltas = [output * (1 - output) * (output - target) for output, target in zip(outputs, targets)]

	#ニューロンごとに重みを計算する
	for i, output_neuron in enumerate(network[-1]):
		#i番目の出力に注目
		for j, hidden_output in enumerate(hidden_outputs + [1]):
			#このニューロンの差分とj番目の入力から、j番目の重みを調整する
			output_neuron[j] -= output_deltas[i] * hidden_output

	#誤差を隠れ層に逆伝播する
	hidden_deltas = [hidden_output * (1 - hidden_output) * dot(output_deltas, [n[i] for n in output_layer]) for i, hidden_output in enumerate(hidden_outputs)]

	#ニュートンごとの出力層の重みを調整する
	for i, hidden_neuron in enumerate(network[0]):
		for j, input in enumerate(input_vector + [1]):
			hidden_neuron[j] -= hidden_deltas[i] * input




#事例：キャプチャ(CAPTCHA)を無効にする
zero_digit = [1, 1, 1, 1, 1,
			  1, 0, 0, 0, 1,
			  1, 0, 0, 0, 1,
			  1, 0, 0, 0, 1,
			  1, 1, 1, 1, 1]

targets = [[1 if i == j else 0 for i in range(10)] for j in ranfe(10)]

random.seed(0)#繰り返し可能な出力のためにランダムを固定
input_size = 25#各入力の長さは25のベクトル
num_hidden = 5#隠れ層には5つのニューロンがある
output_size = 10#各入力に対して10個の出力をする

#各隠れ層ニューロン入力にはそれぞれの重みと、1つのバイアスを加える
hidden_layer = [[random.random() for _ in range(input_size + 1)] for _ in range(num_hidden)]

#各出力ニューロンには、隠れ層ニューロンごとに１つの重みと、１つのバイアスを加える
output_layer = [[random.random() for _ in range(num_hidden + 1)] for _ in range(output_size)]

#ネットワークは無作為の重みから開始する
network = [hidden_layer, output_layer]

#10,000回繰り返せば十分に収束すると考える
for _ in range(10000):
	for input_vector, target_vector in zip(inputs, targets):
		backpropagate(network, input_vector, target_vector)

def predict(input):
	return feed_forward(network, input)[-1]

predict(inputs[7])
#[0.026, 0.0, 0.0, 0.018, 0.001, 0.0, 0.0, 0.967, 0.0, 0.0]

#３を少し崩した形にしてみる
predict([0, 1, 1, 1, 0,
		 0, 0, 0, 1, 1,
		 0, 0, 1, 1, 0,
		 0, 0, 0, 1, 1,
		 0, 1, 1, 1, 0])
#[0.0, 0.0, 0.0, 0.92, 0.0, 0.0, 0.0, 0.01, 0.0, 0.12]

#８に似せた形で試行してみる
predict([0, 1, 1, 1, 0,
		 1, 0, 0, 1, 1,
		 0, 1, 1, 1, 0,
		 1, 0, 0, 1, 1,
		 0, 1, 1, 1, 0])
#[0.0, 0.0, 0.0, 0.0, 0.0, 0.55, 0.0, 0.0, 0.93, 1.0]


#隠れ層がどのように認識されているのかを、5*5の格子である程度把握する
weights = network[0][0]#隠れ層の最初のニューロン
abs_weight = map(abs, weights)#グレーの濃さは絶対値に値する
grid = [abs_weight[row:(row + 5)] for row in range(0, 25, 5)]#重みを格子状に配置する

ax = plt.gca()#網掛けのための軸を作る

ax.imshow(grid, cmap = matplotlib.cm.binary, interpolation = 'none')

#指定された位置に指定された色で網掛けする
def patch(x, y, hatch, color):
	return matplotlib.patches.Rectangle((x - 0.5, y - 0.5), 1, 1, hatch = hatch, fill = False, color = color)

for i in range(5):#row
	for j in range(5):#column
		if weights[5 * i + j] < 0:#row i, column j = weights[5 * i + j]
			ax.add_patch(patch(j, i, '/', "white"))
			ax.add_patch(patch(j, i, '\\', "black"))

#結果を見てみる
left_column_only = [1, 0, 0, 0, 0] * 5
print(feed_forward(network, left_column_only)[0][0])
#1.0

center_middle_row = [0, 0, 0, 0, 0] * 2 + [0, 1, 1, 1, 0] + [0, 0, 0, 0, 0] * 2
print(feed_forward(network, center_middle_row)[0][0])
#0.95

right_column_only = [0, 0, 0, 0, 1] * 5
print(feed_forward(network, right_column_only)[0][0])
#0.0


my_three = [0, 1, 1, 1, 0,
			0, 0, 0, 1, 1,
			0, 0, 1, 1, 0,
			0, 0, 0, 1, 1,
			0, 1, 1, 1, 0]

hidden, output = feed_forward(network, my_three)
"""
0.121080：network[0][0]の(1, 4)により値が小さくなった
0.999979：network[0][1]の(0, 2)と(2, 2)が大きく寄与している
0.999999：network[0][2]の(3, 4)以外の正の値によるもの
0.999992：network[0][3]の(0, 2)と(2, 2)が大きく寄与している
0.000000：network[0][4]の中央の行以外で0以下の値の影響による
"""

"""
-11.61：hidden[0]に対する重み
-2.17：hidden[1]に対する重み
9.31：hidden[2]に対する重み
-1.38：hidden[3]に対する重み
-11.47：hidden[4]に対する重み
-1.92：バイアスに対する重み
"""

#そして以下の計算が行われる
sigmoid(.221 * -11.61 + 1 * -2.17 + 1 * 9.31 - 1.38 * 1 - 0 * 11.47 - 1.92)

