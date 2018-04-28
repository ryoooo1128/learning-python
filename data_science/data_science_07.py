from __probability import normal_cdf, inverse_normal_cdf
import math, random
import matplotlib as plt


#コインが歪んでいる確率
#ベルヌーイ試行のため表が出た回数Xは、pの確率でn個の確率変数を足したものに当たる
def normal_approximation_to_binomial(n, p):
	mu = p * n
	sigma = math.sqrt(p * (1 - p) * n)#???????????

	return mu, sigma#平均と標準偏差

#変数が閾値を下回っていればnormal_cdfで表せる
normal_probablity_below = normal_cdf

#閾値を下回ってなければ、閾値より上にある
def normal_plobablity_above(lo, mu = 0, sigma = 1):
	return 1 - normal_cdf(lo, mu, sigma)

#hiより大きくloより小さければ値はその間にある
def normal_probablity_between(lo, hi, mu = 0, sigma = 1):
	return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)

#間になければ、値はその上にある
def normal_probablity_outside(lo, hi, mu = 0, sigma = 1):
	return 1 - normal_probablity_between(lo, hi, mu, sigma)



#一定の可能性Zになる範囲を求める(上の逆　正規確率に限る：左右対称に限る)
#Z以上になる確率
def normal_upper_bound(probability, mu = 0, sigma = 1):
	return inverse_normal_cdf(probability, mu, sigma)

#Z以下になる確率
def normal_lower_bound(probability, mu = 0, sigma = 1):
	return inverse_normal_cdf(1 - probability, mu, sigma)

def normal_two_sided_bounds(probability, mu = 0, sigma = 1):
	#平均を中心に一定の可能性を含む対対の中心
	tail_probability = (1 - probability) / 2

	#それぞれ境界
	upper_bound = normal_lower_bound(tail_probability, mu, sigma)
	lower_bound = normal_lower_bound(tail_probability, mu, sigma)

	return upper_bound, lower_bound

#p=0.5の時コインに歪みがない
mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)


#検定力
#有意水準に5％を使用した場合の範囲:つまり第1種の過誤が5％の確率で起こる
print(normal_two_sided_bounds(0.95, mu_0, sigma_0))#(469, 531)

#第2種の過誤の起こきない確率
#p=0.5の場合の有意水準5％の範囲を確認
lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)

#p=5.5%になる歪んだコインだった場合
mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)#平均と標準偏差
type_2_probablity = normal_probablity_between(lo, hi, mu_1, sigma_1)#第2種の過誤が起こる確率
power = 1 - type_2_probablity

print(power)#0.887




#p<=0.5、有意水準5％の場合：上の部分のみ調べる
hi = normal_upper_bound(0.95, mu_0, sigma_0)#526:(<531より上側の第1種の過誤が少し大きくなる)
type_2_probablity = normal_probablity_below(hi, mu_1, sigma_1)
power = 1 - type_2_probablity#0.936：より強い検定になる


#両側検定：xが平均より大きいか小さいかに分けて、それぞれ切り捨てる部分を大きい方、小さい方に移動させて検定する：それがx=0.5である可能性を求める
def two_sided_p_value(x, mu = 0, sigma = 1):
	if x >= mu:
		return 2 * normal_plobablity_above(x, mu, sigma)
	else:
		return 2 * normal_probablity_below(x, mu, sigma)


#x=530:表が530回出た時の検定：それがp=0.5である可能性
print(two_sided_p_value(529.5, mu_0, sigma_0))#0.062：棄却しない
'''
ここでは「連続性補正」で530より精度の上がる529.5を利用した
以下は、上記の検定方法の実際のシミュレーション
'''
extreme_value_count = 0
for _ in range(100000):
	num_heads = sum(1 if random.random() < 0.5 else 0#1000回コインを投げて
					for _ in range(1000))			 #表が出る回数を数える
	if num_heads >= 530 or num_heads <= 470:		 #そのうち極端な値が出た回数を
		extreme_value_count += 1					 #数える

print(extreme_value_count / 100000)#0.062

#x=532の時
print(two_sided_p_value(531.5, mu_0, sigma_0))#0.46


#別バージョン
upper_p_value = normal_plobablity_above
lower_p_value = normal_probablity_below

#x=524の時
print(upper_p_value(524.5, mu_0, sigma_0))#0.061
#x=527の時
print(upper_p_value(526.5, mu_0, sigma_0))#0.047




#信頼区間:pの値がわからない場合(試行1000回・525回表) 正規分布の区間に入っているかどうかで判断する
#ベルヌーイ変数の平均値は平均pと標準偏差の正規分布に従うため以下が成り立つ
#math.sqrt(p * (1 - p) / 1000)

p_hat = 525 / 1000
mu = p_hat
sigma = math.sqrt(p_hat * (1 - p_hat) / 1000)#0.0158

print(normal_two_sided_bounds(0.95, mu, sigma))#0.4940, 0.5560:信頼区間



#pハッキング：推定のp値を使って外れ値を取り除いて優位な結果を得ること
def run_experiment():
	return[random.random() < 0.5 for _ in range(1000)]#コインを1000回投げて表が出たらTrue裏ならFalseとする

def reject_faireness(experiment):#有意水準5%を用いる	
	num_heads = len([flip for flip in experiment if flip])
	return num_heads < 469 or num_heads > 531

random.seed(0)

experiments = [run_experiment() for _ in range(1000)]
num_rejection = len([experiment for experiment in experiments if reject_faireness(experiment)])

print(num_rejection)#46

#事例
#N人が見てn人がクリックしたとして、Nがものすごく大きいと仮定した時、n/Nは正規分布に近似する
#よってA=Bを棄却できる
def estimated_paramaters(N, n):
	p = n / N
	sigma = math.sqrt(p * (1 - p) / N)
	return p, sigma

#Aの広告とBの広告が独立なら、Bの確率-Aの確率も正規分布に従う
def a_b_test_statistics(N_A, n_A, N_B, n_B):
	p_A, sigma_A = estimated_paramaters(N_A, n_A)
	p_B, sigam_B = estimated_paramaters(N_B, n_B)
	return (p_B - p_A) / math.sqrt(sigma_A ** 2 + sigam_B **2)

z = a_b_test_statistics(1000, 200, 1000, 180)#-1.14
print(z)
#AとBが同じ時に、この差が起きる確率
print(two_sided_p_value(z))#0.254：棄却できない

z = a_b_test_statistics(1000, 200, 1000, 150)#-2.94
print(z)
print(two_sided_p_value(z))#0.003：帰無仮説になる可能性がかなり低いので、棄却できる



#ベイズ推定：未知の確率(事後分布)をベイズの定理と事前分布を用いて推定する
#ベータ分布：事前分布が未知の場合によく使われる　以下その求め方
def B(alpha, beta):#正規化する(確率の総和が１になるようにする)
	return math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)

def beta_pdf(x, alpha, beta):#ベータ分布
	if x < 0 or x >1:
		return 0
	return x ** (alpha - 1) * (1 - x) ** (beta - 1) / B(alpha, beta)
#一般的にグラフの中心は= alpha/(alpha+beta)となる

#はじめはalphaもbetaも１として、表または裏が出るたびに加えていくことでベイズ推定を行う
#事後分布もベータ分布になる

