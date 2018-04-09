import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


#データの可視化
#折れ線グラフ
years = np.array([1950, 1960, 1970, 1980, 1990, 2000, 2010])
gdp = np.array([300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3])

plt.plot(years, gdp, color="green", marker="o", linestyle="solid")
plt.title("Nominal GDP")

plt.ylabel("Bililon of $")
plt.show()




#折れ線グラフ2
variance = [1, 2, 4, 8, 16, 32, 64, 128, 256]
bias_squared = [256, 128, 64, 32, 16, 8, 4, 2, 1]
total_error = [x + y for x, y in zip(variance, bias_squared)]
xs = [i for i, _ in enumerate(variance)]

plt.plot(xs, variance, 'g-', label = 'variance')
plt.plot(xs, bias_squared, 'r-', label = 'bias^2')
plt.plot(xs, total_error, 'b-', label = 'total error')
#ラベルを指定してるため自動で凡例がつく

plt.legend(loc = 9)
plt.xlabel("model complexity")
plt.title("The Bias-Variance Tradeoff")

plt.show()




#棒グラフ
movies = ["Annie Hall", "Ben-Hur", "Casablanca", "Gandhi", "West Side Story"]
num_oscars = [5, 11, 3, 8, 10]

plt.bar(movies, num_oscars)
plt.ylabel("# of Academy Award")
plt.title("My Favorite Movies")

plt.xticks(movies)

plt.show()




#ヒストグラム
grades = [83, 95, 91, 87, 70, 0, 85, 82, 100, 67, 73, 77, 0]
decile = lambda grade: grade // 10 * 10
histogram = Counter(decile(grade) for grade in grades)

plt.bar([x for x in histogram.keys()],histogram.values(), 8) #最後の数字は棒グラフの幅

plt.axis([-5, 105, 0, 5]) #範囲を定めるx→yの順

plt.xticks([10 * i for i in range(11)]) #0から100までメモリをふる
plt.xlabel("Decile")
plt.ylabel("# of Students")
plt.title("Distribution of Exam 1 Grades")

plt.show()





#散布図
friends = [70, 65, 72, 63, 71, 64, 60, 64, 67]
minutes = [175, 170, 205, 120, 220, 130, 105, 145, 190]
labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

plt.scatter(friends, minutes)

#点のラベル
for label, friend_count, minute_count in zip(labels, friends, minutes):
	plt.annotate(label,
		xy = (friend_count, minute_count),
		xytext = (5, -5),
		textcoords = 'offset points')
plt.title ("Daily Minutes vs. Number of Friends")

plt.show()


