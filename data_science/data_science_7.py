from probability import normal_cdf, inverse_normal_cdf
import math, random


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
mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0,55)#平均と標準偏差
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
for _ in range(100000)
	num_heads = sum(1 if random.random() < 0.5 else 0#1000回コインを投げて
					for _ range(1000))				 #表が出る回数を数える
	if num_heads >= 530 or num_heads <= 470:		 #そのうち極端な値が出た回数を
		extreme_value_count += 1					 #数える

print(extreme_value_count / 100000)#0.062

#x=532の時
print(two_sided_p_value(531.5, mu_0, sigma_0))


#別バージョン
upper_p_value = normal_plobablity_above
lower_p_value = normal_probablity_below

#x=524の時
pritn(upper_p_value(524.5, mu_0, sigma_0))#0.061
#x=527の時
print(upper_p_value(526.5, mu_0, sigma_0))#0.047




#信頼区間


