import random, math
import matplotlib.pyplot as plt
from collections import Counter


#確率


def random_kid():
	return random.choice(["boy","girl"])

def kids_count():
	both_girls = 0
	older_girl = 0
	either_girl = 0

	random.seed(0)
	for _ in range(10000):
		younger = random_kid()
		older = random_kid()
		if older == "girl":
			older_girl += 1
		if older == "girl" and younger == "girl":
			both_girls += 1
		if older == "girl" or younger == "girl":
			either_girl += 1

#1人目が女の子の時、2人とも女の子の確率
print(both_girls / older_girl)
#どちらかが女の子の時、2人とも女の子の確率
print(both_girls / either_girl)




#離散型分布

#連続確率分布
#確率密度関数:連続的な確率では意味がないため、関数を用いて、範囲で積分することで確立を求める
def uniform_pdf(x):
	return 1 if x >= 0 and x < 1 else 0

def uniform_pdf():
	xs = [x / 10.0 for x in range(-50, 50)]
	plt.plot(xs,[uniform_pdf(x) for x in xs])

	plt.show()



#累積分布関数:それまでの確立を足した関数・〜から〜までになる確率を求める時に便利
def uniform_cdf(x):
	if x < 0: return 0
	elif x < 1: return x
	else: return 1

def plot_uniform_cdf():
	xs = [x / 10.0 for x in range(-50, 50)]
	plt.plot(xs,[uniform_cdf(x) for x in xs])

	plt.show()



#正規分布:綺麗な釣鐘型になる確率の分布・平均からの距離が等しい
#確率密度変数
def normal_pdf(x, mu, sigma):#mu=平均・sigma=標準偏差
	sqrt_two_pi = math.sqrt(2 * math.pi)#math.sqrt(平方根)・math.pi(円周率)
	return (math.exp(-(x - mu) ** 2 / 2 / sigma ** 2) / (sqrt_two_pi * sigma))#math.exp(eのx乗)

def plot_normal_pdfs():
	xs = [x / 10.0 for x in range(-50, 50)]
	plt.plot(xs,[normal_pdf(x, mu=0, sigma=1) for x in xs], '_', label='mu=0, sigma=1')#標準正規分布Z:正規分布Xの確立を標準化(mu=0,sigam=1)するとできる
	plt.plot(xs,[normal_pdf(x, mu=0, sigma=2) for x in xs], '--', label='mu=0, sigma=2')
	plt.plot(xs,[normal_pdf(x, mu=0, sigma=0.5) for x in xs], ':', label='mu=0, sigma=0.5')
	plt.plot(xs,[normal_pdf(x, mu=1, sigma=1) for x in xs], '-.', label='mu=1, sigma=1')
	plt.legend()#ラベルとつけているため自動で凡例がつく
	plt.title("Various Normal pdfs")

	plt.show()




#累積分布関数
def normal_cdp(x, mu, sigma):
	return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

def plot_normal_cdfs(plt):
	xs = [x / 10.0 for x in range(-50, 50)]
	plt.plot(xs,[normal_cdp(x, mu=0, sigma=1) for x in xs], '_', label='mu=0, sigma=1')
	plt.plot(xs,[normal_cdp(x, mu=0, sigma=2) for x in xs], '--', label='mu=0, sigma=2')
	plt.plot(xs,[normal_cdp(x, mu=0, sigma=0.5) for x in xs], ':', label='mu=0, sigma=0.5')
	plt.plot(xs,[normal_cdp(x, mu=1, sigma=1) for x in xs], '-.', label='mu=1, sigma=1')
	plt.legend(loc = 4)#凡例を右下に
	plt.title("Various Normal cdfs")

	plt.show()


#累積分布関数の逆関数を二分探索を用いて計算する
def inverse_noremal_cdf(p, mu=0, sigma=1, tollerance=0.00001):
	if mu != 0 or sigma != 1:
		return mu + sigma * inverse_noremal_cdf(p, tollerance = tollerance)

	low_z, low_p = -10.0, 0
	hi_z, hi_p = 10.0, 1
	while hi_z - low_z > tollerance:
		mid_z = (low_z + hi_z) / 2
		mid_p = normal_cdp(mid_z)
		if mid_p < p:
			low_z, low_p = mid_z, mid_p
		elif mid_p > p:
			hi_z, hi_p = mid_z, mid_p
		else:
			break
	return mid_z



#中心極限定理:どんなものも最終的には正規分布になる
#２項確率変数を用いて確認
def bernoulli_trial(p):#乱数がpより大きければ1,小さければ0
	return 1 if random.random() < p else 0#random.randomは浮動小数点数の乱数を生成

#確率pでn個のbernoulli(p)を合計したもの
def binomial(p, n):#上試行をn回行った時にpより大きかった回数
	return sum(bernoulli_trial(p) for _ in range(n))

def make_hist(p, n, num_point):#上試行を10000回行った時の結果
	data = [binomial(p, n) for _ in range(num_point)]

	#二項分布を棒グラフでプロット
	histogram = Counter(data)
	plt.bar([x - 0.4 for x in histogram.keys()],
			[v / num_point for v in histogram.values()],
			 0.8,
			 color='0.75')

	#正規分布の近似値を折れ線グラフでプロット
	mu = p * n
	sigma = math.sqrt(n * p * (1 - p))
	
	xs = range(min(data), max(data) + 1)
	ys = [normal_cdp(i + 0.5, mu, sigma) - normal_cdp(i - 0.5, mu, sigma) for i in xs]
	plt.plot(xs, ys)
	plt.title("Binomial Distribution vs. Normal Approximation")

	plt.show()

