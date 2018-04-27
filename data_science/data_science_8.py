import random
import linear_algebra


#勾配下降法:

#１つのベクトルから１つの実数を返す、簡単な関数を考える
def sum_of_squares(v):
	return sum(v_i ** 2 for v_i in v)
#この関数が最小または最大になるvを求める時に勾配を考える

def difference_quotient(f, x, h):
    return (f(x + h) - f(x)) / h

def plot_estimated_derivative():

    def square(x):
        return x * x

    def derivative(x):
        return 2 * x

    derivative_estimate = lambda x: difference_quotient(square, x, h=0.00001)

    # plot to show they're basically the same
    import matplotlib.pyplot as plt
    x = range(-10,10)
    plt.plot(x, map(derivative, x), 'rx')           # red  x
    plt.plot(x, map(derivative_estimate, x), 'b+')  # blue +
    plt.show()                                      # purple *, hopefully




#勾配の評価：微分係数(接線の傾き) 差分商を極限にしたということ
#多変数関数の場合：i番目の変数以外を固定して、１変数の関数として扱うことでi番目の差分商を求める
def partial_difference_quotient(f, v, i, h):
	w = [v_j + (h if j == i else o)#i番目だけhを加える
		for j, v_j in enumerate(v)]#インデックスつきベクトルを得る

	return (f(w) - f(v) / h)
#勾配(つまり接線)を求める
def estimate_gradient(f, v, h = 0.00001):
	return [partial_difference_quotient(f, v, i, h)
			for i, _ in enumerate(v)]

#勾配を利用してみる
#無造作の点から勾配が増える方向とは逆に、勾配が非常に小さくなるまで移動させていく
def step(v, direction, step_size):
	return [v_i + step_size * direction_i
			for v_i, direcion_i in zip(v, direction)]

def sun_of_squares_gradient(v):#sum_of_squaresの勾配
	return [2 * v_i for v_j in v]

v = [random.randint(-10, 10) for i in range(3)]#任意の点を定める：３つ-10から10の間で整数を返す

tolerance = 0.0000001#限りなく０に近づく限界

while True:
	gradient = sum_of_squares_gradient(v)#vにおける勾配
	next_v = step(v, gradient, -0.01)#vを-0.01移動
	if linear_algebra.distance(next_v, v) < tolerance:
		break
	v = next_v


#移動量を最適化する
#target_fn：最小化したい関数
#gradient_fn：その勾配
def minimmize_batch(target_fn, gradient_fn, theta_0, tolerance = 0.0000001):

	step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]

	#step関数で出てきたv_iを当てはめてみた時に返す傾き　stepを試した時に、エラーが発生しないか確認するための関数
	def safe(f):

		#*arg：引数をいくつとるか未定のタプルでも使える　**kwarge：ディクショナリ　つまりこの場合どちらでも使える
		def safe_f(*args, **kwargs):
			try:#エラーが起こるかもしれない処理
				return f(*args, **kwargs)
			except:#エラーが起こった時に行う処理　今回はあまり気にしなくて良さげ
				return float('inf')#無限大を返すことによって、絶対に最小にならないようにする

		return safe_f#つまりf(*args, **kwargs)

	theta = theta_0#初期値を設定
	target_fn = safe(target_fn)#target_fnの安全版　ここでは値を返さない　ステップ関数を導入して値を入力した時の対策
	value = target_fn(theta)#

	while True:#無限に繰り返す
		gradient = gradient_fn(theta)#まずシータにおける傾きを求める
		next_thetas = [step(theta, gradient, -step_size)#シータからステップサイズを引いて、再度傾きにかける
					   for step_size in step_sizes]
		#最小値を求める
		next_theta = min(next_thetas, key = target_fn)#複数のnext_thetasの中からtarget_fnに代入して最小のthetaを返す
		next_value = target_fn(next_theta)

		if abs(value - next_value) < tolerance:#収束したなら終了する　abs:絶対値
			return theta
		else:
			theta, value = next_theta, next_value

#勾配を利用して最大を求める
def negate(f):#どんな値でも必ず-f(x)を返す関数
	return lambda *args, **kwargs: -f(*args, **kwargs)

def negate_all(f):#fが数値リストを返す場合のnegate関数 傾きの関数に利用する
	return lambda *args, **kwargs: [-y for y in f(*args, **kwargs)]

def maximize_batch(target_fn, gradient_fn, theta_0, tolerance = 0.000001):
	return minimize_batch(negate(target_fn), negate(gradient_fn), theta_0, tolerance)


#確率的勾配下降方　
def in_random_order(data):#データの要素をランダムで返す
	indexes = [i for i, in enumerate(data)]
	random.shuffle(indexes)
	for i in indexes:
		yield data[i]

def minimize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0 = 0.01):

	data = zip(x, y)
	theta = theta_0#初期値設定
	alpha = alpha_0#初期ステップ値設定
	min_theta, min_value = None, float("inf")
	iteration_wish_no_improvement = 0

	while iteration_wish_no_improvement < 100:#100回繰り返しても改善しなかったらストップする
		value = sum(target_fn(x_i, y_i, theta) for x_i, y_i in data)

		if  value < min_value:
			#新しい最小値が見つかれば記憶して、ステップを元に戻す
			min_theta, min_value = theta, value
			iteration_wish_no_improvement = 0
			alpha = alpha_0
		else:
			#そうでなければステップ値を小さくする
			iteration_wish_no_improvement += 1
			alpha *= 0.9

		#各データポイントにおいてステップを適用する
		for x_i, y_i in in_random_order(data):
			gradient_i = gradient_fn(x_i, y_i, theta)
			theta = linear_algebra.vector_subtract(theta, linear_algebra.scalar_multiply(alpha, gradient_i))

	return min_theta


def maximize_stochastic(target_fn, x, y, theta_0, alpha_0 = 0.01):
	return minimize_stochastic(negate(target_fn), negate_all(gradient_fn), x, y, theta_0, alpha_0)


